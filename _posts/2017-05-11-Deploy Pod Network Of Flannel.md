---
layout:     post
title:      "Kubernetes集群之Flannel网络"
subtitle:   "Deploy Pod Network Of Flannel"
date:       Thu, May 11 2017 13:36:08 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Pod-Network-Of-Flannel/head_blog.jpg"
catalog:    true
tags:
    - 工作
    - Kubernetes
---

### 系列博文

- [在CentOS7上使用二进制方式部署Kubernetes](https://o-my-chenjian.com/2017/04/25/Deploy-K8s-By-Source-Code-On-CentOS7/)
- [Kubernetes集群之安全设置](https://o-my-chenjian.com/2017/04/25/Security-Settings-Of-K8s/)
- [Kubernetes集群之搭建ETCD集群](https://o-my-chenjian.com/2017/04/08/Deploy-Etcd-Cluster/)
- [Kubernetes集群之创建kubeconfig文件](https://o-my-chenjian.com/2017/04/26/Create-The-File-Of-Kubeconfig-For-K8s/)
- [Kubernetes集群之Flannel网络](https://o-my-chenjian.com/2017/05/11/Deploy-Pod-Network-Of-Flannel/)
- [Kubernetes集群之Master节点](https://o-my-chenjian.com/2017/04/26/Deploy-Master-Of-K8s/)
- [Kubernetes集群之高可用性Master集群](https://o-my-chenjian.com/2017/05/20/Deploy-HA-Master-Clusters-Of-K8s/)
- [Kubernetes集群之Node节点](https://o-my-chenjian.com/2017/04/26/Deploy-Node-Of-K8s/)
- [带你玩转Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)
- [Kubernetes集群之Kubedns](https://o-my-chenjian.com/2017/04/26/Deploy-Kubedns-Of-K8s/)
- [Kubernetes集群之Dashboard](https://o-my-chenjian.com/2017/04/08/Deploy-Dashboard-With-K8s/)
- [Kubernetes集群之Monitoring](https://o-my-chenjian.com/2017/04/08/Deploy-Monitoring-With-K8s/)
- [Kubernetes集群之Logging](https://o-my-chenjian.com/2017/04/08/Deploy-Logging-With-K8s/)
- [Kubernetes集群之清除集群](https://o-my-chenjian.com/2017/05/11/Clear-The-Cluster-Of-K8s/)


### 在Etcd集群中写入Pod网络信息

操作服务器为：`192.168.1.175／192.168.1.176／192.168.1.177`的任意一台，即etcd集群的三台服务器的任意一台即可。

``` bash
ls /etc/flanneld/ssl/
<<'COMMENT'
flanneld-key.pem  flanneld.pem
COMMENT

/root/local/bin/etcdctl \
--endpoints=${ETCD_ENDPOINTS} \
--ca-file=/etc/kubernetes/ssl/ca.pem \
--cert-file=/etc/flanneld/ssl/flanneld.pem \
--key-file=/etc/flanneld/ssl/flanneld-key.pem \
set ${FLANNEL_ETCD_PREFIX}/config '{"Network":"'${CLUSTER_CIDR}'", "SubnetLen": 24, "Backend": {"Type": "vxlan"}}'

<<'COMMENT'
2017-05-11 13:42:17.082810 I | warning: ignoring ServerName for user-provided CA for backwards compatibility is deprecated
{"Network":"172.30.0.0/16", "SubnetLen": 24, "Backend": {"Type": "vxlan"}}
COMMENT
```

该操作只在第一次部署Flannel网络执行，其他节点不用再写入

### 下载Flannel

操作服务器IP：`192.168.1.171`，即`K8s-master`。本次以`master`为例，需要在master和node上都要安装`Flannel网络`

``` bash
mkdir flannel
wget https://github.com/coreos/flannel/releases/download/v0.7.1/flannel-v0.7.1-linux-amd64.tar.gz
tar -xzvf flannel-v0.7.1-linux-amd64.tar.gz -C flannel
sudo cp flannel/{flanneld,mk-docker-opts.sh} /root/local/bin
```
所有资源可以在[这里](https://pan.baidu.com/s/1pLhmqzL)进行下载

##### flanneld.service

``` bash
cat > flanneld.service <<EOF
[Unit]
Description=Flanneld overlay address etcd agent
After=network.target
After=network-online.target
Wants=network-online.target
After=etcd.service
Before=docker.service

[Service]
Type=notify
ExecStart=/root/local/bin/flanneld \\
  -etcd-cafile=/etc/kubernetes/ssl/ca.pem \\
  -etcd-certfile=/etc/flanneld/ssl/flanneld.pem \\
  -etcd-keyfile=/etc/flanneld/ssl/flanneld-key.pem \\
  -etcd-endpoints=${ETCD_ENDPOINTS} \\
  -etcd-prefix=${FLANNEL_ETCD_PREFIX} \\
  $FLANNEL_OPTIONS
ExecStartPost=/root/local/bin/mk-docker-opts.sh -k DOCKER_NETWORK_OPTIONS -d /run/flannel/docker
Restart=on-failure

[Install]
WantedBy=multi-user.target
RequiredBy=docker.service
EOF
```

- etcd集群启用了双向TLS认证，需要为flanneld指定与etcd集群通信的CA和秘钥

- mk-docker-opts.sh脚本将分配给flanneld的Pod子网网段信息写入到`/run/flannel/docker`文件中，后续docker启动时使用这个文件中参数值设置`docker0`网桥

- `-iface`选项值指定flanneld和其它Node通信的接口，如果机器有内、外网，则最好指定为内网接口

##### 启动Flannel

``` bash
# 启动 flannelds
sudo cp flanneld.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable flanneld

<<'COMMENT'
Created symlink from /etc/systemd/system/multi-user.target.wants/flanneld.service to /etc/systemd/system/flanneld.service.
Created symlink from /etc/systemd/system/docker.service.requires/flanneld.service to /etc/systemd/system/flanneld.service.
COMMENT

sudo systemctl start flanneld
sudo systemctl status flanneld

<<'COMMENT'
● flanneld.service - Flanneld overlay address etcd agent
   Loaded: loaded (/etc/systemd/system/flanneld.service; enabled; vendor preset: disabled)
   Active: active (running) since Thu 2017-05-11 13:54:34 CST; 3s ago
  Process: 4946 ExecStartPost=/root/local/bin/mk-docker-opts.sh -k DOCKER_NETWORK_OPTIONS -d /run/flannel/docker (code=exited, status=0/SUCCESS)
 Main PID: 4938 (flanneld)
   CGroup: /system.slice/flanneld.service
           └─4938 /root/local/bin/flanneld -etcd-cafile=/etc/kubernetes/ssl/ca.pem -etcd-certfile=/etc/flanneld/ssl/flanneld.pem -etcd-keyfile=/etc/flan...

May 11 13:54:33 192-168-1-171.master systemd[1]: Starting Flanneld overlay address etcd agent...
May 11 13:54:34 192-168-1-171.master flanneld[4938]: warning: ignoring ServerName for user-provided CA for backwards compatibility is deprecated
May 11 13:54:34 192-168-1-171.master flanneld[4938]: I0511 13:54:34.030738    4938 main.go:132] Installing signal handlers
May 11 13:54:34 192-168-1-171.master flanneld[4938]: I0511 13:54:34.033839    4938 manager.go:149] Using interface with name ens160 and address ...68.1.171
May 11 13:54:34 192-168-1-171.master flanneld[4938]: I0511 13:54:34.033937    4938 manager.go:166] Defaulting external address to interface addr...8.1.171)
May 11 13:54:34 192-168-1-171.master flanneld[4938]: I0511 13:54:34.114080    4938 local_manager.go:179] Picking subnet in range 172.30.1.0 ... ...30.255.0
May 11 13:54:34 192-168-1-171.master flanneld[4938]: I0511 13:54:34.118711    4938 manager.go:250] Lease acquired: 172.30.87.0/24
May 11 13:54:34 192-168-1-171.master flanneld[4938]: I0511 13:54:34.119706    4938 network.go:58] Watching for L3 misses
May 11 13:54:34 192-168-1-171.master flanneld[4938]: I0511 13:54:34.119739    4938 network.go:66] Watching for new subnet leases
May 11 13:54:34 192-168-1-171.master systemd[1]: Started Flanneld overlay address etcd agent.
Hint: Some lines were ellipsized, use -l to show in full.
COMMENT
```

### 检查flanneld服务

``` bash
# 检查 flanneld 服务
journalctl  -u flanneld |grep 'Lease acquired'
<<'COMMENT'
AMay 11 13:54:34 192-168-1-171.master flanneld[4938]: I0511 13:54:34.118711    4938 manager.go:250] Lease acquired: 172.30.87.0/24
COMMENT

ifconfig flannel.1
<<'COMMENT'
flannel.1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1450
        inet 172.30.1.0  netmask 255.255.255.255  broadcast 0.0.0.0
        ether 3e:27:de:39:f1:1a  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 2 overruns 0  carrier 0  collisions 0
COMMENT
```

##### 检查分配给各flannel的Pod网段信息

操作服务器为：`192.168.1.175／192.168.1.176／192.168.1.177`的任意一台，即etcd集群的三台服务器的任意一台即可。

``` bash
# 检查分配给各 flanneld 的 Pod 网段信息
/root/local/bin/etcdctl \
--endpoints=${ETCD_ENDPOINTS} \
--ca-file=/etc/kubernetes/ssl/ca.pem \
--cert-file=/etc/flanneld/ssl/flanneld.pem \
--key-file=/etc/flanneld/ssl/flanneld-key.pem \
get ${FLANNEL_ETCD_PREFIX}/config

<<'COMMENT'
2017-05-11 13:59:47.686607 I | warning: ignoring ServerName for user-provided CA for backwards compatibility is deprecated
{"Network":"172.30.0.0/16", "SubnetLen": 24, "Backend": {"Type": "vxlan"}}
COMMENT


# 查看已分配的 Pod 子网段列表(/24)
/root/local/bin/etcdctl \
--endpoints=${ETCD_ENDPOINTS} \
--ca-file=/etc/kubernetes/ssl/ca.pem \
--cert-file=/etc/flanneld/ssl/flanneld.pem \
--key-file=/etc/flanneld/ssl/flanneld-key.pem \
ls ${FLANNEL_ETCD_PREFIX}/subnets

<<'COMMENT'
2017-05-11 14:00:17.969753 I | warning: ignoring ServerName for user-provided CA for backwards compatibility is deprecated
/kubernetes/network/subnets/172.30.87.0-24
COMMENT

# 查看某一 Pod 网段对应的 flanneld 进程监听的 IP 和网络参数
/root/local/bin/etcdctl \
--endpoints=${ETCD_ENDPOINTS} \
--ca-file=/etc/kubernetes/ssl/ca.pem \
--cert-file=/etc/flanneld/ssl/flanneld.pem \
--key-file=/etc/flanneld/ssl/flanneld-key.pem \
get ${FLANNEL_ETCD_PREFIX}/subnets/172.30.87.0-24

<<'COMMENT'
2017-05-11 14:00:58.398312 I | warning: ignoring ServerName for user-provided CA for backwards compatibility is deprecated
{"PublicIP":"192.168.1.171","BackendType":"vxlan","BackendData":{"VtepMAC":"3e:27:de:39:f1:1a"}}
COMMENT
```

### 确保各节点间Pod网段能互联互通

当master和所有node节点的Flannel网络部署完成后

操作服务器为：`192.168.1.175／192.168.1.176／192.168.1.177`的任意一台，即etcd集群的三台服务器的任意一台即可。

``` sh
/root/local/bin/etcdctl --endpoints=${ETCD_ENDPOINTS} --ca-file=/etc/kubernetes/ssl/ca.pem --cert-file=/etc/flanneld/ssl/flanneld.pem --key-file=/etc/flanneld/ssl/flanneld-key.pem ls ${FLANNEL_ETCD_PREFIX}/subnets

<<'COMMENT'
2017-05-11 14:45:44.819055 I | warning: ignoring ServerName for user-provided CA for backwards compatibility is deprecated
/kubernetes/network/subnets/172.30.87.0-24
/kubernetes/network/subnets/172.30.81.0-24
COMMENT
```

当前所有节点的Pod网段分别为：172.30.87.0-24，172.30.81.0-24


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/05/11/Deploy-Pod-Network-Of-Flannel/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。