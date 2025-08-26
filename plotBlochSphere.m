%% Plot Bloch Sphere
[Xs, Ys, Zs] = sphere(50);              % higher resolution sphere
mySphere = surf(Xs, Ys, Zs);

axis equal
shading interp
mySphere.FaceAlpha = 0.25;              % set transparency
hold on

% Coordinate axes (white lines)
line([-1 1], [0 0], [0 0], 'LineWidth', 1, 'Color', [1 1 1])
line([0 0], [-1 1], [0 0], 'LineWidth', 1, 'Color', [1 1 1])
line([0 0], [0 0], [-1 1], 'LineWidth', 1, 'Color', [1 1 1])

% Basis state labels
text(0, 0, 1.1, '$|0\rangle$', 'Interpreter','latex', ...
    'FontSize', 20, 'HorizontalAlignment','center','Color','w')
text(0, 0, -1.1, '$|1\rangle$', 'Interpreter','latex', ...
    'FontSize', 20, 'HorizontalAlignment','center','Color','w')
text(1.1, 0, 0, '$|+\rangle$', 'Interpreter','latex', ...
    'FontSize', 20, 'HorizontalAlignment','center','Color','w')
text(-1.1, 0, 0, '$|-\rangle$', 'Interpreter','latex', ...
    'FontSize', 20, 'HorizontalAlignment','center','Color','w')
text(0, 1.1, 0, '$|i\rangle$', 'Interpreter','latex', ...
    'FontSize', 20, 'HorizontalAlignment','center','Color','w')
text(0, -1.1, 0, '$|-i\rangle$', 'Interpreter','latex', ...
    'FontSize', 20, 'HorizontalAlignment','center','Color','w')

% Axis labels
text(1.3,0,0,'X','FontSize',14,'Color','w')
text(0,1.3,0,'Y','FontSize',14,'Color','w')
text(0,0,1.3,'Z','FontSize',14,'Color','w')

 % --- New: Equatorial circles around X, Y, Z axes ---
    t = linspace(0,2*pi,200);

    % Circle in YZ plane (around X-axis)
    plot3(zeros(size(t)), cos(t), sin(t), ...
        'Color', [1 1 1 0.3], 'LineWidth', 1.2);  

    % Circle in XZ plane (around Y-axis)
    plot3(cos(t), zeros(size(t)), sin(t), ...
        'Color', [1 1 1 0.3], 'LineWidth', 1.2);

    % Circle in XY plane (around Z-axis)
    plot3(cos(t), sin(t), zeros(size(t)), ...
        'Color', [1 1 1 0.3], 'LineWidth', 1.2);

% Set viewing angle
view([60 15])
hold off;