---
layout:     post
title:      "定制个自己的CentOS7系统"
subtitle:   "DIY A CentOS7 System"
date:       Mon, Nov 20 2017 23:20:10 GMT+8
author:     "ChenJian"
header-img: "img/in-post/DIY-A-CentOS7-System/head_blog.jpg"
catalog:    true
tags: [工作, Linux]
---

### 官网下载ISO版本镜像

名称：[CentOS-7-x86_64-Minimal-1708.iso](http://mirrors.zju.edu.cn/centos/7/isos/x86_64CentOS-7-x86_64-Minimal-1708.iso)

文件路径：`/home/chenjian/Downloads/IOS/CentOS-7-x86_64-Minimal-1708.iso`

### 安装制作工具

``` sh
yum -y install anaconda createrepo mkisofs rsync syslinux
```

### 挂载光盘，同步文件

``` sh
mkdir /mnt/cdrom

mount -o loop /home/chenjian/Downloads/IOS/CentOS-7-x86_64-Minimal-1708.iso /mnt/cdrom/
<<'COMMENT'
mount: /dev/loop0 is write-protected, mounting read-only
COMMENT

# 同步/mnt/cdrom/下的文件到/ISO/路径下，除了Packages和repodata文件夹
/usr/bin/rsync -a --exclude=Packages/ --exclude=repodata/ /mnt/cdrom/ /ISO/

ls /ISO/
<<'COMMENT'
CentOS_BuildTag  EFI  EULA  GPL  images  isolinux  LiveOS  RPM-GPG-KEY-CentOS-7  RPM-GPG-KEY-CentOS-Testing-7  TRANS.TBL
COMMENT

# 在/ISO/文件夹下新建Packages和repodata文件夹
mkdir -p /ISO/{Packages,repodata}

ls /ISO/
<<'COMMENT'
CentOS_BuildTag  EFI  EULA  GPL  images  isolinux  LiveOS  Packages  repodata  RPM-GPG-KEY-CentOS-7  RPM-GPG-KEY-CentOS-Testing-7  TRANS.TBL
COMMENT

# ======================================================================
# 以下内容为，缩减rpm包数量，减少不必须的安装文件
# 问题：这类做法安装时提示--Error Checking Software Selection--导致安装失败
# 预估为安装包不完整，当把/mnt/cdrom/Packages下全部的rpm包放到/ISO/Packages中，安装完成
cat > copy_rpm.sh <<EOF
#!/bin/bash

cd /root
rpm -qa > package.txt
DVD='/mnt/cdrom/Packages'
NEW_DVD='/ISO/Packages'
while read LINE 
do
cp \${DVD}/\${LINE}*.rpm /\${NEW_DVD} || echo "\$LINE don't cp......."
done < package.txt 
rm -rf package.txt
EOF

chmod +x copy_rpm.sh

./copy_rpm.sh
# ======================================================================

# 全部rpm包
sudo cp /mnt/cdrom/Packages/* /ISO/Packages/

ll /ISO/Packages/ | wc -l
<<'COMMENT'
427
COMMENT
```

### 制作ks.cfg文件

``` sh
cd /ISO/isolinux

cat > ks.cfg <<EOF
#version=Chenjian CentOS
#platform=x86, AMD64, or Intel EM64T
# Install OS instead of upgrade
install
# Keyboard layouts
keyboard --vckeymap=us --xlayouts='us'
# Root password
rootpw --iscrypted $1$Jg7P7.9/$TT.baSvBhZy/wOkSs9CDT/
# System language
lang en_US.UTF-8
# Firewall configuration
firewall --disabled
# System authorization information
auth  --useshadow  --passalgo=sha512
# Use CDROM installation media
cdrom
# Use text mode install
text
# Run the Setup Agent on first boot
firstboot --enable
ignoredisk --only-use=sda
# SELinux configuration
selinux --disabled
# Do not configure the X Window System
skipx

# Network information
network  --bootproto=dhcp --device=ens160 --onboot=yes --ipv6=auto --activate
network  --device=ens160 --hostname=localhost.localdomain
# Reboot after installation
reboot
# System timezone
timezone Asia/Shanghai --isUtc
# System bootloader configuration
bootloader --location=mbr --driveorder=sda --append=""
# Clear the Master Boot Record
zerombr
# Partition clearing information
clearpart --all --initlabel
autopart --type=lvm

%packages
@^minimal
@core
@chenjianrpm

%end

%post

echo "                                                                 " >> /etc/motd
echo " ▄████▄   ██░ ██ ▓█████ ███▄    █  ▄▄▄██▀▀▀██▓▄▄▄      ███▄    █ " >> /etc/motd
echo "▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ██ ▀█   █    ▒██  ▓██▒████▄    ██ ▀█   █ " >> /etc/motd
echo "▒▓█    ▄ ▒██▀▀██░▒███  ▓██  ▀█ ██▒   ░██  ▒██▒██  ▀█▄ ▓██  ▀█ ██▒" >> /etc/motd
echo "▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄▓██▒  ▐▌██▒▓██▄██▓ ░██░██▄▄▄▄██▓██▒  ▐▌██▒" >> /etc/motd
echo "▒ ▓███▀ ░░▓█▒░██▓░▒████▒██░   ▓██░ ▓███▒  ░██░▓█   ▓██▒██░   ▓██░" >> /etc/motd
echo "░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░ ▒░   ▒ ▒  ▒▓▒▒░  ░▓  ▒▒   ▓▒█░ ▒░   ▒ ▒ " >> /etc/motd
echo "  ░  ▒    ▒ ░▒░ ░ ░ ░  ░ ░░   ░ ▒░ ▒ ░▒░   ▒ ░ ▒   ▒▒ ░ ░░   ░ ▒░" >> /etc/motd
echo "░         ░  ░░ ░   ░     ░   ░ ░  ░ ░ ░   ▒ ░ ░   ▒     ░   ░ ░ " >> /etc/motd
echo "░ ░       ░  ░  ░   ░  ░        ░  ░   ░   ░       ░  ░        ░ " >> /etc/motd
echo "░                                                                " >> /etc/motd
echo "                                                                 " >> /etc/motd
echo "                 blog: https://o-my-chenjian.com                 " >> /etc/motd
echo "                 gmail: chenjian158978@gmail.com                 " >> /etc/motd

%end

%post --nochroot

cp /run/install/repo/game_driver/* /mnt/sysimage/usr/bin
chmod 755 /mnt/sysimage/root/game-x86_64-7d5.1.run

%end
EOF

# 修改文件权限，主要是可执行权限
sudo chmod -R 755 /ISO/game_driver/
```

> 将外部文件拷贝到系统内，需在`/ISO`目录下创建`game_dirver`文件夹，将外部文件(例如二进制文件dota_driver)放进`game_driver`目录下。在安装系统期间，该文件的绝对路径为`/run/install/repo/game_driver/`，而系统的文件路径挂载在`/mnt/sysimage`，所以目的地址为`/mnt/sysimage/usr/bin`。

> 这里需要注意文件的权限问题。

### 修改isolinux.cfg

``` sh
cd /ISO/isolinux

chmod 644 isolinux.cfg

sudo vi isolinux.cfg
```

修改的部分内容如下：

``` sh
label linux
  menu label ^Install CentOS 7
  kernel vmlinuz
  append initrd=initrd.img inst.stage2=hd:LABEL=CentOS7 inst.ks=cdrom:/isolinux/ks.cfg quiet
```

- inst.ks为ks.cfg文件位置；

- inst.stage2为安装介质位置，hd:LABEL为介质标签，例如CentOS7。这个和后续生成ISO镜像文件的命令genisoimage的参数`-V`有关。

- modprobe.blacklist=nouveau; 禁用nouveau驱动安装，用于NVIDIA驱动的安装准备工作；

- net.ifnames=0 biosdevname=0； 用于禁用centos7的"一致性网络设备命名法".

> 启动路径改为ks=cdrom:/ks.cfg

``` sh
chmod 444 isolinux.cfg
```

### 制作comps.xml文件

``` sh
cp /mnt/cdrom/repodata/*-minimal-x86_64-comps.xml /ISO/comps.xml
```

- 添加定制rpm安装包

``` xml
  <group>
    <id>chenjianrpm</id>
    <name>chenjianrpm</name>
    <name xml:lang="af">chenjianrpm</name>
    <name xml:lang="am">chenjianrpm ቦታ</name>
    <name xml:lang="ar">chenjianrpm</name>
    <name xml:lang="as">chenjianrpm</name>
    <name xml:lang="bal">chenjianrpm</name>
    ...
    <name xml:lang="tr">chenjianrpm</name>
    <name xml:lang="uk">chenjianrpm</name>
    <name xml:lang="ur">chenjianrpm</name>
    <name xml:lang="vi">chenjianrpm</name>
    <name xml:lang="zh_CN">chenjianrpm</name>
    <name xml:lang="zh_TW">chenjianrpm</name>
    <description>installation chenjianrpm sofeware.</description>
    <description xml:lang="as">installation chenjianrpm sofeware</description>
    <description xml:lang="bn">installation chenjianrpm sofeware</description>
    <description xml:lang="bn_IN">installation chenjianrpm sofeware</description>
    <description xml:lang="cs">installation chenjianrpm sofeware</description>
    <description xml:lang="de">installation chenjianrpm sofeware</description>
    ...
    <description xml:lang="te">installation chenjianrpm sofeware</description>
    <description xml:lang="uk">Мinstallation chenjianrpm sofeware</description>
    <description xml:lang="zh_CN">installation chenjianrpm sofeware</description>
    <description xml:lang="zh_TW">installation chenjianrpm sofeware</description>
    <default>false</default>
    <uservisible>false</uservisible>
    <packagelist>
      <packagereq type="default">PyYAML</packagereq>
      <packagereq type="default">ansible</packagereq>
      <packagereq type="default">libtomcrypt</packagereq>
      <packagereq type="default">libtommath</packagereq>
      <packagereq type="default">libyaml</packagereq>
      <packagereq type="default">openssl</packagereq>
      <packagereq type="default">openssl-libs</packagereq>
      <packagereq type="default">python-babe</packagereq>
      <packagereq type="default">python-setuptools</packagereq>
      <packagereq type="default">python-six</packagereq>
      <packagereq type="default">python2-crypto</packagereq>
      <packagereq type="default">python2-cryptography</packagereq>
      <packagereq type="default">python2-pyasn1</packagereq>
      <packagereq type="default">sshpass</packagereq>
      <packagereq type="default">libselinux</packagereq>
      <packagereq type="default">libselinux-python</packagereq>
      <packagereq type="default">libselinux-utils</packagereq>
    </packagelist>
  </group>
```

> comps文件以`group`来区分包，以`environment`来区分环境，例如centos的mini版本为`minimal`，其核心包为`core`。类似于其格式，可定制自己的rpm包，建立自己的`group id`和`name`，包含自己的`language`及描述，最重要的是`packagelist`，类型`default`为默认的，`mandatory`为强制的

> 将定制的rpm安装包放到`/ISO/Packages/`中。这里需要注意rpm包的依赖性，可以通过以下命令来获得依赖，例如以下需要`perl`安装rpm，然后同样添加到`comps.xml`中

``` sh
rpm -qpR kernel-devel-3.10.0-514.el7.x86_64.rpm

<<'COMMENT'
/usr/bin/find
perl
/bin/sh
rpmlib(PartialHardlinkSets) <= 4.0.4-1
rpmlib(FileDigests) <= 4.6.0-1
rpmlib(PayloadFilesHavePrefix) <= 4.0-1
rpmlib(CompressedFileNames) <= 3.0.4-1
rpmlib(PayloadIsXz) <= 5.2-1
COMMENT
```

- 最后在minimal环境中添加定制的groupid

``` xml
  <environment>
    <id>minimal</id>
    <name>Minimal Install</name>
    <name xml:lang="as">নূন্যতম ইনস্টল</name>
    ...
    <description xml:lang="zh_CN">基本功能。</description>
    <description xml:lang="zh_TW">基本功能。</description>
    <display_order>5</display_order>
    <grouplist>
      <groupid>core</groupid>
      <groupid>core</groupid>
      <groupid>chenjianrpm</groupid>
    </grouplist>
  </environment>
```

> 由comps.xml生成repodata包。**注意当有新包加入，或者更新`comps.xml`文件，均需要重新生成repodata文件夹**

``` sh
cd /ISO

createrepo -g comps.xml .
<<'COMMENT'
Spawning worker 0 with 369 pkgs
Workers Finished
Saving Primary metadata
Saving file lists metadata
Saving other metadata
Generating sqlite DBs
Sqlite DBs complete
COMMENT

ls repodata/
<<'COMMENT'
2b873dfb5efcd23c4556c64f85f8752dea89a1b78ac2d81f5a3a2479a6364aed-primary.sqlite.bz2    ba731bbd51e5526bdf722d98e006d633bfd76ec48c283921f4dfd1eeb95c6478-filelists.xml.gz
36f3b0cba95abd61f2f871ed31db124a1b9c7838e29cf992a59a093935ecf626-other.xml.gz          d36769d1a5c1b5480e99904a03b6d487f84d34c8075b5eb6b290e90802e3ea2a-comps.xml
6d916600909af4ba73f09e2c5877a3fa8e2811d8bf8f43909e83c72c27af51f2-comps.xml.gz          e2987de1d65f29e23f8d4ac01f8544b1fe47596dd93928026f4ac4a766cfb018-primary.xml.gz
6e0e0fec735b69e035c67f68ab629182c703ad1840b37dceefaba9e5093a7747-filelists.sqlite.bz2
repomd.xml
ac0924ead0d2101950c99e0670d1b74c8fea364a6bddca6415d04eb6102d0b08-other.sqlite.bz2
COMMENT
```

### 制作ISO镜像

``` sh
cd /ISO

# 注意参数中的-V，和上面的isolinux.cfg文件有关
genisoimage -joliet-long -V CentOS7 -o CentOS-7-ChenjianOS.iso -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -R -J -v -cache-inodes -T -eltorito-alt-boot -e images/efiboot.img -no-emul-boot /ISO

I: -input-charset not specified, using utf-8 (detected in locale settings)
genisoimage 1.1.11 (Linux)
Scanning /ISO
Scanning /ISO/EFI
Scanning /ISO/EFI/BOOT
Scanning /ISO/EFI/BOOT/fonts
Excluded: /ISO/EFI/BOOT/fonts/TRANS.TBL
Excluded: /ISO/EFI/BOOT/TRANS.TBL
Excluded: /ISO/EFI/TRANS.TBL
Scanning /ISO/LiveOS
Excluded: /ISO/LiveOS/TRANS.TBL
Scanning /ISO/images
Scanning /ISO/images/pxeboot
Excluded: /ISO/images/pxeboot/TRANS.TBL
Excluded: /ISO/images/TRANS.TBL
Scanning /ISO/isolinux
Excluded: /ISO/isolinux/TRANS.TBL
Excluded by match: /ISO/isolinux/boot.cat
Excluded: /ISO/TRANS.TBL
Scanning /ISO/Packages
Scanning /ISO/repodata
Using RPM_G000.;1 for  /RPM-GPG-KEY-CentOS-Testing-7 (RPM-GPG-KEY-CentOS-7)
Using PYTHO000.RPM;1 for  /ISO/Packages/python2-crypto-2.6.1-15.el7.x86_64.rpm (python2-cryptography-1.7.2-1.el7.x86_64.rpm)
...
Using HUNSP002.RPM;1 for  /ISO/Packages/hunspell-en-0.20121024-6.el7.noarch.rpm (hunspell-en-US-0.20121024-6.el7.noarch.rpm)
Using LIBER000.RPM;1 for  /ISO/Packages/liberation-fonts-common-1.07.2-15.el7.noarch.rpm (liberation-sans-fonts-1.07.2-15.el7.noarch.rpm)
Writing:   Initial Padblock                        Start Block 0
Done with: Initial Padblock                        Block(s)    16
Writing:   Primary Volume Descriptor               Start Block 16
Done with: Primary Volume Descriptor               Block(s)    1
Writing:   Eltorito Volume Descriptor              Start Block 17
Size of boot image is 4 sectors -> No emulation
Done with: Eltorito Volume Descriptor              Block(s)    1
Writing:   Joliet Volume Descriptor                Start Block 18
Done with: Joliet Volume Descriptor                Block(s)    1
Writing:   End Volume Descriptor                   Start Block 19
Done with: End Volume Descriptor                   Block(s)    1
Writing:   Version block                           Start Block 20
Done with: Version block                           Block(s)    1
Writing:   Path table                              Start Block 21
Done with: Path table                              Block(s)    4
Writing:   Joliet path table                       Start Block 25
Done with: Joliet path table                       Block(s)    4
Writing:   Directory tree                          Start Block 29
Done with: Directory tree                          Block(s)    42
Writing:   Joliet directory tree                   Start Block 71
Done with: Joliet directory tree                   Block(s)    29
Writing:   Directory tree cleanup                  Start Block 100
Done with: Directory tree cleanup                  Block(s)    0
Writing:   Extension record                        Start Block 100
Done with: Extension record                        Block(s)    1
Writing:   The File(s)                             Start Block 101
  1.43% done, estimate finish Tue Nov 14 17:08:17 2017
  2.87% done, estimate finish Tue Nov 14 17:08:17 2017
  4.30% done, estimate finish Tue Nov 14 17:08:17 2017
 ...
 95.89% done, estimate finish Tue Nov 14 17:08:18 2017
 97.33% done, estimate finish Tue Nov 14 17:08:18 2017
 98.76% done, estimate finish Tue Nov 14 17:08:18 2017
Total translation table size: 106045
Total rockridge attributes bytes: 46850
Total directory bytes: 79872
Path table size(bytes): 140
Done with: The File(s)                             Block(s)    376656
Writing:   Ending Padblock                         Start Block 376757
Done with: Ending Padblock                         Block(s)    150
Max brk space used 85000
349350 extents written (736 MB)

```

### Hybird模式

采用“hybird模式”（混合模式），操作系统可以直接刻录成物理光盘，也可以直接做成可引导的U盘。

``` shell
isohybird -v /ISO/CentOS-7-ChenjianOS.iso
```

### 制作镜像MD5值

``` sh
implantisomd5 /ISO/CentOS-7-ChenjianOS.iso

<<'COMMENT'
Inserting md5sum into iso image...
md5 = ed6233dc8bf6e59353a646e286b7a51f
Inserting fragment md5sums into iso image...
fragmd5 = 4c9fb671374f6b26bdaf49d5452ec7862f97e3899f9eac23a7e8f4f84d25
frags = 20
Setting supported flag to 0
COMMENT
```

### 安装系统

> iso安装系统不再叙述；

> 由于是`text`模式，则进入安装界面，会有一个类似图形安装界面的排版，里面可以选择。所有选择均为`x`的时候，表示正常无误;有`!`的话，则为错误。错误时需要查看日志，其中`Alt+F1`快捷键可以进入`main`界面，`Alt+F2`快捷键可以进入`Shell`界面等等。在`Shell`界面中，可以从`/tmp/packaging.log`中找到rpm包日志，可以从`/tmp/anaconda.log`中找到安装过程中的报错日志;可以从`/run/install/repo`路径下找到外部文件夹；

> 当选项均为`x`时，即表示正常无误，可以不进行操作，其自动进入下一步安装过程，直至安装成功，然后自动重启，显示登录界面。

### 参考博文

1. [制作CentOS 6.5一键自安装ISO镜像光盘](http://yangfannie.com/771.html)
2. [制作CentOS 7一键自安装ISO镜像光盘](http://blog.csdn.net/u013870094/article/details/53179531)
3. [Kickstart Installations](https://www.centos.org/docs/5/html/Installation_Guide-en-US/ch-kickstart2.html)
4. [Text to ASCII Art Generator](http://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20)
5. [CentOS7全自动安装光盘制作详解](http://xiaoli110.blog.51cto.com/1724/1617541/)
6. [Building a custom CentOS 7 kickstart disc](http://blog.chinaunix.net/xmlrpc.php?r=blog/article&uid=26000137&id=4710595)
7. [cobbler中ks.cfg文件配置详解](http://www.codexiu.cn/linux/blog/1939/#OSC_h6_47)
8. [linux权限详解](http://blog.csdn.net/fan_zhen_hua/article/details/2050009)
9. [KICKSTART 语法参考](https://access.redhat.com/documentation/zh-cn/red_hat_enterprise_linux/7/html/installation_guide/sect-kickstart-syntax)

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/11/20/DIY-A-CentOS7-System/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。

