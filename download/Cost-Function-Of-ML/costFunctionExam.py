# -*- coding:utf8 -*-

"""
@author: chenjian158978@gmail.com

@date: Tue, May 23 2017

@time: 19:05:20 GMT+8
"""
import matplotlib.pyplot as plt
import numpy as np

# 都转换成列向量
X = np.array([[0, 1, 2, 4]]).T
Y = np.array([[0, 1, 2, 4]]).T

# 三个不同的theta_1值
theta1 = np.array([[0, 0]]).T
theta2 = np.array([[0, 0.5]]).T
theta3 = np.array([[0, 1]]).T

# 矩阵X的行列(m,n)
X_size = X.shape

# 创建一个(4,1)的单位矩阵
X_0 = np.ones((X_size[0], 1))

# 形成点的坐标
X_with_x0 = np.concatenate((X_0, X), axis=1)

# 两个数组点积
h1 = np.dot(X_with_x0, theta1)
h2 = np.dot(X_with_x0, theta2)
h3 = np.dot(X_with_x0, theta3)

# r:red x: x marker
plt.plot(X, Y, 'rx', label='y')
plt.title("Cost Function Example")
plt.grid(True)
plt.plot(X, h1, color='b', label='h1, theta_1=0')
plt.plot(X, h2, color='m', label='h2, theta_1=0.5')
plt.plot(X, h3, color='g', label='h3, theta_1=1')

# 坐标轴名称
plt.xlabel('X')
plt.ylabel('y/h')

# 坐标轴范围
plt.axis([-0.1, 4.5, -0.1, 4.5])
# plt.legend(loc='upper left')
plt.legend(loc='best')
plt.savefig('liner_gression_error.png', dpi=200)
plt.show()
