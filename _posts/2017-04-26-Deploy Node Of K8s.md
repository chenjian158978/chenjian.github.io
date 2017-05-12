---
layout:     post
title:      "Kubernetes集群之Node节点"
subtitle:   "Deploy Node Of K8s"
date:       Wed, Apr 26 2017 11:39:29 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Node-Of-K8s/head_blog.jpg"
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
- [Kubernetes集群之清除集群](https://o-my-chenjian.com/2017/05/11/Clear-The-Cluster-Of-K8s/)

### 准备工作

操作服务器IP：`192.168.1.173`，即`K8s-node`

``` bash
yum update -y
yum install -y vim
yum install -y wget

# 更改hostname
ipname=192-168-1-173
nodetype=node

echo "${ipname}.${nodetype}" > /etc/hostname
echo "127.0.0.1   ${ipname}.${nodetype}" >> /etc/hosts
sysctl kernel.hostname=${ipname}.${nodetype}

# 关闭防火墙
sudo systemctl stop firewalld
sudo systemctl disable firewalld
```

设置集群的环境变量

``` bash
# 创建必要的文件夹
mkdir /root/local
mkdir /root/local/bin

ifconfig
<<'COMMENT'
ens160: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.173  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::fff8:aea4:232b:63cb  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:a3:ec:3e  txqueuelen 1000  (Ethernet)
        RX packets 3500755  bytes 1462533591 (1.3 GiB)
        RX errors 0  dropped 80  overruns 0  frame 0
        TX packets 848171  bytes 72788405 (69.4 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1  (Local Loopback)
        RX packets 36  bytes 2564 (2.5 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 36  bytes 2564 (2.5 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
COMMENT

# 环境变量
cat >> /etc/profile <<EOF
# 最好使用 主机未用的网段 来定义服务网段和 Pod 网段

# ===============基本信息===============
# 当前部署的节点 IP
export NODE_IP=192.168.1.173

# 当前部署的Master的IP
export MASTER_IP=192.168.1.171

# 将创建好的文件夹加入环境变量
# 后续的kubectl，kubelet等工具将放到该路径下
export PATH=/root/local/bin:\$PATH
# ===============基本信息===============


# ===============ETCD===============
ETCD_0=192.168.1.175
ETCD_1=192.168.1.176
ETCD_2=192.168.1.177

# 当前部署的机器名称
# 随便定义，只要能区分不同机器即可
# 例如
# 192.168.1.175的为etcd-host0
# 192.168.1.176的为etcd-host1
# 192.168.1.177的为etcd-host2
export ETCD_NODE_NAME=etcd-host0

# etcd集群所有机器 IP
export ETCD_NODE_IPS="192.168.1.175 192.168.1.176 192.168.1.177" 

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
BOOTSTRAP_TOKEN="2dc1235a021972ca7d9d486795e57369"

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

# kubelet访问的kube-apiserver的地址
export KUBE_APISERVER="https://\${MASTER_IP}:6443"
# ===============集群信息===============


# ===============FLANNEL信息===============
# flanneld网络配置前缀
export FLANNEL_ETCD_PREFIX="/kubernetes/network"

# 当前部署的节点通信接口名称，使用和其它Node互通的接口即可
export FLANNEL_OPTIONS="-iface=ens160"
# ===============FLANNEL信息===============

EOF

# 激活配置
source /etc/profile
```

注：

- 如果是远程登录master节点，为保证环境变量登录后便激活，需要将这些环境变量加入`~/.bashrc`文件中，再激活配置
- token值，所有节点包括master均要相同

### TLS证书

``` bash
sudo mkdir -p /etc/kubernetes/ssl /var/lib/kubelet /var/lib/kube-proxy /etc/flanneld/ssl
sudo cp ca.pem kubernetes.pem kubernetes-key.pem /etc/kubernetes/ssl
sudo cp bootstrap.kubeconfig kube-proxy.kubeconfig token.csv /etc/kubernetes
sudo cp flanneld-key.pem  flanneld.pem /etc/flanneld/ssl

ls /etc/kubernetes/
<<'COMMENT'
bootstrap.kubeconfig  kubelet.kubeconfig  kube-proxy.kubeconfig  ssl  token.csv
COMMENT

ls /etc/kubernetes/ssl/
<<'COMMENT'
ca.pem kubelet.key  kubernetes-key.pem  kubernetes.pem
COMMENT

ls /etc/flanneld/ssl
<<'COMMENT'
flanneld-key.pem  flanneld.pem
COMMENT
```

### 安装Flannel

请参考[Kubernetes集群之Flannel网络](https://o-my-chenjian.com/2017/05/11/Deploy-Pod-Network-Of-Flannel/)

### 安装Docker

请参考[CentOS7之二进制文件安装](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/#centos7之二进制文件安装)

### 安装kubelet

##### 赋予用户kubelet-bootstrap角色

操作服务器IP：`192.168.1.171`，即`K8s-master`

``` bash
kubectl create clusterrolebinding kubelet-bootstrap --clusterrole=system:node-bootstrapper --user=kubelet-bootstrap

<<'COMMENT'
clusterrolebinding "kubelet-bootstrap" created
COMMENT
```

##### 下载kubelet和kube-proxy二进制文件

操作服务器IP：`192.168.1.173`，即`K8s-node`

``` bash
wget https://github.com/kubernetes/kubernetes/releases/download/v1.6.2/kubernetes.tar.gz
tar -xzvf kubernetes.tar.gz
cd kubernetes
echo y | source cluster/get-kube-binaries.sh

<<'COMMENT'
Kubernetes release: v1.6.2
Server: linux/amd64  (to override, set KUBERNETES_SERVER_ARCH)
Client: linux/amd64  (autodetected)

Will download kubernetes-server-linux-amd64.tar.gz from https://storage.googleapis.com/kubernetes-release/release/v1.6.2
Is this ok? [Y]/n
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  347M  100  347M    0     0  5927k      0  0:00:59  0:00:59 --:--:-- 5905k

md5sum(kubernetes-server-linux-amd64.tar.gz)=6d52bed027ba4ae82aa07bd88013857a
sha1sum(kubernetes-server-linux-amd64.tar.gz)=b02937bbb35b74eb3db401c2a1d791bcfff18e4a
COMMENT

cd server
tar -xzvf kubernetes-server-linux-amd64.tar.gz
cd kubernetes
tar -xzvf  kubernetes-src.tar.gz
sudo cp -r server/bin/{kube-proxy,kubelet} /root/local/bin/
```

##### kubelet.service

``` bash
sudo mkdir /var/lib/kubelet

cat > kubelet.service <<EOF
[Unit]
Description=Kubernetes Kubelet
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=docker.service
Requires=docker.service

[Service]
WorkingDirectory=/var/lib/kubelet
ExecStart=/root/local/bin/kubelet \\
  --address=${NODE_IP} \\
  --hostname-override=${NODE_IP} \\
  --pod-infra-container-image=registry.access.redhat.com/rhel7/pod-infrastructure:latest \\
  --experimental-bootstrap-kubeconfig=/etc/kubernetes/bootstrap.kubeconfig \\
  --kubeconfig=/etc/kubernetes/kubelet.kubeconfig \\
  --require-kubeconfig \\
  --cert-dir=/etc/kubernetes/ssl \\
  --cluster_dns=${CLUSTER_DNS_SVC_IP} \\
  --cluster_domain=${CLUSTER_DNS_DOMAIN} \\
  --hairpin-mode promiscuous-bridge \\
  --allow-privileged=true \\
  --serialize-image-pulls=false \\
  --logtostderr=true \\
  --v=2
ExecStopPost=/sbin/iptables -A INPUT -s 10.0.0.0/8 -p tcp --dport 4194 -j ACCEPT
ExecStopPost=/sbin/iptables -A INPUT -s 172.16.0.0/12 -p tcp --dport 4194 -j ACCEPT
ExecStopPost=/sbin/iptables -A INPUT -s 192.168.0.0/16 -p tcp --dport 4194 -j ACCEPT
ExecStopPost=/sbin/iptables -A INPUT -p tcp --dport 4194 -j DROP
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

- `--address`不能设置为127.0.0.1，否则后续Pods访问kubelet的API接口时会失败，因为Pods访问的127.0.0.1指向自己而不是kubelet

- 如果设置了`--hostname-override`选项，则kube-proxy也需要设置该选项，否则会出现找不到Node的情况

- `--experimental-bootstrap-kubeconfig`指向`bootstrap.kubeconfig`文件，kubelet使用该文件中的用户名和token向kube-apiserver发送TLS Bootstrapping请求

- 管理员通过了CSR请求后，kubelet自动在`--cert-dir`目录创建证书和私钥文件(kubelet-client.crt 和 kubelet-client.key)，然后写入`--kubeconfig`文件

- 建议在`--kubeconfig`配置文件中指定kube-apiserver地址，如果未指定`--api-servers`选项，则必须指定`--require-kubeconfig`选项后才从配置文件中读取kue-apiserver的地址，否则kubelet启动后将找不到kube-apiserver (日志中提示未找到API Server），`kubectl get nodes`不会返回对应的Node信息

- `--cluster_dns` 指定kubedns的Service IP(可以先分配，后续创建kubedns服务时指定该 IP)，`--cluster_domain`指定域名后缀，这两个参数同时指定后才会生效

- kubelet cAdvisor默认在所有接口监听`4194`端口的请求，对于有外网的机器来说不安全，ExecStopPost选项指定的iptables规则只允许内网机器访问`4194`端口

##### 启动kubelet

``` bash
sudo cp kubelet.service /etc/systemd/system/kubelet.service
sudo systemctl daemon-reload
sudo systemctl enable kubelet

<<'COMMENT'
Created symlink from /etc/systemd/system/multi-user.target.wants/kubelet.service to /etc/systemd/system/kubelet.service.
COMMENT

sudo systemctl start kubelet
sudo systemctl status kubelet

<<'COMMENT'
● kubelet.service - Kubernetes Kubelet
   Loaded: loaded (/etc/systemd/system/kubelet.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2017-04-24 16:38:33 CST; 4s ago
     Docs: https://github.com/GoogleCloudPlatform/kubernetes
 Main PID: 19387 (kubelet)
   Memory: 10.1M
   CGroup: /system.slice/kubelet.service
           └─19387 /root/local/bin/kubelet --address=192.168.1.173 --hostname-override=192.168.1.173 --pod-infra-container-image=registry.access.redhat....

Apr 24 16:38:33 192-168-1-173.node systemd[1]: Started Kubernetes Kubelet.
Apr 24 16:38:33 192-168-1-173.node systemd[1]: Starting Kubernetes Kubelet...
Apr 24 16:38:33 192-168-1-173.node kubelet[19387]: I0424 16:38:33.966245   19387 feature_gate.go:144] feature gates: map[]
Apr 24 16:38:34 192-168-1-173.node kubelet[19387]: I0424 16:38:33.968061   19387 bootstrap.go:58] Using bootstrap kubeconfig to generate TLS cli...fig file
Hint: Some lines were ellipsized, use -l to show in full.
COMMENT
```

##### 通过kubelet的TLS证书请求

操作服务器IP：`192.168.1.171`，即`K8s-master`

``` bash
# 查看未授权的 CSR 请求
kubectl get csr
<<'COMMENT'
NAME        AGE       REQUESTOR           CONDITION
csr-tfvgk   38s       kubelet-bootstrap   Pending
COMMENT

kubectl get nodes
<<'COMMENT'
No resources found.
COMMENT

# 通过 CSR 请求
kubectl certificate approve csr-tfvgk
<<'COMMENT'
certificatesigningrequest "csr-tfvgk" approved
COMMENT

kubectl get nodes
<<'COMMENT'
NAME            STATUS     AGE       VERSION
192.168.1.173   Ready      20s        v1.6.2
COMMENT
```

操作服务器IP：`192.168.1.173`，即`K8s-node`

``` bash
ls -l /etc/kubernetes/kubelet.kubeconfig 
<<'COMMENT'
-rw-------. 1 root root 2280 Apr 24 16:40 /etc/kubernetes/kubelet.kubeconfig
COMMENT

ls -l /etc/kubernetes/ssl/kubelet*
<<'COMMENT'
-rw-r--r--. 1 root root 1046 Apr 24 16:40 /etc/kubernetes/ssl/kubelet-client.crt
-rw-------. 1 root root  227 Apr 24 16:38 /etc/kubernetes/ssl/kubelet-client.key
-rw-r--r--. 1 root root 1115 Apr 24 16:40 /etc/kubernetes/ssl/kubelet.crt
-rw-------. 1 root root 1679 Apr 24 16:40 /etc/kubernetes/ssl/kubelet.key
COMMENT
```

### 安装kube-proxy

操作服务器IP：`192.168.1.173`，即`K8s-node`

``` bash
# 创建 kube-proxy 的 systemd unit 文件
sudo mkdir -p /var/lib/kube-proxy

cat > kube-proxy.service <<EOF
[Unit]
Description=Kubernetes Kube-Proxy Server
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=network.target

[Service]
WorkingDirectory=/var/lib/kube-proxy
ExecStart=/root/local/bin/kube-proxy \\
  --bind-address=${NODE_IP} \\
  --hostname-override=${NODE_IP} \\
  --cluster-cidr=${SERVICE_CIDR} \\
  --kubeconfig=/etc/kubernetes/kube-proxy.kubeconfig \\
  --logtostderr=true \\
  --v=2
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF
```

- `--hostname-override`参数值必须与kubelet的值一致，否则kube-proxy启动后会找不到该Node，从而不会创建任何iptables规则

- `--cluster-cidr`必须与kube-apiserver的`--service-cluster-ip-range`选项值一致

- kube-proxy根据`--cluster-cidr`判断集群内部和外部流量，指定`--cluster-cidr` 或`--masquerade-all`选项后kube-proxy才会对访问Service IP的请求做SNAT

- `--kubeconfig`指定的配置文件嵌入了kube-apiserver的地址、用户名、证书、秘钥等请求和认证信息

- 预定义的RoleBinding cluster-admin将User system:kube-proxy与Role system:node-proxier绑定，该Role授予了调用kube-apiserver Proxy相关API的权限

##### 启动kube-proxy

``` bash
# 启动 kube-proxy
sudo cp kube-proxy.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable kube-proxy

<<'COMMENT'
Created symlink from /etc/systemd/system/multi-user.target.wants/kube-proxy.service to /etc/systemd/system/kube-proxy.service.
COMMENT

sudo systemctl start kube-proxy
sudo systemctl status kube-proxy

<<'COMMENT'
● kube-proxy.service - Kubernetes Kube-Proxy Server
   Loaded: loaded (/etc/systemd/system/kube-proxy.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2017-04-24 16:47:15 CST; 3s ago
     Docs: https://github.com/GoogleCloudPlatform/kubernetes
 Main PID: 19602 (kube-proxy)
   Memory: 8.4M
   CGroup: /system.slice/kube-proxy.service
           └─19602 /root/local/bin/kube-proxy --bind-address=192.168.1.173 --hostname-override=192.168.1.173 --cluster-cidr=10.254.0.0/16 --kubeconfig=/...

Apr 24 16:47:16 192-168-1-173.node kube-proxy[19602]: I0424 16:47:16.031559   19602 server.go:173] setting OOM scores is unsupported in this build
Apr 24 16:47:16 192-168-1-173.node kube-proxy[19602]: I0424 16:47:16.054204   19602 server.go:225] Using iptables Proxier.
Apr 24 16:47:16 192-168-1-173.node kube-proxy[19602]: I0424 16:47:16.140492   19602 server.go:249] Tearing down userspace rules.
Apr 24 16:47:16 192-168-1-173.node kube-proxy[19602]: I0424 16:47:16.286207   19602 proxier.go:472] Adding new service "default/kubernetes:https...:443/TCP
Apr 24 16:47:16 192-168-1-173.node kube-proxy[19602]: I0424 16:47:16.286547   19602 conntrack.go:81] Set sysctl 'net/netfilter/nf_conntrack_max' to 131072
Apr 24 16:47:16 192-168-1-173.node kube-proxy[19602]: I0424 16:47:16.286696   19602 proxier.go:741] Not syncing iptables until Services and Endp...m master
Apr 24 16:47:16 192-168-1-173.node kube-proxy[19602]: I0424 16:47:16.286785   19602 proxier.go:540] Received first Endpoints update
Apr 24 16:47:16 192-168-1-173.node kube-proxy[19602]: I0424 16:47:16.290463   19602 conntrack.go:66] Setting conntrack hashsize to 32768
Apr 24 16:47:16 192-168-1-173.node kube-proxy[19602]: I0424 16:47:16.291297   19602 conntrack.go:81] Set sysctl 'net/netfilter/nf_conntrack_tcp_...to 86400
Apr 24 16:47:16 192-168-1-173.node kube-proxy[19602]: I0424 16:47:16.291403   19602 conntrack.go:81] Set sysctl 'net/netfilter/nf_conntrack_tcp_... to 3600
Hint: Some lines were ellipsized, use -l to show in full.
COMMENT
```

### 检验集群可用性

操作服务器IP：`192.168.1.171`，即`K8s-master`

##### nginx-ds.yml

``` bash
cat > nginx-ds.yml <<EOF
apiVersion: v1
kind: Service
metadata:
  name: nginx-ds
  labels:
    app: nginx-ds
spec:
  type: NodePort
  selector:
    app: nginx-ds
  ports:
  - name: http
    port: 80
    targetPort: 80

---

apiVersion: extensions/v1beta1
kind: DaemonSet
metadata:
  name: nginx-ds
  labels:
    addonmanager.kubernetes.io/mode: Reconcile
spec:
  template:
    metadata:
      labels:
        app: nginx-ds
    spec:
      containers:
      - name: my-nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80

EOF
```

##### 创建pod与svc

``` bash
kubectl create -f nginx-ds.yml 
<<'COMMENT'
service "nginx-ds" created
daemonset "nginx-ds" created
COMMENT

kubectl get pods --all-namespaces -o wide
<<'COMMENT'
NAMESPACE   NAME             READY     STATUS    RESTARTS   AGE       IP           NODE
default     nginx-ds-3srdx   1/1       Running   0          13m       172.17.0.2   192.168.1.173
COMMENT

kubectl get svc --all-namespaces
<<'COMMENT'
NAMESPACE   NAME         CLUSTER-IP     EXTERNAL-IP   PORT(S)       AGE
default     kubernetes   10.254.0.1     <none>        443/TCP       3h
default     nginx-ds     10.254.79.44   <nodes>       80:8966/TCP   14m
COMMENT
```

##### 访问nginx网站

操作服务器IP：`192.168.1.173`，即`K8s-node`

``` bash
curl 10.254.79.44

<<'COMMENT'
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
COMMENT
```

出现`Welcome to nginx!`页面


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/26/Deploy-Node-Of-K8s/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。