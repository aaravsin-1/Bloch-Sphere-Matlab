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
ketp = (ket0 + ket1)/sqrt(2);%ket+
ketm = (ket0 - ket1)/sqrt(2);%ket-


rho = ket2dm(ket0);
lambda0 = ket2bv(ket0);
lambda1 = ket2bv(ket1);

% Plot Bloch sphere first
%figure;%opens a new figure each time -- can remove or comment out if not needed
plotBlochSphere;




%plot value
psi = (ketm);%value


%normalise then plot the vector
newKet = psi ;
newKet = newKet / norm(newKet);
plotBlochVect(newKet);

%%Dynamic Title

title(ket2latex(newKet), 'Interpreter','latex','FontSize',16);

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
        'LineWidth',3,'Marker','O','Color','r');
end

function label = ket2latex(psi)
    % Round small numerical noise
    psi = round(psi, 4);

    % Coefficients
    a = psi(1);
    b = psi(2);

    % Format real/imag parts nicely
    a_str = complex2str(a);
    b_str = complex2str(b);

    % Build LaTeX ket expression
    label = ['$|\psi\rangle = ' a_str '|0\rangle + ' b_str '|1\rangle$'];
end

function s = complex2str(c)
    % Handle 0 specially
    if abs(c) < 1e-10
        s = '';
        return
    end
    % If real
    if imag(c) == 0
        s = num2str(real(c));
    % If purely imaginary
    elseif real(c) == 0
        if imag(c) == 1
            s = 'i';
        elseif imag(c) == -1
            s = '-i';
        else
            s = [num2str(imag(c)) 'i'];
        end
    else
        % General complex
        s = ['(' num2str(real(c)) '+' num2str(imag(c)) 'i)'];
    end
    % Add sqrt(2) denominator if exact
    if abs(abs(c) - 1/sqrt(2)) < 1e-6
        s = ['\tfrac{1}{\sqrt{2}}' ];
    end
end