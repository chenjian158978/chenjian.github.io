---
layout:     post
title:      "Docker部署单机版Redis集群"
subtitle:   "Deploy Redis Cluster By Docker"
date:       Wed, May 24 2017 13:22:10 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Redis-Cluster-By-Docker/head_blog.jpg"
catalog:    true
tags:
    - 工作
    - Redis
    - Docker
---

### 基础信息

- 寄主机Ip： 10.0.6.79
- 寄主机系统： Ubuntu 14.04
- Docker Version: 17.04.0-ce
- Redis Version: 3.2.5
- 基础镜像： alpine
- redis端口：6379,6380,6381,6482,6383,6384
- 所有的资源可以在[这里](https://pan.baidu.com/s/1jIQempS)进行下载


### Redis基础镜像

##### Dockerfile

代码下载：[Dockerfile](/download/Cost-Function-Of-ML/Redis-Base/Dockerfile)

``` docker 
FROM alpine:latest
MAINTAINER chenjian chenjian158978@gmail.com

ENV REFRESHED_AT 2016-11-23

RUN apk update \
        && apk --no-cache add curl \
        && curl -sO http://download.redis.io/releases/redis-3.2.5.tar.gz \
        && tar xf redis-3.2.5.tar.gz -C /usr/local/ \
        && rm -rf redis-3.2.5.tar.gz  rm -rf /var/cache/apk/* \
        && cd /usr/local/redis-3.2.5 \
        && apk add --no-cache 'su-exec>=0.2' \
        && apk add --no-cache --virtual .build-deps gcc linux-headers make musl-dev tar \
        && make PREFIX=/usr/local/redis install \
        && apk del .build-deps tar gcc make  \
        && cp utils/redis_init_script /etc/init.d/redis \
        && chmod +x /etc/init.d/redis \
        && sed -i 's@EXEC=/usr/local/bin/redis-server@EXEC=/usr/local/redis/bin/redis-server@' /etc/init.d/redis \
        && sed -i 's@CLIEXEC=/usr/local/bin/redis-cli@CLIEXEC=/usr/local/redis/bin/redis-cli@' /etc/init.d/redis \
        && cd /usr/local \
        && rm -rf /var/cache/apk/* /usr/local/redis-3.2.5

```

##### build.sh

代码下载：[build.sh](/download/Cost-Function-Of-ML/Redis-Base/build.sh)

``` sh
#!/bin/sh
sudo docker build -t redis_base .

echo "镜像redis_base制作完成"
```

### Redis集群镜像

##### Dockerfile

代码下载：[Dockerfile](/download/Cost-Function-Of-ML/Redis-Cluster/Dockerfile)

``` docker
FROM redis_base:latest
MAINTAINER chenjian chenjian158978@gmail.com

ADD redis-6379.conf /usr/local/redis/bin/redis-6379.conf
ADD redis-6380.conf /usr/local/redis/bin/redis-6380.conf
ADD redis-6381.conf /usr/local/redis/bin/redis-6381.conf
ADD redis-6382.conf /usr/local/redis/bin/redis-6382.conf
ADD redis-6383.conf /usr/local/redis/bin/redis-6383.conf
ADD redis-6384.conf /usr/local/redis/bin/redis-6384.conf
ADD start.sh /start.sh
RUN chmod +x /start.sh

ENTRYPOINT ["/start.sh"]
```

##### redis-6379.conf

代码下载：[redis-6379.conf](/download/Cost-Function-Of-ML/Redis-Cluster/redis-6379.conf)

``` sh
egrep -v "^$|^#" redis-6379.conf

<<'COMMENT'
port 6379
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 15000
appendonly yes
protected-mode no
tcp-backlog 511
timeout 0
tcp-keepalive 300
daemonize no
supervised no
pidfile /var/run/redis_6379.pid
loglevel notice
logfile ""
databases 16
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir ./
slave-serve-stale-data yes
slave-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
repl-disable-tcp-nodelay no
slave-priority 100
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
lua-time-limit 5000
slowlog-log-slower-than 10000
slowlog-max-len 128
latency-monitor-threshold 0
notify-keyspace-events ""
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit slave 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10
aof-rewrite-incremental-fsync yes
COMMENT
```

##### start.sh

代码下载：[start.sh](/download/Cost-Function-Of-ML/Redis-Cluster/start.sh)

具体使用哪个config文件，为传入的环境变量所定。

``` sh
#!/bin/bash

cd /usr/local/redis/bin
./redis-server ${conf_file}

```

##### build.sh

代码下载：[build.sh](/download/Cost-Function-Of-ML/Redis-Cluster/build.sh)

``` sh
#!/bin/bash

sudo docker build -t redis-cluster .

```

### 运行容器-run.sh

代码下载：[run.sh](/download/Cost-Function-Of-ML/Redis-Cluster/run.sh)

``` sh
#!/bin/bash

sudo docker run -d -e 'conf_file=redis-6379.conf' --network=host --name redis-cluster_6379 redis-cluster
sudo docker run -d -e 'conf_file=redis-6380.conf' --network=host --name redis-cluster_6380 redis-cluster
sudo docker run -d -e 'conf_file=redis-6381.conf' --network=host --name redis-cluster_6381 redis-cluster
sudo docker run -d -e 'conf_file=redis-6382.conf' --network=host --name redis-cluster_6382 redis-cluster
sudo docker run -d -e 'conf_file=redis-6383.conf' --network=host --name redis-cluster_6383 redis-cluster
sudo docker run -d -e 'conf_file=redis-6384.conf' --network=host --name redis-cluster_6384 redis-cluster

```

- `--network=host`使容器与寄主机同Ip，即内部端口暴露在寄主机上

### 创建集群

``` sh
# 安装ruby
sudo yum install -y ruby
#
sudo apt-get install -y ruby

# 安装redis-3.3.3
sudo gem install redis-3.3.3.gem

# 解压redis-3.5.2
sudo tar -xf redis-3.2.5.tar.gz
```

##### create_cluster.sh

代码下载：[create_cluster.sh](/download/Cost-Function-Of-ML/Redis-Cluster/create_cluster.sh)

``` sh
#!/bin/bash

cd redis-3.2.5

src/redis-trib.rb create --replicas 1 10.0.6.79:6379 10.0.6.79:6380 10.0.6.79:6381 10.0.6.79:6382 10.0.6.79:6383 10.0.6.79:6384
```

##### 运行脚本

``` sh
echo -e yes | source create-cluster.sh

<<'COMMENT'
>>> Creating cluster
>>> Performing hash slots allocation on 6 nodes...
Using 3 masters:
10.0.6.79:6379
10.0.6.79:6380
10.0.6.79:6381
Adding replica 10.0.6.79:6382 to 10.0.6.79:6379
Adding replica 10.0.6.79:6383 to 10.0.6.79:6380
Adding replica 10.0.6.79:6384 to 10.0.6.79:6381
M: c800d55087ad92717bcc374b07792f658cbf3a15 10.0.6.79:6379
   slots:0-5460 (5461 slots) master
M: da6b777d81c90826344a1e65a3af8312f57c0e3d 10.0.6.79:6380
   slots:5461-10922 (5462 slots) master
M: 76537d3ac5ce7b5d45a948a192f41f9009365cd7 10.0.6.79:6381
   slots:10923-16383 (5461 slots) master
S: 4640935f7573279e89bb21bf34e6cbdf29d6a50b 10.0.6.79:6382
   replicates c800d55087ad92717bcc374b07792f658cbf3a15
S: aa38194a8ab1a68dda81e224bed38db3cce02634 10.0.6.79:6383
   replicates da6b777d81c90826344a1e65a3af8312f57c0e3d
S: a88d95808df1b9ad4ffd773629ab0cd9d0fa59b8 10.0.6.79:6384
   replicates 76537d3ac5ce7b5d45a948a192f41f9009365cd7
Can I set the above configuration? (type 'yes' to accept): yes
>>> Nodes configuration updated
>>> Assign a different config epoch to each node
>>> Sending CLUSTER MEET messages to join the cluster
Waiting for the cluster to join...
>>> Performing Cluster Check (using node 10.0.6.79:6379)
M: c800d55087ad92717bcc374b07792f658cbf3a15 10.0.6.79:6379
   slots:0-5460 (5461 slots) master
   1 additional replica(s)
M: da6b777d81c90826344a1e65a3af8312f57c0e3d 10.0.6.79:6380
   slots:5461-10922 (5462 slots) master
   1 additional replica(s)
M: 76537d3ac5ce7b5d45a948a192f41f9009365cd7 10.0.6.79:6381
   slots:10923-16383 (5461 slots) master
   1 additional replica(s)
S: 4640935f7573279e89bb21bf34e6cbdf29d6a50b 10.0.6.79:6382
   slots: (0 slots) slave
   replicates c800d55087ad92717bcc374b07792f658cbf3a15
S: aa38194a8ab1a68dda81e224bed38db3cce02634 10.0.6.79:6383
   slots: (0 slots) slave
   replicates da6b777d81c90826344a1e65a3af8312f57c0e3d
S: a88d95808df1b9ad4ffd773629ab0cd9d0fa59b8 10.0.6.79:6384
   slots: (0 slots) slave
   replicates 76537d3ac5ce7b5d45a948a192f41f9009365cd7
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
COMMENT
```

此时整个Redis集群创建完成

### 端口信息

``` sh
netstat -ntlp|grep -E '6379|6380|6381|6382|6383|6384'

<<'COMMENT'
tcp        0      0 0.0.0.0:6379            0.0.0.0:*               LISTEN      11030/redis-server
tcp        0      0 0.0.0.0:6380            0.0.0.0:*               LISTEN      11080/redis-server
tcp        0      0 0.0.0.0:6381            0.0.0.0:*               LISTEN      11127/redis-server
tcp        0      0 0.0.0.0:6382            0.0.0.0:*               LISTEN      11174/redis-server
tcp        0      0 0.0.0.0:6383            0.0.0.0:*               LISTEN      11217/redis-server
tcp        0      0 0.0.0.0:6384            0.0.0.0:*               LISTEN      11269/redis-server
tcp        0      0 0.0.0.0:16379           0.0.0.0:*               LISTEN      11030/redis-server
tcp        0      0 0.0.0.0:16380           0.0.0.0:*               LISTEN      11080/redis-server
tcp        0      0 0.0.0.0:16381           0.0.0.0:*               LISTEN      11127/redis-server
tcp        0      0 0.0.0.0:16382           0.0.0.0:*               LISTEN      11174/redis-server
tcp        0      0 0.0.0.0:16383           0.0.0.0:*               LISTEN      11217/redis-server
tcp        0      0 0.0.0.0:16384           0.0.0.0:*               LISTEN      11269/redis-server
tcp6       0      0 :::6379                 :::*                    LISTEN      11030/redis-server
tcp6       0      0 :::6380                 :::*                    LISTEN      11080/redis-server
tcp6       0      0 :::6381                 :::*                    LISTEN      11127/redis-server
tcp6       0      0 :::6382                 :::*                    LISTEN      11174/redis-server
tcp6       0      0 :::6383                 :::*                    LISTEN      11217/redis-server
tcp6       0      0 :::6384                 :::*                    LISTEN      11269/redis-server
tcp6       0      0 :::16379                :::*                    LISTEN      11030/redis-server
tcp6       0      0 :::16380                :::*                    LISTEN      11080/redis-server
tcp6       0      0 :::16381                :::*                    LISTEN      11127/redis-server
tcp6       0      0 :::16382                :::*                    LISTEN      11174/redis-server
tcp6       0      0 :::16383                :::*                    LISTEN      11217/redis-server
tcp6       0      0 :::16384                :::*                    LISTEN      11269/redis-server
COMMENT
```

### 容器日志信息

``` sh
docker logs 90f00a395e4c

<<'COMMENT'
8:M 24 May 03:13:52.244 * No cluster configuration found, I'm 4640935f7573279e89bb21bf34e6cbdf29d6a50b
                _._                                                  
           _.-``__ ''-._                                             
      _.-``    `.  `_.  ''-._           Redis 3.2.5 (00000000/0) 64 bit
  .-`` .-```.  ```\/    _.,_ ''-._                                   
 (    '      ,       .-`  | `,    )     Running in cluster mode
 |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6382
 |    `-._   `._    /     _.-'    |     PID: 8
  `-._    `-._  `-./  _.-'    _.-'                                   
 |`-._`-._    `-.__.-'    _.-'_.-'|                                  
 |    `-._`-._        _.-'_.-'    |           http://redis.io        
  `-._    `-._`-.__.-'_.-'    _.-'                                   
 |`-._`-._    `-.__.-'    _.-'_.-'|                                  
 |    `-._`-._        _.-'_.-'    |                                  
  `-._    `-._`-.__.-'_.-'    _.-'                                   
      `-._    `-.__.-'    _.-'                                       
          `-._        _.-'                                           
              `-.__.-'                                               

8:M 24 May 03:13:52.304 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
8:M 24 May 03:13:52.304 # Server started, Redis version 3.2.5
8:M 24 May 03:13:52.304 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
8:M 24 May 03:13:52.304 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
8:M 24 May 03:13:52.304 * The server is now ready to accept connections on port 6382
8:M 24 May 03:24:01.616 # configEpoch set to 4 via CLUSTER SET-CONFIG-EPOCH
8:M 24 May 03:24:01.661 # IP address for this node updated to 10.0.6.79
8:S 24 May 03:24:05.732 # Cluster state changed: ok
8:S 24 May 03:24:06.432 * Connecting to MASTER 10.0.6.79:6379
8:S 24 May 03:24:06.433 * MASTER <-> SLAVE sync started
8:S 24 May 03:24:06.433 * Non blocking connect for SYNC fired the event.
8:S 24 May 03:24:06.433 * Master replied to PING, replication can continue...
8:S 24 May 03:24:06.433 * Partial resynchronization not possible (no cached master)
8:S 24 May 03:24:06.435 * Full resync from master: 0efc2a6030feff483ca96d69242e0d9fafe3912b:1
8:S 24 May 03:24:06.496 * MASTER <-> SLAVE sync: receiving 76 bytes from master
8:S 24 May 03:24:06.496 * MASTER <-> SLAVE sync: Flushing old data
8:S 24 May 03:24:06.496 * MASTER <-> SLAVE sync: Loading DB in memory
8:S 24 May 03:24:06.496 * MASTER <-> SLAVE sync: Finished with success
8:S 24 May 03:24:06.498 * Background append only file rewriting started by pid 11
8:S 24 May 03:24:06.544 * AOF rewrite child asks to stop sending diffs.
11:C 24 May 03:24:06.544 * Parent agreed to stop sending diffs. Finalizing AOF...
11:C 24 May 03:24:06.544 * Concatenating 0.00 MB of AOF diff received from parent.
11:C 24 May 03:24:06.544 * SYNC append only file rewrite performed
11:C 24 May 03:24:06.544 * AOF rewrite: 4 MB of memory used by copy-on-write
8:S 24 May 03:24:06.633 * Background AOF rewrite terminated with success
8:S 24 May 03:24:06.633 * Residual parent diff successfully flushed to the rewritten AOF (0.00 MB)
8:S 24 May 03:24:06.633 * Background AOF rewrite finished successfully
COMMENT
```

### 参考文献

1. [Docker部署Redis cluster3.2.5集群](http://www.linuxea.com/1486.html)


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/05/24/Deploy-Redis-Cluster-By-Docker/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。

