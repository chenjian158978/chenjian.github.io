---
layout:     post
title:      "Deploy Kafka&Zookeeper on Ubuntu14.04"
subtitle:   ""
date:       Mon, Nov 14 17:40:56 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Kafka&Zookeeper-on-Ubuntu14.04/head_blog.jpg"
tags:
    - 工作
---


## 集群配置信息

- 192.168.1.157
- 192.168.1.158
- 192.168.1.159

## ZooKeeper

### 安装

```sh
# 下载zookeeper-3.4.8
sudo wget http://archive.apache.org/dist/zookeeper/zookeeper-3.4.8/zookeeper-3.4.8.tar.gz

# 解压zookeeper-3.4.8.tar.gz到/opt文件下
sudo tar zxvf zookeeper-3.4.8.tar.gz -C /opt/
```

### 配置

```sh
# 进入zookeeper配置文件下
cd /opt/zookeeper-3.4.8/conf/

# 将配置文件改为zoo.cfg
sudo mv zoo_sample.cfg zoo.cfg

# 修改文件内容
sudo vim zoo.cfg

# 1.修改为dataDir=/opt/zookeeper-3.4.8/data 
# 2.尾部添加：
# server.1=192.168.1.158:2888:3888
# server.2=192.168.1.157:2888:3888
# server.3=192.168.1.159:2888:3888

# 在zookeeper-3.4.8下创建日志文件夹
sudo mkdir data

# 创建myid文件
cd data
vim myid

# 根据zoo.cfg中的尾部内容和IP填写唯一标识ID，例如192.168.1.158的myid的内容为1
administrator@administrator158:/opt/zookeeper-3.4.8$ cat data/myid
1
```

### 启动

```sh
cd /opt/zookeeper-3.4.8/

administrator@administrator158:/opt/zookeeper-3.4.8/$ sudo ./bin/zkServer.sh start

ZooKeeper JMX enabled by default
Using config: /opt/zookeeper-3.4.8/bin/../conf/zoo.cfg
Starting zookeeper ... STARTED
```

遇到*Error contacting service. It is probably not running*的问题[^error]：

```sh
# 以前台方式启动，可以看到
sudo ./zkServer.sh start-foreground

ZooKeeper JMX enabled by default
Using config: /opt/zookeeper-3.4.8/bin/../conf/zoo.cfg
2016-11-14 16:48:51,066 [myid:] - INFO  [main:QuorumPeerConfig@103] - Reading configuration from: /opt/zookeeper-3.4.8/bin/../conf/zoo.cfg
2016-11-14 16:48:51,098 [myid:] - INFO  [main:QuorumPeer$QuorumServer@149] - Resolved hostname: 192.168.1.158 to address: /192.168.1.158
2016-11-14 16:48:51,099 [myid:] - INFO  [main:QuorumPeer$QuorumServer@149] - Resolved hostname: 192.168.1.159 to address: /192.168.1.159
2016-11-14 16:48:51,101 [myid:] - INFO  [main:QuorumPeer$QuorumServer@149] - Resolved hostname: 192.168.1.157 to address: /192.168.1.157
2016-11-14 16:48:51,101 [myid:] - INFO  [main:QuorumPeerConfig@331] - Defaulting to majority quorums
2016-11-14 16:48:51,103 [myid:] - ERROR [main:QuorumPeerMain@85] - Invalid config, exiting abnormally
org.apache.zookeeper.server.quorum.QuorumPeerConfig$ConfigException: Error processing /opt/zookeeper-3.4.8/bin/../conf/zoo.cfg
	at org.apache.zookeeper.server.quorum.QuorumPeerConfig.parse(QuorumPeerConfig.java:123)
	at org.apache.zookeeper.server.quorum.QuorumPeerMain.initializeAndRun(QuorumPeerMain.java:101)
	at org.apache.zookeeper.server.quorum.QuorumPeerMain.main(QuorumPeerMain.java:78)
Caused by: java.lang.IllegalArgumentException: /tmp/zookeeper-3.4.8/data/myid file is missing
	at org.apache.zookeeper.server.quorum.QuorumPeerConfig.parseProperties(QuorumPeerConfig.java:341)
	at org.apache.zookeeper.server.quorum.QuorumPeerConfig.parse(QuorumPeerConfig.java:119)
	... 2 more
Invalid config, exiting abnormally
```

### 查看状态

```sh
sudo ./zkServer.sh status

ZooKeeper JMX enabled by default
Using config: /opt/zookeeper-3.4.8/bin/../conf/zoo.cfg
Mode: follower
```
三个zookeeper的节点中，有一个的mode为leader，当前死掉后，follower会变成leader


## Kafka

### 安装

```sh
# 下载kafka_2.11-0.10.0.0
sudo wget http://mirrors.tuna.tsinghua.edu.cn/apache/kafka/0.10.0.0/kafka_2.11-0.10.0.0.tgz

# 解压kafka_2.11-0.10.0.0.tgz到/opt文件下
sudo tar zxvf kafka_2.11-0.10.0.0.tgz -C /opt/
```

### 配置

```sh
# 进入config文件下
cd /opt/kafka_2.11-0.10.0.0/config/

# 修改服务器属性文件
sudo vim server.properties

# 1.添加：host.name=192.168.1.158
# 2.修改：broker.id=0（数字，整形）
# 3.修改：zookeeper.connect=192.168.1.158:2181,192.168.1.157:2181,192.168.1.159:2181
```

### 启动服务

```sh
# 进入kafka文件下
cd /opt/kafka_2.11-0.10.0.0/

# 启动kafka服务
sudo ./bin/kafa-server-start.sh config/server.properties &
```

**后面加`&`，可以退出终端，让其在后台运行**

### 停止服务

```sh
sudo ./bin/kafa-server-stop.sh config/server.properties
```

### topic上的操作

#### create topic

```sh
sudo ./bin/kafka-topics.sh --create --zookeeper 192.168.1.158:2181 --replication-factor 3 --partitions 1 --topic cj_test

WARNING: Due to limitations in metric names, topics with a period ('.') or underscore ('_') could collide. To avoid issues it is best to use either, but not both.
Created topic "cj_test".
```

> --zookeeper： 指定一个zookeeper服务器ip
> 
> --replication-factor：创建3各副本
> 
> --partitions: 使用1个分区
> 
> --topic: 主题名称

#### list topic

```sh
sudo ./bin/kafka-topics.sh --list --zookeeper 192.168.1.158:2181
cj_test
```

#### describe topics

```sh
sudo ./bin/kafka-topics.sh --describe --zookeeper 192.168.1.158:2181 --topic cj_test

Topic:cj_test   PartitionCount:1        ReplicationFactor:3     	Configs:
	Topic: cj_test  Partition: 0    Leader: 1       Replicas: 2,1,0 Isr: 1
```

#### send message

```sh
sudo ./bin/kafka-console-producer.sh --broker-list 192.168.1.158:9092 --topic cj_test

this is chenjian test
```

#### consumer message

```sh
sudo ./bin/kafka-console-consumer.sh --zookeeper 192.168.1.158:2181 	--topic cj_test --from-beginning

this is chenjian test
```

#### add partitions

```sh
sudo ./bin/kafka-topics.sh -zookeeper 192.168.1.157:2181,192.168.1.158:2181,192.168.1.159:2181 –alter –partitions  3 –topic hiddenlink
	
WARNING: If partitions are increased for a topic that has a key, the partition logic or ordering of the messages will be affected
Adding partitions succeeded!
```


[^error]: [zookeeper环境搭建中的几个坑[Error contacting service. It is probably not running]的分析及解决](http://www.paymoon.com/index.php/2015/06/04/zookeeper-building/)