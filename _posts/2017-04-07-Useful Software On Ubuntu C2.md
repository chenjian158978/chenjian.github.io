---
layout:     post
title:      "Useful Software On Ubuntu C2"
subtitle:   "He trusted on the Lord that he would deliver him:
let him deliver him, seeing he delighted in him. Psa 22:8"
date:       Fri, Apr 7 2017 09:15:53 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Useful-Software-On-Ubuntu/head_blog.jpg"
catalog:    true
tags:
    - 工作
    - Ubuntu
---

### 系列博文

- [Useful Software On Ubuntu C1](https://o-my-chenjian.com/2016/04/25/Useful-Software-On-Ubuntu-C1/)
	- [Ubuntu](https://o-my-chenjian.com/2016/04/25/Useful-Software-On-Ubuntu-C1/#ubuntu)
	- [Terminator](https://o-my-chenjian.com/2016/04/25/Useful-Software-On-Ubuntu-C1/#terminator)
	- [Uget+aria2](https://o-my-chenjian.com/2016/04/25/Useful-Software-On-Ubuntu-C1/#ugetaria2)
	- [Google Chrome](https://o-my-chenjian.com/2016/04/25/Useful-Software-On-Ubuntu-C1/#google-chrome)
	- [Leanote](https://o-my-chenjian.com/2016/04/25/Useful-Software-On-Ubuntu-C1/#leanote)
	- [Vim](https://o-my-chenjian.com/2016/04/25/Useful-Software-On-Ubuntu-C1/#vim)
	- [Python](https://o-my-chenjian.com/2016/04/25/Useful-Software-On-Ubuntu-C1/#python)
	- [搜狗输入法](https://o-my-chenjian.com/2016/04/25/Useful-Software-On-Ubuntu-C1/#搜狗输入法)
	- [12VPN](https://o-my-chenjian.com/2016/04/25/Useful-Software-On-Ubuntu-C1/#12vpn)
	- [源](https://o-my-chenjian.com/2016/04/25/Useful-Software-On-Ubuntu-C1/#源)

- [Useful Software On Ubuntu C2](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C2/)
	- [Git](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C2/#git)
	- [Navicat](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C2/#navicat)
	- [JDK](https://o-my-chenjian.com/20172017/04/07/04/07/Useful-Software-On-Ubuntu-C2/#jdk)
	- [Pycharm](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C2/#pycharm)
	- [Eclipse](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C2/#eclipse)
	- [VLC](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C2/#vlc)
	- [MySQL](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C2/#mysql)
	- [RabbitMQ](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C2/#rabbitmq)
	- [Wine](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C2/#wine)
	- [Tree](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C2/#tree)

- [Useful Software On Ubuntu C3](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/)
	- [远程控制windows](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/#远程控制windows)
	- [一鼠标一键盘控制多计算机](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/#一鼠标一键盘控制多计算机)
	- [Rapidsvn](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/#rapidsvn)
	- [wps](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/#wps)
	- [sftp](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/#sftp)
	- [clamav](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/#clamav)
	- [F.lux](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/#flux)
	- [redshift](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/#redshift)
	- [SecureCRT](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/#securecrt)
	


### Git

##### 介绍

版本管理工具

##### 安装

命令：`sudo apt-get install git`

##### 全局变量初始化

用户名称：`git config --global user.name"`

用户邮箱：`git config --global user.email`



### Navicat

##### 介绍

Navicat是一套快速、可靠并价格相宜的数据库管理工具，专为简化数据库的管理及降低系统管理成本而设。

##### 安装

1. 在[navicat官网](https://www.navicat.com/products/navicat-for-mysql)下载相应的安装包

2. 解压到对应文件夹下

命令：`tar -zxvf navicat112_premium_en_x64.tar.gz`

3.  在终端运行start_navicat即可

命令：`./start_navicat`

4.  这时会安装wine。若没有反应，也请安装wine

##### 破解

命令：`rm -rf .navicat`,如果是64位,继续删，`rm -rf .navicat64`
这个操作相当于重新安装一次navicat，从而继续试用。

##### 桌面快捷方式
具体方法参考leanote的一节


### JDK

##### 介绍

JDK是Java 语言的软件开发工具包，主要用于移动设备、嵌入式设备上的java应用程序。

##### 安装

- 命令：

`sudo add-apt-repository ppa:webupd8team/java`

`sudo apt-get update`

`sudo apt-get install oracle-java8-installer`

- 测试：

`java -version`和`javac -version`

- 配置$JAVA_HOME 环境变量
	* 找到java的安装路径
	
	命令：`sudo update-alternatives --config java`
	
	返回结果：`There is only one alternative in link group java (providing /usr/bin/java): /usr/lib/jvm/java-8-oracle/jre/bin/java
Nothing to configure.`
	
	可知安装路径为：`/usr/lib/jvm/java-8-oracle`
	
	* 编写环境文件

	命令：`sudo nano /etc/environment`
	
	添加如下一行：`JAVA_HOME="/usr/lib/jvm/java-8-oracle"`
	
	* 重读环境文件
	
	命令：`source /etc/environment`
	
	* 测试
	
	命令：`echo $JAVA_HOME`
	
	返回：`/usr/lib/jvm/java-8-oracle`

* *重启系统后便可完全使用*


### Pycharm

##### 介绍

PyCharm是一种Python IDE，带有一整套可以帮助用户在使用Python语言开发时提高其效率的工具，比如调试、语法高亮、Project管理、代码跳转、智能提示、自动完成、单元测试、版本控制。此外，该IDE提供了一些高级功能，以用于支持Django框架下的专业Web开发。

##### 安装

参考：[Ubuntu安装PyCharm](http://blog.csdn.net/werm520/article/details/41249113)

- 需要安装JDK，请参考JDK一节

- 在[pycharm官网](http://www.jetbrains.com/pycharm/download/#section=linux)中下载相应的程序，然后解压到相应的文件夹中

- 进入pycharm解压bin目录下：

命令：`cd /home/chenjian/App/pycharm-5.0.4/bin`

打开pycharm：`./pycharm.sh`

- 右键pycharm图标，选择`Lock to launcher`

##### 破解

5.0版本：第一次打开pycharm，在输入license的时候选择`License server`，输入`http://idea.lanyus.com`即可

2016.1版本注册码, 可以登录[http://idea.lanyus.com/](http://idea.lanyus.com/)获得

##### 配置

已经安装好了python,虽然有多个版本,但是通过virtualenv来管理了。于是在pychar中要设置好相应的python。

在File--->settings--->Project--->相应的项目--->Project Interpreter(python解释器)--->选择齿轮--->Add Local--->path--->填写/home/chenjian/.venv/python2.7/bin/python2.7

于是，pycharm中使用的你管理好的python2.7


### Eclipse

##### 介绍

Eclipse 是一个开放源代码的、基于Java的可扩展开发平台。就其本身而言，它只是一个框架和一组服务，用于通过插件组件构建开发环境。幸运的是，Eclipse 附带了一个标准的插件集，包括Java开发工具（Java Development Kit，JDK）。

##### 安装

1. 需要安装JDK，请参考JDK一节
2. 在[eclipse官网](http://www.eclipse.org/downloads/)中下载相应的程序，然后解压到相应的文件夹中
3. 打开安装文件夹中的eclipse程序
4. 右键eclipse图标，选择`Lock to launcher`


### VLC

##### 介绍

VLC是一款开源的多媒体播放器，适用于像Linux、Microsoft Windows、Mac OS X和Android这样的操作系统。VLC播放我们喜爱的影音作品，它可以支持多种格式的音视频格式，
例如：mpeg、divx、mov、mp3、mp4、dvd、vcd、wmv还有quicktime等。

##### 安装

命令：`sudo apt-get install vlc`

或者在ubuntu software中直接搜索安装即可


### MySQL

##### 介绍

Mysql是一个关系数据库，程序员必许会用

##### 安装

命令：

1. `sudo apt-get install mysql-server`

	P.S. 安装过程中输入root的秘密，勿忘！

2. `sudo apt-get isntall mysql-client`
3. `sudo apt-get install libmysqlclient-dev`
4. 检验是否成功：
	
	命令：`sudo netstat -tap | grep mysql`

	结果：
		
``` bash
tcp        0      0 localhost:mysql         *:*                     LISTEN      6087/mysqld
```

mysql处于监听状态，即为成功

##### 远程链接mysql

* 参考文章：
1. [Linux学习笔记：SQLyog链接linux虚拟机上的mysql数据库](http://blog.csdn.net/qq_33251859/article/details/51436021)
2. [允许ubuntu下mysql远程连接](http://blog.csdn.net/hunauchenym/article/details/6933038)

* 操作：

- `vim /etc/mysql/my.cnf`找到`bind-address = 127.0.0.1`
注释掉这行，如：`#bind-address = 127.0.0.1`

或者改为： `bind-address = 0.0.0.0`

允许任意IP访问；

或者自己指定一个IP地址。

- 重启 MySQL：`sudo /etc/init.d/mysql restart`

- 打开Linux命令窗口，进入超级用户。

命令：`[lin@localhost ~]$ su`

Password:输入超级用户密码

- 启动Mysql服务

命令：

``` bash
[root@localhost lin]# service mysqld start

Starting mysqld:                                           [  OK  ]
```

- 进入Mysql

命令：`[root@localhost lin]# mysql -u root -p password`

- 对用户进行远程访问授权

命令：

``` bash
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '密码' WITH GRANT OPTION;
	
Query OK, 0 rows affected (0.02 sec)
```

``` bash
mysql>  FLUSH PRIVILEGES;
	
Query OK, 0 rows affected (0.00 sec)
```

##### 卸载mysql

1. `sudo apt-get autoremove --purge mysql-server-5.5`

2. `sudo apt-get remove mysql-server`

3. `sudo apt-get remove mysql-common`

4. 如果有mysql-client等等,都删除掉

5. 清理残留数据:`dpkg -l |grep ^rc|awk '{print $2}' |sudo xargs dpkg -P`,多次使用直到没有数据


### RabbitMQ

##### 介绍

MQ全称为Message Queue, 消息队列（MQ）是一种应用程序对应用程序的通信方法。本版本为3.6.1

##### 安装

rabbitMQ需要erlang语言的支持，因此需要先安装erlang语言

命令：`sudo apt-get install erlang`

测试：启动`erl`，能否进入

在[rabbitMQ官网](http://www.rabbitmq.com/)中下载相应的ubuntu安装包deb,下载后双击即可安装完毕

##### 设置

添加用户：`sudo rabbitmqctl add_user chenjian chenjian`

添加虚拟队列： `sudo rabbitmqctl add_vhost chenjian`

添加后台管理插件：`sudo rabbitmq-plugins enable rabbitmq_management`

显示：

``` bash
The following plugins have been enabled:
  mochiweb
  webmachine
  rabbitmq_web_dispatch
  amqp_client
  rabbitmq_management_agent
  rabbitmq_management

```

进入[http://127.0.0.1:15672/](http://127.0.0.1:15672/),用guest(密码guest)修改chenjian为管理员账号

进入“chenjian”，将自己添加为虚拟管理员


### Wine

##### 介绍

wine是在linux系统下运行exe等windows软件

##### 安装

稳定版本(1.6.2)命令：

`sudo apt-get install wine`


开发版本（修改过很多bug）命令：

1. `sudo add-apt-repository ppa:wine/wine-builds`

2. `sudo apt-get update`

3. `sudo apt-get install wine-devel`


### Tree

##### 介绍

tree可以很方便的按照树状图展开当前目录下文件的结构

##### 安装
 
命令：`sudo apt-get insatll tree`

##### 效果

命令：`(python2.7) chenjian@chenjian-Rev-1-0:~/PycharmProjects/zqxt_admin$ tree .`

P.S. 输入`tree . /home/chenjian/tree_test.txt`可以将树结构导入txt文件中

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C2/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。