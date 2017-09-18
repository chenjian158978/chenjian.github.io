function J = CostFunction(X, y, theta)

m = length(y);
J = 0;

h = X * theta;
J = sum((h - y).^2) / (2 * m);

end