clc;

%code for tensor products (kronecker)

ket0 = [1;0];
ket1 = [0;1];

ket01 = kron(ket0,ket1);
ket00 = kron(ket0,ket0);

psi = kron(ket0,ket0);

% Hadamard
H = (1/sqrt(2))*[1 1; 1 -1];
I = eye(2);

% Apply H on first qubit
U = kron(H,I);

result = U*psi

% Apply H on second qubit
U = kron(I,H);

result = U*psi

