---
layout:     post
title:      "Kubernetes集群之Logging"
subtitle:   "Deploy Logging With K8s"
date:       Sat, Apr 8 2017 09:41:07 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Logging-With-K8s/head_blog.jpg"
catalog:    true
tags: [工作, Kubernetes]
---

### 使用kubeadm搭建Monitoring

##### 系列博文

- [在Linux上使用Kubeadm工具部署Kubernetes](https://o-my-chenjian.com/2016/12/08/Deploy-K8s-by-Kubeadm-on-Linux/)
- [带你玩转Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)
- [Kubernetes集群之搭建ETCD集群](https://o-my-chenjian.com/2017/04/08/Deploy-Etcd-Cluster/)
- [Kubernetes集群之Dashboard](https://o-my-chenjian.com/2017/04/08/Deploy-Dashboard-With-K8s/)
- [Kubernetes集群之Monitoring](https://o-my-chenjian.com/2017/04/08/Deploy-Monitoring-With-K8s/)
- [Kubernetes集群之Logging](https://o-my-chenjian.com/2017/04/08/Deploy-Logging-With-K8s/)
- [Kubernetes集群之Ingress](https://o-my-chenjian.com/2017/04/08/Deploy-Ingress-With-K8s/)
- [Kubernetes集群之Redis Sentinel集群](https://o-my-chenjian.com/2017/02/06/Deploy-Redis-Sentinel-Cluster-With-K8s/)
- [Kubernetes集群之Kafka和ZooKeeper](https://o-my-chenjian.com/2017/04/11/Deploy-Kafka-And-ZP-With-K8s/)

##### Yaml文件

> 采用Fluentd（用于收集、处理、传输日志数据）+ Elasticsearch（用于实时查询和解析数据）+ Kibana（用于数据可视化）。在整个集群搭建后部署logging，从而记录所有的服务起始，具体操作可以参考文献。

- 下载yaml文件

`git clone https://github.com/kubernetes/kubernetes.git`

1. Elasticsearch和Kibana在`/home/administrator/kubernetes/cluster/addons/fluentd-elasticsearch`中
	
2. Fluentd在`/home/administrator/kubernetes/cluster/saltbase/salt/fluentd-es`中
	
- 将以下镜像放进私有库中

	- `gcr.io/google_containers/fluentd-elasticsearch:1.20`

	- `gcr.io/google_containers/elasticsearch:v2.4.1`

	- `gcr.io/google_containers/kibana:v4.6.1`


- 修改yaml文件, 更改image地址
	
	- `192.168.1.78:5000/fluentd-elasticsearch:1.20`
	- `192.168.1.78:5000/elasticsearch:v2.4.1`
	- `192.168.1.78:5000/kibana:v4.6.1`

- 在`kibana-service.yaml`中添加`NodePort`，让其暴露出端口
	
``` bash
spec:
type: NodePort
ports:
	- port: 5601
```
	
- 更改`fluentd-es.yaml`
	
	* 将apiVersion改为extensions/v1beta1；
	* 将kind改为DaemonSet（让每个node都各创建一个）；
	* 加入template：
	
``` bash
spec:
template:
  metadata:
    namespace: kube-system
    labels:
      k8s-app: fluentd-logging
```
	
原本的spec以下的内容（第21行到第41行）移至同metadata平齐(右移四个空格)，在vim下面用`:21,41s/^/    /`命令

- 分别使用`create -f`和`describe`来创建与查看端口。进入kibana界面后，点create便可创建

### 使用二进制文件搭建Monitoring

该小节主要配合[kubernetes集群的的二进制安装](https://o-my-chenjian.com/2017/04/25/Deploy-K8s-By-Source-Code-On-CentOS7/)。由于环境变量等问题，不支持单独使用，如有需要请进一步阅读相关博文。

- 官方文件路径：`kubernetes/cluster/addons/fluentd-elasticsearch/`

- 所有的资源可以在[这里](https://pan.baidu.com/s/1pLhmqzL)进行下载

##### 系列博文

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


##### YAML文件

操作服务器IP：`192.168.1.171`，即`K8s-master`。在此之前，需要对服务器进行准备工作，具体操作请阅读[Kubernetes集群之安全设置](https://o-my-chenjian.com/2017/04/25/Security-Settings-Of-K8s/)

- es-controller.yaml

代码下载：[es-controller.yaml](/download/Deploy-Logging-With-K8s/es-controller.yaml)

``` yaml
apiVersion: v1
kind: ReplicationController
metadata:
  name: elasticsearch-logging-v1
  namespace: kube-system
  labels:
    k8s-app: elasticsearch-logging
    version: v1
    kubernetes.io/cluster-service: "true"
    addonmanager.kubernetes.io/mode: Reconcile
spec:
  replicas: 2
  selector:
    k8s-app: elasticsearch-logging
    version: v1
  template:
    metadata:
      labels:
        k8s-app: elasticsearch-logging
        version: v1
        kubernetes.io/cluster-service: "true"
    spec:
      serviceAccountName: elasticsearch
      containers:
      - image: gcr.io/google_containers/elasticsearch:v2.4.1-2
        name: elasticsearch-logging
        resources:
          # need more cpu upon initialization, therefore burstable class
          limits:
            cpu: 1000m
          requests:
            cpu: 100m
        ports:
        - containerPort: 9200
          name: db
          protocol: TCP
        - containerPort: 9300
          name: transport
          protocol: TCP
        volumeMounts:
        - name: es-persistent-storage
          mountPath: /data
        env:
        - name: "NAMESPACE"
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
      volumes:
      - name: es-persistent-storage
        emptyDir: {}

```

- es-rbac.yaml

代码下载：[es-rbac.yaml](/download/Deploy-Logging-With-K8s/es-rbac.yaml)

``` yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: elasticsearch
  namespace: kube-system

---

kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1alpha1
metadata:
  name: elasticsearch
subjects:
  - kind: ServiceAccount
    name: elasticsearch
    namespace: kube-system
roleRef:
  kind: ClusterRole
  name: view
  apiGroup: rbac.authorization.k8s.io
```

- es-service.yaml

代码下载：[es-service.yaml](/download/Deploy-Logging-With-K8s/es-service.yaml)

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: elasticsearch-logging
  namespace: kube-system
  labels:
    k8s-app: elasticsearch-logging
    kubernetes.io/cluster-service: "true"
    addonmanager.kubernetes.io/mode: Reconcile
    kubernetes.io/name: "Elasticsearch"
spec:
  ports:
  - port: 9200
    protocol: TCP
    targetPort: db
  selector:
    k8s-app: elasticsearch-logging

```

- fluentd-es-ds.yaml

代码下载：[fluentd-es-ds.yaml](/download/Deploy-Logging-With-K8s/fluentd-es-ds.yaml)

``` yaml
apiVersion: extensions/v1beta1
kind: DaemonSet
metadata:
  name: fluentd-es-v1.22
  namespace: kube-system
  labels:
    k8s-app: fluentd-es
    kubernetes.io/cluster-service: "true"
    addonmanager.kubernetes.io/mode: Reconcile
    version: v1.22
spec:
  template:
    metadata:
      labels:
        k8s-app: fluentd-es
        kubernetes.io/cluster-service: "true"
        version: v1.22
      # This annotation ensures that fluentd does not get evicted if the node
      # supports critical pod annotation based priority scheme.
      # Note that this does not guarantee admission on the nodes (#40573).
      annotations:
        scheduler.alpha.kubernetes.io/critical-pod: ''
    spec:
      serviceAccountName: fluentd
      containers:
      - name: fluentd-es
        image: gcr.io/google_containers/fluentd-elasticsearch:1.22
        command:
          - '/bin/sh'
          - '-c'
          - '/usr/sbin/td-agent 2>&1 >> /var/log/fluentd.log'
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 200Mi
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      nodeSelector:
        beta.kubernetes.io/fluentd-ds-ready: "true"
      terminationGracePeriodSeconds: 30
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers

```

**注意：这里面有个`nodeSelector `，要对需要添加该服务的node添加label**

- fluentd-es-rbac.yaml

代码下载：[fluentd-es-rbac.yaml](/download/Deploy-Logging-With-K8s/fluentd-es-rbac.yaml)

``` yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: fluentd
  namespace: kube-system

---

kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1alpha1
metadata:
  name: fluentd
subjects:
  - kind: ServiceAccount
    name: fluentd
    namespace: kube-system
roleRef:
  kind: ClusterRole
  name: view
  apiGroup: rbac.authorization.k8s.io
```

- kibana-controller.yaml

代码下载：[kibana-controller.yaml](/download/Deploy-Logging-With-K8s/kibana-controller.yaml)

``` yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: kibana-logging
  namespace: kube-system
  labels:
    k8s-app: kibana-logging
    kubernetes.io/cluster-service: "true"
    addonmanager.kubernetes.io/mode: Reconcile
spec:
  replicas: 1
  selector:
    matchLabels:
      k8s-app: kibana-logging
  template:
    metadata:
      labels:
        k8s-app: kibana-logging
    spec:
      containers:
      - name: kibana-logging
        image: gcr.io/google_containers/kibana:v4.6.1-1
        resources:
          # keep request = limit to keep this container in guaranteed class
          limits:
            cpu: 100m
          requests:
            cpu: 100m
        env:
          - name: "ELASTICSEARCH_URL"
            value: "http://elasticsearch-logging:9200"
          - name: "KIBANA_BASE_URL"
            value: "/api/v1/proxy/namespaces/kube-system/services/kibana-logging"
        ports:
        - containerPort: 5601
          name: ui
          protocol: TCP

```

- kibana-service.yaml

代码下载：[kibana-service.yaml](/download/Deploy-Logging-With-K8s/kibana-service.yaml)

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: kibana-logging
  namespace: kube-system
  labels:
    k8s-app: kibana-logging
    kubernetes.io/cluster-service: "true"
    addonmanager.kubernetes.io/mode: Reconcile
    kubernetes.io/name: "Kibana"
spec:
  ports:
  - port: 5601
    protocol: TCP
    targetPort: ui
  selector:
    k8s-app: kibana-logging

```

##### 创建Pod和service

``` sh
# 对Node上面添加label
kubectl get nodes
<<'COMMENT'
NAME            STATUS    AGE       VERSION
192.168.1.173   Ready     4d        v1.6.2
COMMENT

kubectl label nodes 192.168.1.173 beta.kubernetes.io/fluentd-ds-ready=true
<<'COMMENT'
node "192.168.1.173" labeled
COMMENT

kubectl create -f efk/
<<'COMMENT'
replicationcontroller "elasticsearch-logging-v1" created
serviceaccount "elasticsearch" created
clusterrolebinding "elasticsearch" created
service "elasticsearch-logging" created
daemonset "fluentd-es-v1.22" created
serviceaccount "fluentd" created
clusterrolebinding "fluentd" created
deployment "kibana-logging" created
service "kibana-logging" created
COMMENT

kubectl get pods --all-namespaces -o wide
<<'COMMENT'
NAMESPACE     NAME                                    READY     STATUS    RESTARTS   AGE       IP            NODE
default       my-nginx-3418754612-8rq1j               1/1       Running   0          3d        172.30.7.4    192.168.1.173
default       my-nginx-3418754612-q438g               1/1       Running   0          3d        172.30.7.5    192.168.1.173
default       nginx-ds-dfpmj                          1/1       Running   0          3d        172.30.7.2    192.168.1.173
kube-system   elasticsearch-logging-v1-k2vh9          1/1       Running   0          2m        172.30.7.12   192.168.1.173
kube-system   elasticsearch-logging-v1-qwb43          1/1       Running   0          2m        172.30.7.11   192.168.1.173
kube-system   fluentd-es-v1.22-shtq0                  1/1       Running   0          22s       172.30.7.13   192.168.1.173
kube-system   heapster-1554395288-4x2vz               1/1       Running   0          3d        172.30.7.8    192.168.1.173
kube-system   kibana-logging-3757371098-rlxr3         1/1       Running   0          2m        172.30.7.10   192.168.1.173
kube-system   kube-dns-3574069718-f6bwd               3/3       Running   0          3d        172.30.7.3    192.168.1.173
kube-system   kubernetes-dashboard-2970940268-nn9zb   1/1       Running   0          3d        172.30.7.6    192.168.1.173
kube-system   monitoring-grafana-3319647107-bcn3r     1/1       Running   0          3d        172.30.7.7    192.168.1.173
kube-system   monitoring-influxdb-2075516717-s4xqd    1/1       Running   0          3d        172.30.7.9    192.168.1.173
COMMENT

get svc --all-namespaces -o wide
<<'COMMENT'
NAMESPACE     NAME                    CLUSTER-IP       EXTERNAL-IP   PORT(S)                         AGE       SELECTOR
default       kubernetes              10.254.0.1       <none>        443/TCP                         4d        <none>
default       my-nginx                10.254.232.223   <none>        80/TCP                          3d        run=my-nginx
default       nginx-ds                10.254.74.254    <nodes>       80:48923/TCP                    3d        app=nginx-ds
kube-system   elasticsearch-logging   10.254.240.238   <none>        9200/TCP                        3m        k8s-app=elasticsearch-logging
kube-system   heapster                10.254.228.107   <none>        80/TCP                          3d        k8s-app=heapster
kube-system   kibana-logging          10.254.231.11    <none>        5601/TCP                        3m        k8s-app=kibana-logging
kube-system   kube-dns                10.254.0.2       <none>        53/UDP,53/TCP                   3d        k8s-app=kube-dns
kube-system   kubernetes-dashboard    10.254.173.52    <nodes>       80:38888/TCP                    3d        k8s-app=kubernetes-dashboard
kube-system   monitoring-grafana      10.254.35.229    <none>        80/TCP                          3d        k8s-app=grafana
kube-system   monitoring-influxdb     10.254.61.126    <nodes>       8086:34330/TCP,8083:40268/TCP   3d        k8s-app=influxdb
COMMENT
```

##### Kibana界面

**kibana Pod第一次启动时会用较长时间(10-20分钟)来优化和 Cache 状态页面**

非安全地址：`http://192.168.1.171:8080/api/v1/proxy/namespaces/kube-system/services/kibana-logging`

![Kibana界面](/img/in-post/Deploy-Logging-With-K8s/kibana.jpg)

### 参考博文

1. [Kubernetes 容器集群中的日志系统集成实践](https://juejin.im/entry/57a91c216be3ff00654978af)

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/08/Deploy-Logging-With-K8s/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。