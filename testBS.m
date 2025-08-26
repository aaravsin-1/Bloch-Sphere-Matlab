clc;
clear;
%% Constants
X = [0 1; 1 0]; 
Z = [1 0; 0 -1];
Y = [0 -1i; 1i 0];
H = (1/sqrt(2)) * (X + Z);
S = [1 0; 0 i];

%% Calculations
ket0 = [1;0];
ket1 = [0;1];

rho = ket2dm(ket0);
lambda0 = ket2bv(ket0);
lambda1 = ket2bv(ket1);

% Plot Bloch sphere first
%figure;%opens a new figure each time -- can remove or comment out if not needed
plotBlochSphere;




%plot value
psi = (S*H*ket1);%value




%normalise then plot the vector
newKet = psi ;
newKet = newKet / norm(newKet);
plotBlochVect(newKet);

%% --- Helper functions ---
function rho = ket2dm(ket)
    rho = ket * ket'; % Density matrix
end

function lambda = ket2bv(ket)
    rho = ket2dm(ket);
    X = [0 1; 1 0]; 
    Y = [0 -1i; 1i 0]; 
    Z = [1 0; 0 -1];
    S = [1 0; 0 i];
    lambda = [ real(trace(X*rho)); 
               real(trace(Y*rho)); 
               real(trace(Z*rho)) ];
end

function plotBlochVect(ket)
    lambda = ket2bv(ket);
    line([0 lambda(1)], [0 lambda(2)], [0 lambda(3)], ...
        'LineWidth',2,'Marker','o','Color','r');
end