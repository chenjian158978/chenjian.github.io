---
layout:     post
title:      "Deploy RabbitMQ Cluster On Ubuntu14.04"
subtitle:   "Hold up my goings in thy paths,
that my footsteps slip not. Psa 17:5"
date:       Fri, Oct 28 18:03:59 2016 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-RabbitMQ-Cluster-On-Ubuntu14.04/head_blog.png"
tags:
    - 工作
---

### 介绍

MQ全称为Message Queue, 消息队列（MQ）是一种应用程序对应用程序的通信方法。本版本为3.6.1

### Erlang安装

rabbitMQ需要erlang语言的支持，因此需要先安装erlang语言

命令：`sudo apt-get install erlang`

测试：启动`erl`，能否进入

``` sh
root@administrator159:/home/administrator# erl

Erlang R16B03 (erts-5.10.4) [source] [64-bit] [smp:8:8] [async-threads:10] [kernel-poll:false]

Eshell V5.10.4  (abort with ^G)
1> 
```

可以看出来erlang的版本为5.10.4

### RabbitMQ安装

* 鼠标操作模式：
在[rabbitMQ官网](http://www.rabbitmq.com/)中下载相应的ubuntu安装包deb,下载后双击即可安装完毕

* 命令操作模式:

1. 下载：`wget --no-check-certificate http://www.rabbitmq.com/releases/rabbitmq-server/v3.6.2/rabbitmq-server_3.6.2-1_all.deb`

2. 安装： `sudo dpkg -i rabbitmq-server_3.6.2-1_all.deb`

3. 如果遇到问题，修复依赖关系：`sudo apt-get install -f -y`,然后再尝试


### RabbitMQ设置

- 添加用户：`sudo rabbitmqctl add_user chenjian chenjian`

- 添加虚拟队列： `sudo rabbitmqctl add_vhost chenjian`

- 添加后台管理插件：`sudo rabbitmq-plugins enable rabbitmq_management`
显示：

``` sh
administrator@administrator159:~$ sudo rabbitmq-plugins enable rabbitmq_management

The following plugins have been enabled:
  mochiweb
  webmachine
  rabbitmq_web_dispatch
  amqp_client
  rabbitmq_management_agent
  rabbitmq_management

Applying plugin configuration to rabbit@administrator159... started 6 plugins.
```

- 添加用户权限： `rabbitmqctl set_permissions -p chenjian chenjian ".*" ".*" ".*"` 或者 `sudo rabbitmqctl set_permissions -p chenjian chenjian ConfP  WriteP  ReadP`

结果：
``` sh
Setting permissions for user "chenjian" in vhost "chenjian" ...
```

- 修改用户角色：`sudo rabbitmqctl set_user_tags chenjian administrator`
结果：

``` sh
Setting tags for user "chenjian" to [administrator] ...
```

- 设置高可用策略

为了使用HAProxy做负载均衡，必须将整个RabbitMQ集群的状态设置为镜像模式，具体方式是通过以下命令，注意策略的设置也是在3.x版本中添加的功能，2.x版本是没有的。

命令： `sudo rabbitmqctl set_policy -p chenjian ha-allqueue "^" '{"ha-mode":"all"}'`

``` sh
administrator@administrator158:~$ sudo rabbitmqctl set_policy -p chenjian ha-allqueue "^" '{"ha-mode":"all"}'

Setting policy "ha-allqueue" for pattern "^" to "{\"ha-mode\":\"all\"}" with priority "0" ...
```

在浏览器中输入`192.168.1.159:15672`便可进入rabbitmq界面。


### RabbitMQ集群
####集群IP与名称
1. 192.168.1.157 作为集群的**内存节点**
2. 192.168.1.158 作为集群的**磁盘节点**
3. 192.168.1.159 作为集群的**内存节点**
4. 192.168.1.78 作为**反向代理(Haproxy)**
> 集群中有两种节点：
* 内存节点：只保存状态到内存（一个例外的情况是：持久的queue的持久内容将被保存到disk）
*  磁盘节点：保存状态到内存和磁盘。
内存节点虽然不写入磁盘，但是它执行比磁盘节点要好。集群中，只需要一个磁盘节点来保存状态 就足够了
如果集群中只有内存节点，那么不能停止它们，否则所有的状态，消息等都会丢失。

#### 对hostname和hosts的操作 
 
对157,158,159进行操作，以192.168.1.158为例子：

-  记住IP：`cat /etc/hostname` 

``` sh
root@administrator158:/home/administrator# cat /etc/hostname

administrator158
```

- 命令：`vim /etc/hosts`

修改为：

``` sh
root@administrator158:/home/administrator# cat /etc/hosts

127.0.0.1       localhost
127.0.1.1       administrator158
192.168.1.157   administrator157
192.168.1.158   administrator158
192.168.1.159   administrator159


# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

> **修改完后，重启电脑。**
**请注意RabbitMQ集群节点必须在同一个网段里，如果是跨广域网效果就差。**

#### 设置节点的Cookie 

以192.168.1.158为例：

-  查看erlang的cookie：`cat /var/lib/rabbitmq/.erlang.cookie`

内容：

```bash
root@administrator157:/home/administrator# cat /var/lib/rabbitmq/.erlang.cookie

AZPRQAAHZQUNBRRDXNLX
```

- 将这个Cookie放到157,159上，例如在157上进行操作：

- 查看修改`.erlang.cookie`权限

``` sh
root@administrator157:/home/administrator# ll /var/lib/rabbitmq/.erlang.cookie
	
-r-------- 1 rabbitmq rabbitmq 20 10月 28 00:00 /var/lib/rabbitmq/.erlang.cookie
root@administrator157:/home/administrator# chmod 777 /var/lib/rabbitmq/.erlang.cookie
root@administrator157:/home/administrator# ll /var/lib/rabbitmq/.erlang.cookie
-rwxrwxrwx 1 rabbitmq rabbitmq 20 10月 28 00:00 /var/lib/rabbitmq/.erlang.cookie*
```
	
- 修改Cookie
		
``` sh
root@administrator157:/home/administrator# vim /var/lib/rabbitmq/.erlang.cookie
root@administrator157:/home/administrator# cat /var/lib/rabbitmq/.erlang.cookie

AZPRQAAHZQUNBRRDXNLX
```

> **或者，可以通过sftp进行文件传输，一定要确保Cookie相同，例如读写（400），用户（rabbitmq），用户组权限（rabbitmq）。**

- 再次修改`.erlang.cookie`权限

``` sh
root@administrator157:/home/administrator# chmod 400 /var/lib/rabbitmq/.erlang.cookie
root@administrator157:/home/administrator# ll /var/lib/rabbitmq/.erlang.cookie

-r-------- 1 rabbitmq rabbitmq 21 10月 28 15:20 /var/lib/rabbitmq/.erlang.cookie
```

- RabbitMQ重启

- `rabbitmqctl stop`

``` sh
 root@administrator159:/home/administrator# rabbitmqctl stop

Stopping and halting node rabbit@administrator159 ...
```

-  `service rabbitmq-server start`

``` sh
root@administrator159:/home/administrator# sudo service rabbitmq-server start
 
 * Starting message broker rabbitmq-server
 * message broker already running
   ...done.
```

#### 链接nodes

在192.168.1.159上操作：

- `rabbitmqctl stop_app`

``` sh
root@administrator159:/home/administrator# rabbitmqctl stop_app

Stopping node rabbit@administrator159 ...
```

- `rabbitmqctl reset`

``` sh
root@administrator159:/home/administrator# rabbitmqctl reset

Resetting node rabbit@administrator159 ...
```

- `rabbitmqctl join_cluster --ram rabbit@administrator158`

``` sh
root@administrator159:/home/administrator# rabbitmqctl join_cluster --ram rabbit@administrator158

Clustering node rabbit@administrator159 with rabbit@administrator158 ...
```

> *如果要使administrator159在集群里也是磁盘节点，join_cluster 命令去掉--ram参数即可。只要在节点列表里包含了自己，它就成为一个磁盘节点。在RabbitMQ集群里，必须至少有一个磁盘节点存在。*

- `rabbitmqctl start_app`

``` sh
root@administrator159:/home/administrator# rabbitmqctl start_app

Starting node rabbit@administrator159 ...
```

- 查看集群状态：`rabbitmqctl cluster_status`

``` sh
root@administrator159:/home/administrator# rabbitmqctl cluster_status

Cluster status of node rabbit@administrator159 ...
[{nodes,[{disc,[rabbit@administrator158]},
         {ram,[rabbit@administrator159,rabbit@administrator157]}]},
 {running_nodes,[rabbit@administrator158,rabbit@administrator157,
                 rabbit@administrator159]},
 {cluster_name,<<"rabbit@administrator158">>},
 {partitions,[]},
 {alarms,[{rabbit@administrator158,[]},
          {rabbit@administrator157,[]},
          {rabbit@administrator159,[]}]}]
```

可以看到disc为administrator158，而ram为157和159

- 队列消息一致：`rabbitmqctl list_queues -p chenjian`

``` sh
root@administrator159:/home/administrator# rabbitmqctl list_queues -p hrsystem

Listing queues ...
```

> *-p参数为vhost名称*

- 重启RabbitMQ：`sudo service rabbitmq-server reload`

*同样在192.168.1.157上做相同的事情，而192.168.1.158就不用做了。重启158以后，发现user被消除掉了，这时候重复RabbitMQ设置中的添加用户，及配置用户权限与角色的操作*

- 登录浏览器`192.168.1.158：15672`或其他两个均可

### HaProxy反向代理

#### haproxy安装 

IP: `192.168.1.78`

操作系统：`ubuntu14.04` 

命令： `sudo apt-get install haproxy`

作用：**负载均衡器**会监听5672端口，轮询我们的两个内存节点192.168.1.157、192.168.1.159的5672端口，192.168.1.158为磁盘节点，只做备份不提供给生产者、消费者使用，当然如果我们服务器资源充足情况也可以配置多个磁盘节点
，这样磁盘节点除了故障也不会影响，除非同时出故障

#### 修改haproxy配置内容

命令： `sudo vim /etc/haproxy/haproxy.cfg`

- 修改默认`option httplog`为`option tcplog`

``` sh
defaults
        log     global
        mode    tcp
        option  tcplog
        option  dontlognull
```

- 添加haproxy的web端：

添加：

``` sh
listen admin_stat
bind 0.0.0.0:8888
mode http
# 刷新时间段
stats refresh 10s
# 192.168.1.78:8888/rabbitmq_stats
stats uri /rabbitmq_stats
stats realm Haproxy\ Statistics
# 登录的账户密码
stats auth admin:admin
# 是否隐藏haproxy的版本
# stats hide-version
```

- 配置末尾添加：

``` sh
listen rabbitmq_cluster *:5672
     mode tcp
     balance roundrobin
     server rqslave1 192.168.1.157:5672 check inter 2000 rise 2 fall 3
     server rqslave2 192.168.1.159:5672 check inter 2000 rise 2 fall 3
     server rqmaster 192.168.1.158:5672 check inter 2000 rise 2 fall 3
```

#### 启动haproxy服务

- `haproxy -f /etc/haproxy/haproxy.cfg -D`

- `service haproxy start`

查看haproxy的监听：

`netstat -nl| grep 5672`
```bash
root@administrator78:/etc/haproxy# netstat -nl| grep 5672

tcp        0      0 0.0.0.0:5672            0.0.0.0:*               LISTEN
```

或者可以登录`http：//192.168.1.78:8888/rabbitmq_stats`

### python程序中填写

```python
CELERY_BROKER_USER = "chenjian"
CELERY_BROKER_PASSWORD = "chenjian"
CELERY_BROKER_HOST = "192.168.1.78"
CELERY_BROKER_PORT = 5672
CELERY_BROKER_VHOST = "chenjian"

BROKER_URL = "amqp://%s:%s@%s:%s/%s" % (CELERY_BROKER_USER,
                                        CELERY_BROKER_PASSWORD, CELERY_BROKER_HOST,
                                        CELERY_BROKER_PORT, CELERY_BROKER_VHOST)
```

### 博文：

1. [rabbitmq的web管理界面无法使用guest用户登录](http://www.cnblogs.com/mingaixin/p/4134920.html)

2. [Rabbitmq集群高可用测试
](http://www.cnblogs.com/flat_peach/archive/2013/04/07/3004008.html)

3. [Rabbitmq cluster setup with HAproxy](http://www.cloudkb.net/rabbitmq-cluster-setup-haproxy/)

4. [RabbitMQ Clustering on Ubuntu 14.04](http://www.serverlab.ca/tutorials/linux/message-queue/ubuntu-14-04-rabbitmq-clustering/)

5. [RabblitMQ Cluster + HAProxy(负载均衡)](http://flyingdutchman.iteye.com/blog/1912690)

6. [为OpenStack搭建高可用RabbitMQ集群](http://www.tuicool.com/articles/bQ3iu2r)

7. [rabbitmq集群+haproxy 相关 安装与配置和注意事项](https://segmentfault.com/a/1190000003720119)