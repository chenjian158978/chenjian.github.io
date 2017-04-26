---
layout:     post
title:      "Deploy Dashboard With K8s"
subtitle:   "Many bulls have compassed me:
strong bulls of Bashan have beset me round. Psa 22:12"
date:       Sat, Apr 8 2017 09:24:12 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Dashboard-With-K8s/head_blog.jpg"
catalog:    true
tags:
    - 工作
    - Kubernetes
---

### 使用kubeadm搭建Dashboard

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

##### 下载yaml文件

`https://rawgit.com/kubernetes/dadashboard/master/src/deploy/kubernetes-dashboard.yaml`
	
- 将镜像`gcr.io/google_containers/kubernetes-dadashboard-amd64:v1.5.0`放进私有库中

##### 修改yaml文件

	1. 去掉`imagePullPolicy: Always`,在[漠大神的博客](https://mritd.me/2016/10/29/set-up-kubernetes-cluster-by-kubeadm/#section-6)中将值改为IfNotPresent或者Never，但是仍然出错；
	
	2. image地址改为`192.168.1.78:5000/kubernetes-dashboard-amd64:v1.5.0`

#####  部署

``` bash
kubectl create -f kubernetes-dashboard.yaml

<<'COMMENT'
deployment "kubernetes-dashboard" created
service "kubernetes-dashboard" created
COMMENT
```

- 查看deployments

``` bash
kubectl get deployment --all-namespaces

<<'COMMENT'
NAMESPACE     NAME                   DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
kube-system   kube-discovery         1         1         1            1           22h
kube-system   kube-dns               1         1         1            1           22h
kube-system   kubernetes-dashboard   1         1         1            1           30m
COMMENT
```

	
- 查看service

``` bash
kubectl get service --all-namespaces

<<'COMMENT'
NAMESPACE     NAME                   CLUSTER-IP     EXTERNAL-IP   PORT(S)         AGE
default       kubernetes             10.96.0.1      <none>        443/TCP         23h
kube-system   kube-dns               10.96.0.10     <none>        53/UDP,53/TCP   23h
kube-system   kubernetes-dashboard   10.101.241.6   <nodes>       80/TCP          34m
COMMENT
```
	
- 查看dashboard的端口

``` bash
kubectl describe svc kubernetes-dashboard --namespace kube-system

<<'COMMENT'
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
COMMENT	
```

从中可以看出其类型为NodePort,端口为32688;或者可将该端口固定住(在yaml文件中的service中使用NodePort)。

- 访问dashboard
浏览器中输入：`http://192.168.1.168:32688/`即可

- 删除部署

``` bash
kubectl delete -f kubernetes-dashboard.yaml

<<'COMMENT'
deployment "kubernetes-dashboard" deleted
service "kubernetes-dashboard" deleted
COMMENT
```

- 查询Linux暴露出来的端口

``` bash
netstat -tnlp
```

### 使用二进制文件搭建Dashboard


该小节主要配合[kubernetes集群的的二进制安装](https://o-my-chenjian.com/2017/04/25/Deploy-K8s-By-Source-Code-On-CentOS7/)。由于环境变量等问题，不支持单独使用，如有需要请进一步阅读相关博文。

- 官方文件路径：`kubernetes/cluster/addons/dashboard`

- 所有的资源可以在[这里](https://pan.baidu.com/s/1pLhmqzL)进行下载


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

##### YAML文件

操作服务器IP：`192.168.1.171`，即`K8s-master`。在此之前，需要对服务器进行准备工作，具体操作请阅读Security Settings Of K8s

- dashboard-contoller.yaml

``` yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: kubernetes-dashboard
  namespace: kube-system
  labels:
    k8s-app: kubernetes-dashboard
    kubernetes.io/cluster-service: "true"
    addonmanager.kubernetes.io/mode: Reconcile
spec:
  selector:
    matchLabels:
      k8s-app: kubernetes-dashboard
  template:
    metadata:
      labels:
        k8s-app: kubernetes-dashboard
      annotations:
        scheduler.alpha.kubernetes.io/critical-pod: ''
    spec:
      serviceAccountName: dashboard
      containers:
      - name: kubernetes-dashboard
        image: gcr.io/google_containers/kubernetes-dashboard-amd64:v1.6.0
        resources:
          # keep request = limit to keep this container in guaranteed class
          limits:
            cpu: 100m
            memory: 50Mi
          requests:
            cpu: 100m
            memory: 50Mi
        ports:
        - containerPort: 9090
        livenessProbe:
          httpGet:
            path: /
            port: 9090
          initialDelaySeconds: 30
          timeoutSeconds: 30
      tolerations:
      - key: "CriticalAddonsOnly"
        operator: "Exists"
```

- dashboard-rbac.yaml

``` yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: dashboard
  namespace: kube-system

---

kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1alpha1
metadata:
  name: dashboard
subjects:
  - kind: ServiceAccount
    name: dashboard
    namespace: kube-system
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
```

- dashboard-service.yaml

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: kubernetes-dashboard
  namespace: kube-system
  labels:
    k8s-app: kubernetes-dashboard
    kubernetes.io/cluster-service: "true"
    addonmanager.kubernetes.io/mode: Reconcile
spec:
  type: NodePort 
  selector:
    k8s-app: kubernetes-dashboard
  ports:
  - port: 80
    targetPort: 9090
    nodePort: 8888
```

##### 创建Pod和service

``` bash
kubectl create -f dashboard/
<<'COMMENT'
deployment "kubernetes-dashboard" created
serviceaccount "dashboard" created
clusterrolebinding "dashboard" created
service "kubernetes-dashboard" created
COMMENT

# 检查 controller
get pods --all-namespaces -o wide

<<'COMMENT'
NAMESPACE     NAME                                    READY     STATUS    RESTARTS   AGE       IP           NODE
default       my-nginx-3418754612-2zb9g               1/1       Running   0          23m       172.17.0.4   192.168.1.173
default       my-nginx-3418754612-qtdhd               1/1       Running   0          23m       172.17.0.5   192.168.1.173
default       nginx-ds-3srdx                          1/1       Running   0          17h       172.17.0.2   192.168.1.173
kube-system   kube-dns-3574069718-m6rmr               3/3       Running   0          28m       172.17.0.3   192.168.1.173
kube-system   kubernetes-dashboard-2970940268-n5df0   1/1       Running   0          59s       172.17.0.6   192.168.1.173
COMMENT

kubectl get svc --all-namespaces -o wide

<<'COMMENT'
NAMESPACE     NAME                   CLUSTER-IP      EXTERNAL-IP   PORT(S)         AGE       SELECTOR
default       kubernetes             10.254.0.1      <none>        443/TCP         21h       <none>
default       my-nginx               10.254.5.222    <none>        80/TCP          23m       run=my-nginx
default       nginx-ds               10.254.79.44    <nodes>       80:8966/TCP     17h       app=nginx-ds
kube-system   kube-dns               10.254.0.2      <none>        53/UDP,53/TCP   29m       k8s-app=kube-dns
kube-system   kubernetes-dashboard   10.254.139.40   <nodes>       80:8888/TCP     1m        k8s-app=kubernetes-dashboard
COMMENT
```

##### 访问Dashboard

地址：`http://192.168.1.173:8888`


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/08/Deploy-Dashboard-With-K8s/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
