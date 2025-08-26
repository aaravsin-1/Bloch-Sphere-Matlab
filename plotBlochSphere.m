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

% Axes arrows
quiver3(0,0,0, 1.2,0,0, 'w','LineWidth',1.5,'MaxHeadSize',0.3)
quiver3(0,0,0, 0,1.2,0, 'w','LineWidth',1.5,'MaxHeadSize',0.3)
quiver3(0,0,0, 0,0,1.2, 'w','LineWidth',1.5,'MaxHeadSize',0.3)

% Axis labels
text(1.3,0,0,'X','FontSize',14,'Color','w')
text(0,1.3,0,'Y','FontSize',14,'Color','w')
text(0,0,1.3,'Z','FontSize',14,'Color','w')

% Set viewing angle
view([60 15])
hold off;