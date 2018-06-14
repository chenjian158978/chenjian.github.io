---
layout:     post
title:      "带你走进Linux内核工作室"
subtitle:   "Ideas About Inside The Linux Kernel"
date:       Tue, Apr 11 2017 13:07:03 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Ideas-About-Inside-The-Linux-Kernel/head_blog.jpg"
catalog:    true
tags: [Linux]
---

### 前言

无意中找到[turnoff.us/](https://turnoff.us/)，里面的漫画颇为有趣。其中一篇[Inside The Linux Kernel](https://turnoff.us/geek/inside-the-linux-kernel/)也能帮助我们理解Linux系统的内核工作原理。顺序是从下向上，从左到右。

### 全图

![inside-the-linux-kernel-full](https://turnoff.us/image/en/inside-the-linux-kernel-full.png)

### 文件系统层

![filesystem](/img/in-post/Ideas-About-Inside-The-Linux-Kernel/filesystem.png)

这一层是存放系统中的各种文件，它们按照一定的分类进行存储。


##### 进程

左边的小企鹅代表一个进程(Process)，而胸前贴着421号工号，代表它的进程号(PID, Process ID)为421号。它正在查阅文件，代表一个进程号为421号的进程在访问文件系统。

##### 看门狗

右边的小狗，它具有敏锐的嗅觉，代表看门狗(WatchDog)，它的任务就是监视系统的运行，可以在`/dev/`下面看到。可以参考[Linux 软件看门狗 watchdog](http://blog.csdn.net/liigo/article/details/9227205)

### 中心大厅层

![floorone](/img/in-post/Ideas-About-Inside-The-Linux-Kernel/floorone.png)

这一层好热闹！我们从左到右来看

##### 80端口

![apache](/img/in-post/Ideas-About-Inside-The-Linux-Kernel/apache.png)

一个工号为1341的小企鹅正守在门牌号80的门前，它头上插着一根羽毛。这个表示一个进程号为1341的进程正在处理80端口，这个端口负责http网站的进出。而那根羽毛，代表着Apache服务器的Logo。

![apache_logo](https://www.apache.org/img/asf_logo.png)

##### 定时任务

![Cron](/img/in-post/Ideas-About-Inside-The-Linux-Kernel/cron.png)

一个工号为217的小企鹅正着急的看着手表，汗流浃背。它代表一个进程号为217的进程正在处理定时任务(Crontab)，时间一到便要开始工作了。

##### FS通道

![FS](/img/in-post/Ideas-About-Inside-The-Linux-Kernel/fs.png)

这是一个向下的通道，小企鹅们可以通过这个通道进出。它代表着进程们可以通过该通道，进出文件系统(File System,FS)。

##### Linux桌面进程

![clown](/img/in-post/Ideas-About-Inside-The-Linux-Kernel/clown.png)

一个小丑正在乱跳。它代表着Linux的桌面系统Gnome的进程。这个我也是通过邮件与作者联系过，才知晓的。

在此，感谢作者的回答与帮助。

![gnome](/img/in-post/Ideas-About-Inside-The-Linux-Kernel/gnome.png)

##### 管道

![pipeline](/img/in-post/Ideas-About-Inside-The-Linux-Kernel/pipeline.png)

两个小企鹅正在费力的抬着一根管道。它代表两个进程通过管道(Pipeline)进行传输。可以参考[浅谈管道模型](http://blog.csdn.net/yanghua_kobe/article/details/7561016)

##### 21端口

![port21](/img/in-post/Ideas-About-Inside-The-Linux-Kernel/port21.png)

有一扇破旧不堪的门，上面写着21号。它表示FTP协议下的21号端口，曾经的端口目前很少人使用了。

##### 区域进程表

![processtable](/img/in-post/Ideas-About-Inside-The-Linux-Kernel/processtable.png)

这一桌子好热闹，一个企鹅妈妈正在讲什么，其他的小企鹅有的认真听，有的在讲话，有的在瞌睡，各种状态都有。旁边有两个小狗。

企鹅妈妈代表着Linux的初始化进程，即进程号为1的进程。其他小企鹅代表着各种进程，他们正在等待1号进程发布工作安排与任务。而旁边的看门狗正在监管着这一切。

##### Wine

![wine](/img/in-post/Ideas-About-Inside-The-Linux-Kernel/wine.png)

看，这个工号为411的小企鹅右手端着红酒杯，已经不能再喝了。它表示的进程号为411的wine进程，专门负责windows的程序。其中wine就像Linux系统把自己灌醉，以为自己是windows系统，这样就可以执行exe程序了。我是这么理解的。


##### 22端口

![port22](/img/in-post/Ideas-About-Inside-The-Linux-Kernel/port22.png)

在门牌号22旁，有位超酷的企鹅，他带着墨镜与警徽，他是谁？！这表示着一个进程守护(SSH DAEMON)正在监管者22端口(SSH端口)，此端口提供远程连接与控制服务，万一有坏人进来怎么办，所以需要仔细审查。

### 终端层

![terminal](/img/in-post/Ideas-About-Inside-The-Linux-Kernel/terminal.png)

这一层有各种窗口，小企鹅们通过窗口获得任务，或者任务单号。

这代表着各个进程正在获取用户输入的命令(通过terminal或者桌面点击等等)，tty是Teletype的缩写，其为终端设备，或者就像键盘打字一样，可以在`/dev/`下面看到，也可以输入`tty`来参看当前输入的终端号。同时，tty7终端为桌面操作端口。

具体参考[Linux中TTY是什么意思](http://blog.csdn.net/hello_kate/article/details/47065673)

### 总结

整个Linux内核基本的结构展示出来，自己了解了pipeline，tty等等知识点。看来有兴趣可以看看[鳥哥的 Linux 私房菜](http://linux.vbird.org/#)，目前十分好奇。






