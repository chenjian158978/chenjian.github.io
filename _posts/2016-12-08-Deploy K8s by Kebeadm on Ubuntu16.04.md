---
layout:     post
title:      "Deploy K8s by Kebeadm on Ubuntu16.04"
subtitle:   ""
date:       Thu, Dec 8 17:55:56 GMT+8
author:     "ChenJian"
header-img: "img/.jpg"
tags:
    - 工作
    - kubernetes
---

### 系统环境与IP
* 系统环境： ubuntu16.04.1-desktop-amd64, 使用清华的源
* 集群信息：
	- Master：192.168.1.167
	- Node: 192.168.1.168
	- Node: 192.168.1.169
	
	>*整个环境在VM下完成，可用master克隆出两个子机*

> **以下开始的所有操作，在192.168.1.167单点中的root权限下操作**

### 部分软件安装
- 安装VIM： `sudo apt-get install vim -y`
- 安装SSH：`sudo apt-get install openssh-server`
	- 启动SSH：`sudo service ssh start`
- 安装GIT： `sudo apt-get install git -y`

### DOCKER安装与设置

```sh
wget -qO- https://get.docker.com/ | sh

administrator@administrator167:~$ docker -v
Docker version 1.12.3, build 6b644ec
```

链接docker私有库：

- 解决https问题(用于ubuntu16.04，docker1.12)：`echo { \"insecure-registries\":[\"192.168.1.78:5000\"] } > /etc/docker/daemon.json`
- 重启docker服务：`sudo service docker restart`
- 更换镜像的tag：`docker tag 40a673399858 192.168.1.78:5000/docker-whale`
- 上传镜像： `docker push 192.168.1.78:5000/docker-whale`
- 下载镜像： `docker pull 192.168.1.78:5000/docker-whale`
- 浏览器输入：

``` sh
curl http://192.168.1.78:5000/v2/_catalog
	
{"repositories":["addon-resizer","docker-whale","grafana","heapster","influxdb","kube-ui","kube_test","kubedns-amd64","kubernetes-dashboard-amd64","llll","pause","test_docker"]}
```

- 查询镜像tag： 

``` sh
curl http://192.168.1.78:5000/v2/heapster/tags/list
	
"name":"heapster","tags":["v1","canary","latest"]}
```

**建立私有仓库，不仅能保护docker的安全性，有助于下载与上传，同时对于使用kubernets更加方便**

### 安装kubernets之前的准备

#### 修改Ubuntu主机名
由于在VM下进行master的克隆，则需要对新子机进行重新修改主机名：

- `sudo vim /etc/hostname`修改为想要的

``` sh
administrator167
```

- `sudo vim /etc/hosts`，改第二行`127.0.1.1 administrator167`

```sh
127.0.0.1       localhost
127.0.1.1       administrator167

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

- 重启计算机即可：`sudo reboot`

#### 制作kubelet kubeadm kubectl kubernetes-cni
由于网络缘故，无法直接像官网中的操作中直接`apt-get install`，所以需要自己制作所需的安装包。
查看自己的系统信息：

```sh
root@administrator167:/home/administrator# lsb_release -a

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

> 相关下载的deb文件可以从[这里](https://pan.baidu.com/s/1jHChOtK)下载

> 为避免再次下载这些deb文件，可以将其保存，其中`apt install`的包位置如下：

> ```sh
> administrator@administrator167:~$ ll /var/cache/apt/archives/kube*.deb
-rw-r--r-- 1 root root 12165700 12月  8 20:49 /var/cache/apt/archives/kubeadm_1.5.0-alpha.2-421-a6bea3d79b8bba-00_amd64.deb
-rw-r--r-- 1 root root 10292542 12月  8 20:44 /var/cache/apt/archives/kubectl_1.4.4-00_amd64.deb
-rw-r--r-- 1 root root 15701146 12月  8 20:37 /var/cache/apt/archives/kubelet_1.4.4-01_amd64.deb
-rw-r--r-- 1 root root  6873078 12月  8 20:32 /var/cache/apt/archives/kubernetes-cni_0.3.0.1-07a8a2-00_amd64.deb
> ```

#### 下载kubeadm需要的镜像

|images name | version |
|:----------:|:-------:|
|gcr.io/google_containers/kube-discovery-amd64|1.0|
|gcr.io/google_containers/kube-proxy-amd64|v1.4.4|
|gcr.io/google_containers/kube-scheduler-amd64|v1.4.4|
|gcr.io/google_containers/kube-controller-manager-amd64|v1.4.4|
|gcr.io/google_containers/kube-apiserver-amd64|v1.4.4|
|gcr.io/google_containers/etcd-amd64|2.2.5|
|gcr.io/google_containers/pause-amd64|3.0|
|gcr.io/google_containers/kubedns-amd64|1.7|
|gcr.io/google_containers/kube-dnsmasq-amd64|1.3|
|gcr.io/google_containers/exechealthz-amd64|1.1|
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
curl http://192.168.1.78:5000/v2/_catalog
	
{"repositories":["kube-apiserver-amd64","exechealthz-amd64","etcd-amd64","kube-controller-manager-amd64","kube-discovery-amd64","kube-dnsmasq-amd64","kube-proxy-amd64","kube-scheduler-amd64","kubedns-amd64","pause-amd64"]}
```


### kubeadm初始化

```sh
kubeadm init --api-advertise-addresses 192.168.1.167  --use-kubernetes-version v1.4.6 --pod-network-cidr 10.244.0.0/16

Running pre-flight checks
<master/tokens> generated token: "e3b02c.5c85004416c2370c"
<master/pki> generated Certificate Authority key and certificate:
Issuer: CN=kubernetes | Subject: CN=kubernetes | CA: true
Not before: 2016-12-09 08:20:52 +0000 UTC Not After: 2026-12-07 08:20:52 +0000 UTC
Public: /etc/kubernetes/pki/ca-pub.pem
Private: /etc/kubernetes/pki/ca-key.pem
Cert: /etc/kubernetes/pki/ca.pem
<master/pki> generated API Server key and certificate:
Issuer: CN=kubernetes | Subject: CN=kube-apiserver | CA: false
Not before: 2016-12-09 08:20:52 +0000 UTC Not After: 2017-12-09 08:20:53 +0000 UTC
Alternate Names: [192.168.1.167 10.96.0.1 kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local]
Public: /etc/kubernetes/pki/apiserver-pub.pem
Private: /etc/kubernetes/pki/apiserver-key.pem
Cert: /etc/kubernetes/pki/apiserver.pem
<master/pki> generated Service Account Signing keys:
Public: /etc/kubernetes/pki/sa-pub.pem
Private: /etc/kubernetes/pki/sa-key.pem
<master/pki> created keys and certificates in "/etc/kubernetes/pki"
<util/kubeconfig> created "/etc/kubernetes/kubelet.conf"
<util/kubeconfig> created "/etc/kubernetes/admin.conf"
<master/apiclient> created API client configuration
<master/apiclient> created API client, waiting for the control plane to become ready
<master/apiclient> all control plane components are healthy after 162.920907 seconds
<master/apiclient> waiting for at least one node to register and become ready
<master/apiclient> first node is ready after 3.013021 seconds
<master/apiclient> attempting a test deployment
<master/apiclient> test deployment succeeded
<master/discovery> created essential addon: kube-discovery, waiting for it to become ready
<master/discovery> kube-discovery is ready after 1.005440 seconds
<master/addons> created essential addon: kube-proxy
<master/addons> created essential addon: kube-dns

Kubernetes master initialised successfully!

You can now join any number of machines by running the following on each node:

kubeadm join --token=e3b02c.5c85004416c2370c 192.168.1.167
```
1. 记住token的值，这个在后续需要
2. 如果init失败，下一次开始前输入：
	
	2.1 `kubeadm reset`
	
	2.2 `systemctl start kubelet.service`
3. `--api-advertise-addresses 192.168.1.167`设置指定的网络接口
4. `--use-kubernetes-version v1.4.6`设置k8s的版本
5. `--pod-network-cidr 10.244.0.0/16`设置指定的网段(Flannel选项)

### pod网络创建
采用*Flannel*：
`kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml`
这里会pull镜像quay.io/coreos/flannel-git:v0.6.1-28-g5dde68d-amd64，其托管在quay.io上，不需要梯子

### 查看集群状态

```sh
kubectl get pods --all-namespaces

NAMESPACE     NAME                                       READY     STATUS    RESTARTS   AGE
kube-system   dummy-2088944543-59wwx                     1/1       Running   0          3m
kube-system   etcd-administrator167                      1/1       Running   0          5m
kube-system   kube-apiserver-administrator167            1/1       Running   0          6m
kube-system   kube-controller-manager-administrator167   1/1       Running   0          3m
kube-system   kube-discovery-1150918428-593z5            1/1       Running   0          3m
kube-system   kube-dns-654381707-eyqdy                   2/3       Running   0          3m
kube-system   kube-flannel-ds-rkznr                      2/2       Running   0          10s
kube-system   kube-proxy-djxez                           1/1       Running   0          3m
kube-system   kube-scheduler-administrator167            1/1       Running   0          5m
```

> **到此，单节点的k8s集群已经搭建完成**

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

#### 查看集群节点信息

```sh
kubectl get nodes
NAME               STATUS    AGE
administrator167   Ready     21h
administrator168   Ready     13s
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
kubectl create -f kubernetes-dashboard.yaml
	
deployment "kubernetes-dashboard" created
service "kubernetes-dashboard" created
```

- 查看deployments

```sh
kubectl get deployment --all-namespaces
	
NAMESPACE     NAME                   DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
kube-system   kube-discovery         1         1         1            1           22h
kube-system   kube-dns               1         1         1            1           22h
kube-system   kubernetes-dashboard   1         1         1            1           30m
```
	
- 查看pod

```sh
kubectl get pods --all-namespaces
	
NAMESPACE     NAME                                       READY     STATUS    RESTARTS   AGE
kube-system   dummy-2088944543-59wwx                     1/1       Running   1          23h
kube-system   etcd-administrator167                      1/1       Running   1          23h
kube-system   kube-apiserver-administrator167            1/1       Running   1          23h
kube-system   kube-controller-manager-administrator167   1/1       Running   1          23h
kube-system   kube-discovery-1150918428-593z5            1/1       Running   1          23h
kube-system   kube-dns-654381707-eyqdy                   3/3       Running   7          23h
kube-system   kube-flannel-ds-rkznr                      2/2       Running   2          22h
kube-system   kube-flannel-ds-wiy3d                      2/2       Running   1          1h
kube-system   kube-proxy-djxez                           1/1       Running   1          23h
kube-system   kube-proxy-zsbk9                           1/1       Running   0          1h
kube-system   kube-scheduler-administrator167            1/1       Running   1          23h
kube-system   kubernetes-dashboard-1567724484-xrj6b      1/1       Running   0          31m
```
	
- 查看service

```sh
kubectl get service --all-namespaces
	
NAMESPACE     NAME                   CLUSTER-IP     EXTERNAL-IP   PORT(S)         AGE
default       kubernetes             10.96.0.1      <none>        443/TCP         23h
kube-system   kube-dns               10.96.0.10     <none>        53/UDP,53/TCP   23h
kube-system   kubernetes-dashboard   10.101.241.6   <nodes>       80/TCP          34m
```

- 查看某pod的具体信息

```sh
kubectl describe pod kubernetes-shboard-1567724484-xrj6b --namespace kube-system
 
Name:           kubernetes-dashboard-1567724484-xrj6b
Namespace:      kube-system
Node:           administrator168/192.168.1.168
Start Time:     Sat, 10 Dec 2016 14:55:50 +0800
Labels:         app=kubernetes-dashboard
            pod-template-hash=1567724484
Status:         Running
IP:             10.244.1.14
Controllers:    ReplicaSet/kubernetes-dashboard-1567724484
Containers:
kubernetes-dashboard:
Container ID:       docker://b1cb949f2231f76e641360f0cbde0330a3f20a5968ee8a4d8f006d3ed250c52d
Image:              192.168.1.78:5000/kubernetes-dashboard-amd64:v1.5.0
Image ID:           docker://sha256:e5133bac8024ac6c916f16df8790259b5504a800766bee87dcf90ec7d634a418
Port:               9090/TCP
State:              Running
  Started:          Sat, 10 Dec 2016 14:55:56 +0800
Ready:              True
Restart Count:      0
Liveness:           http-get http://:9090/ delay=30s timeout=30s period=10s #success=1 #failure=3
Volume Mounts:
  /var/run/secrets/kubernetes.io/serviceaccount from default-token-t0bmd (ro)
Environment Variables:      <none>
Conditions:
Type          Status
Initialized   True 
Ready         True 
PodScheduled  True 
Volumes:
default-token-t0bmd:
Type:       Secret (a volume populated by a Secret)
SecretName: default-token-t0bmd
QoS Class:      BestEffort
Tolerations:    dedicated=master:Equal:NoSchedule
Events:
FirstSeen     LastSeen        Count   From                            SubobjectPath                           Type            Reason          Message
---------     --------        -----   ----                            -------------                           --------        ------          -------
35m           35m             1       {default-scheduler }                                                    Normal          Scheduled       Successfully assigned kubernetes-dashboard-1567724484-xrj6b to administrator168
35m           35m             1       {kubelet administrator168}      spec.containers{kubernetes-dashboard}   Normal          Pulling         pulling image "192.168.1.78:5000/kubernetes-dashboard-amd64:v1.5.0"
35m           35m             1       {kubelet administrator168}      spec.containers{kubernetes-dashboard}   Normal          Pulled          Successfully pulled image "192.168.1.78:5000/kubernetes-dashboard-amd64:v1.5.0"
35m           35m             1       {kubelet administrator168}      spec.containers{kubernetes-dashboard}   Normal          Created         Created container with docker id b1cb949f2231; Security:[seccomp=unconfined]
35m           35m             1       {kubelet administrator168}      spec.containers{kubernetes-dashboard}   Normal          Started         Started container with docker id b1cb949f2231
```
从中可以看到这个pod的状态为running，部署在administrator168/192.168.1.168的节点上
	
- 查看dashboard的端口

```sh
kubectl describe svc kubernetes-dashboard --namespace kube-system
	
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
从中可以看出其类型为NodePort,端口为32688

- 访问dashboard
浏览器中输入：`http://192.168.1.168:32688/`即可

- 删除部署

```sh
kubectl delete -f kubernetes-dashboard.yaml
	
deployment "kubernetes-dashboard" deleted
service "kubernetes-dashboard" deleted
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

### Logging部署

> 采用Fluentd（用于收集、处理、传输日志数据）+ Elasticsearch（用于实时查询和解析数据）+ Kibana（用于数据可视化）

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


### 参考文献：
1.  [Installing Kubernetes on Linux with kubeadm](http://kubernetes.io/docs/getting-started-guides/kubeadm/)
2. [漠然博客](https://mritd.me/)
3. [ubuntu 16.04 L2TP](http://blog.csdn.net/hhbgk/article/details/52549816)
4. [Can not pull/push images after update docker to 1.12](http://stackoverflow.com/questions/38695515/can-not-pull-push-images-after-update-docker-to-1-12)
5. [Tear down](http://kubernetes.io/docs/getting-started-guides/kubeadm/#tear-down)
6. [storage-schema](https://github.com/kubernetes/heapster/blob/master/docs/storage-schema.md)
7. [influxdb](https://docs.influxdata.com/influxdb/v1.1/introduction/getting_started/)
8. [总结部署 Kubernetes+Heapster+InfluxDB+Grafana 详解](http://blog.csdn.net/qq_21398167/article/details/52920288)



