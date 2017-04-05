---
layout:     post
title:      "Useful Software On Ubuntu"
subtitle:   "Hold up my goings in thy paths,
that my footsteps slip not. Psa 17:5"
date:       Mon, Apr 25 18:02:54 2016 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Useful-Software-On-Ubuntu/head_blog.jpg"
tags:
    - 工作
    - Ubuntu
---

## 摘要

由于一次又一次的安装系统，安装软件。此过程中的各种问题与配置简直让人头痛，所以产生了本篇博文，用来总结与更新此般经历的想法。本篇是安装在ubuntu16.04系统之上的内容，包含总多，例如vim，uget+aria2，navicat等等。而且随着跟新会越来越详细，也欢迎各位同仁提出意见与批评。好了，JUST DO IT！

作者原系统为windows7 64bit，采用双系统安装ubuntu16.04 64bit版本。



## Ubuntu

### 介绍

Ubuntu（乌班图）是一个以桌面应用为主的Linux操作系统，其名称来自非洲南部祖鲁语或豪萨语的“ubuntu”一词，意思是“人性”、“我的存在是因为大家的存在”，是非洲传统的一种价值观，类似华人社会的“仁爱”思想。

### 安装

本人使用windows7 64bit。

1. 计算机是否支持虚拟化技术
参考：[如何查看自己的电脑CPU是否支持硬件虚拟化](http://jingyan.baidu.com/article/fec7a1e5fe2f221190b4e7fe.html)

工具：`securable`

支持的话，建议安装虚拟机`VMware Workstation`,具体安装敬请期待！

不支持的话，请看下文；

2. 不支持虚拟化技术，采用windows/Ubuntu双系统

参考： [win7和ubuntu双系统安装](http://blog.sciencenet.cn/blog-685489-759452.html)

工具： `UltraISO`,`EasyBCD`

### 处理

1. 如何处理启动项删除

打开EasyBCD，点击”Edit Boot   Menu“，在"Entry"面板里就可以看到一系列的启动的选择了，选择一个像删除的，点击"Delete"就行了。

### 优化

1. 除去amazon：`sudo apt-get remove unity-webapps-common`

### 美化

- tweak安装

	`sudo add-apt-repository ppa:tualatrix/ppa`

	`sudo apt-get update`  

	`sudo apt-get install ubuntu-tweak`

-  Ultra flat 2.0主题安装网页：[ultra flat 2.0](http://www.ubuntuthemes.org/downloads/ultra-flat-2-0/)

	将其解压缩在`/usr/share/themes`中，再在tweak中将其打开

- Ultra-flat图标

	`sudo add-apt-repository ppa:noobslab/icons`

	`sudo apt-get update`

	蓝色图标（推荐）：`sudo apt-get install ultra-flat-icons`

	橘色图标（推荐）：`sudo apt-get install ultra-flat-icons-orange`

	绿色图标（推荐）：`sudo apt-get install ultra-flat-icons-green



## Terminator

### 介绍

Terminator是一款多窗口Linux终端，它支持将窗口拆分成多个，可以很方便的在各个不同的窗口上执行不同的任务

### 安装

命令：`sudo apt-get install terminator`

### 美化：

参考：[使用Terminator增强你的终端](http://blog.wentong.me/2014/05/work-with-terminator/)

配置文件路径：~/.config/terminator/config

p.s. 如果没有此文件，建议用vim建立

文件

```sh
[global_config]
  window_state = maximise
  suppress_multiple_term_dialog = True
  inactive_color_offset = 0.58
[keybindings]
[profiles]
  [[default]]
    use_system_font = False
    login_shell = True
    background_darkness = 0.92
    background_type = transparent
    background_image = None
    cursor_color = "#3036ec"
    foreground_color = "#00ff00"
    show_titlebar = False
    custom_command = tmux
    font = Monaco 10
[layouts]
  [[default]]
    [[[child1]]]
      type = Terminal
      parent = window0
      profile = default
    [[[window0]]]
      type = Window
      parent = ""
[plugins]
```

### 快捷键

1. Ctrl+T: ubuntu---System Settings---Keyboard---shortcuts---launch terminal---Ctrl+T

2. [terminator 的常用快捷键](http://www.cnblogs.com/xiazh/articles/2407328.html)



## Uget+aria2

### 介绍

ubuntu中的下载神器，类似win中的迅雷

### 安装

添加uget依赖：`sudo add-apt-repository ppa:plushuang-tw/uget-stable`

更新依赖：`sudo apt-get update`

安装uget：`sudo apt-get install uget`

添加aria2的依赖：`sudo add-apt-repository ppa:t-tujikawa/ppa`

更新依赖：`sudo apt-get update`

安装aria2：`sudo apt-get install aria2`

### 配置
* uget---All Category---右键---Properties---Default for new download1---Max Connections---16

* uget---右键---settings---Plug-in---Plug-in matching order---aria2
同时，下方的arguments: --enable-rpc=true 
如图：

### 备注

还有与firefox浏览器的插件，可以自寻资料



## Google Chrome

### 介绍

程序员必备浏览器，很好用，支持很多插件，例如evernote，vpn12等

### 安装

1. 不翻墙的话，可以去chrome百度贴吧中的资源有离线包；

2. 翻墙的话，直接去官网下载就行了。

命令：`sudo dpkg -i xxxx.deb`

出现问题：`sudo apt-get -f install`

再次执行：`sudo dpkg -i xxxx.deb`

### 配置

1. 在ubuntu16.04中chrome的字体有问题，可以在地址栏中输入：`chrome//settings/fonts`,随后进行修改

2. 关于登陆用户问题，建议先完成12vpn的安装与配置，在翻墙模式下登陆与同步

3. 编写search engines，其中keyword可用tab键，后面的url为搜索命令（不为首页url），如baidu的“https://www.baidu.com/s?wd=%s”

### 卸载

1. `sudo apt-get --purge remove google-chrome-stable`

2. 删除数据： `sudo rm -rf ~/.config/google-chrome`




## Leanote

### 介绍

leanote 是一款在线的云笔记服务,开源,支持Markdown,程序代码高亮,多人协作,笔记历史记录,可以直接将笔记发布为博客等功能。

如果大家也想用leanote可以找我，我来邀请你们！

### 安装

直接去[leanote.com](https://leanote.com/)中下载，解压后即可使用

### 桌面快捷方式

1. `cd /usr/share/applications`

2. `sudo gedit leanote.desktop`

3. 复制以下内容于leanote.desktop,注意每行的结尾不能有空格，Eexc为终端中可以执行软件的代码，Icon为图标路径

 ```
[Desktop Entry]
Name=leanote
Comment=Leanote IDE
Exec=/home/chenjian/App/Leanote/leanote
Icon=/home/chenjian/App/Leanote/leanote.png
Terminal=false
StartupNotify=true
Type=Application
Categories=Application;
 ```

p.s. 配置文件详见相应路径

4. 在/usr/share/applications中找到建立的桌面快捷方式，打开后右键图标，选择`Lock to Launcher `



## Vim

### 介绍

Vim是一个类似于Vi的著名的功能强大、高度可定制的文本编辑器，在Vi的基础上改进和增加了很多特性。

### 安装

命令:`sudo apt install vim -y`



## Python

### 介绍

这个是我吃饭用的。ubuntu中本身就有，建议不要删除，如果不嫌麻烦的话。

### 配置

参考：[在Ubuntu下配置舒服的Python开发环境](http://blog.csdn.net/kingppy/article/details/13080919)

主要用到virtualenv的版本管理利器,可以参考廖雪峰的文章[virtualenv](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432712108300322c61f256c74803b43bfd65c6f8d0d0000)。

命令：

- 安装pip：`sudo apt-get install python-pip`

- 安装virtualenv：`sudo pip install virtualenv`

- 尽量在 virtualenv 下进行 Python 包的安装:

命令：`virtualenv --no-site-packages -p /usr/bin/python2.7 ~/.venv/python2.7`

命令：`virtualenv --no-site-packages -p /usr/bin/python3.5 ~/.venv/python3.5`
 
- 然后将下面的代码增加到~/.bashrc的最后面，缺省使用 virtualenv 来代替系统 Python 环境：

命令：`sudo vim ~/.bashrc`

输入：

```sh
    if [ -f ~/.venv/python2.7/bin/activate ]; then
        . ~/.venv/python2.7/bin/activate
    fi
```

-  激活python2.7

命令：`source ~/.venv/python2.7/bin/activate`

- 在随后的终端中，我们会发现命令行头部都有`(python2.7)`，整个说明当前正在python2.7环境之下，所有的pip或者easy_install均在2.7版本环境之内。

转换到python3.5版本之下：

命令：`deactivate`

随后进入正常模式，激活python3.5模式：

命令：`source ~/.venv/python3.5/bin/activate`

- python2.7的路径为: /home/chenjian/.venv/python2.7/



## 搜狗输入法

### 介绍

全英文在中国还是混不下去的，只有装搜狗输入法

### 安装

不要随意删除ibus，强烈建议！

参考：[ubuntu14.04英文环境下安装中文输入法](http://my.oschina.net/No5stranger/blog/290026)

- 在software center中安装fcitx，安装好后系统任务栏右上角有一个fcitx图标（键盘）

- 在System Settings---Language Support---Keyboard input method system---fcitx

- [http://pinyin.sogou.com/](http://pinyin.sogou.com/)官网中，下载相应的
linux安装包deb

命令：`sudo dpkg -i xxxx.deb`

出现问题：`sudo apt-get -f install`

再次执行：`sudo dpkg -i xxxx.deb`

- Text Entry Setting---+---Chinese

- 设置fcitx---Input Method Configuration---Addon---sogoupinyin---configure

- 在Input Method中可以查看当前输入法



## 12VPN

### 介绍

这是一个翻墙软件，还挺不错的。以下操作在你购买了一个账号再说！

### 在chrome中的插件

在[vpn12官网](https://twelverocks.com/)中下载CRX文件，打开chrome的扩展页面，将CRX文件拖入其中便可安装，随后输入账户与密码便可翻墙。

### 在ubuntu系统中设置VPN，这是整个电脑能翻墙。

参考：[12vpn官网说明ubuntu安装](https://tweleverocks.com/downloads/ubuntu-14-10/)

安装openvonnect客户端：`sudo apt-get install network-manager-openconnect-gnome`

...


## 源

### 原先使用163源，最近改用阿里云源

### 更新

参考：[Ubuntu怎样修改软件源地址——高峰必备](http://jingyan.baidu.com/article/75ab0bcbea7e43d6864db2f1.html)

## Git

### 介绍

版本管理工具

### 安装

命令：`sudo apt-get install git`

### 全局变量初始化

用户名称：`git config --global user.name"`

用户邮箱：`git config --global user.email`



## Navicat

### 介绍

Navicat是一套快速、可靠并价格相宜的数据库管理工具，专为简化数据库的管理及降低系统管理成本而设。

### 安装

1. 在[navicat官网](https://www.navicat.com/products/navicat-for-mysql)下载相应的安装包

2. 解压到对应文件夹下

命令：`tar -zxvf navicat112_premium_en_x64.tar.gz`

3.  在终端运行start_navicat即可

命令：`./start_navicat`

4.  这时会安装wine。若没有反应，也请安装wine

### 破解

命令：`rm -rf .navicat`,如果是64位,继续删，`rm -rf .navicat64`
这个操作相当于重新安装一次navicat，从而继续试用。

### 桌面快捷方式
具体方法参考leanote的一节


## JDK

### 介绍

JDK是Java 语言的软件开发工具包，主要用于移动设备、嵌入式设备上的java应用程序。

### 安装

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


## Pycharm

### 介绍

PyCharm是一种Python IDE，带有一整套可以帮助用户在使用Python语言开发时提高其效率的工具，比如调试、语法高亮、Project管理、代码跳转、智能提示、自动完成、单元测试、版本控制。此外，该IDE提供了一些高级功能，以用于支持Django框架下的专业Web开发。

### 安装

参考：[Ubuntu安装PyCharm](http://blog.csdn.net/werm520/article/details/41249113)

- 需要安装JDK，请参考JDK一节

- 在[pycharm官网](http://www.jetbrains.com/pycharm/download/#section=linux)中下载相应的程序，然后解压到相应的文件夹中

- 进入pycharm解压bin目录下：

命令：`cd /home/chenjian/App/pycharm-5.0.4/bin`

打开pycharm：`./pycharm.sh`

- 右键pycharm图标，选择`Lock to launcher`

### 破解

5.0版本：第一次打开pycharm，在输入license的时候选择`License server`，输入`http://idea.lanyus.com`即可

2016.1版本注册码：

```sh
43B4A73YYJ-eyJsaWNlbnNlSWQiOiI0M0I0QTczWVlKIiwibGljZW5zZWVOYW1lIjoibGFuIHl1IiwiYXNzaWduZWVOYW1lIjoiIiwiYXNzaWduZWVFbWFpbCI6IiIsImxpY2Vuc2VSZXN0cmljdGlvbiI6IkZvciBlZHVjYXRpb25hbCB1c2Ugb25seSIsImNoZWNrQ29uY3VycmVudFVzZSI6ZmFsc2UsInByb2R1Y3RzIjpbeyJjb2RlIjoiSUkiLCJwYWlkVXBUbyI6IjIwMTctMDItMjUifSx7ImNvZGUiOiJBQyIsInBhaWRVcFRvIjoiMjAxNy0wMi0yNSJ9LHsiY29kZSI6IkRQTiIsInBhaWRVcFRvIjoiMjAxNy0wMi0yNSJ9LHsiY29kZSI6IlBTIiwicGFpZFVwVG8iOiIyMDE3LTAyLTI1In0seyJjb2RlIjoiRE0iLCJwYWlkVXBUbyI6IjIwMTctMDItMjUifSx7ImNvZGUiOiJDTCIsInBhaWRVcFRvIjoiMjAxNy0wMi0yNSJ9LHsiY29kZSI6IlJTMCIsInBhaWRVcFRvIjoiMjAxNy0wMi0yNSJ9LHsiY29kZSI6IlJDIiwicGFpZFVwVG8iOiIyMDE3LTAyLTI1In0seyJjb2RlIjoiUEMiLCJwYWlkVXBUbyI6IjIwMTctMDItMjUifSx7ImNvZGUiOiJSTSIsInBhaWRVcFRvIjoiMjAxNy0wMi0yNSJ9LHsiY29kZSI6IldTIiwicGFpZFVwVG8iOiIyMDE3LTAyLTI1In0seyJjb2RlIjoiREIiLCJwYWlkVXBUbyI6IjIwMTctMDItMjUifSx7ImNvZGUiOiJEQyIsInBhaWRVcFRvIjoiMjAxNy0wMi0yNSJ9XSwiaGFzaCI6IjMzOTgyOTkvMCIsImdyYWNlUGVyaW9kRGF5cyI6MCwiYXV0b1Byb2xvbmdhdGVkIjpmYWxzZSwiaXNBdXRvUHJvbG9uZ2F0ZWQiOmZhbHNlfQ==-keaxIkRgXPKE4BR/ZTs7s7UkP92LBxRe57HvWamu1EHVXTcV1B4f/KNQIrpOpN6dgpjig5eMVMPmo7yMPl+bmwQ8pTZaCGFuLqCHD1ngo6ywHKIQy0nR249sAUVaCl2wGJwaO4JeOh1opUx8chzSBVRZBMz0/MGyygi7duYAff9JQqfH3p/BhDTNM8eKl6z5tnneZ8ZG5bG1XvqFTqWk4FhGsEWdK7B+He44hPjBxKQl2gmZAodb6g9YxfTHhVRKQY5hQ7KPXNvh3ikerHkoaL5apgsVBZJOTDE2KdYTnGLmqxghFx6L0ofqKI6hMr48ergMyflDk6wLNGWJvYHLWw==-MIIEPjCCAiagAwIBAgIBBTANBgkqhkiG9w0BAQsFADAYMRYwFAYDVQQDDA1KZXRQcm9maWxlIENBMB4XDTE1MTEwMjA4MjE0OFoXDTE4MTEwMTA4MjE0OFowETEPMA0GA1UEAwwGcHJvZDN5MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxcQkq+zdxlR2mmRYBPzGbUNdMN6OaXiXzxIWtMEkrJMO/5oUfQJbLLuMSMK0QHFmaI37WShyxZcfRCidwXjot4zmNBKnlyHodDij/78TmVqFl8nOeD5+07B8VEaIu7c3E1N+e1doC6wht4I4+IEmtsPAdoaj5WCQVQbrI8KeT8M9VcBIWX7fD0fhexfg3ZRt0xqwMcXGNp3DdJHiO0rCdU+Itv7EmtnSVq9jBG1usMSFvMowR25mju2JcPFp1+I4ZI+FqgR8gyG8oiNDyNEoAbsR3lOpI7grUYSvkB/xVy/VoklPCK2h0f0GJxFjnye8NT1PAywoyl7RmiAVRE/EKwIDAQABo4GZMIGWMAkGA1UdEwQCMAAwHQYDVR0OBBYEFGEpG9oZGcfLMGNBkY7SgHiMGgTcMEgGA1UdIwRBMD+AFKOetkhnQhI2Qb1t4Lm0oFKLl/GzoRykGjAYMRYwFAYDVQQDDA1KZXRQcm9maWxlIENBggkA0myxg7KDeeEwEwYDVR0lBAwwCgYIKwYBBQUHAwEwCwYDVR0PBAQDAgWgMA0GCSqGSIb3DQEBCwUAA4ICAQC9WZuYgQedSuOc5TOUSrRigMw4/+wuC5EtZBfvdl4HT/8vzMW/oUlIP4YCvA0XKyBaCJ2iX+ZCDKoPfiYXiaSiH+HxAPV6J79vvouxKrWg2XV6ShFtPLP+0gPdGq3x9R3+kJbmAm8w+FOdlWqAfJrLvpzMGNeDU14YGXiZ9bVzmIQbwrBA+c/F4tlK/DV07dsNExihqFoibnqDiVNTGombaU2dDup2gwKdL81ua8EIcGNExHe82kjF4zwfadHk3bQVvbfdAwxcDy4xBjs3L4raPLU3yenSzr/OEur1+jfOxnQSmEcMXKXgrAQ9U55gwjcOFKrgOxEdek/Sk1VfOjvS+nuM4eyEruFMfaZHzoQiuw4IqgGc45ohFH0UUyjYcuFxxDSU9lMCv8qdHKm+wnPRb0l9l5vXsCBDuhAGYD6ss+Ga+aDY6f/qXZuUCEUOH3QUNbbCUlviSz6+GiRnt1kA9N2Qachl+2yBfaqUqr8h7Z2gsx5LcIf5kYNsqJ0GavXTVyWh7PYiKX4bs354ZQLUwwa/cG++2+wNWP+HtBhVxMRNTdVhSm38AknZlD+PTAsWGu9GyLmhti2EnVwGybSD2Dxmhxk3IPCkhKAK+pl0eWYGZWG3tJ9mZ7SowcXLWDFAk0lRJnKGFMTggrWjV8GYpw5bq23VmIqqDLgkNzuoog==
```

### 配置

已经安装好了python,虽然有多个版本,但是通过virtualenv来管理了。于是在pychar中要设置好相应的python。

在File--->settings--->Project--->相应的项目--->Project Interpreter(python解释器)--->选择齿轮--->Add Local--->path--->填写/home/chenjian/.venv/python2.7/bin/python2.7

于是，pycharm中使用的你管理好的python2.7


## Eclipse

### 介绍

Eclipse 是一个开放源代码的、基于Java的可扩展开发平台。就其本身而言，它只是一个框架和一组服务，用于通过插件组件构建开发环境。幸运的是，Eclipse 附带了一个标准的插件集，包括Java开发工具（Java Development Kit，JDK）。

### 安装

1. 需要安装JDK，请参考JDK一节
2. 在[eclipse官网](http://www.eclipse.org/downloads/)中下载相应的程序，然后解压到相应的文件夹中
3. 打开安装文件夹中的eclipse程序
4. 右键eclipse图标，选择`Lock to launcher`


## VLC

### 介绍

VLC是一款开源的多媒体播放器，适用于像Linux、Microsoft Windows、Mac OS X和Android这样的操作系统。VLC播放我们喜爱的影音作品，它可以支持多种格式的音视频格式，
例如：mpeg、divx、mov、mp3、mp4、dvd、vcd、wmv还有quicktime等。

### 安装

命令：`sudo apt-get install vlc`

或者在ubuntu software中直接搜索安装即可


## MySQL

### 介绍

Mysql是一个关系数据库，程序员必许会用

### 安装

命令：

1. `sudo apt-get install mysql-server`

	P.S. 安装过程中输入root的秘密，勿忘！

2. `sudo apt-get isntall mysql-client`
3. `sudo apt-get install libmysqlclient-dev`
4. 检验是否成功：
	
	命令：`sudo netstat -tap | grep mysql`

	结果：
		
	```
	tcp        0      0 localhost:mysql         *:*                     LISTEN      6087/mysqld
	```
	mysql处于监听状态，即为成功

### 远程链接mysql

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

```sh
[root@localhost lin]# service mysqld start

Starting mysqld:                                           [  OK  ]
```

- 进入Mysql

命令：`[root@localhost lin]# mysql -u root -p password`

- 对用户进行远程访问授权

命令：

```sh
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '密码' WITH GRANT OPTION;
	
Query OK, 0 rows affected (0.02 sec)
```

```sh
mysql>  FLUSH PRIVILEGES;
	
Query OK, 0 rows affected (0.00 sec)
```

### 卸载mysql

1. `sudo apt-get autoremove --purge mysql-server-5.5`

2. `sudo apt-get remove mysql-server`

3. `sudo apt-get remove mysql-common`

4. 如果有mysql-client等等,都删除掉

5. 清理残留数据:`dpkg -l |grep ^rc|awk '{print $2}' |sudo xargs dpkg -P`,多次使用直到没有数据


## RabbitMQ

### 介绍

MQ全称为Message Queue, 消息队列（MQ）是一种应用程序对应用程序的通信方法。本版本为3.6.1

### 安装

rabbitMQ需要erlang语言的支持，因此需要先安装erlang语言

命令：`sudo apt-get install erlang`

测试：启动`erl`，能否进入

在[rabbitMQ官网](http://www.rabbitmq.com/)中下载相应的ubuntu安装包deb,下载后双击即可安装完毕

### 设置

添加用户：`sudo rabbitmqctl add_user chenjian chenjian`

添加虚拟队列： `sudo rabbitmqctl add_vhost chenjian`

添加后台管理插件：`sudo rabbitmq-plugins enable rabbitmq_management`

显示：

```sh
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


## Wine

### 介绍

wine是在linux系统下运行exe等windows软件

### 安装

稳定版本(1.6.2)命令：

`sudo apt-get install wine`


开发版本（修改过很多bug）命令：

1. `sudo add-apt-repository ppa:wine/wine-builds`

2. `sudo apt-get update`

3. `sudo apt-get install wine-devel`


## Tree

### 介绍

tree可以很方便的按照树状图展开当前目录下文件的结构

### 安装
 
命令：`sudo apt-get insatll tree`

### 效果

命令：`(python2.7) chenjian@chenjian-Rev-1-0:~/PycharmProjects/zqxt_admin$ tree .`

P.S. 输入`tree . /home/chenjian/tree_test.txt`可以将树结构导入txt文件中

## 远程控制windows

### ubuntu端

安装命令：`sudo apt-get install rdesktop`

输入命令：`rdesktop -f -a 16  10.0.0.41`

参数解释：`-f`:全屏; `-a`:16位色 `10.0.0.41`:windows端IP

输入账户密码：`Administator`，`××××××××`

切换：

1. 用`Ctrl + Alt + Enter`可以退出全屏模式吗，然后就可以最小化窗口。
2. 再按下`Ctrl + Alt + Enter`又可以回到全屏模式。

### windows端

1. 我的电脑--->控制面板--->用户帐户--->Administator--->管理帐户\更改帐户--->添加密码`××××××××`

2. 我的电脑--->右键--->属性--->远程设置--->远程--->*勾选*允许远程链接此计算机--->选择用户--->*添加* Administator(实际已有)

P.S. 如果添加其他用户，需要授予权限。

## 一鼠标一键盘控制多计算机

### 两台windows

[mouse without borders使用方法](http://jingyan.baidu.com/article/77b8dc7fe512076174eab6cc.html)

### 一台linux一台windows

这时候mouse without borders就不行了！运用Synergy！

[Synergy安装方法](http://www.cnblogs.com/gis_gps/archive/2012/10/27/2742526.html)

p.s. 

1. mode选择OFB，然后输入密码

2. 两台计算机上的synergy版本要相同，作者均是1.4.12

## Rapidsvn

### 介绍
svn是一种版本管理，类似git

### 安装

在software中输入rapidsvn，下载即可

具体使用方法见：[linux教程：[1]Ubuntu下安装使用SVN](http://jingyan.baidu.com/article/647f01159232ee7f2048a85d.html)


## wps

###介绍

一个办公软件，有时间再试下microsoft office系类

### 安装

官网[wps](http://www.wps.cn/)：下载linux版本

命令：`sudo dpkg -i wps-office_10.1.0.5444~a20_amd64.deb`

出现问题：`sudo apt-get -f install`

再次执行：`sudo dpkg -i wps-office_10.1.0.5444~a20_amd64.deb`


## sftp

### 介绍

sftp 是一个交互式文件传输程式。它类似于 ftp, 但它进行加密传输，比FTP有更高的安全性。下边就简单介绍一下如何远程连接主机，进行文件的上传和下载，以及一些相关操作。

### 操作

命令：`sftp usr@192.168.1.243`

上传：`put xxxx(本地单个问题件) xxxx(远程某文文件路径)`

对于文件夹：`put -r dir/. xxxx/dir(需要提前建好)`

下载：`get xxx xxx`

### 通过shell来快速上传与下载

安装： `sudo apt-get install -y lftp`

sftp.shell:

``` sh
#!/usr/bin/env bash

HOST=10.0.0.174
USER=usr
PASSWORD=111222
FILENAME=$1
LOCAL_PATH=/var/webmonitor/hiddenlink_img/
REMOTE_PATH=/home/usr/hiddenlink_img/

lftp -u ${USER},${PASSWORD} sftp://${HOST} << EOF
  lcd ${LOCAL_PATH}
  cd ${REMOTE_PATH}
  put ${FILENAME}
  bye
EOF
```

命令： `./sftp.shell filename`

便可直接将文件上传过去

### 参考

1. [linux下如何使用sftp命令](http://www.cnblogs.com/chen1987lei/archive/2010/11/26/1888391.html)

2. [ftp/sftp自动上传、下载脚本](http://blog.csdn.net/ligt0610/article/details/7255817)

3. [shell调用ftp（sftp）实现自动批量上传（下载）](http://my.oschina.net/u/1377935/blog/262209)

关于**挂载**的博客：

1. [如何在 Linux 上使用 SSHfs 挂载一个远程文件系统](https://linux.cn/article-6586-1.html)

2. [Ubuntu下使用sshfs挂载远程目录到本地](http://blog.csdn.net/netwalk/article/details/12952719)


## clamav

### 介绍

Clam AntiVirus是一个类UNIX系统上使用的反病毒软件包。

### 安装

命令:`sudo apt-get install clamav -y`

对于GUI:`sudo apt-get install clamtk -y`

### 操作
- 对全文件进行扫描:

`sudo clamscan -r -i --bell / -l /home/chenjian/test.log --exclude-dir="^/sys"`

说明:

 *  -r 对整个文件夹
 * -l 保存为日志
 * -i 只显示受感染的文件
 * --bell 报警声
 * --exclude-dir除去不扫描的文件夹

- 更新病毒库

命令：`sudo freshclam`

- 查看clamav进程

命令： `ps ax |grep clam`


### 参考博客

1. [How do I scan for viruses with ClamAV?](http://askubuntu.com/questions/250290/how-do-i-scan-for-viruses-with-clamav)

2. [Thread: clamav and all files scan](https://ubuntuforums.org/showthread.php?t=2061307)
 

## F.lux

### 介绍

是一个多平台（windows,macos,linux）可以通过调节屏幕的色温来达到保护眼睛的效果，对于长时间使用电脑的人来说应该是比较必要的，该软件可以根据用户指定的位置的日出日落时间自动的调整屏幕的色温。

### 安装

* gui网站：[F.Lux For Ubuntu](https://kilianvalkhof.com/2010/linux/flux-for-ubuntu/)

* `sudo add-apt-repository ppa:kilian/f.lux`

* `sudo apt-get update`

* `sudo apt-get install fluxgui`


### 设置经纬度

杭州经度：120.19， 维度：30.26

### 博文

1. [f.lux怎么设置](http://zhidao.baidu.com/question/495460575605868924.html)

2. [f.lux - 全天候保护眼睛健康软件！自动调整屏幕色温减少蓝光防疲劳，长时间玩电脑必备！](http://www.iplaysoft.com/flux.html)

### 问题

1. 两台ubuntu，有一台很正常，另外一台perference点击没反应

2. 没找到相关设置，晚上偏黄

## redshift

### 介绍

和flux一样，官网：[redshift](http://jonls.dk/redshift/)

### 安装

命令： `sudo apt-get install gtk-redshift`

### 操作

gtk-redshift 执行 && 勾选 Autostart
或者生成配置文件 vim ~/.config/redshift.conf(详见官网说明)
redshift.conf内容如下：

```sh
; Global settings for redshift
[redshift]
; Set the day and night screen temperatures
temp-day=5500
temp-night=4500

; Enable/Disable a smooth transition between day and night
; 0 will cause a direct change from day to night screen temperature.
; 1 will gradually increase or decrease the screen temperature.
transition=1

; Set the screen brightness. Default is 1.0.
;brightness=0.9
; It is also possible to use different settings for day and night
; since version 1.8.
;brightness-day=0.7
;brightness-night=0.4
; Set the screen gamma (for all colors, or each color channel
; individually)
gamma=0.8
;gamma=0.8:0.7:0.8
; This can also be set individually for day and night since
; version 1.10.
;gamma-day=0.8:0.7:0.8
;gamma-night=0.6

; Set the location-provider: 'geoclue', 'geoclue2', 'manual'
; type 'redshift -l list' to see possible values.
; The location provider settings are in a different section.
location-provider=manual

; Set the adjustment-method: 'randr', 'vidmode'
; type 'redshift -m list' to see all possible values.
; 'randr' is the preferred method, 'vidmode' is an older API.
; but works in some cases when 'randr' does not.
; The adjustment method settings are in a different section.
adjustment-method=randr

; Configuration of the location-provider:
; type 'redshift -l PROVIDER:help' to see the settings.
; ex: 'redshift -l manual:help'
; Keep in mind that longitudes west of Greenwich (e.g. the Americas)
; are negative numbers.
[manual]
lat=30.26
lon=120.19

; Configuration of the adjustment-method
; type 'redshift -m METHOD:help' to see the settings.
; ex: 'redshift -m randr:help'
; In this example, randr is configured to adjust screen 1.
; Note that the numbering starts from 0, so this is actually the
; second screen. If this option is not specified, Redshift will try
; to adjust _all_ screens.
; [randr]
; screen=1

```

### 博文

1. [f.lux & redshift](http://blog.csdn.net/u014015972/article/details/50667845) 

2. [推荐一款软件Redshift，通俗点讲就是去蓝光咯](http://tieba.baidu.com/p/4033030555)


## SecureCRT

###介绍

如果经常ssh远程的计算机，为了避免多次输入账户密码，可使用SecureCRT

###博文

1. [ubuntu14.04 SecureCRT 安装破解](http://www.phperstar.com/post/323)

2. [Linux（Ubuntu）下面SecureCRT 完全破解](http://www.cnblogs.com/wangkongming/p/3533240.html)

### 设置字体与背景颜色

* 背景颜色：
Options $\rightarrow$ Global Options $\rightarrow$ Terminal $\rightarrow$ Advanced $\rightarrow$ Monochrome $\rightarrow$ Edit
我的设置： Foreground:RGB(0, 255, 0), Background: RGB(0, 0, 0)

* 字体
Options $\rightarrow$ Session Options $\rightarrow$ Termainl $\rightarrow$ Apperance 


## 作者与版权说明

作者：**陈健** 

邮箱：**chenjian158978@gmail.com** 

版权说明： **本评论版权属于作者陈健，并受法律保护。除非评论正文中另有声明，没有作者本人的书面许可任何人不得转载或使用整体或任何部分的内容。**
 



