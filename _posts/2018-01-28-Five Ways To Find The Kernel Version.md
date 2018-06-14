---
layout:     post
title:      "五种获得Linux内核版本的方法"
subtitle:   "Five Ways To Find The Kernel Version"
date:       Sun, Jan 28 2018 22:44:51 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Five-Ways-To-Find-The-Kernel-Version/head_blog.jpg"
catalog:    true
tags: [工作, Linux]
---

### 前言

在特定的Linux系统中，知晓内核（Kernel）的版本号是非常有价值的。不仅仅是其本身的优势，更在于通过内核发布版本包含一些或大或小的改变与更新，可以帮助使用者诊断和升级系统。

幸运的是，获取这些信息是十分简单的，而且至少有五种方法可以使用。进一步来说，每一种方法可以通过一点点改变来获得更多的系统信息。

#### 内核版本号

面对Linux内核含有大量的校订与发行的特征,甚至新版本处在开发状态中，需要有一个系统来清楚的识别与管理它们。内核是一个程序，它是计算机操作系统的最主要的核心，用来控制系统之所有运行程序。Linux内核原由[Linus Torvalds](http://www.linfo.org/linus.html)基于`UNIX`和`MINIX`系统开发而来。

最初的Linux内核有个非常简单的版本系统。在1991年9月Torvalds发布后，命名为`0.01`。随后在下个月发布`0.02`版本的内核。当前的版本系统基于在1994年3月发布的内核`1.0`版本。

现在，Linux内核版本由一系列4个数组成，偶尔还会添加一系列字符。

```
3.10.0-693.el7.x86_64
大版本.开发版本/稳定版本.释出版本-修改版本 
```

`第一位数`为内核大版本。它很少变化，只有涉及到**内核概念或内核代码发生重大改变**时才会改变。

`第二位数`可分为内核两条线，其中第二位数为奇数时，例如`7`或`9`，表示该版本为**开发版本（不适合生产环境）**,该版本主要由内核开发人员使用。如果有新代码的更新，会更新到这个分支上。当第二位数为偶数时，例如`8`或`10`,表示该版本为**稳定版本**,该版本由家庭或者企业进行使用，主要是提供一个稳定环境。

`第三位数`为释出版本。在前两位架构不变的情况下，新增的功能累积到一定的程度后所新释出的核心版本。 而由于Linux核心是使用GPL的授权，因此大家都能够进行核心程序代码的修改。因此，如果你有针对某个版本的核心修改过部分的程序代码， 那么那个被修改过的新的核心版本就可以加上所谓的修改版本了。

`第四位数`为修改版本。主要是标识一些安全性问题解决，或者bug的修复。

### 五个方法

##### [uname命令](http://www.runoob.com/linux/linux-comm-uname.html)

最简单的便是`uname命令`（用来获取系统的软硬件信息）加上`-r参数`。

``` shell
# 显示操作系统内核版本
uname -r
<<'COMMENT'
3.10.0-693.el7.x86_64
COMMENT
```


该方法可以通过最少的输入,来获得最准确的的内核信息。

其他信息：

``` shell
# 显示系统信息
uname -a
<<'COMMENT'
Linux chenjian 3.10.0-693.el7.x86_64 #1 SMP Tue Aug 22 21:09:27 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux
COMMENT

# 显示操作内核名称
uname -s
<<'COMMENT'
Linux
COMMENT

# 显示计算机名
uname -n
<<'COMMENT'
chenjian
COMMENT

# 显示操作系统的版本
uname -v
#1 SMP Tue Aug 22 21:09:27 UTC 2017

# 显示操作系统处理器类型
uname -p
<<'COMMENT'
x86_64
COMMENT

# 显示硬件平台类型
uname -i
<<'COMMENT'
x86_64
COMMENT

# 显示操作系统类型
uname -o
<<'COMMENT'
GNU/Linux
COMMENT
```

##### 查看/proc/version文件

可以查看`/proc/version`文件信息,通过`cat命令`。

``` shell
cat /proc/version
<<'COMMENT'
Linux version 3.10.0-693.el7.x86_64 (builder@kbuilder.dev.centos.org) (gcc version 4.8.5 20150623 (Red Hat 4.8.5-16) (GCC) ) #1 SMP Tue Aug 22 21:09:27 UTC 2017
COMMENT
```

##### [rpm命令](http://www.runoob.com/linux/linux-comm-rpm.html)

可以通过`rpm命令`（红帽子包管理器）,加上参数`-q`和关键字`kernel`查询。

``` shell
rpm -q kernel
<<'COMMENT'
kernel-3.10.0-693.el7.x86_64
COMMENT
```

该命令其优势是输出结果只涉及到内核信息，而且其劣势是它只适用Linux的发行版本（[Major Linux Distributions](http://www.linfo.org/distributions_list.html)）中使用**rpm包管理系统**，例如红帽子（Red Hat）。

##### [dmesg命令](http://www.runoob.com/linux/linux-comm-dmesg.html)

可以通过`dmesg命令`的输出信息，即系统信息(自启动以后)。由于dmesg会产生大量输出结果,可以通过管道(Pipe)方式，然后以`grep命名`来进行过滤只包含关键字`Linux`的结果。

``` shell
dmesg | grep Linux

<<'COMMENT'
[    0.000000] Linux version 3.10.0-693.el7.x86_64 (builder@kbuilder.dev.centos.org) (gcc version 4.8.5 20150623 (Red Hat 4.8.5-16) (GCC) ) #1 SMP Tue Aug 22 21:09:27 UTC 2017
[    0.000091] SELinux:  Initializing.
[    0.000104] SELinux:  Starting in permissive mode
[    0.645414] [Firmware Bug]: ACPI: BIOS _OSI(Linux) query ignored
[    1.254357] SELinux:  Registering netfilter hooks
[    1.304016] Linux agpgart interface v0.103
[    1.314240] usb usb1: Manufacturer: Linux 3.10.0-693.el7.x86_64 ehci_hcd
[    1.324226] usb usb2: Manufacturer: Linux 3.10.0-693.el7.x86_64 ehci_hcd
[    1.325765] usb usb3: Manufacturer: Linux 3.10.0-693.el7.x86_64 xhci-hcd
[    1.327647] usb usb4: Manufacturer: Linux 3.10.0-693.el7.x86_64 xhci-hcd
[    2.369007] Loaded X.509 cert 'CentOS Linux kpatch signing key: ea0413152cde1d98ebdca3fe6f0230904c9ef717'
[    2.369025] Loaded X.509 cert 'CentOS Linux Driver update signing key: 7f421ee0ab69461574bb358861dbe77762a4201b'
[    2.369928] Loaded X.509 cert 'CentOS Linux kernel signing key: da187dca7dbe53ab05bd13bd0c4e21f422b6a49c'
[    2.690961] pps_core: LinuxPPS API ver. 1 registered
[    4.445001] SELinux:  Disabled at runtime.
[    4.445036] SELinux:  Unregistering netfilter hooks
COMMENT
```
该方法的劣势是需要额外的输出，而结果却包含大量非相关信息，需要进一步过滤。

##### 查看/boot文件夹

可以查看开发者在文件夹中遗留下来的源码包。这个方法在不同系统下会有不同结果，有些系统中根本不包含源码文件。内核通常存在`/boot`文件夹中，通过`ls -l命令`查看。

``` shell
ls -l /boot/
total 96888
-rw-r--r--. 1 root root   140894 Aug 23 05:21 config-3.10.0-693.el7.x86_64
drwxr-xr-x. 3 root root     4096 Jan 18 14:05 efi
drwxr-xr-x. 2 root root     4096 Jan 18 14:07 grub
drwx------. 5 root root     4096 Jan 18 14:14 grub2
-rw-------. 1 root root 48097208 Jan 18 14:11 initramfs-0-rescue-98e5da157c424125b7b4e1c40a1ac55c.img
-rw-------. 1 root root 18510467 Jan 18 14:14 initramfs-3.10.0-693.el7.x86_64.img
-rw-------  1 root root 16527966 Jan 18 14:20 initramfs-3.10.0-693.el7.x86_64kdump.img
-rw-r--r--. 1 root root   612108 Jan 18 14:10 initrd-plymouth.img
drwx------. 2 root root    16384 Jan 18 14:04 lost+found
-rw-r--r--. 1 root root   293027 Aug 23 05:24 symvers-3.10.0-693.el7.x86_64.gz
-rw-------. 1 root root  3228420 Aug 23 05:21 System.map-3.10.0-693.el7.x86_64
-rwxr-xr-x. 1 root root  5877760 Jan 18 14:11 vmlinuz-0-rescue-98e5da157c424125b7b4e1c40a1ac55c
-rwxr-xr-x. 1 root root  5877760 Aug 23 05:21 vmlinuz-3.10.0-693.el7.x86_64
```

这个命令输出一些版本参考，与当前已安装和正在运行内核相同，例如`vmlinuz-3.10.0-693.el7.x86_64`。`vmlinuz`是压缩后的Linux内核，其具有`可引导性`,也就是说它可以将操作系统加载到内存中，从而使计算机变得可用，应用程序能够运行。


### 参考博文

1. [How to Find The Kernel Version](http://www.linfo.org/find_kernel_version.html)

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2018/01/28/Five-Ways-To-Find-The-Kernel-Version/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。