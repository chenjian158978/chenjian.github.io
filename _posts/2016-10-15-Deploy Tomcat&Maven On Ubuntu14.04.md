---
layout:     post
title:      "在Ubuntu14.04上部署Tomcat和Maven"
subtitle:   "Deploy Tomcat&Maven On Ubuntu14.04"
date:       Mon, Oct 15 2016 09:52:25 2016 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Tomcat&Maven-On-Ubuntu14.04/head_blog.jpg"
catalog:    true
tags: [工作]
---

###  TOMCAT

##### tomcat介绍

Tomcat 服务器是一个免费的开放源代码的Web 应用服务器，属于轻量级应用服务器，在中小型系统和并发访问用户不是很多的场合下被普遍使用，是开发和调试JSP 程序的首选。对于一个初学者来说，可以这样认为，当在一台机器上配置好Apache 服务器，可利用它响应HTML（标准通用标记语言下的一个应用）页面的访问请求。实际上Tomcat 部分是Apache 服务器的扩展，但它是独立运行的，所以当你运行tomcat 时，它实际上作为一个与Apache 独立的进程单独运行的。

##### 下载

* tomcat官网：[tomcat官网](http://tomcat.apache.org/index.html)
* 找到下载页面的core下的tar.gz，下载

##### 安装

参考博客：

1. [Ubuntu14.04 安装配置Tomcat7服务器](https://my.oschina.net/u/1431757/blog/543563)

2. [ubuntu14.04 配置tomcat8](http://blog.csdn.net/xingjiarong/article/details/49386989)

3. [ubuntu14.04安装tomcat8](http://jinjzk.iteye.com/blog/2084151)

> 需要安装和配置JDK，请访问作者博客[CHENJIAN_blog](http://chenjian.leanote.com),进行查阅

命令：

- `sudo tar zxvf apache-tomcat-8.0.9.tar.gz -C /usr/local`

- `cd /usr/local`

- `sudo mv apache-tomcat-8.0.9/ tomcat8`

- `sudo chmod -R 777 /usr/local/tomcat8`

- `sudo su`

- `vim /etc/profile`

- 在最下方添加： `CATALINA_HOME=/usr/local/tomcat8`

- `source /etc/profile`

- `cd $CATALINA_HOME/bin`

- `vim catalina.sh`

- 在`# OS specific support. $var _must_ be set t`上面一行添加（看文件内容就知道为何要在这行添加）：

``` bash
CATALINA_HOME=/usr/local/tomcat8
JAVA_HOME=/usr/lib/jvm/java-8-oracle
JRE_HOME=${JAVA_HOME}/jre
PATH=$JAVA_HOME/bin:$PATH
CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
TOMCAT_HOME=/usr/lib/tomcat8
```

- `exit` 退出root

- `sudo $CATALINA_HOME/bin/startup.sh`

结果内容如下：

``` bash
Using CATALINA_BASE:   /usr/local/tomcat8
Using CATALINA_HOME:   /usr/local/tomcat8
Using CATALINA_TMPDIR: /usr/local/tomcat8/temp
Using JRE_HOME:        /usr/lib/jvm/java-8-oracle/jre
Using CLASSPATH:       /usr/local/tomcat8/bin/bootstrap.jar:/usr/local/tomcat8/bin/tomcat-juli.jar
Tomcat started.
```

- 安装tomcat服务:`sudo cp $CATALINA_HOME/bin/catalina.sh /etc/init.d/tomcat`

- 查看tomcat状态： `sudo service tomcat status` 或者 `/etc/init.d/tomcat status`

内容如下：

``` bash
Using CATALINA_BASE:   /usr/local/tomcat8
Using CATALINA_HOME:   /usr/local/tomcat8
Using CATALINA_TMPDIR: /usr/local/tomcat8/temp
Using JRE_HOME:        /usr/lib/jvm/java-8-oracle/jre
Using CLASSPATH:       /usr/local/tomcat8/bin/bootstrap.jar:/usr/local/tomcat8/bin/tomcat-juli.jar
Usage: catalina.sh ( commands ... )
commands:
  debug             Start Catalina in a debugger
  debug -security   Debug Catalina with a security manager
  jpda start        Start Catalina under JPDA debugger
  run               Start Catalina in the current window
  run -security     Start in the current window with security manager
  start             Start Catalina in a separate window
  start -security   Start in a separate window with security manager
  stop              Stop Catalina, waiting up to 5 seconds for the process to end
  stop n            Stop Catalina, waiting up to n seconds for the process to end
  stop -force       Stop Catalina, wait up to 5 seconds and then use kill -KILL if still running
  stop n -force     Stop Catalina, wait up to n seconds and then use kill -KILL if still running
  configtest        Run a basic syntax check on server.xml - check exit code for result
  version           What version of tomcat are you running?
Note: Waiting for the process to end and use of the -force option require that $CATALINA_PID is defined
```

- 在浏览器中输入`127.0.0.1:8080`，便可看到tomcat的界面


### MAVEN

##### 介绍

Maven项目对象模型(POM)，可以通过一小段描述信息来管理项目的构建，报告和文档的软件项目管理工具。

##### 下载

* [MAVEN官网](http://maven.apache.org/index.html)

* 找到download中的`apache-maven-3.3.9-bin.tar.gz`

##### 安装

- [ubuntu14.04安装maven](http://jinjzk.iteye.com/blog/2094289)
- [ubuntu maven环境安装配置](https://my.oschina.net/hongdengyan/blog/150472)https://my.oschina.net/hongdengyan/blog/150472

> 需要安装和配置JDK，请访问作者博客[CHENJIAN_blog](http://chenjian.leanote.com),进行查阅


- `sudo tar zxvf apache-maven-3.3.9-bin.tar.gz -C /usr/local`

- `cd /usr/local`

- `sudo mv apache-maven-3.3.9/ maven`

- `sudo chmod -R 777 /usr/local/maven`

- `sudo su`

- `vim /etc/profile`

在末尾加入：

``` bash
# maven setting
export M2_HOME=/usr/local/maven
export M2=$M2_HOME/bin  
export PATH=$M2:$PATH 
```

- `source /etc/profile`

- `mvn --version`

内容如下：

``` bash
Apache Maven 3.3.9 (bb52d8502b132ec0a5a3f4c09453c07478323dc5; 2015-11-11T00:41:47+08:00)
Maven home: /usr/local/maven
Java version: 1.8.0_101, vendor: Oracle Corporation
Java home: /usr/lib/jvm/java-8-oracle/jre
Default locale: en_US, platform encoding: UTF-8
OS name: "linux", version: "4.2.0-42-generic", arch: "amd64", family: "unix"
```

> **表示成功**

- 自动生成.m2目录：`mvn clean`

- `cp /usr/local/maven/conf/settings.xml  ~/.m2/`

- `sudo vim ~/.m2/settings.xml`

修改以下内容：

``` bash
<!-- localRepository
   | The path to the local repository maven will use to store artifacts.
   |
   | Default: ${user.home}/.m2/repository
  <localRepository>/path/to/local/repo</localRepository>
-->
```

为

``` bash
<!-- localRepository
   | The path to the local repository maven will use to store artifacts.
   |
   | Default: ${user.home}/.m2/repository
  <localRepository>/path/to/local/repo</localRepository>
  -->

 <localRepository>${user.home}/repository/maven</localRepository>
```

> ${user.home}/repository/maven是你maven本地仓库的路径。

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2016/10/15/Deploy-Tomcat&Maven-On-Ubuntu14.04/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
