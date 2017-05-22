---
layout:     post
title:      "Kubernetes集群之高可用性Master集群"
subtitle:   "Deploy HA Master Clusters Of K8s"
date:       Sat, May 20 2017 13:56:13 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-HA-Master-Clusters-Of-K8s/head_blog.jpg"
catalog:    true
tags:
    - 工作
    - Kubernetes
---

### 申明

本篇博文为原创。

整个kuberetes集群基于[在CentOS7上使用二进制方式部署Kubernetes](https://o-my-chenjian.com/2017/04/25/Deploy-K8s-By-Source-Code-On-CentOS7/)一系列博文，请读者在进行**高可用性Master集群**搭建之前，熟悉理解并实践整个系类博文的搭建。

同时，再次感谢作者**opsnull**，以及其在Github上的[opsnull/follow-me-install-kubernetes-cluster](https://github.com/opsnull/follow-me-install-kubernetes-cluster)项目，如有兴趣请star或者fork他的项目。还要感谢**深圳-小刚**提供的思路，这里不方便透露朋友的信息，在此请给予原谅。

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

### 系统环境信息

相对之前单个Master，这次是**三台Mster**，其他信息基本不变

|  类型  |     IP       | /etc/hosts | /etc/hostname|
|:-----:|:------------:|:----------:|:-----:|
| k8s-master-1 | 192.168.1.153 |127.0.0.1   192-168-1-153.master|192-168-1-153.master|
| k8s-master-2 | 192.168.1.154 |127.0.0.1   192-168-1-154.master|192-168-1-154.master|
| k8s-master-3 | 192.168.1.155 |127.0.0.1   192-168-1-155.master|192-168-1-155.master|
| k8s-node | 192.168.1.156|127.0.0.1   192-168-1-156.node|192-168-1-156.node|
| etcd-0 | 192.168.1.157|127.0.0.1   192-168-1-157.etcd|192-168-1-157.etcd|
| etcd-1 | 192.168.1.158|127.0.0.1   192-168-1-158.etcd|192-168-1-158.etcd|
| etcd-2 | 192.168.1.159|127.0.0.1   192-168-1-159.etcd|192-168-1-177.etcd|

### 准备工作

操作服务器IP：`192.168.1.153`，即`K8s-master-1`。其他`master-2`和`master-3`均采用类似操作，不同之处会在下文中提示。

``` sh
# 更新源
yum update -y
yum install -y vim
yum install -y wget

# 更改hostname
ipname=192-168-1-153
nodetype=master

echo "${ipname}.${nodetype}" > /etc/hostname
echo "127.0.0.1   ${ipname}.${nodetype}" >> /etc/hosts
sysctl kernel.hostname=${ipname}.${nodetype}

# 关闭防火墙
sudo systemctl stop firewalld
sudo systemctl disable firewalld
setenforce 0
```

CentOS7设置网络静态IP

``` sh
# 原先IP为192.168.1.161
ip=192.168.1.162

sed -i "s/192.168.1.161/${ip}/g" /etc/sysconfig/network-scripts/ifcfg-ens160
sed -i "s/BOOTPROTO=\"none\"/BOOTPROTO=\"static\"/g" /etc/sysconfig/network-scripts/ifcfg-ens160
echo "NO_CONTROLLED=\"no\"" >> /etc/sysconfig/network-scripts/ifcfg-ens160
systemctl restart network.service
```

设置集群的环境变量

``` sh
# 创建必要的文件夹
mkdir /root/local
mkdir /root/local/bin

# TLS Bootstrapping使用的Token
head -c 16 /dev/urandom | od -An -t x | tr -d ' '
<<'COMMENT'
bbaeb8257add810bb900627deda629c1
COMMENT

cat >> /etc/profile <<EOF
# 最好使用主机未用的网段来定义服务网段和Pod网段

# ===============基本信息===============
# 当前部署的节点 IP
export NODE_IP=192.168.1.153

# 当前部署的Master集群的IP
export MASTER_IP_1=192.168.1.153
export MASTER_IP_2=192.168.1.154
export MASTER_IP_3=192.168.1.155

# 将创建好的文件夹加入环境变量
# 后续的kubectl，kubelet等工具将放到该路径下
export PATH=/root/local/bin:\$PATH
# ===============基本信息===============


# ===============ETCD===============
ETCD_0=192.168.1.157
ETCD_1=192.168.1.158
ETCD_2=192.168.1.159

# 当前部署的机器名称
# 随便定义，只要能区分不同机器即可
# 例如
# 192.168.1.157的为etcd-host0
# 192.168.1.158的为etcd-host1
# 192.168.1.159的为etcd-host2
export ETCD_NODE_NAME=etcd-host0

# etcd集群所有机器 IP
export ETCD_NODE_IPS="\${ETCD_0} \${ETCD_1} \${ETCD_2}" 

# etcd 集群各机器名称和对应的IP、端口
export ETCD_NODES=etcd-host0=https://\${ETCD_0}:2380,etcd-host1=https://\${ETCD_1}:2380,etcd-host2=https://\${ETCD_2}:2380

# etcd 集群服务地址列表
export ETCD_ENDPOINTS="https://\${ETCD_0}:2379,https://\${ETCD_1}:2379,https://\${ETCD_2}:2379"
# ===============ETCD===============


# ===============集群信息===============
# 服务网段 (Service CIDR），部署前路由不可达，部署后集群内使用IP:Port可达
SERVICE_CIDR="10.254.0.0/16"

# POD网段(Cluster CIDR，部署前路由不可达，**部署后**路由可达(flanneld保证)
CLUSTER_CIDR="172.30.0.0/16"

# token文件
BOOTSTRAP_TOKEN="bbaeb8257add810bb900627deda629c1"

# 服务端口范围 (NodePort Range)，建议使用高端口
export NODE_PORT_RANGE="30000-50000"

# kubernetes服务IP 
# 一般是SERVICE_CIDR中第一个IP
export CLUSTER_KUBERNETES_SVC_IP="10.254.0.1"

# 集群DNS服务IP 
# 从 SERVICE_CIDR 中预分配
export CLUSTER_DNS_SVC_IP="10.254.0.2"

# 集群DNS域名
export CLUSTER_DNS_DOMAIN="cluster.local."

# master上kubectl访问的kube-apiserver的地址
export MASTER_KUBE_APISERVER="https://\${MASTER_IP_1}:6443"

# node上kubelet访问的kube-apiserver的地址
export NODE_KUBE_APISERVER="http://127.0.0.1:5002"
# ===============集群信息===============


# ===============FLANNEL信息===============
# flanneld网络配置前缀
export FLANNEL_ETCD_PREFIX="/kubernetes/network"

# 当前部署的节点通信接口名称，使用和其它Node互通的接口即可
export FLANNEL_OPTIONS="-iface=ens160"
# ===============FLANNEL信息===============

EOF

source /etc/profile
```

- 更新MASTER_IP为MASTER_IP_N，从而代表Master集群IP
- 新增NODE_KUBE_APISERVER，使Node访问本地的5002端口，由haproxy监听端口并负载均衡于各个Master
- 新增MASTER_KUBE_APISERVER，使master上的kubectl能访问本地的kube-apisever

### Kubernetes集群之安全设置

操作服务器IP：`192.168.1.153`，即`K8s-master-1`。其他master节点均采用该`K8s-master-1`制作出的证书，节点不再制作证书

- 更新之处：

##### kubernetes证书申请表

``` bash
cat <<EOF > kubernetes-csr.json
{
  "CN": "kubernetes",
  "hosts": [
    "127.0.0.1",
    "192.168.1.153",
    "192.168.1.154",
    "192.168.1.155",
    "10.254.0.1",
    "kubernetes",
    "kubernetes.default",
    "kubernetes.default.svc",
    "kubernetes.default.svc.cluster",
    "kubernetes.default.svc.cluster.local"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "BeiJing",
      "L": "BeiJing",
      "O": "k8s",
      "OU": "System"
    }
  ]
}

EOF
```

- hosts 字段分别指定了k8s-master集群的IP(192.168.1.153/192.168.1.154/192.168.1.155)

- 添加 kube-apiserver注册的名为kubernetes的服务IP(Service Cluster IP)，一般是`kube-apiserver --service-cluster-ip-range`选项值指定的网段的第一个IP，如 "10.254.0.1"

### Kubernetes集群之创建kubeconfig文件

操作服务器IP：`192.168.1.153`，即`K8s-master-1`。

其他master节点均采用`K8s-master-1`上生成的token.csv文件。

- 更新之处：

##### 生成kubectl的kubeconfig文件

``` bash
# 设置集群参数
kubectl config set-cluster kubernetes \
--certificate-authority=/etc/kubernetes/ssl/ca.pem \
--embed-certs=true \
--server=${MASTER_KUBE_APISERVER}

<<'COMMENT'
Cluster "kubernetes" set.
COMMENT
```

master上面的kubectl需要访问本级的kube-apiserver，因此该操作每个master节点都需要执行，注意环境变量中的`export MASTER_KUBE_APISERVER="https://\${MASTER_IP_1}:6443"`需要根据不同节点IP变化

此步骤后续操作，和原先相同。全部完成后，每个master节点均有其自己的`~/.kube/config`文件

##### 生成kubelet的bootstrapping kubeconfig文件

``` bash
kubectl config set-cluster kubernetes \
--certificate-authority=/etc/kubernetes/ssl/ca.pem \
--embed-certs=true \
--server=${NODE_KUBE_APISERVER} \
--kubeconfig=bootstrap.kubeconfig

<<'COMMENT'
Cluster "kubernetes" set.
COMMENT
```

该操作只需要在`K8s-master-1`上操作。

##### 生成kube-proxy的kubeconfig文件

``` bash
# 设置集群参数
kubectl config set-cluster kubernetes \
--certificate-authority=/etc/kubernetes/ssl/ca.pem \
--embed-certs=true \
--server=${NODE_KUBE_APISERVER} \
--kubeconfig=kube-proxy.kubeconfig

<<'COMMENT'
Cluster "kubernetes" set.
COMMENT
```

该操作只需要在`K8s-master-1`上操作。

### Kubernetes集群之Master节点

操作服务器IP：`192.168.1.153`，即`K8s-master-1`。

- 更新之处：

##### kube-apiserver.service

``` bash
cat > kube-apiserver.service <<EOF 
[Unit]
Description=Kubernetes API Server
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=network.target

[Service]
ExecStart=/root/local/bin/kube-apiserver \\
  --admission-control=NamespaceLifecycle,LimitRanger,ServiceAccount,DefaultStorageClass,ResourceQuota \\
  --advertise-address=${MASTER_IP_1} \\
  --bind-address=${MASTER_IP_1} \\
  --insecure-bind-address=${MASTER_IP_1} \\
  --authorization-mode=RBAC \\
  --runtime-config=rbac.authorization.k8s.io/v1alpha1 \\
  --kubelet-https=true \\
  --experimental-bootstrap-token-auth \\
  --token-auth-file=/etc/kubernetes/token.csv \\
  --service-cluster-ip-range=${SERVICE_CIDR} \\
  --service-node-port-range=${NODE_PORT_RANGE} \\
  --tls-cert-file=/etc/kubernetes/ssl/kubernetes.pem \\
  --tls-private-key-file=/etc/kubernetes/ssl/kubernetes-key.pem \\
  --client-ca-file=/etc/kubernetes/ssl/ca.pem \\
  --service-account-key-file=/etc/kubernetes/ssl/ca-key.pem \\
  --etcd-cafile=/etc/kubernetes/ssl/ca.pem \\
  --etcd-certfile=/etc/etcd/ssl/etcd.pem \\
  --etcd-keyfile=/etc/etcd/ssl/etcd-key.pem \\
  --etcd-servers=${ETCD_ENDPOINTS} \\
  --enable-swagger-ui=true \\
  --allow-privileged=true \\
  --apiserver-count=3 \\
  --audit-log-maxage=30 \\
  --audit-log-maxbackup=3 \\
  --audit-log-maxsize=100 \\
  --audit-log-path=/var/lib/audit.log \\
  --event-ttl=1h \\
  --v=2
Restart=on-failure
RestartSec=5
Type=notify
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF
```

- 更新`--advertise-address`，`--bind-address`和`--insecure-bind-address`，三个参数均根据各自master的IP改动

##### kube-controller-manager.service

``` bash
cat > kube-controller-manager.service <<EOF 
[Unit]
Description=Kubernetes Controller Manager
Documentation=https://github.com/GoogleCloudPlatform/kubernetes

[Service]
ExecStart=/root/local/bin/kube-controller-manager \\
  --address=127.0.0.1 \\
  --master=http://${MASTER_IP_1}:8080 \\
  --allocate-node-cidrs=true \\
  --service-cluster-ip-range=${SERVICE_CIDR} \\
  --cluster-cidr=${CLUSTER_CIDR} \\
  --cluster-name=kubernetes \\
  --cluster-signing-cert-file=/etc/kubernetes/ssl/ca.pem \\
  --cluster-signing-key-file=/etc/kubernetes/ssl/ca-key.pem \\
  --service-account-private-key-file=/etc/kubernetes/ssl/ca-key.pem \\
  --root-ca-file=/etc/kubernetes/ssl/ca.pem \\
  --leader-elect=true \\
  --v=2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

- 更新`--master`，参数均根据各自master的IP改动
- `--leader-elect=true`，一定要写上

##### kube-scheduler.service

``` bash
cat > kube-scheduler.service <<EOF
[Unit]
Description=Kubernetes Scheduler
Documentation=https://github.com/GoogleCloudPlatform/kubernetes

[Service]
ExecStart=/root/local/bin/kube-scheduler \\
  --address=127.0.0.1 \\
  --master=http://${MASTER_IP_1}:8080 \\
  --leader-elect=true \\
  --v=2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

- 更新`--master`，参数均根据各自master的IP改动
- `--leader-elect=true`，一定要写上

### Kubernetes集群之Node节点

操作服务器IP：`192.168.1.156`，即`K8s-node`。

在安装kubelet之前，需要[在Linux上部署Haproxy](https://o-my-chenjian.com/2017/05/20/Deploy-Haproxy-On-Linux/)，使其打开并监听`端口5002`

- 更新之处：

##### 通过kubelet的TLS证书请求

操作服务器IP：`192.168.1.153`，即`K8s-master-1`

``` bash
# 查看未授权的 CSR 请求
kubectl get csr
<<'COMMENT'
NAME        AGE       REQUESTOR   CONDITION
csr-08zjq   34s                   Pending
csr-74jv2   1m                    Pending
csr-7hrq3   2m                    Pending
csr-l90x2   4m                    Pending
COMMENT

kubectl get nodes
<<'COMMENT'
No resources found.
COMMENT

# 通过 CSR 请求
kubectl certificate approve csr-08zjq csr-74jv2 csr-7hrq3 csr-l90x2 
<<'COMMENT'
certificatesigningrequest "csr-08zjq" approved
certificatesigningrequest "csr-74jv2" approved
certificatesigningrequest "csr-7hrq3" approved
certificatesigningrequest "csr-l90x2" approved
COMMENT

kubectl get nodes
<<'COMMENT'
NAME            STATUS     AGE       VERSION
192.168.1.156   Ready     16s       v1.6.2
COMMENT
```

### 查看Master集群的leader

操作服务器IP：`192.168.1.153`，`192.168.1.154`或`192.168.1.155`中任一一台上操作。

``` sh
kubectl -n kube-system get ep kube-controller-manager -o yaml
<<'COMMENT'
apiVersion: v1
kind: Endpoints
metadata:
  annotations:
    control-plane.alpha.kubernetes.io/leader: '{"holderIdentity":"192-168-1-153.master-1","leaseDurationSeconds":15,"acquireTime":"2017-05-18T03:53:20Z","renewTime":"2017-05-19T07:40:09Z","leaderTransitions":0}'
  creationTimestamp: 2017-05-18T03:53:20Z
  name: kube-controller-manager
  namespace: kube-system
  resourceVersion: "100117"
  selfLink: /api/v1/namespaces/kube-system/endpoints/kube-controller-manager
  uid: 88a08362-3b7d-11e7-95db-005056a366fb
subsets: []
COMMENT
```

可以得知，此时leader为`192.168.1.153`这台机器

**此时，关闭`192.168.1.153`，再次查看集群leader**

操作服务器IP：`192.168.1.154`或`192.168.1.155`中任一一台上操作。

``` sh
kubectl -n kube-system get ep kube-scheduler -o yaml
<<'COMMENT'
apiVersion: v1
kind: Endpoints
metadata:
  annotations:
    control-plane.alpha.kubernetes.io/leader: '{"holderIdentity":"192-168-1-154.master-2","leaseDurationSeconds":15,"acquireTime":"2017-05-19T07:52:54Z","renewTime":"2017-05-19T07:53:14Z","leaderTransitions":1}'
  creationTimestamp: 2017-05-18T03:53:23Z
  name: kube-scheduler
  namespace: kube-system
  resourceVersion: "100984"
  selfLink: /api/v1/namespaces/kube-system/endpoints/kube-scheduler
  uid: 8a4d3291-3b7d-11e7-95db-005056a366fb
subsets: []
COMMENT
```

可以得知，此时leader为`192.168.1.154`这台机器

至此，整个高可用性Master集群便成功完成。


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/05/20/Deploy-HA-Master-Clusters-Of-K8s/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。

