---
layout:     post
title:      "在Centos7上使用Iptables"
subtitle:   "Using Iptables On Centos7"
date:       Tue, Feb 28 2017 15:04:33 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Using-Iptables-On-Centos7/head_blog.jpg"
catalog:    true
tags: [工作, Linux, Kubernetes]
---

### 前言

在部署Kubernetes中遇到了关闭Firewalld服务问题，于是涉及到iptables的设置。Centos7系统采用新的firewalld服务代替iptables，但并没有摒弃iptables。

### 准备工作

``` sh
# 关闭firewalld服务
sudo systemctl disable firewalld
sudo systemctl stop firewalld

# 查看firewall状态
sudo systemctl status firewalld

# 检查iptables是否安装
sudo systemctl status iptables

# 安装iptables
sudo yum install -y iptables

# 升级iptables
sudo yum update iptables

# 安装iptables-services
sudo yum install -y iptables-services
```

#### iptalbes操作命令

- 基本操作：

``` sh
## 查看iptables现有规则
iptables -L -v -n --line-number

# 清空所有默认规则
iptables -F

# 清空所有自定义规则
iptables -X

# 所有计数器归0
iptables -Z

# 删除INPUT中的第5个
iptables -D INPUT 5
```

- 添加8080端口：

``` sh
iptables -A INPUT -d 10.0.0.42 -p tcp --dport 8080 -m limit --limit 2/second --limit-burst 3 -m state --state NEW -j ACCEPT
```

> -A INPUT 在指定链INPUT的末尾添加（–append）一条新的规则
> 
> -d 10.0.0.42 指定目的地址10.0.0.42
> 
> -p tcp 指定规则协议，如tcp, udp,icmp等，可以使用all来指定所有协议
> 
> --dport 8080 目标端口8080
> 
> -m limit 显示扩展条件
> 
> --limit 2/second 速率（每秒2个数据包）
> 
> --limit-burst 3 峰值速率（最大不超过3个数据包）
> 
> -m state 显示扩展条件
> 
> --state NEW 用于链接状态的检测NEW, ESTABLISHED，RELATED，INVALID
> 
> -j ACCEPT 添加处理机制，ACCEPT接受，DROP丢弃

##### 用例

- 通过命令iptables改变防火墙设置

目标：只允许10.0.0.44可以ssh（端口22）链接192.168.1.179

``` sh
# 首先是允许10.0.0.44可以ssh链接
iptables -A INPUT -d 10.0.0.44 -p tcp --dport 22 -j ACCEPT
iptables -A OUTPUT -d 10.0.0.44 -p tcp --dport 22 -j ACCEPT

# 再丢否定其他所有的链接
iptables -A INPUT -p tcp --dport 22 -j DROP
iptables -A OUTPUT -p tcp --sport 22 -j DROP
```

查看iptables状态

``` sh
# iptables -L -v -n --line-number

<<'COMMENT'
Chain INPUT (policy ACCEPT 20151 packets, 3544K bytes)
num   pkts bytes target     prot opt in     out     source               destination         
1        0     0 ACCEPT     udp  --  virbr0 *       0.0.0.0/0            0.0.0.0/0            udp dpt:53
2        0     0 ACCEPT     tcp  --  virbr0 *       0.0.0.0/0            0.0.0.0/0            tcp dpt:53
3        0     0 ACCEPT     udp  --  virbr0 *       0.0.0.0/0            0.0.0.0/0            udp dpt:67
4        0     0 ACCEPT     tcp  --  virbr0 *       0.0.0.0/0            0.0.0.0/0            tcp dpt:67
5      233 22978 ACCEPT     tcp  --  *      *       10.0.0.44            0.0.0.0/0            tcp dpt:22
6        4   240 DROP       tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:22

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination         
1        0     0 DOCKER     all  --  *      docker0  0.0.0.0/0            0.0.0.0/0           
2        0     0 ACCEPT     all  --  *      docker0  0.0.0.0/0            0.0.0.0/0            ctstate RELATED,ESTABLISHED
3        0     0 ACCEPT     all  --  docker0 !docker0  0.0.0.0/0            0.0.0.0/0           
4        0     0 ACCEPT     all  --  docker0 docker0  0.0.0.0/0            0.0.0.0/0         
5        0     0 ACCEPT     all  --  virbr0 virbr0  0.0.0.0/0            0.0.0.0/0           
6        0     0 REJECT     all  --  *      virbr0  0.0.0.0/0            0.0.0.0/0            reject-with icmp-port-unreachable
7       0     0 REJECT     all  --  virbr0 *       0.0.0.0/0            0.0.0.0/0            reject-with icmp-port-unreachable

Chain OUTPUT (policy ACCEPT 327 packets, 40172 bytes)
num   pkts bytes target     prot opt in     out     source               destination         
1        0     0 ACCEPT     udp  --  *      virbr0  0.0.0.0/0            0.0.0.0/0            udp dpt:68
2        0     0 ACCEPT     tcp  --  *      *       10.0.0.44            0.0.0.0/0            tcp dpt:22
COMMENT
```

> 还有很多服务，例如ssh服务的22，邮件服务器的25,110端口， FTP服务器的21端口，DNS服务器的53端口，HTTP的80端口，HTTPS的443端口等等

##### 启动iptables服务

``` sh
# 保存上述规则
service iptables save

# 注册iptables服务
# 相当于以前的chkconfig iptables on
systemctl enable iptables.service

# 开启服务
systemctl start iptables.service

# 查看状态
systemctl status iptables.service
```

- 通过写iptables配置文件改变防火墙设置

``` sh
# 通过命令行改变iptables是临时的，永远改变iptables需要在/etc/sysconfig/iptables中写入配置
cat >> /etc/sysconfig/iptables <<EOF
sed -i'/COMMIT/i \-A INPUT -d 10.0.0.44 -p tcp --dport 22 -j ACCEPT' /etc/sysconfig/iptables
sed -i'/COMMIT/i \-A OUTPUT -d 10.0.0.44 -p tcp --dport 22 -j ACCEPT' /etc/sysconfig/iptables
sed -i'/COMMIT/i \-A INPUT -p tcp --dport 22 -j DROP' /etc/sysconfig/iptables
sed -i'/COMMIT/i \-A OUTPUT -p tcp --sport 22 -j DROP' /etc/sysconfig/iptables
EOF

# 重启服务
service iptables restart

# 保存上述规则。此命令单独运行会让配置文件复原，需要在restart之后运行
service iptables save

# 注册iptables服务
# 相当于以前的chkconfig iptables on
systemctl enable iptables.service

# 开启服务
systemctl start iptables.service

# 查看状态
systemctl status iptables.service
```

### 参考博文

1. [centos7搭建集群必知：centos7已经无iptables，只有firewall](http://www.aboutyun.com/thread-17535-1-1.html)
2. [看了那么多iptables的教程，这篇教程还是比较全面易懂的](https://www.91yun.org/archives/1690)
3. [iptables](http://79076431.blog.51cto.com/8977042/1811282)
4. [linux系统中查看己设置iptables规则](http://6226001001.blog.51cto.com/9243584/1826054)

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/02/28/Using-Iptables-On-Centos7/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。