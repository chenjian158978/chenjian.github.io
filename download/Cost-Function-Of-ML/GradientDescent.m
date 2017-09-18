function [theta, J_history] = GradientDescent(X, y, theta, alpha, iterations_num)

m = length(y);
J_history = zeros(iterations_num, 1);

for iter = 1:iterations_num
    h = X * theta;
    t = [0; 0];
    for i = 1:m
        t = t + (h(i) - y(i)) * X(i,:)';
    end

    theta = theta - alpha * (1 / m) * t;

    J_history(iter) = CostFunction(X, y, theta);
end

end