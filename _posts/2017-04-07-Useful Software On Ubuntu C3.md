---
layout:     post
title:      "Useful Software On Ubuntu C3"
subtitle:   "I was cast upon thee from the womb:
thou art my God from my mother's belly. Psa 22:10"
date:       Fri, Apr 7 2017 09:41:47 GMT+8
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


### 远程控制windows

##### ubuntu端

安装命令：`sudo apt-get install rdesktop`

输入命令：`rdesktop -f -a 16  10.0.0.41`

参数解释：`-f`:全屏; `-a`:16位色 `10.0.0.41`:windows端IP

输入账户密码：`Administator`，`××××××××`

切换：

1. 用`Ctrl + Alt + Enter`可以退出全屏模式吗，然后就可以最小化窗口。
2. 再按下`Ctrl + Alt + Enter`又可以回到全屏模式。

##### windows端

1. 我的电脑--->控制面板--->用户帐户--->Administator--->管理帐户\更改帐户--->添加密码`××××××××`

2. 我的电脑--->右键--->属性--->远程设置--->远程--->*勾选*允许远程链接此计算机--->选择用户--->*添加* Administator(实际已有)

P.S. 如果添加其他用户，需要授予权限。

### 一鼠标一键盘控制多计算机

##### 两台windows

[mouse without borders使用方法](http://jingyan.baidu.com/article/77b8dc7fe512076174eab6cc.html)

##### 一台linux一台windows

这时候mouse without borders就不行了！运用Synergy！

[Synergy安装方法](http://www.cnblogs.com/gis_gps/archive/2012/10/27/2742526.html)

p.s. 

1. mode选择OFB，然后输入密码

2. 两台计算机上的synergy版本要相同，作者均是1.4.12

### Rapidsvn

##### 介绍
svn是一种版本管理，类似git

##### 安装

在software中输入rapidsvn，下载即可

具体使用方法见：[linux教程：[1]Ubuntu下安装使用SVN](http://jingyan.baidu.com/article/647f01159232ee7f2048a85d.html)


### wps

##### 介绍

一个办公软件，有时间再试下microsoft office系类

##### 安装

官网[wps](http://www.wps.cn/)：下载linux版本

命令：`sudo dpkg -i wps-office_10.1.0.5444~a20_amd64.deb`

出现问题：`sudo apt-get -f install`

再次执行：`sudo dpkg -i wps-office_10.1.0.5444~a20_amd64.deb`


### sftp

##### 介绍

sftp 是一个交互式文件传输程式。它类似于 ftp, 但它进行加密传输，比FTP有更高的安全性。下边就简单介绍一下如何远程连接主机，进行文件的上传和下载，以及一些相关操作。

##### 操作

命令：`sftp usr@192.168.1.243`

上传：`put xxxx(本地单个问题件) xxxx(远程某文文件路径)`

对于文件夹：`put -r dir/. xxxx/dir(需要提前建好)`

下载：`get xxx xxx`

##### 通过shell来快速上传与下载

安装： `sudo apt-get install -y lftp`

sftp.shell:

``` bash
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

##### 参考

1. [linux下如何使用sftp命令](http://www.cnblogs.com/chen1987lei/archive/2010/11/26/1888391.html)

2. [ftp/sftp自动上传、下载脚本](http://blog.csdn.net/ligt0610/article/details/7255817)

3. [shell调用ftp（sftp）实现自动批量上传（下载）](http://my.oschina.net/u/1377935/blog/262209)

关于**挂载**的博客：

1. [如何在 Linux 上使用 SSHfs 挂载一个远程文件系统](https://linux.cn/article-6586-1.html)

2. [Ubuntu下使用sshfs挂载远程目录到本地](http://blog.csdn.net/netwalk/article/details/12952719)


### clamav

##### 介绍

Clam AntiVirus是一个类UNIX系统上使用的反病毒软件包。

##### 安装

命令:`sudo apt-get install clamav -y`

对于GUI:`sudo apt-get install clamtk -y`

##### 操作
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


##### 参考博客

1. [How do I scan for viruses with ClamAV?](http://askubuntu.com/questions/250290/how-do-i-scan-for-viruses-with-clamav)

2. [Thread: clamav and all files scan](https://ubuntuforums.org/showthread.php?t=2061307)
 

### F.lux

##### 介绍

是一个多平台（windows,macos,linux）可以通过调节屏幕的色温来达到保护眼睛的效果，对于长时间使用电脑的人来说应该是比较必要的，该软件可以根据用户指定的位置的日出日落时间自动的调整屏幕的色温。

##### 安装

* gui网站：[F.Lux For Ubuntu](https://kilianvalkhof.com/2010/linux/flux-for-ubuntu/)

* `sudo add-apt-repository ppa:kilian/f.lux`

* `sudo apt-get update`

* `sudo apt-get install fluxgui`


##### 设置经纬度

杭州经度：120.19， 维度：30.26

##### 博文

1. [f.lux怎么设置](http://zhidao.baidu.com/question/495460575605868924.html)

2. [f.lux - 全天候保护眼睛健康软件！自动调整屏幕色温减少蓝光防疲劳，长时间玩电脑必备！](http://www.iplaysoft.com/flux.html)

##### 问题

1. 两台ubuntu，有一台很正常，另外一台perference点击没反应

2. 没找到相关设置，晚上偏黄

### redshift

##### 介绍

和flux一样，官网：[redshift](http://jonls.dk/redshift/)

##### 安装

命令： `sudo apt-get install gtk-redshift`

##### 操作

gtk-redshift 执行 && 勾选 Autostart
或者生成配置文件 vim ~/.config/redshift.conf(详见官网说明)
redshift.conf内容如下：

``` bash
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

##### 博文

1. [f.lux & redshift](http://blog.csdn.net/u014015972/article/details/50667845) 

2. [推荐一款软件Redshift，通俗点讲就是去蓝光咯](http://tieba.baidu.com/p/4033030555)


### SecureCRT

##### 介绍

如果经常ssh远程的计算机，为了避免多次输入账户密码，可使用SecureCRT

##### 博文

1. [ubuntu14.04 SecureCRT 安装破解](http://www.phperstar.com/post/323)

2. [Linux（Ubuntu）下面SecureCRT 完全破解](http://www.cnblogs.com/wangkongming/p/3533240.html)

##### 设置字体与背景颜色

* 背景颜色：
Options ➡️ Global Options ➡️ Terminal ➡️ Advanced ➡️ Monochrome ➡️ Edit
我的设置： Foreground:RGB(0, 255, 0), Background: RGB(0, 0, 0)

* 字体
Options ➡️ Session Options ➡️ Termainl ➡️ Apperance 



<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。