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

### 搭建说明

Etcd集群对整个k8s集群非常重要，需要抽出搭建。以下包含两种搭建：

- 没有CA认证的etcd集群，即普通的搭建方法
- 含有CA认证的etcd集群，此方法配合[k8s的二进制搭建](https://o-my-chenjian.com/2017/04/25/Deploy-K8s-By-Source-Code-On-CentOS7/)

**同时，注意kubeadm不支持高可用性，及不支持etcd集群**

### 无CA认证的Etcd集群

##### 系列博文

- [Deploy K8s by Kubeadm on Linux](https://o-my-chenjian.com/2016/12/08/Deploy-K8s-by-Kubeadm-on-Linux/)
- [Easy With Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)
- [Deploy Etcd Cluster](https://o-my-chenjian.com/2017/04/08/Deploy-Etcd-Cluster/)
- [Deploy Dashboard With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Dashboard-With-K8s/)
- [Deploy Monitoring With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Monitoring-With-K8s/)
- [Deploy Logging With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Logging-With-K8s/)
- [Deploy Ingress With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Ingress-With-K8s/)
- [Deploy Redis Sentinel Cluster With K8s](https://o-my-chenjian.com/2017/02/06/Deploy-Redis-Sentinel-Cluster-With-K8s/)
- [Deploy Kafka And ZP With K8s](https://o-my-chenjian.com/2017/04/11/Deploy-Kafka-And-ZP-With-K8s/)

##### 集群信息

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

<<'COMMENT'
etcd Version: 2.3.7
Git SHA: fd17c91
Go Version: go1.6.3
Go OS/Arch: linux/amd64
COMMENT
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

<<'COMMENT'
etcd     16010  1.3  1.1  49112 20728 ?        Ssl  10:18   2:30 /usr/bin/etcd --name=etcd0 --data-dir=/var/lib/etcd/etcd0 --listen-client-urls=http://0.0.0.0:2379,http://0.0.0.0:4001 --advertise-client-urls=http://192.168.1.157:2379,http://192.168.1.157:4001 --initial-cluster-token=etcd-cluster --initial-cluster=etcd0=http://192.168.1.157:2380,etcd1=http://192.168.1.158:2380,etcd2=http://192.168.1.159:2380 --initial-cluster-state=new
root     18440  0.0  0.0 112652   956 pts/0    S+   13:28   0:00 grep --color=auto etcd
COMMENT
```

- 查看etcd集群的节点信息

``` bash
etcdctl member list

<<'COMMENT'
5a2567911e869c1: name=etcd1 peerURLs=http://192.168.1.158:2380 clientURLs=http://192.168.1.158:2379,http://192.168.1.158:4001 isLeader=true
588d5e8d3a8648b5: name=etcd2 peerURLs=http://192.168.1.159:2380 clientURLs=http://192.168.1.159:2379,http://192.168.1.159:4001 isLeader=false
bd2d658f033f9bcc: name=etcd0 peerURLs=http://192.168.1.157:2380 clientURLs=http://192.168.1.157:2379,http://192.168.1.157:4001 isLeader=false
COMMENT
```

- 查看etcd集群的健康情况

``` bash
etcdctl cluster-health

<<'COMMENT'
member 5a2567911e869c1 is healthy: got healthy result from http://192.168.1.158:2379
member 588d5e8d3a8648b5 is healthy: got healthy result from http://192.168.1.159:2379
member bd2d658f033f9bcc is healthy: got healthy result from http://192.168.1.157:2379
cluster is healthy
COMMENT
```

### 含CA认证的Etcd集群搭建

##### 系列博文

- [Deploy K8s By Source Code On CentOS7](https://o-my-chenjian.com/2017/04/25/Deploy-K8s-By-Source-Code-On-CentOS7/)
- [Security Settings Of K8s](https://o-my-chenjian.com/2017/04/25/Security-Settings-Of-K8s/)
- [Deploy Etcd Cluster](https://o-my-chenjian.com/2017/04/08/Deploy-Etcd-Cluster/)
- [Create The File Of Kubeconfig For K8s](https://o-my-chenjian.com/2017/04/26/Create-The-File-Of-Kubeconfig-For-K8s/)
- [Deploy Master Of K8s](https://o-my-chenjian.com/2017/04/26/Deploy-Master-Of-K8s/)
- [Deploy Node Of K8s](https://o-my-chenjian.com/2017/04/26/Deploy-Node-Of-K8s/)
- [Easy With Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)
- [Deploy Kubedns Of K8s](https://o-my-chenjian.com/2017/04/26/Deploy-Kubedns-Of-K8s/)
- [Deploy Dashboard With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Dashboard-With-K8s/)

##### 搭建前准备工作

操作服务器为：`192.168.1.175／192.168.1.176／192.168.1.177`，即etcd集群的三台服务器。**以下以`192.168.1.175`为例子**。其他两台服务器，对配置文件需要相对应的修改。

- 安装基本软件和更名

``` bash
# 更新源
yum update -y
yum install -y vim
yum install -y wget

# 更改hostname
ipname=192-168-1-175
nodetype=etcd

echo "${ipname}.${nodetype}" > /etc/hostname
echo "127.0.0.1   ${ipname}.${nodetype}" >> /etc/hosts
sysctl kernel.hostname=${ipname}.${nodetype}

# 关闭防火墙
sudo systemctl stop firewalld
sudo systemctl disable firewalld
```

- 设置集群的环境变量

``` bash
# 创建必要的文件夹
mkdir /root/local
mkdir /root/local/bin

# 环境变量
cat >> /etc/profile <<EOF
# 最好使用 主机未用的网段 来定义服务网段和 Pod 网段

ETCD_0=192.168.1.175
ETCD_1=192.168.1.176
ETCD_2=192.168.1.177

# 服务网段 (Service CIDR），部署前路由不可达，部署后集群内使用IP:Port可达
SERVICE_CIDR="10.254.0.0/16"

# POD 网段 (Cluster CIDR），部署前路由不可达，**部署后**路由可达(flanneld保证)
CLUSTER_CIDR="172.30.0.0/16"

# 服务端口范围 (NodePort Range)，建议使用高端口
export NODE_PORT_RANGE="30000-50000"

# etcd 集群服务地址列表
export ETCD_ENDPOINTS="https://\${ETCD_0}:2379,https://\${ETCD_1}:2379,https://\${ETCD_2}:2379"

# flanneld 网络配置前缀
export FLANNEL_ETCD_PREFIX="/kubernetes/network"

# kubernetes服务IP 
# 一般是SERVICE_CIDR中第一个IP
export CLUSTER_KUBERNETES_SVC_IP="10.254.0.1"

# 集群 DNS 服务 IP 
# 从 SERVICE_CIDR 中预分配
export CLUSTER_DNS_SVC_IP="10.254.0.2"

# 集群 DNS 域名
export CLUSTER_DNS_DOMAIN="cluster.local."

# 将创建好的文件夹加入环境变量
export PATH=/root/local/bin:\$PATH

# 当前部署的机器名称
# 随便定义，只要能区分不同机器即可
# 例如
# 192.168.1.175的为etcd-host0
# 192.168.1.176的为etcd-host1
# 192.168.1.177的为etcd-host2
export NODE_NAME=etcd-host0

# 当前部署的机器 IP
export NODE_IP=192.168.1.175

# etcd 集群所有机器 IP
export NODE_IPS="192.168.1.175 192.168.1.176 192.168.1.177" 

# etcd 集群各机器名称和对应的IP、端口
export ETCD_NODES=etcd-host0=https://\${ETCD_0}:2380,etcd-host1=https://\${ETCD_1}:2380,etcd-host2=https://\${ETCD_2}:2380
EOF

# 激活配置
source /etc/profile
```

- 添加CA认证文件

``` bash
sudo mkdir -p /etc/kubernetes/ssl
sudo cp ca.pem kubernetes-key.pem kubernetes.pem /etc/kubernetes/ssl
```
	
其中的`ca.pem kubernetes-key.pem kubernetes.pem`，请详细阅读[Security Settings Of K8s](https://o-my-chenjian.com/2017/04/25/Security-Settings-Of-K8s/)

##### 安装ETCD

``` bash
wget https://github.com/coreos/etcd/releases/download/v3.1.6/etcd-v3.1.6-linux-amd64.tar.gz
tar -xvf etcd-v3.1.6-linux-amd64.tar.gz
mkdir /root/local
mkdir /root/local/bin
sudo mv etcd-v3.1.6-linux-amd64/etcd* /root/local/bin
```

##### etcd.service

``` bash
# 创建etcd的工作目录和数据目录
sudo mkdir -p /var/lib/etcd

cat <<EOF > etcd.service
[Unit]
Description=Etcd Server
After=network.target
After=network-online.target
Wants=network-online.target
Documentation=https://github.com/coreos

[Service]
Type=notify
WorkingDirectory=/var/lib/etcd/
ExecStart=/root/local/bin/etcd \\
  --name=${NODE_NAME} \\
  --cert-file=/etc/kubernetes/ssl/kubernetes.pem \\
  --key-file=/etc/kubernetes/ssl/kubernetes-key.pem \\
  --peer-cert-file=/etc/kubernetes/ssl/kubernetes.pem \\
  --peer-key-file=/etc/kubernetes/ssl/kubernetes-key.pem \\
  --trusted-ca-file=/etc/kubernetes/ssl/ca.pem \\
  --peer-trusted-ca-file=/etc/kubernetes/ssl/ca.pem \\
  --initial-advertise-peer-urls=https://${NODE_IP}:2380 \\
  --listen-peer-urls=https://${NODE_IP}:2380 \\
  --listen-client-urls=https://${NODE_IP}:2379,http://127.0.0.1:2379 \\
  --advertise-client-urls=https://${NODE_IP}:2379 \\
  --initial-cluster-token=etcd-cluster-0 \\
  --initial-cluster=${ETCD_NODES} \\
  --initial-cluster-state=new \\
  --data-dir=/var/lib/etcd
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF
```

- 为了保证通信安全，需要指定etcd的公私钥(cert-file和key-file)、Peers通信的公私钥和CA证书(peer-cert-file、peer-key-file、peer-trusted-ca-file)、客户端的CA证书（trusted-ca-file）

- 创建kubernetes.pem证书时使用的`kubernetes-csr.json`文件的hosts字段包含所有 etcd节点的NODE_IP，否则证书校验会出错；
- `--initial-cluster-state`值为new时，`--name`的参数值必须位于`--initial-cluster`列表中；

##### 启动Etcd服务

``` bash
sudo mv etcd.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable etcd
sudo systemctl start etcd
sudo systemctl status etcd

<<'COMMENT'
● etcd.service - Etcd Server
   Loaded: loaded (/etc/systemd/system/etcd.service; enabled; vendor preset: disabled)
   Active: active (running) since Fri 2017-04-21 16:40:31 CST; 4 days ago
     Docs: https://github.com/coreos
 Main PID: 20318 (etcd)
   CGroup: /system.slice/etcd.service
           └─20318 /root/local/bin/etcd --name=etcd-host0 --cert-file=/etc/kubernetes/ssl/kubernetes.pem --key-file=/etc/kubernetes/ssl/kubernetes-key.pem...

Apr 25 16:59:31 192-168-1-175.etcd etcd[20318]: store.index: compact 108673
Apr 25 16:59:31 192-168-1-175.etcd etcd[20318]: finished scheduled compaction at 108673 (took 1.261052ms)
Apr 25 17:03:27 192-168-1-175.etcd etcd[20318]: start to snapshot (applied: 300030, lastsnap: 290029)
Apr 25 17:03:27 192-168-1-175.etcd etcd[20318]: saved snapshot at index 300030
Apr 25 17:03:27 192-168-1-175.etcd etcd[20318]: compacted raft log at 295030
Apr 25 17:03:43 192-168-1-175.etcd etcd[20318]: purged file /var/lib/etcd/member/snap/000000000000018b-000000000003d0a9.snap successfully
Apr 25 17:04:31 192-168-1-175.etcd etcd[20318]: store.index: compact 109010
Apr 25 17:04:31 192-168-1-175.etcd etcd[20318]: finished scheduled compaction at 109010 (took 1.520503ms)
Apr 25 17:09:31 192-168-1-175.etcd etcd[20318]: store.index: compact 109346
Apr 25 17:09:31 192-168-1-175.etcd etcd[20318]: finished scheduled compaction at 109346 (took 2.276838ms)
COMMENT
```

##### 验证Etcd集群可用性

``` bash
# 验证服务
for ip in ${NODE_IPS}; do
	ETCDCTL_API=3 /root/local/bin/etcdctl \
	--endpoints=https://${ip}:2379  \
	--cacert=/etc/kubernetes/ssl/ca.pem \
	--cert=/etc/kubernetes/ssl/kubernetes.pem \
	--key=/etc/kubernetes/ssl/kubernetes-key.pem \
	endpoint health; done

<<'COMMENT'
2017-04-21 16:43:30.876258 I | warning: ignoring ServerName for user-provided CA for backwards compatibility is deprecated
https://192.168.1.175:2379 is healthy: successfully committed proposal: took = 3.004876ms
2017-04-21 16:43:30.975044 I | warning: ignoring ServerName for user-provided CA for backwards compatibility is deprecated
https://192.168.1.176:2379 is healthy: successfully committed proposal: took = 3.826212ms
2017-04-21 16:43:31.075350 I | warning: ignoring ServerName for user-provided CA for backwards compatibility is deprecated
https://192.168.1.177:2379 is healthy: successfully committed proposal: took = 3.955607ms
COMMENT
```

其中的`warning`可以忽视

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/08/Deploy-Etcd-Cluster/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。