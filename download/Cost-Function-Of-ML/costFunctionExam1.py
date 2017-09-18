# -*- coding:utf8 -*-

"""
@author: chenjian158978@gmail.com

@date: Tue, May 23 2017

@time: 19:05:20 GMT+8
"""

import matplotlib.pyplot as plt
import numpy as np


def calcu_cost(theta, X, Y):
    """ 计算代价函数的值

    :param theta: 斜率
    :param X: x值
    :param Y: y值
    :return: J值
    """
    m = X.shape[0]
    h = np.dot(X, theta)
    return np.dot((h - Y).T, (h - Y)) / (2 * m)


X = np.array([[0, 1, 2, 4]]).T
Y = np.array([[0, 1, 2, 4]]).T

# 从-2到4之间返回均匀间隔的数字,共101个
# theta是101*1的矩阵
theta = np.array([np.linspace(-2, 4, 101)]).T

J_list = []
for i in range(101):
    current_theta = theta[i:(i + 1)].T
    cost = calcu_cost(current_theta, X, Y)
    J_list.append(cost[0, 0])

plt.plot(theta, J_list)

plt.xlabel('theta_1')
plt.ylabel('J(theta)')
plt.title('Cost Function Example1')
plt.grid(True)
plt.savefig('cost_theta.png', dpi=200)
plt.show()
