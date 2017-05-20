---
layout:     post
title:      "Kubernetes集群之Master节点"
subtitle:   "Deploy Master Of K8s"
date:       Wed, Apr 26 2017 10:33:29 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Master-Of-K8s/head_blog.jpg"
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


### Master节点的组件

该博文主要在master上部署三个息息相关的组件：

- kube-apiserver
- kube-scheduler
- kube-controller-manager

操作服务器IP：`192.168.1.171`，即`K8s-master`。在此之前，需要对服务器进行准备工作，具体操作请阅读Security Settings Of K8s

### TLS证书

通过之前的步骤，我们已经生成了所需的`token.csv`和各种`*.pem`文件

``` bash
ls /etc/kubernetes/
<<'COMMENT'
ssl  token.csv
COMMENT

ls /etc/kubernetes/ssl/
<<'COMMENT'
admin-key.pem  admin.pem  ca-key.pem  ca.pem  kube-proxy-key.pem  kube-proxy.pem  kubernetes-key.pem  kubernetes.pem
COMMENT
```

### 下载二进制文件

``` bash
# 下载最新版本的二进制文件
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

# 将二进制文件拷贝到指定路径
sudo cp -r server/bin/{kube-apiserver,kube-controller-manager,kube-scheduler,kubectl,kube-proxy,kubelet} /root/local/bin/

ls /root/local/bin/
<<'COMMENT'
cfssl           cfssljson       flanneld        kube-controller-manager  kubefed  kube-proxy      mk-docker-opts.sh
cfssl-certinfo  environment.sh  kube-apiserver  kubectl                  kubelet  kube-scheduler
COMMENT
```

所有资源可以在[这里](https://pan.baidu.com/s/1pLhmqzL)进行下载

### 部署kube-apiserver

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
  --advertise-address=${MASTER_IP} \\
  --bind-address=${MASTER_IP} \\
  --insecure-bind-address=${MASTER_IP} \\
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

- kube-apiserver 1.6版本开始使用etcd v3 API和存储格式

- `--authorization-mode=RBAC`指定在安全端口使用RBAC授权模式，拒绝未通过授权的请求

- `kube-scheduler`、`kube-controller-manager`和`kube-apiserver`部署在同一台机器上，它们使用非安全端口和kube-apiserver通信

- kubelet、kube-proxy、kubectl部署在其它Node节点上，如果通过安全端口访问 kube-apiserver，则必须先通过TLS证书认证，再通过RBAC授权

- kube-proxy、kubectl通过在使用的证书里指定相关的User、Group来达到通过RBAC授权的目的

- 如果使用了kubelet TLS Boostrap机制，则不能再指定`--kubelet-certificate-authority`、`--kubelet-client-certificate`和`--kubelet-client-key`选项，否则后续kube-apiserver校验kubelet证书时出现`x509: certificate signed by unknown authority`错误

- `--admission-control`值必须包含ServiceAccount

- `--bind-address`不能为`127.0.0.1`

- `--service-cluster-ip-range`指定Service Cluster IP地址段，该地址段不能路由可达

- `--service-node-port-range=${NODE_PORT_RANGE}`指定 NodePort 的端口范围

- 缺省情况下kubernetes对象保存在`etcd /registry`路径下，可以通过`--etcd-prefix`参数进行调整

##### 启动kube-apiserver

``` bash
sudo cp kube-apiserver.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable kube-apiserver

<<'COMMENT'
Created symlink from /etc/systemd/system/multi-user.target.wants/kube-apiserver.service to /etc/systemd/system/kube-apiserver.service.
COMMENT

sudo systemctl start kube-apiserver
sudo systemctl status kube-apiserver

<<'COMMENT'
● kube-apiserver.service - Kubernetes API Server
   Loaded: loaded (/etc/systemd/system/kube-apiserver.service; enabled; vendor preset: disabled)
   Active: active (running) since Thu 2017-05-11 14:12:04 CST; 5s ago
     Docs: https://github.com/GoogleCloudPlatform/kubernetes
 Main PID: 5071 (kube-apiserver)
   CGroup: /system.slice/kube-apiserver.service
           └─5071 /root/local/bin/kube-apiserver --admission-control=NamespaceLifecycle,LimitRanger,ServiceAccount,DefaultStorageClass,ResourceQuota --a...

May 11 14:12:05 192-168-1-171.master kube-apiserver[5071]: I0511 14:12:05.787845    5071 wrap.go:75] GET /apis/rbac.authorization.k8s.io/v1beta1/...:52700]
May 11 14:12:05 192-168-1-171.master kube-apiserver[5071]: I0511 14:12:05.793909    5071 wrap.go:75] POST /apis/rbac.authorization.k8s.io/v1beta1...:52700]
May 11 14:12:05 192-168-1-171.master kube-apiserver[5071]: I0511 14:12:05.794291    5071 storage_rbac.go:196] created clusterrolebinding.rbac.aut...troller
May 11 14:12:05 192-168-1-171.master kube-apiserver[5071]: I0511 14:12:05.796895    5071 wrap.go:75] GET /apis/rbac.authorization.k8s.io/v1beta1/...:52700]
May 11 14:12:05 192-168-1-171.master kube-apiserver[5071]: I0511 14:12:05.803308    5071 wrap.go:75] POST /apis/rbac.authorization.k8s.io/v1beta1...:52700]
May 11 14:12:05 192-168-1-171.master kube-apiserver[5071]: I0511 14:12:05.803961    5071 storage_rbac.go:196] created clusterrolebinding.rbac.aut...llector
May 11 14:12:05 192-168-1-171.master kube-apiserver[5071]: I0511 14:12:05.806195    5071 wrap.go:75] GET /apis/rbac.authorization.k8s.io/v1beta1/...:52700]
May 11 14:12:05 192-168-1-171.master kube-apiserver[5071]: I0511 14:12:05.812121    5071 wrap.go:75] POST /apis/rbac.authorization.k8s.io/v1beta1...:52700]
May 11 14:12:05 192-168-1-171.master kube-apiserver[5071]: I0511 14:12:05.813210    5071 storage_rbac.go:196] created clusterrolebinding.rbac.aut...oscaler
May 11 14:12:05 192-168-1-171.master kube-apiserver[5071]: I0511 14:12:05.815368    5071 wrap.go:75] GET /apis/rbac.authorization.k8s.io/v1beta1/...:52700]
Hint: Some lines were ellipsized, use -l to show in full.
COMMENT
```

### 部署kube-controller-manager

##### kube-controller-manager.service

``` bash
cat > kube-controller-manager.service <<EOF 
[Unit]
Description=Kubernetes Controller Manager
Documentation=https://github.com/GoogleCloudPlatform/kubernetes

[Service]
ExecStart=/root/local/bin/kube-controller-manager \\
  --address=127.0.0.1 \\
  --master=http://${MASTER_IP}:8080 \\
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

- `--address`值必须为`127.0.0.1`，因为当前kube-apiserver期望scheduler 和 controller-manager在同一台机器

- `--master=http://{MASTER_IP}:8080`：使用非安全8080端口与kube-apiserver 通信

- `--cluster-cidr`指定Cluster中Pod的CIDR范围，该网段在各Node间必须路由可达(flanneld保证)

- `--service-cluster-ip-range`参数指定Cluster中Service的CIDR范围，该网络在各 Node间必须路由不可达，必须和kube-apiserver中的参数一致

- `--cluster-signing-*` 指定的证书和私钥文件用来签名为TLS BootStrap创建的证书和私钥

- `--root-ca-file`用来对kube-apiserver证书进行校验，指定该参数后，才会在Pod容器的ServiceAccount中放置该CA证书文件

- `--leader-elect=true`部署多台机器组成的master集群时选举产生一处于工作状态的 kube-controller-manager进程

##### 启动kube-controller-manager

``` bash
sudo cp kube-controller-manager.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable kube-controller-manager

<<'COMMENT'
Created symlink from /etc/systemd/system/multi-user.target.wants/kube-controller-manager.service to /etc/systemd/system/kube-controller-manager.service.
COMMENT

sudo systemctl start kube-controller-manager
sudo systemctl status kube-controller-manager

<<'COMMENT'
● kube-controller-manager.service - Kubernetes Controller Manager
   Loaded: loaded (/etc/systemd/system/kube-controller-manager.service; enabled; vendor preset: disabled)
   Active: active (running) since Thu 2017-05-11 14:18:11 CST; 3s ago
     Docs: https://github.com/GoogleCloudPlatform/kubernetes
 Main PID: 5132 (kube-controller)
   CGroup: /system.slice/kube-controller-manager.service
           └─5132 /root/local/bin/kube-controller-manager --address=127.0.0.1 --master=http://192.168.1.171:8080 --allocate-node-cidrs=true --service-cl...

May 11 14:18:12 192-168-1-171.master kube-controller-manager[5132]: I0511 14:18:12.397279    5132 controllermanager.go:427] Starting "replicaset"
May 11 14:18:12 192-168-1-171.master kube-controller-manager[5132]: I0511 14:18:12.398061    5132 controllermanager.go:437] Started "replicaset"
May 11 14:18:12 192-168-1-171.master kube-controller-manager[5132]: I0511 14:18:12.398088    5132 controllermanager.go:427] Starting "job"
May 11 14:18:12 192-168-1-171.master kube-controller-manager[5132]: I0511 14:18:12.408565    5132 controllermanager.go:437] Started "job"
May 11 14:18:12 192-168-1-171.master kube-controller-manager[5132]: I0511 14:18:12.408649    5132 plugins.go:101] No cloud provider specified.
May 11 14:18:12 192-168-1-171.master kube-controller-manager[5132]: I0511 14:18:12.409078    5132 nodecontroller.go:219] Sending events to api server.
May 11 14:18:12 192-168-1-171.master kube-controller-manager[5132]: I0511 14:18:12.409478    5132 ttlcontroller.go:117] Starting TTL controller
May 11 14:18:12 192-168-1-171.master kube-controller-manager[5132]: I0511 14:18:12.409737    5132 resource_quota_controller.go:240] Starting resou...roller
May 11 14:18:12 192-168-1-171.master kube-controller-manager[5132]: I0511 14:18:12.409833    5132 replica_set.go:155] Starting ReplicaSet controller
May 11 14:18:12 192-168-1-171.master kube-controller-manager[5132]: I0511 14:18:12.560168    5132 garbagecollector.go:116] Garbage Collector: All ...arbage
Hint: Some lines were ellipsized, use -l to show in full.
COMMENT
```

### 部署kube-scheduler

##### kube-scheduler.service

``` bash
cat > kube-scheduler.service <<EOF
[Unit]
Description=Kubernetes Scheduler
Documentation=https://github.com/GoogleCloudPlatform/kubernetes

[Service]
ExecStart=/root/local/bin/kube-scheduler \\
  --address=127.0.0.1 \\
  --master=http://${MASTER_IP}:8080 \\
  --leader-elect=true \\
  --v=2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

##### 启动kube-scheduler

``` bash
sudo cp kube-scheduler.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable kube-scheduler

<<'COMMENT'
Created symlink from /etc/systemd/system/multi-user.target.wants/kube-scheduler.service to /etc/systemd/system/kube-scheduler.service.
COMMENT


sudo systemctl start kube-scheduler
sudo systemctl status kube-scheduler

<<'COMMENT'
● kube-scheduler.service - Kubernetes Scheduler
   Loaded: loaded (/etc/systemd/system/kube-scheduler.service; enabled; vendor preset: disabled)
   Active: active (running) since Thu 2017-05-11 14:19:27 CST; 3s ago
     Docs: https://github.com/GoogleCloudPlatform/kubernetes
 Main PID: 5190 (kube-scheduler)
   CGroup: /system.slice/kube-scheduler.service
           └─5190 /root/local/bin/kube-scheduler --address=127.0.0.1 --master=http://192.168.1.171:8080 --leader-elect=true --v=2

May 11 14:19:27 192-168-1-171.master systemd[1]: Started Kubernetes Scheduler.
May 11 14:19:27 192-168-1-171.master systemd[1]: Starting Kubernetes Scheduler...
May 11 14:19:28 192-168-1-171.master kube-scheduler[5190]: I0511 14:19:28.176209    5190 factory.go:300] Creating scheduler from algorithm provid...ovider'
May 11 14:19:28 192-168-1-171.master kube-scheduler[5190]: I0511 14:19:28.176379    5190 factory.go:346] Creating scheduler with fit predicates '...eDiskPr
May 11 14:19:28 192-168-1-171.master kube-scheduler[5190]: I0511 14:19:28.176818    5190 leaderelection.go:179] attempting to acquire leader lease...
May 11 14:19:28 192-168-1-171.master kube-scheduler[5190]: I0511 14:19:28.211692    5190 leaderelection.go:189] successfully acquired lease kube-...heduler
May 11 14:19:28 192-168-1-171.master kube-scheduler[5190]: I0511 14:19:28.213323    5190 event.go:217] Event(v1.ObjectReference{Kind:"Endpoints", Namesp...
Hint: Some lines were ellipsized, use -l to show in full.
COMMENT
```

### 检验Master功能

``` bash
kubectl get componentstatuses
<<'COMMENT'
NAME                 STATUS    MESSAGE              ERROR
scheduler            Healthy   ok                   
controller-manager   Healthy   ok                   
etcd-0               Healthy   {"health": "true"}   
etcd-2               Healthy   {"health": "true"}   
etcd-1               Healthy   {"health": "true"}  
COMMENT
```


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/26/Deploy-Master-Of-K8s/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。

