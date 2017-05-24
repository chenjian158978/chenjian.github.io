---
layout:     post
title:      "机器学习之基本术语与理论"
subtitle:   "Basic Terms And Theory Of Machine Learning"
date:       Wed, May 24 2017 15:44:33 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Basic-Terms-And-Theory-Of-Machine-Learning/head_blog.jpg"
catalog:    true
mathjax:    true
tags:
    - 工作
    - 机器学习
---


### 涉及内容

1. 《机器学习》-刘志华-清华大学出版社
2. [machine-learning](https://www.coursera.org/learn/machine-learning/home/welcome) 斯坦福大学的Coursera教程

### 基本术语

**说明：**

这个世界上有N个西瓜，我们将所有的西瓜的数据全都记录下来

- 数据集(data set)：
	
	{(颜色:绿色; 尺寸:10; 形状:圆形; ...), (颜色:绿色; 尺寸:14; 形状:方形; ...), ...}
	
- 示例(instance)/样本(sample)：
	
	例如(颜色:绿色; 尺寸:10; 形状:圆形; ...)所代表的一个西瓜
	
- 属性(attribute)/特征(feature)

	例如：颜色，尺寸，形状的...
	
- 属性值(attribute value):

	绿色，10，圆形...
	
- 属性空间(attribute space)/样本空间(sample space)/输入空间(input space):

	{颜色，尺寸，形状, ...}
	
- 特征向量(feature vector):

	一个示例在属性空间中，其属性代表坐标轴，则可找到一个点代表该示例

综上所述，包含m个示例的数据集可表示如下：

$$D=\{x_{1}, x_{2}, ..., x_{m}\}$$

每个实例包含d个属性，该示例可以表示为d维样本空间\\(\chi\\)的一个向量\\(x_{i}\\)：

$$x_{i}=\{x_{i1};x_{i2};...x_{id}\}$$

其中，\\(x_{ij}\\)是\\(x_{i}\\)在第j个属性上的属性值，d为样本\\(x_{i}\\)的维数(dimensionality)

- 学习(learning)/训练(training):
	
	从数据中得到模型的过程
	
- 训练数据(training data):

	训练过程中使用的数据
	
- 训练样本(traing sample):

	训练中使用的每一个样本

- 训练集(training set)：

	训练样本的集合
	
- 假设(hypothesis)：
	
	训练过程中获得的某种规律

- 真相/真实(ground-truth):

	假设中存在的某种规律自身
	
- 模型(model)/学习器(learner):

	学习算法在数据和参数空间上的实例化
	
- 标记(label)：

	关于实例结果的信息

- 样例(example)：

	拥有标记信息的实例
	
- 标记空间(label space)/输出空间(output space):

	第i个样例可表示为\\((x_{i},y_{i})\\)，其中\\(y_{j}\in Y\\)是实例\\(x_{i}\\)的标记，\\(Y\\)为所有标记的集合
	
- 分类(classification):

	预测为离散值，例如“真”或者“假”
	
- 回归(regression):

	预测为连续值，例如0.1,0.2,0.3

- 二分类(binary classification)：

	只涉及两个类别的任务，一为正类(positive class)，另一为负类(negative class)
	
- 多分类(multi-class classification)：

	涉及多个类别的任务
	
综上所述，预测任务过程如下：

对训练集

$$\{(x_{1},y_{1}),(x_{2},y_{2}),...,(x_{m},y_{m})\}$$

进行学习，建立一个从输入空间\\(\chi\\)到输出空间\\(Y\\)的映射：

$$f:\chi \rightarrow Y$$

对于二分类任务，则\\(Y={-1, +1}或者{0,1}\\);

对于多分类任务，则\\(\|Y\|>2\\)；

对于回归任务，则\\(Y=R, R为实数集\\)。

- 测试(testing)：

	使用模型进行预测的过程

- 测试样本(testing sample)：

	测试中的样本
	
- 聚类(clustering)：

	对训练集进行分类

- 簇(cluster)：

	聚类中的每一组，其代表某些潜在概念
	
- 监督学习(supervised learning)：

	含有标记信息的学习任务，例如分类和回归
	
- 无监督学习(unsupervised learning)：

	不含有标记信息的学习任务，例如聚类
	
- 泛化(generalization)：

	模型对于新样本的适应能力

- 归纳(induction)：

	从特殊到一般的“泛化”的过程，例如“归纳学习(inductive learning)”
	
- 演绎(deduction)：

	从一般到特殊的“特化”的过程
	
- 假设空间(hypothesis space):

	所有样本组成的空间
	
- 版本空间(version space):

	与训练集一致的假设空间
	
### 基础理论

##### 奥卡姆剃刀(Occam's razor)

一种常用的，自然科学研究中最基础的思考原则，或者说原理，即

> Do not multiply entities beyond necessity, but also do not reduce them beyond necessity.

> 切勿浪费较多东西，去做‘用较少的东西，同样可以做好的事情’

换句话说，“若多个假设和观察一致时，选择最简单的那个”

##### “没有免费的午餐”定理(No Free Lunch Theorem, NFL定理)

没有优化算法适合于所有优化问题：只能说针对某一类优化问题，某某算法更有优势。而不能笼统的说，某种优化算法比另一种更优。

1. 算法基于具体问题，才有“好算法”之说；
2. 脱离具体问题，空谈“什么算法更好”毫无意义

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/05/24/Basic-Terms-And-Theory-Of-Machine-Learning/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	