clc;
clear;
%% Constants
X = [0 1; 1 0]; 
Z = [1 0; 0 -1];
Y = [0 -1i; 1i 0];
H = (1/sqrt(2)) * (X + Z);
S = [1 0; 0 1i];
T = [1 0;0 exp(1i*pi/4)];

%% Calculations
ket0 = [1;0];
ket1 = [0;1];
ketp = (ket0 + ket1)/sqrt(2);%ket+
ketm = (ket0 - ket1)/sqrt(2);%ket-


rho = ket2dm(ket0);
lambda0 = ket2bv(ket0);
lambda1 = ket2bv(ket1);




%% Plot Bloch sphere first
figure;%opens a new figure each time -- can remove or comment out if not needed
plotBlochSphere;

%plot value
psi = (T*ketp);%value

%normalise then plot the vector
newKet = psi ;
newKet = newKet / norm(newKet);
plotBlochVect(newKet,'r');
%Dynamic Title
title(ket2latex(newKet), 'Interpreter','latex','FontSize',16);

%second qubit
psi2 = (ketp);%value

%normalise then plot the vector
newKet = psi2 ;
newKet = newKet / norm(newKet);
plotBlochVect(newKet,'g');%vector,color




%% --- Helper functions ---
function rho = ket2dm(ket)
    rho = ket * ket'; % Density matrix
end

function lambda = ket2bv(ket)
    rho = ket2dm(ket);
    X = [0 1; 1 0]; 
    Y = [0 -1i; 1i 0]; 
    Z = [1 0; 0 -1];
    lambda = [ real(trace(X*rho)); 
               real(trace(Y*rho)); 
               real(trace(Z*rho)) ];
end

function plotBlochVect(ket,col)
    lambda = ket2bv(ket);
    line([0 lambda(1)], [0 lambda(2)], [0 lambda(3)], ...
        'LineWidth',3,'Marker','O','Color',col);
end

function label = ket2latex(psi)
    psi = round(psi,4);
    a = psi(1); b = psi(2);
    
    a_str = complex2str(a, '|0\rangle');
    b_str = complex2str(b, '|1\rangle');
    
    % Combine terms with correct sign
    if isempty(a_str)
        label = ['$\displaystyle |\psi\rangle = ' b_str '$'];
    elseif isempty(b_str)
        label = ['$\displaystyle |\psi\rangle = ' a_str '$'];
    else
        if real(b) >= 0
            label = ['$\displaystyle |\psi\rangle = ' a_str ' + ' b_str '$'];
        else
            label = ['$\displaystyle |\psi\rangle = ' a_str ' ' b_str '$'];
        end
    end
end

function s = complex2str(c, ketLabel)
    if nargin < 2, ketLabel = ''; end
    
    % Zero
    if abs(c) < 1e-10
        s = '';
        return;
    end

    % Handle 1/sqrt(2)
    if abs(abs(c) - 1/sqrt(2)) < 1e-5
        if real(c) < 0
            s = ['-\frac{1}{\sqrt{2}}' ketLabel];
        else
            s = ['\frac{1}{\sqrt{2}}' ketLabel];
        end
        return;
    end
    
    % Handle 1 or -1
    if abs(real(c)) == 1 && imag(c) == 0
        if c > 0
            s = ketLabel; % omit 1
        else
            s = ['-' ketLabel]; % show minus
        end
        return;
    end

    % Pure real
    if imag(c) == 0
        s = [num2str(real(c)) ketLabel];
        return;
    end
    
    % Pure imaginary
    if real(c) == 0
        if imag(c) == 1
            s = ['i' ketLabel];
        elseif imag(c) == -1
            s = ['-i' ketLabel];
        else
            s = [num2str(imag(c)) 'i' ketLabel];
        end
        return;
    end

    % General complex
    s = ['(' num2str(real(c)) '+' num2str(imag(c)) 'i)' ketLabel];
end