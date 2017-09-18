data = [0 0; 1 1; 2 2; 4 4];
x = data(:,1); y = data(:,2);

figure;
plot(x, y, 'rx', 'MarkerSize', 10);
xlabel('x'); ylabel('y');title('Data Map')
fprintf('Program paused. Press enter to continue.\n');
pause;

m = length(y);

X = [ones(m, 1), data(:,1)];
theta = zeros(2, 1);
alpha = 0.01;
iterations = 1500;

theta = GradientDescent(X, y, theta, alpha, iterations);

hold on;
plot(x, X*theta, '-')
legend('Training data', 'Linear regression')
hold off;

fprintf('the theta_0 is %f\n', theta(1,1));
fprintf('the theta_1 is %f\n', theta(2,1));

min_x=-20;
max_x=20;
num=110;
theta_1=linspace(min_x, max_x, num);
theta_0=linspace(min_x, max_x, num);

J = zeros(length(theta_0), length(theta_1));

for i = 1:num
    for j = 1:num
        t = [theta_0(i); theta_1(j)];
        h = X * t;
        J(i, j) = sum((h - y).^2) / (2 * m);
    end
end

figure;
surf(theta_0, theta_1, J);
xlabel('\theta_0');ylabel('\theta_1');zlabel('J(\theta_0, \theta_1)')
title('Cost Function Map')

[b, c] = find(J==min(J(:)));
disp([b, c]);

figure;
contour(theta_0, theta_1, J, logspace(-2, 3, 20))
xlabel('\theta_0'); ylabel('\theta_1');
title('Contour Map')
hold on;
plot(theta_0(c), theta_1(b), 'rx', 'MarkerSize', 10, 'LineWidth', 2);
hold off;
