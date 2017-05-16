---
layout:     post
title:      "Kubernetes集群之清除集群"
subtitle:   "Clear The Cluster Of K8s"
date:       Thu, May 11 2017 09:47:52 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Clear-The-Cluster-Of-K8s/head_blog.jpg"
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
- [Kubernetes集群之Node节点](https://o-my-chenjian.com/2017/04/26/Deploy-Node-Of-K8s/)
- [带你玩转Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)
- [Kubernetes集群之Kubedns](https://o-my-chenjian.com/2017/04/26/Deploy-Kubedns-Of-K8s/)
- [Kubernetes集群之Dashboard](https://o-my-chenjian.com/2017/04/08/Deploy-Dashboard-With-K8s/)
- [Kubernetes集群之Monitoring](https://o-my-chenjian.com/2017/04/08/Deploy-Monitoring-With-K8s/)
- [Kubernetes集群之Logging](https://o-my-chenjian.com/2017/04/08/Deploy-Logging-With-K8s/)
- [Kubernetes集群之清除集群](https://o-my-chenjian.com/2017/05/11/Clear-The-Cluster-Of-K8s/)

### 清除K8s集群的Etcd集群

操作服务器为：`192.168.1.175／192.168.1.176／192.168.1.177`，即etcd集群的三台服务器。**以下以`192.168.1.175`为例子**。

##### 暂停相关服务

``` sh
sudo systemctl stop etcd
```

##### 清除相关文件

``` sh
# 删除 etcd 的工作目录和数据目录
sudo rm -rf /var/lib/etcd

# 删除etcd.service文件
sudo rm -rf /etc/systemd/system/etcd.service

# 删除程序文件
sudo rm -rf /root/local/bin/etcd

# 删除TLS证书文件
sudo rm -rf /etc/etcd/ssl/*
```

### 清除K8s集群的Master节点

操作服务器IP：`192.168.1.171`，即`K8s-master`

##### 暂停相关服务

``` sh
sudo systemctl stop kube-apiserver kube-controller-manager kube-scheduler flanneld
```

##### 清除相关文件

``` sh
# 删除kube-apiserver工作目录
sudo rm -rf /var/run/kubernetes

# 删除service文件
sudo rm -rf /etc/systemd/system/{kube-apiserver,kube-controller-manager,kube-scheduler,flanneld}.service

# 删除程序文件
sudo rm -rf /root/local/bin/{kube-apiserver,kube-controller-manager,kube-scheduler,flanneld,mk-docker-opts.sh}

# 删除证书文件
sudo rm -rf /etc/flanneld/ssl /etc/kubernetes/ssl

# 删除kubelet缓存
sudo rm -rf ~/.kube/cache ~/.kube/schema
```


### 清除K8s集群的Node节点

操作服务器IP：`192.168.1.173`，即`K8s-node`

##### 暂停相关服务

``` sh
sudo systemctl stop kubelet kube-proxy flanneld docker
```

##### 清除相关文件

``` sh
# umount kubelet 挂载的目录
mount | grep '/var/lib/kubelet'| awk '{print $3}'|xargs sudo umount

# 删除kubelet工作目录
sudo rm -rf /var/lib/kubelet

# 删除docker工作目录
sudo rm -rf /var/lib/docker

# 删除flanneld写入的网络配置文件
sudo rm -rf /var/run/flannel/

# 删除service文件
sudo rm -rf /etc/systemd/system/{kubelet,docker,flanneld}.service

# 删除程序文件
sudo rm -rf /root/local/bin/{kubelet,docker,flanneld,mk-docker-opts.sh}

# 删除证书文件
sudo rm -rf /etc/flanneld/ssl /etc/kubernetes/ssl
```

##### 清除Iptables

``` sh
sudo iptables -F && sudo iptables -X && sudo iptables -F -t nat && sudo iptables -X -t nat
```

##### 清除网桥

``` sh
ip link del flannel.1

ip link del docker0
```

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/05/11/Clear-The-Cluster-Of-K8s/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。