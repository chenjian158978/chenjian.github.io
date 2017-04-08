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
    - kubernetes
---

### 系列博文

- [Deploy K8s by Kubeadm on Linux](https://o-my-chenjian.com/2016/12/08/Deploy-K8s-by-Kubeadm-on-Linux/)
- [Easy With Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)
- [Deploy Etcd Cluster](https://o-my-chenjian.com/2017/04/08/Deploy-Etcd-Cluster/)
- [Deploy Dashboard With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Dashboard-With-K8s/)
- [Deploy Monitoring With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Monitoring-With-K8s/)
- [Deploy Logging With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Logging-With-K8s/)
- [Deploy Ingress With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Ingress-With-K8s/)

### Dashboard搭建

- 下载yaml文件

`https://rawgit.com/kubernetes/dadashboard/master/src/deploy/kubernetes-dashboard.yaml`
	
- 将镜像`gcr.io/google_containers/kubernetes-dadashboard-amd64:v1.5.0`放进私有库中

- 修改yaml文件

	1. 去掉`imagePullPolicy: Always`,在[漠大神的博客](https://mritd.me/2016/10/29/set-up-kubernetes-cluster-by-kubeadm/#section-6)中将值改为IfNotPresent或者Never，但是仍然出错；
	
	2. image地址改为`192.168.1.78:5000/kubernetes-dashboard-amd64:v1.5.0`

- 部署

``` bash
kubectl create -f kubernetes-dashboard.yaml
	
deployment "kubernetes-dashboard" created
service "kubernetes-dashboard" created
```

- 查看deployments

``` bash
kubectl get deployment --all-namespaces
	
NAMESPACE     NAME                   DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
kube-system   kube-discovery         1         1         1            1           22h
kube-system   kube-dns               1         1         1            1           22h
kube-system   kubernetes-dashboard   1         1         1            1           30m
```

	
- 查看service

``` bash
kubectl get service --all-namespaces
	
NAMESPACE     NAME                   CLUSTER-IP     EXTERNAL-IP   PORT(S)         AGE
default       kubernetes             10.96.0.1      <none>        443/TCP         23h
kube-system   kube-dns               10.96.0.10     <none>        53/UDP,53/TCP   23h
kube-system   kubernetes-dashboard   10.101.241.6   <nodes>       80/TCP          34m
```
	
- 查看dashboard的端口

``` bash
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

从中可以看出其类型为NodePort,端口为32688;或者可将该端口固定住(在yaml文件中的service中使用NodePort)。

- 访问dashboard
浏览器中输入：`http://192.168.1.168:32688/`即可

- 删除部署

``` bash
kubectl delete -f kubernetes-dashboard.yaml
	
deployment "kubernetes-dashboard" deleted
service "kubernetes-dashboard" deleted
```

- 查询Linux暴露出来的端口

``` bash
netstat -tnlp
```


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/08/Deploy-Dashboard-With-K8s/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
