---
layout:     post
title:      "CentOS7修改网卡名称"
subtitle:   "Change Network Card Name On CentOS7"
date:       Fri, Nov 2 2018 20:17:12 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Change-Network-Card-Name-On-CentOS7/head_blog.jpg"
catalog:    true
tags: [工作, Linux]
---

### 系统信息

| 操作系统 | 版本 | 备注 |
| :-----: | :--: | :--: |
| CentOS | 7.5.1804 | |

### 查看IP信息

``` shell
ip a

<<"COMMENT"
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: ens2p3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 0c:c4:7c:7g:af:50 brd ff:ff:ff:ff:ff:ff
    inet 10.13.14.203/24 brd 10.13.14.255 scope global noprefixroute ens2p3
       valid_lft forever preferred_lft forever
    inet6 fe80::ec4:7aff:fe7e:ef20/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
3: ens2p2: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN group default qlen 1000
    link/ether 0c:c4:7c:7g:af:51 brd ff:ff:ff:ff:ff:ff
COMMENT
```

### 修改网卡配置文件

``` shell
cd /etc/sysconfig/network-scripts/

# 复制文件
cp ifcfg-ens2p3 ifcfg-eth0
cp ifcfg-ens2p2 ifcfg-eth1

# 修改网口名 eth0
sed -i "s/ens2p3/eth0/g" ifcfg-eth0
sed -i "/ONBOOT/d" ifcfg-eth0
sed -i "/BOOTPROTO/d" ifcfg-eth0

# 修改网口名 eth1
sed -i "s/ens2p2/eth1/g" ifcfg-eth1

# 添加具体内容
cat >> ifcfg-eth0 << EOF
ONBOOT="yes"
BOOTPROTO="static"
IPADDR=10.13.14.202
NETMASK=255.255.255.0
GATEWAY=10.13.14.254
DNS1=1.1.1.1
DNS2=8.8.8.8
EOF

# 删除原有文件
rm -f ifcfg-ens2p3 ifcfg-ens2p2
```

### 关闭“一致性设备命名法”

``` shell
# 更新grub文件
sed -i "s/rhgb/biosdevname=0 net.ifnames=0 rhgb/g" /etc/sysconfig/grub

# 更新GRUB、内核配置
grub2-mkconfig -o /boot/grub2/grub.cfg

# 添加设备规则配置文件
echo "SUBSYSTEM==\"net\", ACTION==\"add\", DRIVERS==\"?*\", ATTR{address}==\"0c:c4:7c:7g:af:50\", ATTR{type}==\"1\", KERNEL==\"eth*\", NAME=\"eth0\"" >> /etc/udev/rules.d/70-persistent-net.rules
echo "SUBSYSTEM==\"net\", ACTION==\"add\", DRIVERS==\"?*\", ATTR{address}==\"0c:c4:7c:7g:af:51\", ATTR{type}==\"1\", KERNEL==\"eth*\", NAME=\"eth1\"" >> /etc/udev/rules.d/70-persistent-net.rules
```

- 注意：MAC地址与网卡名称一定要对应上，可以通过`ip a`查看

### 重启设备

``` shell
reboot

# 重启后
ip a

<<"COMMENT"
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 0c:c4:7c:7g:af:50 brd ff:ff:ff:ff:ff:ff
    inet 10.13.14.202/24 brd 10.13.14.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::ec4:7aff:fe7e:ef20/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
3: eth1: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN group default qlen 1000
    link/ether 0c:c4:7c:7g:af:51 brd ff:ff:ff:ff:ff:ff
COMMENT
```

### 网卡的一些常用命令

``` shell
# 查看network服务
systemctl status network.service

# 重启network服务
systemctl restart network.service

# 关闭NetworkManager服务
systemctl stop NetworkManager.service
# 关闭NetworkManager服务自动重启
systemctl disable NetworkManager.service

# 关闭网卡eth0
ifdown eth0

# 开启网卡eth0
ifup eth0

# 检查网卡eth0状态，可以查看到网线处于连接状态
ethtool eth0
<<'COMMENT'
Settings for eth0:
	Supported ports: [ TP ]
	Supported link modes:   1baseT/Half 1baseT/Full 
	                        10baseT/Half 10baseT/Full 
	                        100baseT/Full 
	Supported pause frame use: Symmetric
	Supports auto-negotiation: Yes
	Supported FEC modes: Not reported
	Advertised link modes:  1baseT/Half 1baseT/Full 
	                        10baseT/Half 10baseT/Full 
	                        100baseT/Full 
	Advertised pause frame use: Symmetric
	Advertised auto-negotiation: Yes
	Advertised FEC modes: Not reported
	Speed: 1000Mb/s
	Duplex: Full
	Port: Twisted Pair
	PHYAD: 1
	Transceiver: internal
	Auto-negotiation: on
	MDI-X: on (auto)
	Supports Wake-on: pumbg
	Wake-on: g
	Current message level: 0x00000007 (7)
			       drv probe link
	Link detected: yes
COMMENT
```

- 很多人喜欢执行重启network服务，来设置IP。但不建议这样，因为该命令是对所有网卡操作。建议使用"ifup"与"ifdown"命令操作单独的网卡；

### BMC的常用命令

``` shell
# 安装ipmitool工具
yum install -y ipmitool

# 查看BMC的IP类型与IP值
ipmitool lan print 1|grep "IP Address"

<<'COMMENT'
IP Address Source       : Static Address
IP Address              : 10.13.14.20
COMMENT

# 设置ipsrc的类型(dhcp/static)，set 1表示网络连接的类型，为channel1
ipmitool lan set 1 ipsrc static

# 设置静态IP
ipmitool lan set 1 ipaddr 172.20.1.1

# 查看枫树转速
ipmitool sdr list | grep -i '^FAN'

<<'COMMENT'
FAN1_Speed       | 2000 RPM          | ok
FAN2_Speed       | 2000 RPM          | ok
FAN3_Speed       | 2000 RPM          | ok
FAN1_Present     | 0x00              | ok
FAN2_Present     | 0x00              | ok
FAN3_Present     | 0x00              | ok
COMMENT

```

### 参考文献

1. [centos7修改网卡名](https://blog.csdn.net/henulwj/article/details/47061023)
2. [CentOS 7.2更改网卡名称](http://www.cnblogs.com/nidey/p/6275485.html)
3. [关闭NetworkManager的作用](https://www.cnblogs.com/kaishirenshi/p/7872771.html)
4. [ipmi的使用_命令与ip设置](https://blog.csdn.net/clark_xu/article/details/11356659)

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2018/11/02/Change-Network-Card-Name-On-CentOS7/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。