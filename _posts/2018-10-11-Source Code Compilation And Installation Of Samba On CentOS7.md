---
layout:     post
title:      "在CentOS7上源码编译与安装Samba"
subtitle:   "Source Code Compilation And Installation Of Samba On CentOS7"
date:       Thu, Oct 11 2018 21:36:07 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Source-Code-Compilation-And-Installation-Of-Samba-On-CentOS7/head_blog.jpg"
catalog:    true
tags: [工作, Linux]
---

### samba简介

Samba是一个能让Linux系统应用Microsoft网络通讯协议的软件，而SMB是Server Message Block的缩写，即为服务器消息块 ，SMB主要是作为Microsoft的网络通讯协议，后来Samba将SMB通信协议应用到了Linux系统上，就形成了现在的Samba软件。后来微 软又把 SMB 改名为 CIFS（Common Internet File System），即公共 Internet 文件系统，并且加入了许多新的功能，这样一来，使得Samba具有了更强大的功能。

Samba最大的功能就是可以用于Linux与windows系统直接的文件共享和打印共享，Samba既可以用于windows与Linux 之间的文件共享，也可以用于Linux与Linux之间的资源共享，由于NFS(网络文件系统）可以很好的完成Linux与Linux之间的数据共享，因 而 Samba较多的用在了Linux与windows之间的数据共享上面。

SMB是基于客户机/服务器型的协议，因而一台Samba服务器既可以充当文件共享服务器，也可以充当一个Samba的客户端，例如，一台在 Linux 下已经架设好的Samba服务器，windows客户端就可以通过SMB协议共享Samba服务器上的资源文件，同时，Samba服务器也可以访问网络中 其它windows系统或者Linux系统共享出来的文件。
Samba在windows下使用的是NetBIOS协议，如果你要使用Linux下共享出来的文件，请确认你的windows系统下是否安装了NetBIOS协议。

组成Samba运行的有两个服务，一个是SMB，另一个是NMB；SMB是Samba 的核心启动服务，主要负责建立 Linux Samba服务器与Samba客户机之间的对话， 验证用户身份并提供对文件和打印系统的访问，只有SMB服务启动，才能实现文件的共享，监听139 TCP端口；而NMB服务是负责解析用的，类似与DNS实现的功能，NMB可以把Linux系统共享的工作组名称与其IP对应起来，如果NMB服务没有启 动，就只能通过IP来访问共享文件，监听137和138 UDP端口。

### 系统环境介绍

| 软件名称 | 版本说明 | 其他 |
| :------: | :------: |:--: |
| CentOS | 7.5.1804 | |
| samba | 4.9.1 | 协议GPL3 |
| SELIUNX | | 关闭 |
| firewalld | | 关闭 |
| windows | 7 | Service Pack 1 |

### 下载samba

``` shell
wget https://download.samba.org/pub/samba/stable/samba-4.9.1.tar.gz
```

### 安装samba

可以先阅读[samba官方安装文档](https://wiki.samba.org/index.php/Installing_Samba)

##### 解决依赖

以下的依赖包并非全部都要安装，主要还看用户使用需求，例如是使用AD DC还是别的。

``` shell
# CentOS 7
yum install attr bind-utils docbook-style-xsl gcc gdb krb5-workstation \
    libsemanage-python libxslt perl perl-ExtUtils-MakeMaker \
    perl-Parse-Yapp perl-Test-Base pkgconfig policycoreutils-python \
    python-crypto gnutls-devel libattr-devel keyutils-libs-devel \
    libacl-devel libaio-devel libblkid-devel libxml2-devel openldap-devel \
    pam-devel popt-devel python-devel readline-devel zlib-devel systemd-devel \
    lmdb-devel jansson-devel gpgme-devel python-gpgme libarchive-devel
```

##### 编译源码

在此使用samba的Daemon模式，而非AD DC模式，所以windows端访问samba需要使用IP。

``` shell
# 解压tar.gz
tar -zxf samba-4.9.1.tar.gz

cd samba-4.9.1
./configure --without-ad-dc --sbindir=/usr/sbin/  --sysconfdir=/etc/samba/ --mandir=/usr/share/man/

make -j 4
sudo make install
```

- 通过 `./configure --help`命令，可以查看相关参数；
- - 例如`--without-ad-dc`, 即不安装AD DC模式(能力)
- - 例如`--sbindir=/usr/sbin/`，执行文件放在`/usr/sbin`，而非默认的`/usr/local/samba/sbin/`中
- - 例如`--sysconfdir=/etc/samba/`，配置文件放在`/etc/samba/`，而非默认的`/usr/local/samba/etc/`中
- - 例如`--mandir=/usr/share/man/`，文档文件放在`/usr/share/man/`
- 通过`make -j 4`，可以同时并行4个子任务，使make更快；
- 通过`make test`，可以自行测试make；

##### 配置操作

``` shell
# 将samba命令加入系统环境中
echo "export PATH=$PATH:/usr/local/samba/bin/:/usr/local/samba/sbin" >> /etc/profile.d/samba.sh

# 将samba的动态链接库文件加入系统库环境中
echo "/usr/local/samba/lib" >> /etc/ld.so.conf.d/samba.conf 
ldconfig

# 输入chenjian用户的密码
(echo chenjian; echo chenjian) | /usr/local/samba/bin/smbpasswd -a -s -U chenjian
```

##### smb.conf文件

smb.conf文件定义了samba的安全机制、文件共享和打印共享的目录和参数以及其他一些系统配置功能。可以查阅[官方samba配置文档](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html)

``` text
# See smb.conf.example for a more detailed config file or
# read the smb.conf manpage.
# Run 'testparm' to verify the config is correct after
# you modified it.

[global]
	workgroup = WORKGROUP
	security = user

	passdb backend = tdbsam

	server signing = mandatory
	client signing = required

[chenjian]
	comment = Chen Jian Personal Directories
	path = /home/chenjian/
	guest ok = no
	browseable = yes
	writable = yes
```

- [global]

    该设置都是与Samba服务整体运行环境有关的选项，它的设置项目是针对所有共享资源的。

- workgroup = WORKGROUP
    
    相关资料可查阅[workgroup (G)](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html#WORKGROUP)

    设定 Samba Server 所要加入的工作组或者域。

- security = user
    
    相关资料可查阅[security (G)](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html#SECURITY)

    说明：设置用户访问Samba Server的验证方式，一共有四种验证方式AUTO,USER,DOMAIN和ADS。

- passdb backend = tdbsam

    相关资料可查阅[passdb backend (G)](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html#PASSDBBACKEND)

    passdb backend就是用户后台的意思。目前有三种后台：smbpasswd、tdbsam和ldapsam。sam应该是security account manager（安全账户管理）的简写。

    1. smbpasswd：该方式是使用smb自己的工具smbpasswd来给系统用户（真实用户或者虚拟用户）设置一个Samba密码，客户端就用这个密码来访问Samba的资源。smbpasswd文件默认在/etc/samba目录下，不过有时候要手工建立该文件。

    2. tdbsam： 该方式则是使用一个数据库文件来建立用户数据库。数据库文件叫passdb.tdb，默认在/etc/samba目录下。passdb.tdb用户数据库 可以使用smbpasswd –a来建立Samba用户，不过要建立的Samba用户必须先是系统用户。

    3. ldapsam：该方式则是基于LDAP的账户管理方式来验证用户。首先要建立LDAP服务，然后设置“passdb backend = ldapsam:ldap://LDAP Server”

- [chenjian]

    windows系统中文件夹地址栏中输入`\\ip\chenjian`，可以访问samba

- comment = Chen Jian Personal Directories

    对共享目录的说明文件，自己可以定义说明信息

- path = /home/chenjian/
  
    samba用来指定的共享目录

- guest ok = no
  
    并非所有人可查看

- browseable = yes

    browseable用来指定该共享是否可以浏览。

- writable = yes
  
    writable用来指定该共享路径是否可写。

- Samba安装好后，使用testparm命令可以测试smb.conf配置是否正确。使用testparm –v命令可以详细的列出smb.conf支持的配置参数。

操作：

``` shell
ln -s /etc/samba/smb.conf   /usr/local/samba/lib/smb.conf
```

##### 创建并授权共享文件夹

``` shell
mkdir -p /home/chenjian
chmod -R 777 /home/chenjian/
```

##### 加入sysv中

- samba.init

``` text
#!/bin/sh
# chkconfig: - 91 35
#
# Copyright (c) Timo Knuutila <knuutila@cs.utu.fi>     1996.
#
# This file should have uid root, gid sys and chmod 744
#
if [ ! -d /usr/bin ]
then                    # /usr not mounted
        exit
fi

killproc() {            # kill the named process(es)
        pid=`/usr/bin/ps -e |
             /usr/bin/grep -w $1 |
             /usr/bin/sed -e 's/^  *//' -e 's/ .*//'`
        [ "$pid" != "" ] && kill $pid
}

# Start/stop processes required for samba server

case "$1" in

'start')
#
# Edit these lines to suit your installation (paths, workgroup, host)
#
   /usr/sbin/smbd -D -l/var/log/samba -s/etc/samba/smb.conf
   /usr/sbin/nmbd -D -l/var/log/samba -s/etc/samba/smb.conf
   ;;
'stop')
   killproc nmbd
   killproc smbd
   ;;
*)
   echo "Usage: /etc/init.d/samba.server { start | stop }"
   ;;
esac

```

- 操作：
  
``` shell
cp -f samba.init /etc/init.d/samba
chmod 755 /etc/init.d/samba
chkconfig --add samba
chkconfig samba on
/etc/init.d/samba start
```

### systemd与sysV

上述采用sysV。对于使用systemd模式，尝试过，但不能以守护进程方式执行。

有几个问题：

1. ./configure有两个参数，`--systemd-install-services`与`--with-systemd`有什么作用；
2. 如何编写正确的`samba.service`

以下是一种方式：

``` text
[Unit]
Description=Samba SMB Daemon
After=syslog.target network.target nmb.service winbind.service
 
[Service]
Type=notify
NotifyAccess=all
PIDFile=/run/smbd.pid
LimitNOFILE=16384
EnvironmentFile=-/etc/sysconfig/samba
ExecStart=/usr/sbin/smbd --foreground --no-process-group $SMBDOPTIONS
ExecReload=/usr/bin/kill -HUP $MAINPID
LimitCORE=infinity
 
[Install]
WantedBy=multi-user.target
```

### 参考文献

1. [samba官网](https://www.samba.org/)
2. [linux应用之samba服务的安装及配置（centos）](https://www.cnblogs.com/tankblog/p/6080986.html)
3. [用源码编译安装Samba 4.8.2做域控](http://blog.51cto.com/423877/2119157)
4. [CentOS6源码编译搭建Samba](https://www.wanghualang.com/centos6-make-samba.html)
5. [Samba AD DC:Configure Server](https://www.server-world.info/en/note?os=CentOS_7&p=samba&f=4)
6. [源码编译安装samba](https://blog.csdn.net/cupidove/article/details/47756225)
7. [源码安装samba](https://blog.csdn.net/llmys/article/details/81941412)
8. [升级samba](https://blog.csdn.net/caspiansea/article/details/79619678#comments)
9. [服务器重启后samba启动不了](https://blog.csdn.net/dasunwarman/article/details/79745603)
10. [CentOS 7 巨大变动之 systemd 取代 SysV的Init](https://www.cnblogs.com/dsc65749924/p/5841731.html)


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2018/10/11/Source-Code-Compilation-And-Installation-Of-Samba-On-CentOS7/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。