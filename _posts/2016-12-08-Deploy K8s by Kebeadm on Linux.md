---
layout:     post
title:      "Deploy K8s by Kebeadm on Linux"
subtitle:   "There were they in great fear:
for God is in the generation of the righteous. Psa 14:5"
date:       Thu, Dec 8 2016 17:55:56 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-K8s-by-Kebeadm-on-Linux/head_blog.jpg"
tags:
    - 工作
    - kubernetes
---

### 系统环境与IP

* 系统环境： 

	- 之前使用ubuntu16.04.1-desktop-amd64, 使用清华的源

	- 随后使用centos7(推荐)

* 集群信息：

	|  Node |     IP       |
	|:-----:|:------------:|
	| Master | 192.168.1.167|
	| Node | 192.168.1.168|
	| Node | 192.168.1.169|
	

>*整个环境在VM下完成，可用master克隆出两个子机*

>**注意VM的网络设置。发现只有weave网络能在虚拟机中使用，但是flannel，calico和weave均能在物理机上使用，即DNS解析没有问题**

> **以下开始的所有操作，在192.168.1.167单点中的root权限下操作**

### CentOS7系统备份与还原

> 备份：

``` sh
# sudo su

# cd /

# tar cvpzf backup.tgz --exclude=/proc --exclude=/backup.tgz --exclude=/mnt --exclude=/sys /
# 或者
# tar cvpjf backup.tar.bz2 --exclude=/proc --exclude=/backup.tar.bz2 --exclude=/mnt --exclude=/sys /
```

> 系统恢复：

``` sh
# tar xvpfz backup.tgz -C /
# 或者
# tar xvpfj backup.tar.bz2 -C /

# mkdir proc
# mkdir lost+found
# mkdir mnt
# mkdir sys
```

### 部分软件安装

> Ubuntu16.04

- 安装VIM： `sudo apt-get install vim -y`
	
- 安装SSH：`sudo apt-get install openssh-server`
	
	- 启动SSH：`sudo service ssh start`
	
- 安装GIT： `sudo apt-get install git -y`

> CentOS7

- `sudo yum update`

- 关闭firewalls等:

``` sh
# systemctl disable firewalld

# systemctl stop firewalld

# yum install -y ebtables

# setenforce是Linux的selinux防火墙配置命令 执行setenforce 0 表示关闭selinux防火墙。
# setenforce 0
```

centos7以firewalld代替iptables，我们可以关闭自带的firewalld，启动iptables

``` sh
# sudo yum install -y iptables

# sudo yum update iptables

# sudo yum install -y iptables-services
```

### DOCKER安装与设置

> Ubuntu16.04

```sh
# wget -qO- https://get.docker.com/ | sh

administrator@administrator167:~$ docker -v
Docker version 1.12.3, build 6b644ec
```

> CentOS7

所需的两个docker的rpm文件的链接：[kubeadm-rpm](https://pan.baidu.com/s/1pLrrlCR)

然后，`sudo yum install * -y`

链接docker私有库：

- 解决https问题
	
	- 用于ubuntu16.04，docker1.12：`echo { \"insecure-registries\":[\"10.0.0.153:5000\"] } > /etc/docker/daemon.json`
	
	- 用于Centos7, docker1.10:`echo "INSECURE_REGISTRY='--insecure-registry 10.0.0.153:5000'" >> /etc/sysconfig/docker`
	
	- 用于Centos7，docker1.12：

```sh
# sudo vim /usr/lib/systemd/system/docker.service

#ExecStart=/usr/bin/dockerd 
ExecStart=/usr/bin/dockerd --insecure-registry 10.0.0.153:5000
```

- 解决docker的容器数量限制

``` sh
# sudo mkdir -p /etc/systemd/system/docker.service.d/

# sudo tee /etc/systemd/system/docker.service.d/tasksmax.conf <<-'EOF'
[Service]
TasksMax=infinity
EOF
```

岂是在`/usr/lib/systemd/system/docker.service`中有被注释掉的`#TasksMax=infinity`，可将其注释去掉

- 重启docker服务：

	- Ubuntu14.04: `sudo service docker restart`

	- Ubuntu16.04: `sudo systemctl restart docker`

	- Centos7： 

```
# sudo systemctl stop docker

# sudo systemctl daemon-reload 

# sudo systemctl enable docker

# sudo systemctl start docker
```

- 更换镜像的tag：`docker tag 40a673399858 192.168.1.78:5000/docker-whale`

- 上传镜像： `docker push 10.0.0.153:5000/docker-whale`

- 下载镜像： `docker pull 10.0.0.153:5000/docker-whale`

- 浏览器输入：

``` sh
# curl http://192.168.1.78:5000/v2/_catalog
	
{"repositories":["addon-resizer","docker-whale","grafana","heapster","influxdb","kube-ui","kube_test","kubedns-amd64","kubernetes-dashboard-amd64","llll","pause","test_docker"]}
```

- 查询镜像tag： 

``` sh
# curl http://192.168.1.78:5000/v2/heapster/tags/list
	
"name":"heapster","tags":["v1","canary","latest"]}
```

**建立私有仓库，不仅能保护docker的安全性，有助于下载与上传，同时对于使用kubernets更加方便**

### 安装kubernets之前的准备

#### 搭建Etcd集群

Etcd集群对整个k8s集群非常重要，需要抽出搭建。**当时kubeadm不支持高可用性，及不支持etcd集群**

> 搭建环境：**CentOS7**
> 
> 
|  Node |     IP       |
|:-----:|:------------:|
| etcd0 | 192.168.1.157|
| etcd1 | 192.168.1.158|
| etcd2 | 192.168.1.159|

- 关闭防火墙

```sh
# systemctl stop firewalld

# systemctl disable firewalld
```


- 安装命令：

```sh
# yum install etcd -y
```


```sh
# etcd --version

etcd Version: 2.3.7
Git SHA: fd17c91
Go Version: go1.6.3
Go OS/Arch: linux/amd64
```

- 修改etcd配置

默认文件位于`/etc/etcd/etcd.conf`

```sh
# rm -rf /etc/etcd/etcd.conf

# sudo cat <<EOF |  sudo tee /etc/etcd/etcd.conf
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

```sh
# sudo cat <<EOF |  sudo tee /lib/systemd/system/etcd.service
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

```sh
# sudo systemctl stop etcd

# sudo systemctl daemon-reload 

# sudo systemctl enable etcd

# sudo systemctl start etcd

# sudo systemctl status etcd
```

- 查看etcd的启动参数

```sh
# ps aux|grep etcd

etcd     16010  1.3  1.1  49112 20728 ?        Ssl  10:18   2:30 /usr/bin/etcd --name=etcd0 --data-dir=/var/lib/etcd/etcd0 --listen-client-urls=http://0.0.0.0:2379,http://0.0.0.0:4001 --advertise-client-urls=http://192.168.1.157:2379,http://192.168.1.157:4001 --initial-cluster-token=etcd-cluster --initial-cluster=etcd0=http://192.168.1.157:2380,etcd1=http://192.168.1.158:2380,etcd2=http://192.168.1.159:2380 --initial-cluster-state=new
root     18440  0.0  0.0 112652   956 pts/0    S+   13:28   0:00 grep --color=auto etcd
```

- 查看etcd集群的节点信息

```sh
# etcdctl member list

5a2567911e869c1: name=etcd1 peerURLs=http://192.168.1.158:2380 clientURLs=http://192.168.1.158:2379,http://192.168.1.158:4001 isLeader=true
588d5e8d3a8648b5: name=etcd2 peerURLs=http://192.168.1.159:2380 clientURLs=http://192.168.1.159:2379,http://192.168.1.159:4001 isLeader=false
bd2d658f033f9bcc: name=etcd0 peerURLs=http://192.168.1.157:2380 clientURLs=http://192.168.1.157:2379,http://192.168.1.157:4001 isLeader=false
```

- 查看etcd集群的健康情况

```sh
# etcdctl cluster-health

member 5a2567911e869c1 is healthy: got healthy result from http://192.168.1.158:2379
member 588d5e8d3a8648b5 is healthy: got healthy result from http://192.168.1.159:2379
member bd2d658f033f9bcc is healthy: got healthy result from http://192.168.1.157:2379
cluster is healthy
```


#### 修改Linux主机名

> Ubuntu16.04

由于在VM下进行master的克隆，则需要对新子机进行重新修改主机名：

- `sudo vim /etc/hostname`修改为想要的

``` sh
192-168-1-167.master
```

- `sudo vim /etc/hosts`，改第二行`127.0.1.1 administrator167`

```sh
127.0.0.1       localhost
127.0.1.1       192-168-1-167.master

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

- 重启计算机即可：`sudo reboot`

> CentOS7

``` sh
# ipname=192-168-1-167

# nodetype=master

# echo "${ipname}.${nodetype}" > /etc/hostname

# echo "127.0.0.1   ${ipname}.${nodetype}" >> /etc/hosts

# sysctl kernel.hostname=${ipname}.${nodetype}
```

#### 制作kubelet kubeadm kubectl kubernetes-cni

> Ubuntu16.04

由于网络缘故，无法直接像官网中的操作中直接`apt-get install`，所以需要自己制作所需的安装包。

查看自己的系统信息：

```sh
# lsb_release -a

No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 16.04.1 LTS
Release:        16.04
Codename:       xenial
```
需要从[kubernetes/release](https://github.com/kubernetes/release)中间开始制作：

1. `git clone https://github.com/chenjian158978/release.git`

2. `cd release`

3. `docker build --tag=debian-packager debian` 

4. `docker run --volume="$(pwd)/debian:/src" debian-packager`

> 其中第3，4步要等好长时间，然后在`debian/bin`中找`xenial`文件夹。

**目前来说，第四步失败，报错为无法访问国外的网站，与漠大神的交流中感觉还是需要个梯子**，制作四个deb文件就是为了安装，所以通过梯子，很快的安装好了。

1. 在ubuntu16.04上安装L2TP，详见文献参考；

2. 登上梯子，这个不叙述;

3. `curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -`

4. `cat <<EOF > /etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF`

5. `apt-get update`

6. `apt-get install -y kubelet kubeadm kubectl kubernetes-cni`

> 相关下载的deb文件可以从[这里](https://pan.baidu.com/s/1jHChOtK)下载，然后通过`sudo dpkg -i *`即可安装完毕

> 为避免再次下载这些deb文件，可以将其保存，其中`apt install`的包位置如下：

```sh
# ll /var/cache/apt/archives/kube*.deb

-rw-r--r-- 1 root root 12165700 12月  8 20:49 /var/cache/apt/archives/kubeadm_1.5.0-alpha.2-421-a6bea3d79b8bba-00_amd64.deb
-rw-r--r-- 1 root root 10292542 12月  8 20:44 /var/cache/apt/archives/kubectl_1.4.4-00_amd64.deb
-rw-r--r-- 1 root root 15701146 12月  8 20:37 /var/cache/apt/archives/kubelet_1.4.4-01_amd64.deb
-rw-r--r-- 1 root root  6873078 12月  8 20:32 /var/cache/apt/archives/kubernetes-cni_0.3.0.1-07a8a2-00_amd64.deb
```

> CentOS7

吸取了在ubuntu系统上的教训，直接通过梯子获得四个rpm的安装文件，相关链接为[kubeadm-rpm](https://pan.baidu.com/s/1o8vxbGQ)，通过命令`sudo yum install * -y`即可安装完。

启动kubelet服务：

``` sh
# systemctl enable kubelet && systemctl start kubelet
```


#### 下载kubeadm需要的镜像

|images name | version |
|:----------:|:-------:|
|gcr.io/google_containers/kube-discovery-amd64|1.0|
|gcr.io/google_containers/kube-proxy-amd64|v1.5.1|
|gcr.io/google_containers/kube-scheduler-amd64|v1.5.1|
|gcr.io/google_containers/kube-controller-manager-amd64|v1.5.1|
|gcr.io/google_containers/kube-apiserver-amd64|v1.5.1|
|gcr.io/google_containers/etcd-amd64|3.0.14-kubeadm|
|gcr.io/google_containers/pause-amd64|3.0|
|gcr.io/google_containers/kubedns-amd64|1.9|
|gcr.io/google_containers/kube-dnsmasq-amd64|1.4|
|gcr.io/google_containers/exechealthz-amd64|1.2|
|gcr.io/google_containers/kubernetes-dadashboard-amd64|v1.5.0|
|gcr.io/google_containers/heapster\_grafana|v3.1.1|
|kubernetes/heapster|canary|
|kubernetes/heapster_influxdb|v0.6|
|gcr.io/google_containers/fluentd-elasticsearch|1.20|
|gcr.io/google_containers/elasticsearch|v2.4.1|
|gcr.io/google_containers/kibana|v4.6.1|

1. 这些images可以在漠然大神的[dockerhub](https://hub.docker.com/u/mritd/)上pull,需要注意tag问题，需要什么版本，拉什么tag。然后push到私有库上。
2. 同时，可以从[这里](https://pan.baidu.com/s/1jHChOtK)下载对应镜像的tar文件

查看私有库文件：

```sh
# curl http://10.0.0.153:5000/v2/_catalog
	
{"repositories":["kube-apiserver-amd64","exechealthz-amd64","etcd-amd64","kube-controller-manager-amd64","kube-discovery-amd64","kube-dnsmasq-amd64","kube-proxy-amd64","kube-scheduler-amd64","kubedns-amd64","pause-amd64"]}
```

- 批量准备所需镜像

```sh
# images=(kube-discovery-amd64:1.0 kube-proxy-amd64:v1.5.1 kube-scheduler-amd64:v1.5.1 kube-controller-manager-amd64:v1.5.1 kube-apiserver-amd64:v1.5.1 etcd-amd64:3.0.14-kubeadm pause-amd64:3.0 kubedns-amd64:1.9 kube-dnsmasq-amd64:1.4 exechealthz-amd64:1.2 dnsmasq-metrics-amd64:1.0)
for image in ${images[@]}; do
	docker pull 10.0.0.153:5000/k8s/$image
	docker tag 10.0.0.153:5000/k8s/$image gcr.io/google_containers/$image
	docker rmi 10.0.0.153:5000/k8s/$image
done
```

### kubeadm初始化

```sh
# kubeadm init --api-advertise-addresses 192.168.1.167  --use-kubernetes-version v1.5.1 --pod-network-cidr 10.244.0.0/16 --external-etcd-endpoints http://192.168.1.157:2379,http://192.168.1.158:2379,http://192.168.1.159:2379

Flag --external-etcd-endpoints has been deprecated, this flag will be removed when componentconfig exists
[kubeadm] WARNING: kubeadm is in alpha, please do not use it for production clusters.
[preflight] Running pre-flight checks
[preflight] Starting the kubelet service
[init] Using Kubernetes version: v1.5.1
[tokens] Generated token: "b54b79.c8c5e44532a817ff"
[certificates] Generated Certificate Authority key and certificate.
[certificates] Generated API Server key and certificate
[certificates] Generated Service Account signing keys
[certificates] Created keys and certificates in "/etc/kubernetes/pki"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/kubelet.conf"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/admin.conf"
[apiclient] Created API client, waiting for the control plane to become ready
[apiclient] All control plane components are healthy after 16.880375 seconds
[apiclient] Waiting for at least one node to register and become ready
[apiclient] First node is ready after 5.526103 seconds
[apiclient] Creating a test deployment
[apiclient] Test deployment succeeded
[token-discovery] Created the kube-discovery deployment, waiting for it to become ready
[token-discovery] kube-discovery is ready after 680.505062 seconds
[addons] Created essential addon: kube-proxy
[addons] Created essential addon: kube-dns

Your Kubernetes master has initialized successfully!

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
    http://kubernetes.io/docs/admin/addons/

You can now join any number of machines by running the following on each node:

kubeadm join --token=b54b79.c8c5e44532a817ff 192.168.1.167
```

- 记住token的值，这个在后续需要。如果你丢失了，可使用以下命令：

```sh
# kubectl -n kube-system get secret clusterinfo -o yaml | grep token-map | awk '{print $2}' | base64 -d | sed "s|{||g;s|}||g;s|:|.|g;s/\"//g;" | xargs echo
```

- 如果init失败，下一次开始前输入：
	
``` sh
# kubeadm reset

# docker rm `docker ps -a -q`

# find /var/lib/kubelet | xargs -n 1 findmnt -n -t tmpfs -o TARGET -T | uniq | xargs -r umount -v

# rm -r -f /etc/kubernetes /var/lib/kubelet /var/lib/etcd
``` 
	
- `--api-advertise-addresses 192.168.1.167`设置指定的网络接口

- `--use-kubernetes-version v1.4.6`设置k8s的版本

- `--pod-network-cidr 10.244.0.0/16`设置指定的网段(Flannel需要)

- `--external-etcd-endpoints http://192.168.1.157:2379,http://192.168.1.158:2379,http://192.168.1.159:2379`设置外部的etcd集群.**目前使用kubeadm不支持HA，即etcd集群，只支持单节点的etcd**

### pod网络创建

**网络方式有多种选择。如果k8s集群建在虚拟机中，可以使用weave（较为稳定），或者flannel（有部分问题）；如果k8s集群创建在实体机中，建议是用calico（最好的选择）**

采用*Flannel*：

`kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml`

这里会pull镜像quay.io/coreos/flannel-git:v0.6.1-28-g5dde68d-amd64，其托管在quay.io上，不需要梯子

但尽量先pull好镜像,并且整理好经常使用的yaml文件，可以节省时间。


### 查看集群状态

```sh
kubectl get pods --all-namespaces -o wide
```

> **但状态均为Running，到此，单节点的k8s集群已经搭建完成**

### 添加节点

#### 说明

1. 添加节点`192.168.1.168`的虚拟机，直接克隆`192.168.1.167`，然后改IP；

2. 修改主机名，详细见上文；

3. 停止克隆的集群服务

	3.1 `kubeadm reset`
	
	3.2 `systemctl start kubelet.service`
	
	3.3 `` docker rm `docker ps -a -q` ``

4. 重启`167`机器后发现：

```sh 
root@administrator167:/home/administrator# kubectl get pods --all-namespaces
	
The connection to the server localhost:8080 was refused - did you specify the right host or port?
```

这时候，重启一下机器
	
#### kubeadm join

在`192.168.1.168`上操作：

```sh
kubeadm join --token=e3b02c.5c85004416c2370c 192.168.1.167

Running pre-flight checks
<util/tokens> validating provided token
<node/discovery> created cluster info discovery client, requesting info from "http://192.168.1.167:9898/cluster-info/v1/?token-id=e3b02c"
<node/discovery> cluster info object received, verifying signature using given token
<node/discovery> cluster info signature and contents are valid, will use API endpoints [https://192.168.1.167:6443]
<node/bootstrap> trying to connect to endpoint https://192.168.1.167:6443
<node/bootstrap> detected server version v1.4.6
<node/bootstrap> successfully established connection with endpoint https://192.168.1.167:6443
<node/csr> created API client to obtain unique certificate for this node, generating keys and certificate signing request
<node/csr> received signed certificate from the API server:
Issuer: CN=kubernetes | Subject: CN=system:node:administrator168 | CA: false
Not before: 2016-12-10 05:53:00 +0000 UTC Not After: 2017-12-10 05:53:00 +0000 UTC
<node/csr> generating kubelet configuration
<util/kubeconfig> created "/etc/kubernetes/kubelet.conf"

Node join complete:
* Certificate signing request sent to master and response
  received.
* Kubelet informed of new secure connection details.

Run 'kubectl get nodes' on the master to see this machine join.
```

### Kubectl的基本命令

> 查看集群信息

``` sh
# kubectl cluster-info
```  

> 查看集群节点信息

``` sh
# kubectl get nodes --show-labels
```

> 描述某个节点的信息

``` sh
# kubectl describe node 10-0-0-171.node
```

> 查询全部pod信息

``` sh
# kubectl get pods -o wide --all-namespaces
```

> 查看全部svc信息

``` sh
# kubectl get svc --all-namespaces -o wide
```

> 查看全部deployments信息

``` sh
# kubectl get deployments --all-namespaces
```

> 查看全部ingress信息

``` sh
# kubectl get ingresses --all-namespaces
```

> 查看全部secret信息

``` sh
# kubectl get secret --all-namespaces
```

> 查看某pod的yaml文件内容

``` sh
# kubectl get pod weave-net-xhh0h --namespace=kube-system -o yaml
```

> 描述某pod的运行状态

``` sh
# kubectl describe pod calico-etcd --namespace=kube-system
```

> 描述某svc的运行状态

``` sh
# kubectl describe svc kube-dns --namespace=kube-system
```

> 描述某deployments的运行状态

``` sh
# kubectl describe deployments sitealive --namespace=wmcluster2016
```

> 删除某pod

``` sh
# kubectl delete pod sitealive-3553544168-q4gtx --namespace=wmcluster2016
```

> 查询某pod的log

``` sh
# kubectl logs proxycrawler-2347617609-mwzts --namespace=wmcluster2016
```

> 进去某pod的容器

``` sh
# kubectl exec -it busybox -- sh

# ubuntu系统
# kubectl exec -it ubuntu-system -- /bin/bash
```

> 在某pod的容器中执行一段命令

``` sh
# kubectl exec -it busybox -- nslookup kubernetes.default
```

> 更新某deployments的replicas

``` sh
# kubectl scale deployments sitealive --namespace=cluster2016 --replicas=25
```

> 为某个node添加tag

``` sh
# kubectl label nodes administrator167 master=heapster-master
```

> 添加namespace

``` sh
# kubectl create namespace cludfdfdf20d
```

### Dashboard部署

- 下载yaml文件

`https://rawgit.com/kubernetes/dadashboard/master/src/deploy/kubernetes-dashboard.yaml`
	
- 将镜像`gcr.io/google_containers/kubernetes-dadashboard-amd64:v1.5.0`放进私有库中

- 修改yaml文件

	1. 去掉`imagePullPolicy: Always`,在[漠大神的博客](https://mritd.me/2016/10/29/set-up-kubernetes-cluster-by-kubeadm/#section-6)中将值改为IfNotPresent或者Never，但是仍然出错；
	
	2. image地址改为`192.168.1.78:5000/kubernetes-dashboard-amd64:v1.5.0`

- 部署

```sh
# kubectl create -f kubernetes-dashboard.yaml
	
deployment "kubernetes-dashboard" created
service "kubernetes-dashboard" created
```

- 查看deployments

```sh
# kubectl get deployment --all-namespaces
	
NAMESPACE     NAME                   DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
kube-system   kube-discovery         1         1         1            1           22h
kube-system   kube-dns               1         1         1            1           22h
kube-system   kubernetes-dashboard   1         1         1            1           30m
```

	
- 查看service

```sh
# kubectl get service --all-namespaces
	
NAMESPACE     NAME                   CLUSTER-IP     EXTERNAL-IP   PORT(S)         AGE
default       kubernetes             10.96.0.1      <none>        443/TCP         23h
kube-system   kube-dns               10.96.0.10     <none>        53/UDP,53/TCP   23h
kube-system   kubernetes-dashboard   10.101.241.6   <nodes>       80/TCP          34m
```
	
- 查看dashboard的端口

```sh
# kubectl describe svc kubernetes-dashboard --namespace kube-system
	
Name:                   kubernetes-dashboard
Namespace:              kube-system
Labels:                 app=kubernetes-dashboard
Selector:               app=kubernetes-dashboard
Type:                   NodePort
IP:                     10.101.241.6
Port:                   <unset> 80/TCP
NodePort:               <unset> 32688/TCP
Endpoints:              10.244.1.14:9090
Session Affinity:       None	
```

从中可以看出其类型为NodePort,端口为32688;或者可将该端口固定住。

- 访问dashboard
浏览器中输入：`http://192.168.1.168:32688/`即可

- 删除部署

```sh
# kubectl delete -f kubernetes-dashboard.yaml
	
deployment "kubernetes-dashboard" deleted
service "kubernetes-dashboard" deleted
```

- 查询Linux暴露出来的端口

``` sh
# netstat -tnlp
```

### Monitoring部署

> 采用Grafana+Heapster+Influxdb

- 下载yaml文件

`git clone https://github.com/kubernetes/heapster.git`
	
- 将镜像`gcr.io/google_containers/heapster_grafana:v3.1.1`,`kubernetes/heapster:canary`,`kubernetes/heapster_influxdb:v0.6`放进私有库中

- 修改yaml文件

	* 在`/home/administrator/heapster/deploy/kube-config/influxdb`下6个文件，将image地址分别改为:
	
	`192.168.1.78:5000/grafana:v3.1.1`
	`192.168.1.78:5000/heapster:canary`
	`192.168.1.78:5000/influxdb:v0.6`
	
	* 在`influxdb-service.yaml`文件中，修改成：
	
```sh
...
spec:
	type: NodePort
	ports:
	   - name: http
        port: 8083
        targetPort: 8083
      - name: api
        port: 8086
        targetPort: 8086
		selector:
        k8s-app: influxdb
```
	
暴露出influxdb的8083端口，注意yaml的文件格式，以及不要用tab键

- 部署

```sh
pwd
	
/home/administrator/heapster/deploy/kube-config/influxdb
	
kubectl create -f .
	
deployment "monitoring-grafana" created
service "monitoring-grafana" created
deployment "heapster" created
service "heapster" created
deployment "monitoring-influxdb" created
service "monitoring-influxdb" created
```
	
- 查看pod状态，确定均为`running`，失败的用`describe`来查看问题

- 查看grafana的端口

```sh
kubectl describe svc monitoring-grafana --namespace kube-system
	
Name:                   monitoring-grafana
Namespace:              kube-system
Labels:                 kubernetes.io/cluster-service=true
                    kubernetes.io/name=monitoring-grafana
Selector:               k8s-app=grafana
Type:                   NodePort
IP:                     10.96.33.128
Port:                   <unset> 80/TCP
NodePort:               <unset> 32735/TCP
Endpoints:              10.244.1.18:3000
Session Affinity:       None
```

通过`192.168.1.168:32735`进入grafana，进去后即可发现influxdb数据库已经链接好

或者查看数据库通过：
	
```sh
curl http://192.168.1.168:32735/api/datasources/proxy/1/query?db=k8s&q=SHOW%20DATABASES&epoch=ms
	
{"results":[{"series":[{"name":"databases","columns":["name"],"values":[["_internal"],["k8s"]]}]}]}
```
	
- 通过`http://192.168.1.167:4194`，`节点IP：4194`进入cAdvisor

- 查看influxdb的端口

```sh
kubectl describe svc monitoring-influxdb --namespace kube-system
	
Name:                   monitoring-influxdb
Namespace:              kube-system
Labels:                 kubernetes.io/cluster-service=true
                    kubernetes.io/name=monitoring-influxdb
                    task=monitoring
Selector:               k8s-app=influxdb
Type:                   NodePort
IP:                     10.110.51.194
Port:                   http    8083/TCP
NodePort:               http    32552/TCP
Endpoints:              10.244.1.23:8083
Port:                   api     8086/TCP
NodePort:               api     30758/TCP
Endpoints:              10.244.1.23:8086
Session Affinity:       None
```
	
其中，通过`http://192.168.1.168:32552/`进入influxdb的UI端口，在设置中，填写`192.168.1.168:30758`完成设置

- 具体设置，可阅读相关资料，例如[storage-schema](https://github.com/kubernetes/heapster/blob/master/docs/storage-schema.md)

#### 添加邮件

含有告警(Altering)功能，需要Grafana的版本在4.0之上，并且需要在启动脚本(run.sh)中添加一些参数

- run.sh

``` sh
#!/bin/sh

: "${GF_PATHS_DATA:=/var/lib/grafana}"
: "${GF_PATHS_LOGS:=/var/log/grafana}"
: "${GF_SMTP_ENABLED:=true}"
: "${GF_SMTP_HOST:=smtp.163.com:25}"
: "${GF_SMTP_USER:=qgssoft@163.com}"
: "${GF_SMTP_PASSWORD:=qwer1234}"
: "${GF_SMTP_SKIP_VERIFY:=true}"
: "${GF_SMTP_FROM_ADDRESS:=qgssoft@163.com}"

# Allow access to dashboards without having to log in
# Export these variables so grafana picks them up
export GF_AUTH_ANONYMOUS_ENABLED=${GF_AUTH_ANONYMOUS_ENABLED:-true}
export GF_SERVER_HTTP_PORT=${GRAFANA_PORT}
export GF_SERVER_PROTOCOL=${GF_SERVER_PROTOCOL:-http}

echo "Starting a utility program that will configure Grafana"
setup_grafana >/dev/stdout 2>/dev/stderr &

echo "Starting Grafana in foreground mode"
exec /usr/sbin/grafana-server \
  --homepath=/usr/share/grafana \
  --config=/etc/grafana/grafana.ini \
  cfg:default.paths.data="$GF_PATHS_DATA"  \
  cfg:default.paths.logs="$GF_PATHS_LOGS"   \
  cfg:default.smtp.enabled="$GF_SMTP_ENABLED"    \
  cfg:default.smtp.host="$GF_SMTP_HOST"     \
  cfg:default.smtp.user="$GF_SMTP_USER"     \
  cfg:default.smtp.password="$GF_SMTP_PASSWORD"    \
  cfg:default.smtp.skip_verify="$GF_SMTP_SKIP_VERIFY" \
  cfg:default.smtp.from_address="$GF_SMTP_FROM_ADDRESS"
```

> 其中添加的是smtp的参数。

- DockerFile

``` sh
FROM 10.0.0.153:5000/k8s/heapster-grafana-amd64:v4.0.2
ADD run.sh /
RUN chmod 777 run.sh
```

### Logging部署

> 采用Fluentd（用于收集、处理、传输日志数据）+ Elasticsearch（用于实时查询和解析数据）+ Kibana（用于数据可视化）。在整个集群搭建后部署logging，从而记录所有的服务起始，具体操作可以参考文献。

- 下载yaml文件

`git clone https://github.com/kubernetes/kubernetes.git`

1. Elasticsearch和Kibana在`/home/administrator/kubernetes/cluster/addons/fluentd-elasticsearch`中
	
2. Fluentd在`/home/administrator/kubernetes/cluster/saltbase/salt/fluentd-es`中
	
- 将镜像`gcr.io/google_containers/fluentd-elasticsearch:1.20`,`gcr.io/google_containers/elasticsearch:v2.4.1`,`gcr.io/google_containers/kibana:v4.6.1`放进私有库中


- 修改yaml文件, 更改image地址
	
	- `192.168.1.78:5000/fluentd-elasticsearch:1.20`
	- `192.168.1.78:5000/elasticsearch:v2.4.1`
	- `192.168.1.78:5000/kibana:v4.6.1`

- 在`kibana-service.yaml`中添加`NodePort`，让其暴露出端口
	
```sh
spec:
type: NodePort
ports:
	- port: 5601
```
	
- 更改`fluentd-es.yaml`
	
	* 将apiVersion改为extensions/v1beta1；
	* 将kind改为DaemonSet（让每个node都各创建一个）；
	* 加入template：
	
```sh
spec:
template:
  metadata:
    namespace: kube-system
    labels:
      k8s-app: fluentd-logging
```
	
原本的spec以下的内容（第21行到第41行）移至同metadata平齐(右移四个空格)，在vim下面用`:21,41s/^/    /`命令

- 分别使用`create -f`和`describe`来创建与查看端口。进入kibana界面后，点create便可创建

### Ingress部署http

#### 部署默认后端

`kubectl create -f default-backend.yaml`

#### 部署 Ingress Controller

修改yaml文件中，添加`hostNetwork: true`，使其监听宿主机 80 端口：

``` sh
spec:
  template:
    metadata:
      labels:
        name: nginx-ingress-lb
    spec:
      terminationGracePeriodSeconds: 60
      hostNetwork: true
```

`kubectl create -f nginx-ingress-daemonset.yaml`

#### 部署 Ingress

`kubectl create -f dashboard-ingress.yaml`

#### 修改hosts文件

添加集群中的某个node或master的IP到hosts文件中，例如Linux系统：

`echo "10.0.0.171  dashboard.chenjian.com" >> /etc/hosts`

### Ingress部署TLS（HTTPS）

#### 创建证书

``` sh
# 生成CA自签证书文件夹
mkdir cert && cd cert

# 生成CA自签证书的密钥
openssl genrsa -out ca-key.pem 2048

# 生成CA自签证书
openssl req -x509 -new -nodes -key ca-key.pem -days 10000 -out ca.pem -subj "/CN=kube-ca"

# 配置openssl部署
cp /etc/pki/tls/openssl.cnf .
vim openssl.cnf

# 修改如下
[ req ]
req_extensions = v3_req # 这行默认注释关着的 把注释删掉
# 下面配置是新增的
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = dashboard.chenjian.me
DNS.2 = kibana.chenjian.me

# 生成证书密钥
openssl genrsa -out ingress-key.pem 2048

# 生成证书的申请表
openssl req -new -key ingress-key.pem -out ingress.csr -subj "/CN=kube-ingress" -config openssl.cnf

# 生成证书 有效期为365天
openssl x509 -req -in ingress.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out ingress.pem -days 365 -extensions v3_req -extfile openssl.cnf
```

#### 创建secret

ingress-secret.yaml文件格式如下：

``` sh
apiVersion: v1
data:
  tls.crt: ##内容为ingress.pem里的内容##
  tls.key: ##内容为ingress-key.pem里的内容##
kind: Secret
metadata:
  name: ingress-secret
  namespace: kube-system
type: Opaque
```

create完成：

`kubectl create -f ingress-secret.yaml`

或者直接用文件：

`kubectl create secret tls ingress-secret --key cert/ingress-key.pem --cert cert/ingress.pem --namespace kube-system`

#### 部署Ingress

`kubectl create -f dashboard-ingress-tls.yaml`

#### 修改hosts文件

添加集群中的某个node或master的IP到hosts文件中，例如Linux系统：

`echo "10.0.0.171  dashboard.chenjian.com" >> /etc/hosts`

#### 访问地址dashboard.chenjian.com

部署TLS后的80端口会自动重定向到443（HTTPS端口）

开始出现“Your connnection is not private”

在chrome浏览器中，HTTPS/SSL中添加ca.pem文件，并给予全部权限。

再次打开，没有https提示（钥匙上带叉的logo），但是URL栏中出现“Not Secure”这样的红色字样。

解决这个问题，需要重服务商买权威的CA证书。


### Troubleshooting

#### Node status is NotReady

- 某些节点失败 

```sh
kubectl get nodes
	
NAME            STATUS     AGE
192.168.1.157   NotReady   42d
192.168.1.158   Ready      42d
192.168.1.159   Ready      42d
```
	
- 查看详细信息
	
```sh
kubectl describe node 192.168.1.157
	
......
Conditions:
Type          Status          LastHeartbeatTime                       LastTransitionTime                      Reason                  Message
----          ------          -----------------                       ------------------                      ------                  -------
OutOfDisk     Unknown         Sat, 28 May 2016 12:56:01 +0000         Sat, 28 May 2016 12:56:41 +0000         NodeStatusUnknown       Kubelet stopped posting node status.
Ready         Unknown         Sat, 28 May 2016 12:56:01 +0000         Sat, 28 May 2016 12:56:41 +0000         NodeStatusUnknown       Kubelet stopped posting node status.
......
```
	
从中可以看到节点unready的原因是**outofdisk**，从而导致**Kubelet stopped posting node status.**
所以可以查看下`192.168.1.157`的容量，其操作系统是ubuntu14.04，可通过`df`进行查看：
	
```sh
df
	
Filesystem     1K-blocks     Used Available Use% Mounted on
udev             2008212        4   2008208   1% /dev
tmpfs             403856     3784    400072   1% /run
/dev/sda1       12253360 10108744   1499140  88% /
none                   4        0         4   0% /sys/fs/cgroup
none                5120        0      5120   0% /run/lock
none             2019260      256   2019004   1% /run/shm
none              102400       40    102360   1% /run/user
```

然后通过`docker rmi image`来删除一些没用的镜像
	
- 重启kubelet
	
```sh
1. ssh administrator@192.168.1.157

2. sudo su

3. /etc/init.d/kubelet restart
	
stop: Unknown instance: 
kubelet start/running, process 59261
```
	
- 查看节点
	
```sh
kubectl get nodes
	
NAME            STATUS    AGE
192.168.1.157   Ready     42d
192.168.1.158   Ready     42d
192.168.1.159   Ready     42d
```

恢复正常

#### Failed to create "kube-discovery" deployment

- 重新kubeadm init出现kube-discovery

```sh
failed to create "kube-discovery" deployment [deployments.extensions "kube-discovery" already exists]
```

问题在于外部的etcd集群内还有上一些的k8s集群信息，需要在每个etcd节点中删除数据，重启服务

```sh
# rm -rf /var/lib/etcd/etcd0 

# if [[ true ]]; then
	systemctl stop etcd
	systemctl start etcd 
	systemctl status etcd
fi
```

在master上面重启k8s

```sh
# systemctl stop kubelet

# docker rm -f -v $(docker ps -q)

# find /var/lib/kubelet | xargs -n 1 findmnt -n -t tmpfs -o TARGET -T | uniq | xargs -r umount -v

# rm -r -f /etc/kubernetes /var/lib/kubelet /var/lib/etcd

# systemctl start kubelet

# kubeadm init xxxx
```

#### tcp 10.96.0.1:443: i/o timeout

- 在基本的k8s集群建立后,均为正常。开启一个服务（例如busybox），服务总出于ContainerCreating中。通过对node上的docker容器观察，一直处于pause容器创建过程中，问题是无法tcp连接到kubernetes服务的Apiserver（10.96.0.1:443）上

- 解决方法，在节点上添加：

`route add 10.96.0.1 gw <your real master IP>`


### 参考文献：
1.  [Installing Kubernetes on Linux with kubeadm](http://kubernetes.io/docs/getting-started-guides/kubeadm/)
2. [漠然博客](https://mritd.me/)
3. [ubuntu 16.04 L2TP](http://blog.csdn.net/hhbgk/article/details/52549816)
4. [Can not pull/push images after update docker to 1.12](http://stackoverflow.com/questions/38695515/can-not-pull-push-images-after-update-docker-to-1-12)
5. [Tear down](http://kubernetes.io/docs/getting-started-guides/kubeadm/#tear-down)
6. [storage-schema](https://github.com/kubernetes/heapster/blob/master/docs/storage-schema.md)
7. [influxdb](https://docs.influxdata.com/influxdb/v1.1/introduction/getting_started/)
8. [总结部署 Kubernetes+Heapster+InfluxDB+Grafana 详解](http://blog.csdn.net/qq_21398167/article/details/52920288)
9. [Ubuntu16.04如何安装VMware Tools](http://jingyan.baidu.com/article/bad08e1ef759f209c85121de.html)
10. [Installing Kubernetes Cluster with 3 minions on CentOS 7 to manage pods and services](http://severalnines.com/blog/installing-kubernetes-cluster-minions-centos7-manage-pods-services)
11. [基于 CentOS7 的 Kubernetes 集群](http://blog.opskumu.com/k8s-cluster-centos7.html)
12. [Kubernetes 1.4.5](http://xf80.com/2016/10/31/kubernetes-update-1.4.5/)
13. [centos7系统备份与还原](http://www.itdadao.com/articles/c15a1080406p0.html)
14. [CentOS7系统升级备份恢复实验](http://www.centoscn.com/CentOS/Intermediate/2016/0112/6648.html)
15. [Kibana4指南](http://www.code123.cc/docs/kibana-logstash/v4/index.html)
16. [elasticsearch + fluentd + kibana4(EFK) 安裝詳細流程 in ubuntu14.04](http://chi15036-blog.logdown.com/posts/297025-elasticsearch-fluentd-kibana4-installation-details-processes-in-ubuntu1404)
17. [Kibana4学习<三>](http://www.cnblogs.com/guozhe/p/5206216.html)
18. [How to fix weave-net CrashLoopBackOff for the second node?
](http://stackoverflow.com/questions/39872332/how-to-fix-weave-net-crashloopbackoff-for-the-second-node#40338365)