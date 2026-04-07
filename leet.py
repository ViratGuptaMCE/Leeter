import streamlit as st
import requests
import pandas as pd
from datetime import datetime

LEETCODE_GRAPHQL_URL = 'https://leetcode.com/graphql'

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
    "Content-Type": "application/json"
}

def extract_username(text):
    """Extracts the username whether the user pastes a full URL or just the name."""
    text = text.strip()
    if text.startswith("http"):
        parts = [p for p in text.rstrip('/').split('/') if p]
        return parts[-1]
    return text

def fetch_user_stats(username):
    """Fetches the total problem-solving counts broken down by difficulty."""
    query = """
    query userProblemsSolved($username: String!) {
      matchedUser(username: $username) {
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """
    response = requests.post(
        LEETCODE_GRAPHQL_URL, 
        json={'query': query, 'variables': {"username": username}},
        headers=HEADERS
    )
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and data['data'].get('matchedUser'):
            return data['data']['matchedUser']['submitStatsGlobal']['acSubmissionNum']
    return None

def fetch_recent_submissions(username, limit=20):
    """Fetches the user's most recent accepted submissions. 
       Note: LeetCode's public API caps this at 20."""
    query = """
    query recentAcSubmissions($username: String!, $limit: Int!) {
      recentAcSubmissionList(username: $username, limit: $limit) {
        id
        title
        titleSlug
        timestamp
      }
    }
    """
    response = requests.post(
        LEETCODE_GRAPHQL_URL, 
        json={'query': query, 'variables': {"username": username, "limit": limit}},
        headers=HEADERS
    )
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'recentAcSubmissionList' in data['data']:
            return data['data']['recentAcSubmissionList']
    return []

def fetch_question_difficulty(title_slug):
    """Fetches the difficulty level for a specific problem using its slug."""
    query = """
    query questionTitle($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        difficulty
      }
    }
    """
    response = requests.post(
        LEETCODE_GRAPHQL_URL, 
        json={'query': query, 'variables': {"titleSlug": title_slug}},
        headers=HEADERS
    )
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and data['data'].get('question'):
            return data['data']['question']['difficulty']
    return "Unknown"

st.set_page_config(page_title="LeetCode Profile Tracker", page_icon="", layout="wide")

st.title("LeetCode Stats & Submissions Tracker")
st.markdown("Extract a user's total statistics and filter their most recent accepted questions based on timeline and hardness.")

st.markdown("### Search Profile")
username_input = st.text_input("Enter LeetCode Username or Profile URL:", placeholder="e.g., neetcode or https://leetcode.com/neetcode/")

if st.button("Fetch Data", type="primary"):
    if not username_input:
        st.warning("Please enter a valid username or URL to proceed.")
    else:
        username = extract_username(username_input)
        
        with st.spinner(f"Scraping data for **{username}**..."):
            stats = fetch_user_stats(username)
            
            if not stats:
                st.error(f"Could not find data for user '{username}'. Make sure the profile exists and is public.")
            else:
                easy, med, hard, total = 0, 0, 0, 0
                for item in stats:
                    if item['difficulty'] == "All": total = item['count']
                    elif item['difficulty'] == "Easy": easy = item['count']
                    elif item['difficulty'] == "Medium": med = item['count']
                    elif item['difficulty'] == "Hard": hard = item['count']
                
                st.success(f"Profile loaded successfully!")
                
                st.markdown("---")
                st.markdown(f"### Lifetime Stats for `{username}`")
                cols = st.columns(4)
                cols[0].metric(label="Total Solved", value=total)
                cols[1].metric(label="Easy", value=easy)
                cols[2].metric(label="Medium", value=med)
                cols[3].metric(label="Hard", value=hard)
                
                st.markdown("---")
                st.markdown("### Recent Submissions Activity")
                
                submissions = fetch_recent_submissions(username, limit=20)
                
                if not submissions:
                    st.warning("No recent accepted submissions found for this user.")
                else:
                    data_rows = []
                    progress_text = "Mapping difficulty levels..."
                    my_bar = st.progress(0, text=progress_text)
                    
                    for idx, sub in enumerate(submissions):
                        diff = fetch_question_difficulty(sub['titleSlug'])
                        dt_obj = datetime.fromtimestamp(int(sub['timestamp']))
                        
                        data_rows.append({
                            "Question": sub['title'],
                            "Difficulty": diff,
                            "Date": dt_obj.date(),
                            "Time": dt_obj.strftime('%H:%M:%S'),
                            "Link": f"https://leetcode.com/problems/{sub['titleSlug']}/"
                        })
                        
                        my_bar.progress((idx + 1) / len(submissions), text=progress_text)
                        
                    my_bar.empty() 
                    st.session_state['df'] = pd.DataFrame(data_rows)
                    st.session_state['username'] = username

if 'df' in st.session_state:
    df = st.session_state['df']
    
    st.markdown("#### Filter Results")
    
    f_cols = st.columns(2)
    with f_cols[0]:
        min_date = df['Date'].min()
        max_date = df['Date'].max()
        selected_dates = st.date_input("Filter by Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
        
    with f_cols[1]:
        difficulties = ["All", "Easy", "Medium", "Hard"]
        selected_diff = st.selectbox("Filter by Difficulty", difficulties)
    
    filtered_df = df.copy()
    
    if len(selected_dates) == 2:
        start_date, end_date = selected_dates
        filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]
    elif len(selected_dates) == 1:
        start_date = selected_dates[0]
        filtered_df = filtered_df[filtered_df['Date'] == start_date]
        
    if selected_diff != "All":
        filtered_df = filtered_df[filtered_df['Difficulty'] == selected_diff]
        
    st.markdown(f"**Showing {len(filtered_df)} result(s)**")
    
    st.dataframe(
        filtered_df,
        column_config={
            "Question": st.column_config.TextColumn("Problem Title", width="large"),
            "Difficulty": st.column_config.TextColumn("Hardness"),
            "Date": st.column_config.DateColumn("Date Solved", format="MMM DD, YYYY"),
            "Link": st.column_config.LinkColumn("LeetCode Link", display_text="Open Problem")
        },
        use_container_width=True,
        hide_index=True
    )