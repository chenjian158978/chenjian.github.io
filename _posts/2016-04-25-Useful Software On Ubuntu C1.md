---
layout:     post
title:      "Ubuntu上的优秀软件之第一章节"
subtitle:   "Useful Software On Ubuntu C1"
date:       Mon, Apr 25 18:02:54 2016 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Useful-Software-On-Ubuntu/head_blog.jpg"
catalog:    true
tags: [工作, Ubuntu]
---

### 摘要

由于一次又一次的安装系统，安装软件。此过程中的各种问题与配置简直让人头痛，所以产生了本篇博文，用来总结与更新此般经历的想法。本篇是安装在ubuntu16.04系统之上的内容，包含总多，例如vim，uget+aria2，navicat等等。而且随着跟新会越来越详细，也欢迎各位同仁提出意见与批评。好了，JUST DO IT！

作者原系统为windows7 64bit，采用双系统安装ubuntu16.04 64bit版本。

### 系列博文

- [Ubuntu上的优秀软件之第一章节](https://o-my-chenjian.com/2016/04/25/Useful-Software-On-Ubuntu-C1/)
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

- [Ubuntu上的优秀软件之第二章节](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C2/)
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

- [Ubuntu上的优秀软件之第三章节](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/)
	- [远程控制windows](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/#远程控制windows)
	- [一鼠标一键盘控制多计算机](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/#一鼠标一键盘控制多计算机)
	- [Rapidsvn](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/#rapidsvn)
	- [wps](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/#wps)
	- [sftp](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/#sftp)
	- [clamav](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/#clamav)
	- [F.lux](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/#flux)
	- [redshift](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/#redshift)
	- [SecureCRT](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/#securecrt)
	

### Ubuntu

##### 介绍

Ubuntu（乌班图）是一个以桌面应用为主的Linux操作系统，其名称来自非洲南部祖鲁语或豪萨语的“ubuntu”一词，意思是“人性”、“我的存在是因为大家的存在”，是非洲传统的一种价值观，类似华人社会的“仁爱”思想。

##### 安装

本人使用windows7 64bit。

- 计算机是否支持虚拟化技术

参考：[如何查看自己的电脑CPU是否支持硬件虚拟化](http://jingyan.baidu.com/article/fec7a1e5fe2f221190b4e7fe.html)

工具：`securable`

支持的话，建议安装虚拟机`VMware Workstation`,具体安装敬请期待！

不支持的话，请看下文；

- 不支持虚拟化技术，采用windows/Ubuntu双系统

参考： [win7和ubuntu双系统安装](http://blog.sciencenet.cn/blog-685489-759452.html)

工具： `UltraISO`,`EasyBCD`

##### 处理

- 如何处理启动项删除

打开EasyBCD，点击”Edit Boot   Menu“，在"Entry"面板里就可以看到一系列的启动的选择了，选择一个像删除的，点击"Delete"就行了。

##### 优化

- 除去amazon：`sudo apt-get remove unity-webapps-common`

##### 美化

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

### Terminator

##### 介绍

Terminator是一款多窗口Linux终端，它支持将窗口拆分成多个，可以很方便的在各个不同的窗口上执行不同的任务

##### 安装

命令：`sudo apt-get install terminator`

##### 美化：

参考：[使用Terminator增强你的终端](http://blog.wentong.me/2014/05/work-with-terminator/)

配置文件路径：~/.config/terminator/config

p.s. 如果没有此文件，建议用vim建立

文件

``` bash
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

##### 快捷键

1. Ctrl+T: ubuntu---System Settings---Keyboard---shortcuts---launch terminal---Ctrl+T

2. [terminator 的常用快捷键](http://www.cnblogs.com/xiazh/articles/2407328.html)

### Uget+aria2

##### 介绍

ubuntu中的下载神器，类似win中的迅雷

##### 安装

添加uget依赖：`sudo add-apt-repository ppa:plushuang-tw/uget-stable`

更新依赖：`sudo apt-get update`

安装uget：`sudo apt-get install uget`

添加aria2的依赖：`sudo add-apt-repository ppa:t-tujikawa/ppa`

更新依赖：`sudo apt-get update`

安装aria2：`sudo apt-get install aria2`

##### 配置
* uget---All Category---右键---Properties---Default for new download1---Max Connections---16

* uget---右键---settings---Plug-in---Plug-in matching order---aria2
同时，下方的arguments: --enable-rpc=true 
如图：

##### 备注

还有与firefox浏览器的插件，可以自寻资料

### Google Chrome

##### 介绍

程序员必备浏览器，很好用，支持很多插件，例如evernote，vpn12等

##### 安装

1. 不翻墙的话，可以去chrome百度贴吧中的资源有离线包；

2. 翻墙的话，直接去官网下载就行了。

命令：`sudo dpkg -i xxxx.deb`

出现问题：`sudo apt-get -f install`

再次执行：`sudo dpkg -i xxxx.deb`

##### 配置

1. 在ubuntu16.04中chrome的字体有问题，可以在地址栏中输入：`chrome//settings/fonts`,随后进行修改

2. 关于登陆用户问题，建议先完成12vpn的安装与配置，在翻墙模式下登陆与同步

3. 编写search engines，其中keyword可用tab键，后面的url为搜索命令（不为首页url），如baidu的“https://www.baidu.com/s?wd=%s”

##### 卸载

1. `sudo apt-get --purge remove google-chrome-stable`

2. 删除数据： `sudo rm -rf ~/.config/google-chrome`


### Leanote

##### 介绍

leanote 是一款在线的云笔记服务,开源,支持Markdown,程序代码高亮,多人协作,笔记历史记录,可以直接将笔记发布为博客等功能。

如果大家也想用leanote可以找我，我来邀请你们！

##### 安装

直接去[leanote.com](https://leanote.com/)中下载，解压后即可使用

##### 桌面快捷方式

1. `cd /usr/share/applications`

2. `sudo gedit leanote.desktop`

3. 复制以下内容于leanote.desktop,注意每行的结尾不能有空格，Eexc为终端中可以执行软件的代码，Icon为图标路径

 ``` bash
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



### Vim

##### 介绍

Vim是一个类似于Vi的著名的功能强大、高度可定制的文本编辑器，在Vi的基础上改进和增加了很多特性。

##### 安装

命令:`sudo apt install vim -y`


### Python

##### 介绍

这个是我吃饭用的。ubuntu中本身就有，建议不要删除，如果不嫌麻烦的话。

##### 配置

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

``` bash
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



### 搜狗输入法

##### 介绍

全英文在中国还是混不下去的，只有装搜狗输入法

##### 安装

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

- 设置fcitx---Input Method Configuration---Input Method---添加---Sogou Pinyin(要大写)

- 设置fcitx---Input Method Configuration---Addon---sogoupinyin---configure

- 在Input Method中可以查看当前输入法


### 12VPN

##### 介绍

这是一个翻墙软件，还挺不错的。以下操作在你购买了一个账号再说！

2017/04/07 目前已不使用

##### 在chrome中的插件

在[vpn12官网](https://twelverocks.com/)中下载CRX文件，打开chrome的扩展页面，将CRX文件拖入其中便可安装，随后输入账户与密码便可翻墙。

##### 在ubuntu系统中设置VPN，这是整个电脑能翻墙。

参考：[12vpn官网说明ubuntu安装](https://tweleverocks.com/downloads/ubuntu-14-10/)

安装openvonnect客户端：`sudo apt-get install network-manager-openconnect-gnome`

...


### 源

##### 原先使用163源，最近改用阿里云源

##### 更新

参考：[Ubuntu怎样修改软件源地址——高峰必备](http://jingyan.baidu.com/article/75ab0bcbea7e43d6864db2f1.html)


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2016/04/25/Useful-Software-On-Ubuntu-C1/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
