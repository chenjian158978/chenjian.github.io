---
layout:     post
title:      "Deploy Logging With K8s"
subtitle:   "They gaped upon me with their mouths,
as a ravening and a roaring lion. Psa 22:13"
date:       Sat, Apr 8 2017 09:41:07 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Logging-With-K8s/head_blog.jpg"
catalog:    true
tags:
    - 工作
    - Kubernetes
---

### 系列博文

- [Deploy K8s by Kubeadm on Linux](https://o-my-chenjian.com/2016/12/08/Deploy-K8s-by-Kubeadm-on-Linux/)
- [Easy With Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)
- [Deploy Etcd Cluster](https://o-my-chenjian.com/2017/04/08/Deploy-Etcd-Cluster/)
- [Deploy Dashboard With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Dashboard-With-K8s/)
- [Deploy Monitoring With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Monitoring-With-K8s/)
- [Deploy Logging With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Logging-With-K8s/)
- [Deploy Ingress With K8s](https://o-my-chenjian.com/2017/04/08/Deploy-Ingress-With-K8s/)
- [Deploy Redis Sentinel Cluster With K8s](https://o-my-chenjian.com/2017/02/06/Deploy-Redis-Sentinel-Cluster-With-K8s/)
- [Deploy Kafka And ZP With K8s](https://o-my-chenjian.com/2017/04/11/Deploy-Kafka-And-ZP-With-K8s/)

### Logging搭建

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

### 参考

1. [Kubernetes 容器集群中的日志系统集成实践](https://juejin.im/entry/57a91c216be3ff00654978af)

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/08/Deploy-Logging-With-K8s/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。