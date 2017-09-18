# -*- coding:utf8 -*-

"""
@author: chenjian158978@gmail.com

@date: Tue, May 23 2017

@time: 19:05:20 GMT+8

matplotlib version: 2.0.2
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np


def calcu_cost(theta_0, theta_1, X, Y):
    """ 计算代价函数的值

    :param theta_0: y轴上的值
    :param theta_1: 斜率
    :param X: x值
    :param Y: y值
    :return: J值
    """
    m = X.shape[0]
    h = np.dot(X, theta_1) + theta_0
    return np.dot((h - Y).T, (h - Y)) / (2 * m)


X = np.array([[0, 1, 2, 4]]).T
Y = np.array([[0, 1, 2, 4]]).T

# 预估的点数
points_num = 41
# 点数最小值
min_point = -2
# 点数最大值
max_point = 2

# 从-2到4之间返回均匀间隔的数字,共101个
origin_theta_0 = np.array([np.linspace(min_point, max_point, points_num)]).T
origin_theta_1 = np.array([np.linspace(min_point, max_point, points_num)]).T

theta_0_list = []
theta_1_list = []

J_list = []
for i in range(points_num):
    current_theta_0 = origin_theta_0[i:(i + 1)].T
    for j in range(points_num):
        theta_0_list.append(current_theta_0[0, 0])
        current_theta_1 = origin_theta_1[j:(j + 1)].T
        theta_1_list.append(current_theta_1[0, 0])
        cost = calcu_cost(current_theta_0, current_theta_1, X, Y)
        J_list.append(cost[0, 0])

fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(theta_0_list, theta_1_list, J_list, color='c')

for j in range(len(theta_0_list)):
    if J_list[j] == min(J_list):
        label_txt = 'Min J_theta(%s, %s)= %s' % (str(theta_0_list[j]), str(theta_1_list[j]), str(J_list[j]))
        ax.scatter(theta_0_list[j], theta_1_list[j], J_list[j], color='k', label=label_txt)
ax.set_xlabel('theta_0')
ax.set_ylabel('theta_1')
ax.set_zlabel('J_theta')
ax.legend(loc='upper right')
ax.view_init(30, 35)
plt.show()
