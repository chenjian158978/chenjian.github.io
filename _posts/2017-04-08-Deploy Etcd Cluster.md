---
layout:     post
title:      "Deploy Etcd Cluster"
subtitle:   "Deliver my soul from the sword;
my darling from the power of the dog. Psa 22:20"
date:       Sat, Apr 8 2017 09:05:47 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Etcd-Cluster/head_blog.jpg"
catalog:    true
tags:
    - 工作
    - Kubernetes
---

### 系列博文

- [Deploy K8s by Kubeadm on Linux](https://o-my-chenjian.com/2016/12/08/Deploy-K8s-by-Kubeadm-on-Linux/)
- [Easy With Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)
- [Deploy Etcd Cluster](https://o-my-chenjian.com/2017/04/08/Deploy-Etcd-Cluster/)
- [Deploy Dashboard With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Dashboard-With-K8s/)
- [Deploy Monitoring With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Monitoring-With-K8s/)
- [Deploy Logging With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Logging-With-K8s/)
- [Deploy Ingress With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Ingress-With-K8s/)
- [Deploy Redis Sentinel Cluster With K8s](https://o-my-chenjian.com/2017/02/06/Deploy-Redis-Sentinel-Cluster-With-K8s/)

### Etcd搭建

Etcd集群对整个k8s集群非常重要，需要抽出搭建。

**但kubeadm不支持高可用性，及不支持etcd集群**

> 搭建环境：**CentOS7**
> 
> 
|  Node |     IP       |
|:-----:|:------------:|
| etcd0 | 192.168.1.157|
| etcd1 | 192.168.1.158|
| etcd2 | 192.168.1.159|

- 关闭防火墙

``` bash
sudo systemctl stop firewalld
sudo systemctl disable firewalld
```

- 安装命令：

``` bash
sudo yum install etcd -y
```


``` bash
etcd --version

etcd Version: 2.3.7
Git SHA: fd17c91
Go Version: go1.6.3
Go OS/Arch: linux/amd64
```

- 修改etcd配置

默认文件位于`/etc/etcd/etcd.conf`

``` bash
rm -rf /etc/etcd/etcd.conf

sudo cat <<EOF |  sudo tee /etc/etcd/etcd.conf
ETCD_NAME=etcd0
ETCD_DATA_DIR="/var/lib/etcd/etcd0"
ETCD_LISTEN_PEER_URLS="http://0.0.0.0:2380"
ETCD_LISTEN_CLIENT_URLS="http://0.0.0.0:2379,http://0.0.0.0:4001"
ETCD_INITIAL_ADVERTISE_PEER_URLS="http://192.168.1.157:2380"
ETCD_INITIAL_CLUSTER="etcd0=http://192.168.1.157:2380,etcd1=http://192.168.1.158:2380,etcd2=http://192.168.1.159:2380"
ETCD_INITIAL_CLUSTER_STATE="new"
ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster"
ETCD_ADVERTISE_CLIENT_URLS="http://192.168.1.157:2379,http://192.168.1.157:4001"
ETCD_DISCOVERY=""
EOF
```

- 修改etcd的service文件

``` bash
sudo cat <<EOF |  sudo tee /lib/systemd/system/etcd.service
[Unit]
Description=Etcd Server
After=network.target
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
WorkingDirectory=/var/lib/etcd/
EnvironmentFile=-/etc/etcd/etcd.conf
User=etcd
# set GOMAXPROCS to number of processors
ExecStart=/bin/bash -c "GOMAXPROCS=$(nproc) /usr/bin/etcd --name=\"${ETCD_NAME}\" --data-dir=\"${ETCD_DATA_DIR}\" --listen-client-urls=\"${ETCD_LISTEN_CLIENT_URLS}\" 
--advertise-client-urls=\"${ETCD_ADVERTISE_CLIENT_URLS}\" --initial-cluster-token=\"${ETCD_INITIAL_CLUSTER_TOKEN}\" --initial-cluster=\"${ETCD_INITIAL_CLUSTER}\" --initial-cluster-state=\"${ETCD_INITIAL_CLUSTER_STATE}\""
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF
```

- 启动etcd的service

``` bash
sudo systemctl stop etcd

sudo systemctl daemon-reload 

sudo systemctl enable etcd

sudo systemctl start etcd

sudo systemctl status etcd
```

- 查看etcd的启动参数

``` bash
ps aux|grep etcd

etcd     16010  1.3  1.1  49112 20728 ?        Ssl  10:18   2:30 /usr/bin/etcd --name=etcd0 --data-dir=/var/lib/etcd/etcd0 --listen-client-urls=http://0.0.0.0:2379,http://0.0.0.0:4001 --advertise-client-urls=http://192.168.1.157:2379,http://192.168.1.157:4001 --initial-cluster-token=etcd-cluster --initial-cluster=etcd0=http://192.168.1.157:2380,etcd1=http://192.168.1.158:2380,etcd2=http://192.168.1.159:2380 --initial-cluster-state=new
root     18440  0.0  0.0 112652   956 pts/0    S+   13:28   0:00 grep --color=auto etcd
```

- 查看etcd集群的节点信息

``` bash
etcdctl member list

5a2567911e869c1: name=etcd1 peerURLs=http://192.168.1.158:2380 clientURLs=http://192.168.1.158:2379,http://192.168.1.158:4001 isLeader=true
588d5e8d3a8648b5: name=etcd2 peerURLs=http://192.168.1.159:2380 clientURLs=http://192.168.1.159:2379,http://192.168.1.159:4001 isLeader=false
bd2d658f033f9bcc: name=etcd0 peerURLs=http://192.168.1.157:2380 clientURLs=http://192.168.1.157:2379,http://192.168.1.157:4001 isLeader=false
```

- 查看etcd集群的健康情况

``` bash
etcdctl cluster-health

member 5a2567911e869c1 is healthy: got healthy result from http://192.168.1.158:2379
member 588d5e8d3a8648b5 is healthy: got healthy result from http://192.168.1.159:2379
member bd2d658f033f9bcc is healthy: got healthy result from http://192.168.1.157:2379
cluster is healthy
```

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/08/Deploy-Etcd-Cluster/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。