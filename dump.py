'''
clc; 
clear; 

M = [1  1; 
     1  4];  

range = -4:0.5:4; 
[X, Y] = meshgrid(range, range); 

DX = M(1,1)*X + M(1,2)*Y;   % dx/dt 
DY = M(2,1)*X + M(2,2)*Y;   % dy/dt 

figure; 
quiver(X, Y, DX, DY, 'b'); 
axis tight; 
grid on; 
title('Direction Field of the System'); 
xlabel('x'); 
ylabel('y'); 


lambda = eig(M); 
disp('System Matrix M:'); 
disp(M); 
disp('Eigenvalues of M:'); 
disp(lambda); 










clc; clear; close all;

A = [-1 2; -2 -3];
b = [1; 0];

x_eq = -A\b;

eigvals = eig(A)

f = @(t,X) A*X + b;

tspan = [0 10];

IC = [0 0; 2 1; -1 2; 3 -2];

figure; hold on;
for i=1:size(IC,1)
    [t,sol] = ode45(f,tspan,IC(i,:)');
    plot(sol(:,1),sol(:,2),'LineWidth',1.5);
end
plot(x_eq(1),x_eq(2),'ro','MarkerSize',8,'LineWidth',2);
xlabel('x'); ylabel('y'); 
title('Phase Plane Trajectories');
grid on;

figure;
for i=1:size(IC,1)
    [t,sol] = ode45(f,tspan,IC(i,:)');
    subplot(2,1,1); hold on; plot(t,sol(:,1),'LineWidth',1.5);
    title('x(t) vs t');
    subplot(2,1,2); hold on; plot(t,sol(:,2),'LineWidth',1.5);
    title('y(t) vs t');
end
grid on; 







syms x y; 
f = 2*x + 8*y + 1; 
g = 5*x + 7*y;
S = solve([f == 0,g == 0] , [x,y]);

critical_point = double([S.x;S.y]);
A = jacobian([f;g],[x,y]); 
A = double(A);

[V,D] = eig(A);
EigenValues = diag(D);
EigenVectors = V;

disp('---RESULTS---');
disp('Critical Point');
disp(critical_point);

disp('Jacobian Matrix(Coefficient Matrix)');
disp(A);
disp("Eigenvalues");
disp(EigenValues);
disp('Eigenvectors');
disp(EigenVectors);








% Example : 2*s^3 + 4*s^2 - 2s + 24 = 0 ->[2,4,-2,24]
coeff = [2,4,-2,24];
n = length(coeff);
cols = ceil(n/2);
RouthTable = zeros(n,cols);

RouthTable(1,:) = [coeff(1:2:n)];
RouthTable(2,:) = [coeff(2:2:n)];
for i = 3:n
   for j = 1:cols-1
       numerator = RouthTable(i-1,1)*RouthTable(i-2,j+1) - RouthTable(i-2,1)*RouthTable(i-1,j+1);
       denominator = RouthTable(i-1,1)
       if denominator == 0
           denominator = 1e-10; 
       end
       RouthTable(i,j) = numerator/denominator;
   end
end
first_col = RouthTable(:,1);
sign_changes = 0;
for k = 1:length(first_col) - 1
   if sign(first_col(k)) ~= sign(first_col(k+1))
       sign_changes = sign_changes+1;
   end
end
fprintf("---------------------------------------------------------\n");
fprintf("Routh Table:\n");
disp(RouthTable);
if sign_changes == 0 && all(first_col ~= 0)
   fprintf("Result: System is Stable\n");
else
   fprintf("Result: System is Unstable\n");
   fprintf("Sign Changes : %d \n",sign_changes);
end
fprintf("---------------------------------------------------------\n");










% Step 1: Define system matrix A 
A = [-2  2; 
     -5 -7]; 
% Step 2: Choose positive definite matrix Q 
Q = eye(size(A));  
% Step 3: Solve Lyapunov equation  A'P + PA = -Q 
P = lyap(A', Q); % Step 4: Display P 
disp('Matrix P obtained from Lyapunov equation:'); 
disp(P); 
% Step 5: Check if P is positive definite 
eigenvalues_P = eig(P); 
disp('Eigenvalues of P are:'); 
disp(eigenvalues_P); 
if all(eigenvalues_P > 0)     
    disp('P is positive definite');     
    disp('System is ASYMPTOTICALLY STABLE'); 
else     
    disp('P is NOT positive definite');     
    disp('Cannot conclude stability'); 
end 










a = 0.7;
b = 0.9;
c = 0.8;
d = 0.24;
params = [a;b;c;d];
% ax-bxy = dx/dt
% cxy - dy = dy/dt
% x  prey population
% y predator population
% Initial condition : [prey; predator]
y0 = [100;35];
% Time Span
tspan = 0:0.01:150;
% Solve ODE
[t,y] = ode45(@(t,y) LVeqn(t,y,params),tspan,y0);
% Time Domain plot
figure;
plot(t,y(:,1),'LineWidth',1); % prey
hold on;
plot(t,y(:,2),'LineWidth',1) % Predator
hold off;
legend('Prey','Predator');
set(gca,'Linewidth',1,'FontSize',10);
title("Prey Predator Model");
xlabel("Time");
ylabel("Population");
figure;
plot(y(:,1),y(:,2),'LineWidth',1)
xlabel("Prey");
ylabel("Predator");
title("Prey vs Predator");
set(gca,'LineWidth',1,'FontSize',10);
% Vector Field
u = 0:1:20;
v = 0:1:10;
[u,v] = meshgrid(u,v);
V1 = a*u+b*u.*v;
V2 = c*u.*v - d*v;
VF = sqrt(V1.^2 + V2.^2);
hold on;
quiver(u,v,V1./VF,V2./VF,0.5);
axis([0 20 0 10]);
hold off;

function df = LVeqn(~,var,params)
   a = params(1);
   b = params(2);
   c = params(3);
   d = params(4);
   x = var(1);
   y = var(2);
  
   df = zeros(2,1);
   df(1) = a*x - b*x*y;
   df(2) = c*x*y - d*y;
end









beta = 0.3; % Infection Rate
gamma = 0.1; % Recovery rate
% Initial Conditions
S0 = 0.99;
I0 = 0.01;
R0 = 0;
x0 = [S0 I0 R0];
% Time span
tspan = [0 160];
% SiR eqns
sir = @(t,x) [
   -beta*x(1)*x(2);
   beta*x(1)*x(2) - gamma*x(2);
   gamma*x(2);
];
% Solve ODE
[t,x] = ode45(sir,tspan,x0);
figure;
plot(t,x(:,1),'b',t,x(:,2),'r',t,x(:,3),'g','LineWidth',2);
xlabel('Time');
ylabel('Population fraction');
title('SIR Model Simulation');
legend('Susceptible','Infected','recovered');
grid on;
% Effect of time varying infection rate
beta_values = [0.2 0.4 0.6];
gamma = 0.1;
figure;
hold on;
for beta = beta_values
   sir = @(t,x) [
       -beta*x(1)*x(2);
       beta*x(1)*x(2) - gamma*x(2);
       gamma*x(2);];
   [t,x] = ode45(sir,tspan,x0);
   plot(t,x(:,2),'LineWidth',2);
end
xlabel('Time');
ylabel('Infected Population');
title('Effect of Infection rate (\beta)');
legend('\beta = 0.2','\beta = 0.4','\beta = 0.6');
grid on;
% Effect of time varying recovery rate
beta = 0.3;
gamma_values = [0.05 0.1 0.2];
figure;
hold on;
for gamma = gamma_values
   sir = @(t,x) [
       -beta*x(1)*x(2);
       beta*x(1)*x(2) - gamma*x(2);
       gamma*x(2);];
   [t,x] = ode45(sir,tspan,x0);
   plot(t,x(:,2),'LineWidth',2);
end
xlabel('Time');
ylabel('Infected population');
title('Effect of Recovery rate (\gamma)');
legend('\gamma = 0.05','\gamma = 0.1','\gamma = 0.2');
grid on;







r = linspace(-1,5,400);

x1 = sqrt(r); 
x2 = -sqrt(r); 

x1(imag(x1) ~= 0) = NaN;
x2(imag(x2) ~= 0) = NaN;

figure;
plot(r,x1,'b','LineWidth',2);
hold on;
plot(r, x2, 'r', 'LineWidth', 2);
plot(0, 0, 'ko', 'MarkerSize', 8, 'LineWidth', 2);
xlabel('Bifurcation Parameter r');
ylabel('Equilibrium Points x');
title('Saddle-Node Bifurcation Diagram');
legend('Stable Equilibrium', 'Unstable Equilibrium', 'Bifurcation Point');
grid on;
% Time-domain analysis for different r values
tspan = [0 6];
x0 = 0.5;    % Initial condition
r_values = [-1, 0, 1];
figure;
hold on;
for r = r_values
   f = @(t, x) r - x.^2;
   [t, x] = ode45(f, tspan, x0);
   plot(t, x, 'LineWidth', 2);
end
xlabel('Time');
ylabel('State x(t)');
title('Time Response for Different r Values');
legend('r = -1', 'r = 0', 'r = 1');











r = linspace(-2,2,400);
 
x1 = zeros(size(r)); % x = 0
x2 = r;             % x = r 

figure;
plot(r,x1,'r--','LineWidth',2);
hold on; % holds the figure
plot(r,x2,'b','LineWidth',2);
plot(0,0,'ko','MarkerSize',8,'LineWidth',2);
xlabel('Bifurcation Parameter r');
ylabel('Equilibriumm Points x');
title('Transcritical Bifurcation Diagram');
legend('X = 0 (Unstable ? Stable)','x = r (Stable->Unstable)','Bifurcation Point');
grid on;

tspan = [0 2];
x0 = 2; % Initial condition
r_values = [-1,2.5,0];
 
figure;
hold on;
for r = r_values
   f = @(t,x) r*x - x.^2;
   [t,x] = ode45(f,tspan,x0);
   plot(t,x,'LineWidth',2);
end
xlabel('Time');
ylabel('State x(t)');
title('Time Response Showing Transcriptal Bifurcation ');
legend('r = -1','r = 2.5','r = 0');
grid on;









sigma = 10; % : σ is the Prandtl number
rho = 28; % ρ is the Rayleigh number
beta = 8/3; %  physical dimensions of the fluid layer
% Time span and initial conditions
tspan = [0 100];
x0 = [1,1,1];
% Lorenz equations
lorenz = @(t,x) [
   sigma*(x(2) - x(1));
   x(1)*(rho - x(3)) - x(2);
   x(1)*x(2) - beta*x(3);
];
% Solve ODE using ode45
[t,x] = ode45(lorenz,tspan,x0);
% Plot time response
figure;
plot(t,x(:,1),t,x(:,2),t,x(:,3),'LineWidth',1.5); % Plot all 3 simultaneously
xlabel('Time');
ylabel('States'); % different states of system
title('Time Response of Lorenz System');
legend('x(t)','y(t)','z(t)'); %
grid on; % grid for more clarity
% 3D phase space plot
figure;
plot3(x(:,1),x(:,2),x(:,3),'k','LineWidth',1);
xlabel('x');
ylabel('y');
zlabel('z');
title('Lorenz Chaotic Attractor');
grid on;

'''