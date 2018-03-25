---
layout:     post
title:      "更新CentOS7上的内核版本"
subtitle:   "Update The Version Of Kernel On CentOS7"
date:       Sun, Mar 25 2018 08:22:35 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Update-The-Version-Of-Kernel-On-CentOS7/head_blog.jpg"
catalog:    true
tags:
    - 工作
    - Linux
---

### 查看当前Kernel版本

``` shell
uname -r

<<'COMMENT'
3.10.0-123.el7.x86_64
COMMENT

```

### 查看当前系统启动引导项

- 可以看出有两个引导项

- - 第一个是 3.10.0-123.el7.x86_64
- - 第二个是 0-rescue-f892a2a55b8041868ce40ff2a39cc252

```
cat /boot/grub2/grub.cfg |grep menuentry

<<'COMMENT'
if [ x"${feature_menuentry_id}" = xy ]; then
  menuentry_id_option="--id"
  menuentry_id_option=""
export menuentry_id_option
menuentry 'CentOS Linux (3.10.0-123.el7.x86_64) 7 (Core)' --class centos --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-123.el7.x86_64-advanced-ef2e2ae4-386d-4353-ad99-b42e21fee3f1' {
menuentry 'CentOS Linux (0-rescue-f892a2a55b8041868ce40ff2a39cc252) 7 (Core)' --class centos --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-0-rescue-f892a2a55b8041868ce40ff2a39cc252-advanced-ef2e2ae4-386d-4353-ad99-b42e21fee3f1' {
COMMENT
```

### 查看当前Kernel包

``` 
rpm -qa |grep kernel

<<'COMMENT'
kernel-3.10.0-123.el7.x86_64
kernel-devel-3.10.0-123.el7.x86_64
kernel-devel-3.10.0-693.el7.x86_64
kernel-devel-3.10.0-693.21.1.el7.x86_64
abrt-addon-kerneloops-2.1.11-48.el7.centos.x86_64
kernel-tools-libs-3.10.0-693.21.1.el7.x86_64
kernel-headers-3.10.0-693.21.1.el7.x86_64
COMMENT
```

### Kernel版本升级

> 通过elrepo源，可以下载到最新的稳定版kernel版本。

```
# 方法一
yum update -y

# 方法二
# ELRepo项目(yum源）侧重于硬件相关的包来增强你的经验与企业Linux, 包括文件系统驱动,显卡驱动,网络驱动程序,声音驱动,摄像头和视频驱动程序。
# 适用于RHEL-7, SL-7 or CentOS-7
rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org

rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm

<<'COMMENT'
Retrieving http://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm
Preparing...                          ################################# [100%]
Updating / installing...
   1:elrepo-release-7.0-3.el7.elrepo  ################################# [100%]
COMMENT

yum --disablerepo="*" --enablerepo="elrepo-kernel" list available

<<'COMMENT'
Loaded plugins: fastestmirror
elrepo-kernel                                                                                                                        | 2.9 kB  00:00:00     
elrepo-kernel/primary_db                                                                                                             | 1.7 MB  00:00:24     
Loading mirror speeds from cached hostfile
 * elrepo-kernel: mirrors.tuna.tsinghua.edu.cn
Available Packages
kernel-lt.x86_64                                                              4.4.123-1.el7.elrepo                                             elrepo-kernel
kernel-lt-devel.x86_64                                                        4.4.123-1.el7.elrepo                                             elrepo-kernel
kernel-lt-doc.noarch                                                          4.4.123-1.el7.elrepo                                             elrepo-kernel
kernel-lt-headers.x86_64                                                      4.4.123-1.el7.elrepo                                             elrepo-kernel
kernel-lt-tools.x86_64                                                        4.4.123-1.el7.elrepo                                             elrepo-kernel
kernel-lt-tools-libs.x86_64                                                   4.4.123-1.el7.elrepo                                             elrepo-kernel
kernel-lt-tools-libs-devel.x86_64                                             4.4.123-1.el7.elrepo                                             elrepo-kernel
kernel-ml.x86_64                                                              4.15.12-1.el7.elrepo                                             elrepo-kernel
kernel-ml-devel.x86_64                                                        4.15.12-1.el7.elrepo                                             elrepo-kernel
kernel-ml-doc.noarch                                                          4.15.12-1.el7.elrepo                                             elrepo-kernel
kernel-ml-headers.x86_64                                                      4.15.12-1.el7.elrepo                                             elrepo-kernel
kernel-ml-tools.x86_64                                                        4.15.12-1.el7.elrepo                                             elrepo-kernel
kernel-ml-tools-libs.x86_64                                                   4.15.12-1.el7.elrepo                                             elrepo-kernel
kernel-ml-tools-libs-devel.x86_64                                             4.15.12-1.el7.elrepo                                             elrepo-kernel
perf.x86_64                                                                   4.15.12-1.el7.elrepo                                             elrepo-kernel
python-perf.x86_64                                                            4.15.12-1.el7.elrepo                                             elrepo-kernel
COMMENT

# 目前这个下载的是版本为4.15.12-1.el7.elrepo
yum --enablerepo=elrepo-kernel install kernel-ml
```

### 修改启动项顺序

```
# 将第一个内核作为默认内核
sed -i 's/GRUB_DEFAULT=saved/GRUB_DEFAULT=0/g' /etc/default/grub

# 重新配置内核项
grub2-mkconfig -o /boot/grub2/grub.cfg

<<'COMMENT'
Generating grub configuration file ...
Found linux image: /boot/vmlinuz-3.10.0-693.21.1.el7.x86_64
Found initrd image: /boot/initramfs-3.10.0-693.21.1.el7.x86_64.img
Found linux image: /boot/vmlinuz-3.10.0-123.el7.x86_64
Found initrd image: /boot/initramfs-3.10.0-123.el7.x86_64.img
Found linux image: /boot/vmlinuz-0-rescue-f892a2a55b8041868ce40ff2a39cc252
Found initrd image: /boot/initramfs-0-rescue-f892a2a55b8041868ce40ff2a39cc252.img
done
COMMENT

# 修改开机时默认使用的内核
grub2-set-default 'CentOS Linux (3.10.0-693.21.1.el7.x86_64) 7 (Core)'

# 查看内核修改结果
grub2-editenv list
<<'COMMENT'
saved_entry=CentOS Linux (3.10.0-693.21.1.el7.x86_64) 7 (Core)
COMMENT
```

### 查看升级后的系统启动引导项

- 可以看出有两个：

- - 第一个是 3.10.0-693.21.1.el7.x86_64
- - 第二个是 3.10.0-123.el7.x86_64
- - 第三个是 0-rescue-f892a2a55b8041868ce40ff2a39cc252

```
cat /boot/grub2/grub.cfg |grep menuentry

<<'COMMENT'
if [ x"${feature_menuentry_id}" = xy ]; then
  menuentry_id_option="--id"
  menuentry_id_option=""
export menuentry_id_option
menuentry 'CentOS Linux (3.10.0-693.21.1.el7.x86_64) 7 (Core)' --class centos --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-693.21.1.el7.x86_64-advanced-ef2e2ae4-386d-4353-ad99-b42e21fee3f1' {
menuentry 'CentOS Linux (3.10.0-123.el7.x86_64) 7 (Core)' --class centos --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-123.el7.x86_64-advanced-ef2e2ae4-386d-4353-ad99-b42e21fee3f1' {
menuentry 'CentOS Linux (0-rescue-f892a2a55b8041868ce40ff2a39cc252) 7 (Core)' --class centos --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-0-rescue-f892a2a55b8041868ce40ff2a39cc252-advanced-ef2e2ae4-386d-4353-ad99-b42e21fee3f1' {
COMMENT

```

### 重启系统

- 选择需要的内核版本为3.10.0-693.21.1.el7.x86_64的启动引导项

```
reboot
```

### 查看升级后的Kernel版本

```
# 查看当前内核版本
uname -r

<<'COMMENT'
3.10.0-693.21.1.el7.x86_64
COMMENT

```

### 删除原有内核版本

```
yum remove kernel-3.10.0-123.el7.x86_64 kernel-3.10.0-693.21.1.el7.x86_64 -y
```

### 参考文献

1. [CentOS 7 中安装或升级最新的内核](http://www.jb51.net/article/108926.htm)
2. [centos7选定默认启动内核及删除无用内核](https://www.cnblogs.com/niyeshiyoumo/p/6762193.html)
3. [CentOS6和CentOS7一键更换内核](https://www.zhangfangzhou.cn/lotserver.html)
4. [不得不装的CentOS的三大yum源](http://www.mamicode.com/info-detail-1166434.html)

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2018/03/25/Update-The-Version-Of-Kernel-On-CentOS7/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。

