---
layout:     post
title:      "Deploy Monitoring With K8s"
subtitle:   "Be not far from me; for trouble is near;
for there is none to help. Psa 22:11"
date:       Sat, Apr 8 2017 09:31:44 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Monitoring-With-K8s/head_blog.jpg"
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

### Monitoring搭建

> 采用Grafana+Heapster+Influxdb

- 下载yaml文件

`git clone https://github.com/kubernetes/heapster.git`
	
- 将以下镜像放进私有库中

	- `gcr.io/google_containers/heapster_grafana:v3.1.1`

	- `kubernetes/heapster:canary`

	- `kubernetes/heapster_influxdb:v0.6` 

- 修改yaml文件

	* 在`/home/administrator/heapster/deploy/kube-config/influxdb`下6个文件，将image地址分别改为:
	
	`192.168.1.78:5000/grafana:v3.1.1`
	`192.168.1.78:5000/heapster:canary`
	`192.168.1.78:5000/influxdb:v0.6`
	
	* 在`influxdb-service.yaml`文件中，修改成：
	
``` bash
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
	
暴露出influxdb的8083端口，注意yaml的文件格式，以及**不要用tab键**

- 部署

``` bash
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

``` bash
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
	
``` bash
curl http://192.168.1.168:32735/api/datasources/proxy/1/query?db=k8s&q=SHOW%20DATABASES&epoch=ms
	
{"results":[{"series":[{"name":"databases","columns":["name"],"values":[["_internal"],["k8s"]]}]}]}
```
	
- 通过`http://192.168.1.167:4194`，`节点IP：4194`进入cAdvisor

- 查看influxdb的端口

``` bash
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

``` bash
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

``` docker
FROM 10.0.0.153:5000/k8s/heapster-grafana-amd64:v4.0.2
ADD run.sh /
RUN chmod 777 run.sh
```

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/08/Deploy-Monitoring-With-K8s/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。

