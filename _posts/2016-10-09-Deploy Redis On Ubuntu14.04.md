---
layout:     post
title:      "Deploy Redis On Ubuntu14.04"
subtitle:   "He sent from above, he took me,
he drew me out of many waters. Psa 18:16"
date:       Sun, Oct 09 2016 17:49:22 2016 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Redis-On-Ubuntu14.04/head_blog.jpg"
catalog:    true
tags:
    - 工作
    - Redis
    - Ubuntu
---

### Redis的安装

命令： `sudo apt-get install redis-server`

通过该命令的安装，redis版本较低(2.8.4)，但是不需要太多设置。

* 配置文件： /etc/redis/redis.conf

* 服务路径： /etc/init.d/redis-server


**安装最新的redis**

1. [redis官网](http://redis.io/)

2. [redis的github](https://github.com/antirez/redis)

按照官网的说明：

- `wget http://download.redis.io/releases/redis-x.x.x.tar.gz`

- `tar xzf redis-x.x.x.tar.gz`

- `cd redis-3.2.4`

- `make`

*如果你认真读redis的readme，你会发现上面操作是建立一个“要开启”的redis-server， 往下读，你会发现如何建立永久的redis-ser*
在**readme中的Installing Redis**

- `make install` 

对于生产环境(production system)

- `cd utils`

- `sudo ./install_server.sh`  随后的一些问题选默认即可

##### redis简易操作

启动redis服务：

命令： `cd /etc/init.d/`  $\rightarrow$  `redis-server &`

* 加上`&`号使redis以后台程序方式运行

启动redis客户端：

命令：`redis-cli`

随后，查看redis配置信息：`INFO`

内容如下：

``` bash
# Server
redis_version:3.2.4
redis_git_sha1:00000000
redis_git_dirty:0
redis_build_id:5436d4788e38f72c
redis_mode:standalone
os:Linux 4.2.0-42-generic x86_64
arch_bits:64
multiplexing_api:epoll
gcc_version:4.8.4
process_id:1136
run_id:c0058beaa6b81885ac3f24b77606df47d481061c
tcp_port:6379
uptime_in_seconds:9569
uptime_in_days:0
hz:10
lru_clock:16452656
executable:/usr/local/bin/redis-server
config_file:/etc/redis/6379.conf

# Clients
connected_clients:1
client_longest_output_list:0
client_biggest_input_buf:0
blocked_clients:0

# Memory
used_memory:822432
used_memory_human:803.16K
used_memory_rss:9359360
used_memory_rss_human:8.93M
used_memory_peak:822432
used_memory_peak_human:803.16K
total_system_memory:6221660160
total_system_memory_human:5.79G
used_memory_lua:37888
used_memory_lua_human:37.00K
maxmemory:0
maxmemory_human:0B
maxmemory_policy:noeviction
mem_fragmentation_ratio:11.38
mem_allocator:jemalloc-4.0.3

# Persistence
loading:0
rdb_changes_since_last_save:0
rdb_bgsave_in_progress:0
rdb_last_save_time:1476066366
rdb_last_bgsave_status:ok
rdb_last_bgsave_time_sec:0
rdb_current_bgsave_time_sec:-1
aof_enabled:0
aof_rewrite_in_progress:0
aof_rewrite_scheduled:0
aof_last_rewrite_time_sec:-1
aof_current_rewrite_time_sec:-1
aof_last_bgrewrite_status:ok
aof_last_write_status:ok

# Stats
total_connections_received:2
total_commands_processed:5
instantaneous_ops_per_sec:0
total_net_input_bytes:125
total_net_output_bytes:11758604
instantaneous_input_kbps:0.00
instantaneous_output_kbps:0.00
rejected_connections:0
sync_full:0
sync_partial_ok:0
sync_partial_err:0
expired_keys:0
evicted_keys:0
keyspace_hits:0
keyspace_misses:0
pubsub_channels:0
pubsub_patterns:0
latest_fork_usec:1744
migrate_cached_sockets:0

# Replication
role:master
connected_slaves:0
master_repl_offset:0
repl_backlog_active:0
repl_backlog_size:1048576
repl_backlog_first_byte_offset:0
repl_backlog_histlen:0

# CPU
used_cpu_sys:6.52
used_cpu_user:4.72
used_cpu_sys_children:0.00
used_cpu_user_children:0.00

# Cluster
cluster_enabled:0

# Keyspace
db0:keys=1,expires=0,avg_ttl=0
```

##### redis.conf的主要参数

>daemonize：是否以后台daemon方式运行
pidfile：pid文件位置
port：监听的端口号
timeout：请求超时时间
loglevel：log信息级别
logfile：log文件位置
databases：开启数据库的数量
save * *：保存快照的频率，第一个*表示多长时间，第三个*表示执行多少次写操作。在一定时间内执行一定数量的写操作时，自动保存快照。可设置多个条件。
rdbcompression：是否使用压缩
dbfilename：数据快照文件名（只是文件名，不包括目录）
dir：数据快照的保存目录（这个是目录）
appendonly：是否开启appendonlylog，开启的话每次写操作会记一条log，这会提高数据抗风险能力，但影响效率。
appendfsync：appendonlylog如何同步到磁盘（三个选项，分别是每次写都强制调用fsync、每秒启用一次fsync、不调用fsync等待系统自己同步）


##### redis开启远程 

- 修改redis配置文件(`/etc/redis/6379.conf`), 将`bind localhost`或`bind 127.0.0.1`注释掉；

- 修改`protected-mode`

遇到`(error) DENIED Redis is running in protected mode because protected mode is enabled`这个问题，需要把配置文件中的`protected-mode `的值改为`no`；

- 重启redis服务：`sudo service redis_6379 restart`, 其中`redis_6379`在`/etc/init.d/`中

- 验证：`ps -aux| grep redis`

``` bash
root      5674  0.0  0.1  40448  9164 ?        Ssl  11:56   0:00 /usr/local/bin/redis-server *:6379              
chenjian  5680  0.0  0.0  15944  2224 pts/7    S+   11:56   0:00 grep --color=auto redis
```

- 本机(10.0.0.44)redis内容如下：

``` bash
(python2.7) chenjian@chenjian-Pc:/usr/local/bin$ redis-cli 
127.0.0.1:6379> KEYS *
1) "chenjian"
127.0.0.1:6379> GET chenjian
"26"
```

- 远程在10.0.0.41中的python程序“
 
``` python
# -*- encoding=utf-8 -*-

import redis

chenjian_host = "10.0.0.44"
chenjian_port = 6379
chenjian_db = 0

r = redis.StrictRedis(host=chenjian_host, port=chenjian_port, db=chenjian_db)
print r.keys()
print r.get('chenjian')
```

结果：

``` bash
['chenjian']
26
```

### 参考

1. [Redis的三种启动方式](http://www.tuicool.com/articles/aQbQ3u)
2. [redis安装部署维护备份](http://blog.csdn.net/huwei2003/article/details/40536905)
3. [Redis开启远程登录连接](http://www.cnblogs.com/machanghai/p/5497084.html)
4. [redis 报错 Redis protected-mode 配置文件没有真正启动](http://www.th7.cn/db/nosql/201608/201681.shtml) 
5. [redis教程-自强教程](http://www.runoob.com/redis/redis-tutorial.html)
6. [redis快速入门](http://www.yiibai.com/redis/redis_quick_guide.html)


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2016/10/09/Deploy-Redis-On-Ubuntu14.04/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
