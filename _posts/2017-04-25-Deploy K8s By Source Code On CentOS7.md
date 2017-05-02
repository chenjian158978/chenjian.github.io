---
layout:     post
title:      "在CentOS7上使用二进制方式部署Kubernetes"
subtitle:   "Deploy K8s By Source Code On CentOS7"
date:       Tue, Apr 25 2017 13:17:35 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-K8s-By-Source-Code-On-CentOS7/head_blog.jpg"
catalog:    true
tags:
    - 工作
    - Kubernetes
---

### 申明

此系列博文在学习[opsnull/follow-me-install-kubernetes-cluster](https://github.com/opsnull/follow-me-install-kubernetes-cluster)后实践和总结完成，大体与其相似，但会进一步重构文章结构与补充细节内容。

感谢作者**opsnull**的分享与努力，如有兴趣请star或者fork他的项目。


### 系列博文

- [在CentOS7上使用二进制方式部署Kubernetes](https://o-my-chenjian.com/2017/04/25/Deploy-K8s-By-Source-Code-On-CentOS7/)
- [Kubernetes集群之安全设置](https://o-my-chenjian.com/2017/04/25/Security-Settings-Of-K8s/)
- [Kubernetes集群之搭建ETCD集群](https://o-my-chenjian.com/2017/04/08/Deploy-Etcd-Cluster/)
- [Kubernetes集群之创建kubeconfig文件](https://o-my-chenjian.com/2017/04/26/Create-The-File-Of-Kubeconfig-For-K8s/)
- [Kubernetes集群之Master节点](https://o-my-chenjian.com/2017/04/26/Deploy-Master-Of-K8s/)
- [Kubernetes集群之Node节点](https://o-my-chenjian.com/2017/04/26/Deploy-Node-Of-K8s/)
- [带你玩转Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)
- [Kubernetes集群之Kubedns](https://o-my-chenjian.com/2017/04/26/Deploy-Kubedns-Of-K8s/)
- [Kubernetes集群之Dashboard](https://o-my-chenjian.com/2017/04/08/Deploy-Dashboard-With-K8s/)

### Kubernetes框架

![Kubernetes框架](/img/in-post/Deploy-K8s-By-Source-Code-On-CentOS7/k8s.jpg)


### 系统环境信息

- 操作系统： 
	- CentOS7 server版本
	- 用户名：administrator
	- 密码： nizhidaoyemeiyong
- 集群信息：

	|  类型  |     IP       | /etc/hosts | /etc/hostname|
	|:-----:|:------------:|:----------:|:-----:|
	| k8s-master | 192.168.1.171|127.0.0.1   192-168-1-171.master|192-168-1-171.master|
	| k8s-node | 192.168.1.173|127.0.0.1   192-168-1-173.node|192-168-1-173.node|
	| k8s-node | 192.168.1.174|127.0.0.1   192-168-1-174.node |192-168-1-174.node|
	| etcd-0 | 192.168.1.175|127.0.0.1   192-168-1-175.etcd|192-168-1-175.etcd|
	| etcd-1 | 192.168.1.176|127.0.0.1   192-168-1-176.etcd|192-168-1-176.etcd|
	| etcd-2 | 192.168.1.177|127.0.0.1   192-168-1-177.etcd|192-168-1-177.etcd|
- 操作权限
	- 所有操作均是`sudo su`下完成
- 软件版本
	- Kubernetes: 1.6.2
	- Docker： 17.04.0-ce
	- Etcd: 3.1.6
	- Flannel: 0.7.1
- 所有的资源可以在[这里](https://pan.baidu.com/s/1pLhmqzL)进行下载

### Kubernetes集群之安全设置

[Kubernetes集群之安全设置-详文](https://o-my-chenjian.com/2017/04/25/Security-Settings-Of-K8s/)
	
### Kubernetes集群之搭建ETCD集群

[Kubernetes集群之搭建ETCD集群-详文](https://o-my-chenjian.com/2017/04/08/Deploy-Etcd-Cluster/)

### Kubernetes集群之创建kubeconfig文件

[Kubernetes集群之创建kubeconfig文件-详文](https://o-my-chenjian.com/2017/04/26/Create-The-File-Of-Kubeconfig-For-K8s/)

### Kubernetes集群之Master节点

[Kubernetes集群之Master节点-详文](https://o-my-chenjian.com/2017/04/26/Deploy-Master-Of-K8s/)


### Kubernetes集群之Node节点

[Kubernetes集群之Node节点-详文](https://o-my-chenjian.com/2017/04/26/Deploy-Node-Of-K8s/)

### Kubernetes集群之Kubedns

[Kubernetes集群之Kubedns-详文](https://o-my-chenjian.com/2017/04/26/Deploy-Kubedns-Of-K8s/)

### Kubernetes集群之Dashboard

[Kubernetes集群之Dashboard-详文](https://o-my-chenjian.com/2017/04/08/Deploy-Dashboard-With-K8s/)





<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/25/Deploy-K8s-By-Source-Code-On-CentOS7/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。





