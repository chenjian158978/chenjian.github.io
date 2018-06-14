---
layout:     post
title:      "Kubernetes集群之Redis Sentinel集群"
subtitle:   "Deploy Redis Sentinel Cluster With K8s"
date:       Mon, Feb 6 2017 09:42:59 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Redis-Sentinel-Cluster-With-K8s/head_blog.jpg"
catalog:    true
tags: [工作, Redis, Kubernetes, Python, JavaScript]
---

### 系列博文

- [在Linux上使用Kubeadm工具部署Kubernetes](https://o-my-chenjian.com/2016/12/08/Deploy-K8s-by-Kubeadm-on-Linux/)
- [带你玩转Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)
- [Kubernetes集群之搭建ETCD集群](https://o-my-chenjian.com/2017/04/08/Deploy-Etcd-Cluster/)
- [Kubernetes集群之Dashboard](https://o-my-chenjian.com/2017/04/08/Deploy-Dashboard-With-K8s/)
- [Kubernetes集群之Monitoring](https://o-my-chenjian.com/2017/04/08/Deploy-Monitoring-With-K8s/)
- [Kubernetes集群之Logging](https://o-my-chenjian.com/2017/04/08/Deploy-Logging-With-K8s/)
- [Kubernetes集群之Ingress](https://o-my-chenjian.com/2017/04/08/Deploy-Ingress-With-K8s/)
- [Kubernetes集群之Redis Sentinel集群](https://o-my-chenjian.com/2017/02/06/Deploy-Redis-Sentinel-Cluster-With-K8s/)
- [Kubernetes集群之Kafka和ZooKeeper](https://o-my-chenjian.com/2017/04/11/Deploy-Kafka-And-ZP-With-K8s/)

### 参照官网与GITHUB

主要是github上面的[Reliable, Scalable Redis on Kubernetes](https://github.com/kubernetes/kubernetes/tree/master/examples/storage/redis)

- 下载相关的yaml文件

- 下载相关镜像，并pull到搭建好的私有库

- 修改yaml文件，例如images路径 

**注意**：从改yaml文件中看到，redis部署在命名空间为default中，其环境变量也均在命名空间default中

- 镜像	

根据官方给的DockerFile文件，进行了一定的修改：

``` docker
FROM alpine:3.5

RUN apk update
RUN apk upgrade
RUN apk add --no-cache redis sed bash

COPY redis-master.conf /redis-master/redis.conf
COPY redis-slave.conf /redis-slave/redis.conf
COPY run.sh /run.sh

CMD [ "/run.sh" ]

ENTRYPOINT [ "bash", "-c" ]
```

1. 更新了alpine版本，从而提高了redis版本；
2. 添加apk的更新 

- 部署

``` bash
# Create a bootstrap master
kubectl create -f redis-master.yaml

# Create a service to track the sentinels
kubectl create -f redis-sentinel-service.yaml

# Create a replication controller for redis servers
kubectl create -f redis-controller.yaml

# Create a replication controller for redis sentinels
kubectl create -f redis-sentinel-controller.yaml

# Scale both replication controllers
kubectl scale rc redis --replicas=3
kubectl scale rc redis-sentinel --replicas=3

# Delete the original master pod
kubectl delete pods redis-master
```

- 结果

``` bash
[root@192-168-1-177 administrator]# kubectl get pods -o wide --all-namespaces
NAMESPACE     NAME                                           READY     STATUS    RESTARTS   AGE       IP              NODE
default       redis-0b305                                    1/1       Running   0          16d       10.44.0.2       192-168-1-178.node
default       redis-2407k                                    1/1       Running   0          16d       10.44.0.5       192-168-1-178.node
default       redis-4szpv                                    1/1       Running   0          54m       10.44.0.14      192-168-1-178.node
default       redis-sentinel-5xkv4                           1/1       Running   0          16d       10.44.0.6       192-168-1-178.node
default       redis-sentinel-f7p13                           1/1       Running   0          16d       10.44.0.3       192-168-1-178.node
default       redis-sentinel-q6ms7                           1/1       Running   0          16d       10.44.0.7       192-168-1-178.node
```

从中可以看到在pod内部，通过IP(10.44.0.2,10.44.0.5和10.44.0.14)进行访问

``` bash
[root@192-168-1-177 administrator]# kubectl get svc --all-namespaces
NAMESPACE     NAME                  CLUSTER-IP      EXTERNAL-IP   PORT(S)                         AGE
default       redis-sentinel        10.105.11.83    <none>        26379/TCP                       16d
```

从中通过访问10.105.11.83:26379来获得master与slave。

### python链接redis sentinel

**注意**： 需保证以下代码所在的pod的命名空间与redis相同

代码：

``` python
# -*- encoding=utf-8 -*-

import os
import redis

from redis.sentinel import Sentinel

redis_host = os.environ['REDIS_SENTINEL_SERVICE_HOST']
redis_port = os.environ['REDIS_SENTINEL_SERVICE_PORT']

sentinel = Sentinel([(redis_host, int(redis_port))], socket_timeout=0.1)
print sentinel.discover_master('mymaster')
print sentinel.discover_slaves('mymaster')

master = sentinel.master_for('mymaster', socket_timeout=0.1)
master.set('foo', 'bar')

print slave.get('foo')
print master.get('chenjian')
```

结果：

``` bash
('10.44.0.5', 6379)
[('10.44.0.14', 6379), ('10.44.0.2', 6379)]
bar
26
```

可以看出在redis sentinel cluster中，master为`10.44.0.5`,slaves为`10.44.0.14`和`10.44.0.2`。在某一个redis死掉后，会有新的master被选举出来，并且pod中的环境变量会自动更新。*但是当service（redis-sentinel）死掉后，环境变量不会自动更新。*

环境变量：

``` bash
# env |grep REDIS
REDIS_SENTINEL_PORT_26379_TCP_ADDR=10.105.11.83
REDIS_SENTINEL_SERVICE_HOST=10.105.11.83
REDIS_SENTINEL_SERVICE_PORT=26379
REDIS_SENTINEL_PORT_26379_TCP_PORT=26379
REDIS_SENTINEL_PORT_26379_TCP=tcp://10.105.11.83:26379
REDIS_SENTINEL_PORT_26379_TCP_PROTO=tcp
REDIS_SENTINEL_PORT=tcp://10.105.11.83:26379
```

### nodejs链接redis sentinel

``` javascript
var Redis = require('ioredis');

console.log(process.env.REDIS_SENTINEL_SERVICE_HOST);
console.log(process.env.REDIS_SENTINEL_SERVICE_PORT);

var redis = new Redis({
    sentinels: [{ host: process.env.REDIS_SENTINEL_SERVICE_HOST, port: process.env.REDIS_SENTINEL_SERVICE_PORT }],
    name: 'mymaster'
});

redis.set('foo', 'bar');

redis.get('foo', function (err, res) {
    if (!err) {
        console.log(res);
    } else {
        console.log(err);
    }
});
```

结果：

``` sh
10.96.12.100
26379
bar
```

### 参考博文

1. [Reliable, Scalable Redis on Kubernetes](https://github.com/kubernetes/kubernetes/tree/master/examples/storage/redis)
2. [redis的python客户端redis-py初识](http://www.tuicool.com/articles/FzmaeiY)
3. [Redis Sentinel机制与用法一](https://segmentfault.com/a/1190000002680804)
4. [redis-cluster研究和使用](http://hot66hot.iteye.com/blog/2050676)


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/02/06/Deploy-Redis-Sentinel-Cluster-With-K8s/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
