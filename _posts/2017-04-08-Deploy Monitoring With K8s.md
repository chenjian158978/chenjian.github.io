---
layout:     post
title:      "Kubernetes集群之Monitoring"
subtitle:   "Deploy Monitoring With K8s"
date:       Sat, Apr 8 2017 09:31:44 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Monitoring-With-K8s/head_blog.jpg"
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

### 使用二进制文件搭建Monitoring

该小节主要配合[kubernetes集群的的二进制安装](https://o-my-chenjian.com/2017/04/25/Deploy-K8s-By-Source-Code-On-CentOS7/)。由于环境变量等问题，不支持单独使用，如有需要请进一步阅读相关博文。

- 官方文件路径：`heapster/deploy/kube-config/influxdb`

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

- grafana-deployment.yaml

代码下载：[grafana-deployment.yaml](/download/Deploy-Monitoring-With-K8s/grafana-deployment.yaml)

``` yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: monitoring-grafana
  namespace: kube-system
spec:
  replicas: 1
  template:
    metadata:
      labels:
        task: monitoring
        k8s-app: grafana
    spec:
      containers:
      - name: grafana
        image: gcr.io/google_containers/heapster-grafana-amd64:v4.0.2
        ports:
          - containerPort: 3000
            protocol: TCP
        volumeMounts:
        - mountPath: /var
          name: grafana-storage
        env:
        - name: INFLUXDB_HOST
          value: monitoring-influxdb
        - name: GRAFANA_PORT
          value: "3000"
        - name: GF_AUTH_BASIC_ENABLED
          value: "false"
        - name: GF_AUTH_ANONYMOUS_ENABLED
          value: "true"
        - name: GF_AUTH_ANONYMOUS_ORG_ROLE
          value: Admin
        - name: GF_SERVER_ROOT_URL
          # If you're only using the API Server proxy, set this value instead:
          value: /api/v1/proxy/namespaces/kube-system/services/monitoring-grafana/
          # value: /
      volumes:
      - name: grafana-storage
        emptyDir: {}

```

**需要将`GF_SERVER_ROOT_URL`设置为`/api/v1/proxy/namespaces/kube-system/services/monitoring-grafana/`**

- grafana-service.yaml

代码下载：[grafana-service.yaml](/download/Deploy-Monitoring-With-K8s/grafana-service.yaml)

``` yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    kubernetes.io/cluster-service: 'true'
    kubernetes.io/name: monitoring-grafana
  name: monitoring-grafana
  namespace: kube-system
spec:
  ports:
  - port: 80
    targetPort: 3000
  selector:
    k8s-app: grafana

```

- heapster-deployment.yaml

代码下载：[heapster-deployment.yaml](/download/Deploy-Monitoring-With-K8s/heapster-deployment.yaml)

``` yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: heapster
  namespace: kube-system
spec:
  replicas: 1
  template:
    metadata:
      labels:
        task: monitoring
        k8s-app: heapster
    spec:
      serviceAccountName: heapster
      containers:
      - name: heapster
        image: gcr.io/google_containers/heapster-amd64:v1.3.0-beta.1
        imagePullPolicy: IfNotPresent
        command:
        - /heapster
        - --source=kubernetes:https://kubernetes.default
        - --sink=influxdb:http://monitoring-influxdb:8086

```

- heapster-rbac.yaml

代码下载：[heapster-rbac.yaml](/download/Deploy-Monitoring-With-K8s/heapster-rbac.yaml)

``` yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: heapster
  namespace: kube-system

---

kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1alpha1
metadata:
  name: heapster
subjects:
  - kind: ServiceAccount
    name: heapster
    namespace: kube-system
roleRef:
  kind: ClusterRole
  name: system:heapster
  apiGroup: rbac.authorization.k8s.io

```

- heapster-service.yaml

代码下载：[heapster-service.yaml](/download/Deploy-Monitoring-With-K8s/heapster-service.yaml)

``` yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    task: monitoring
    kubernetes.io/cluster-service: 'true'
    kubernetes.io/name: Heapster
  name: heapster
  namespace: kube-system
spec:
  ports:
  - port: 80
    targetPort: 8082
  selector:
    k8s-app: heapster

```

- influxdb-cm.yaml

代码下载：[influxdb-cm.yaml](/download/Deploy-Monitoring-With-K8s/influxdb-cm.yaml)

``` yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: influxdb-config
  namespace: kube-system
data:
  config.toml: |
    reporting-disabled = true
    bind-address = ":8088"

    [meta]
      dir = "/data/meta"
      retention-autocreate = true
      logging-enabled = true

    [data]
      dir = "/data/data"
      wal-dir = "/data/wal"
      query-log-enabled = true
      cache-max-memory-size = 1073741824
      cache-snapshot-memory-size = 26214400
      cache-snapshot-write-cold-duration = "10m0s"
      compact-full-write-cold-duration = "4h0m0s"
      max-series-per-database = 1000000
      max-values-per-tag = 100000
      trace-logging-enabled = false

    [coordinator]
      write-timeout = "10s"
      max-concurrent-queries = 0
      query-timeout = "0s"
      log-queries-after = "0s"
      max-select-point = 0
      max-select-series = 0
      max-select-buckets = 0

    [retention]
      enabled = true
      check-interval = "30m0s"

    [admin]
      enabled = true
      bind-address = ":8083"
      https-enabled = false
      https-certificate = "/etc/ssl/influxdb.pem"

    [shard-precreation]
      enabled = true
      check-interval = "10m0s"
      advance-period = "30m0s"

    [monitor]
      store-enabled = true
      store-database = "_internal"
      store-interval = "10s"

    [subscriber]
      enabled = true
      http-timeout = "30s"
      insecure-skip-verify = false
      ca-certs = ""
      write-concurrency = 40
      write-buffer-size = 1000

    [http]
      enabled = true
      bind-address = ":8086"
      auth-enabled = false
      log-enabled = true
      write-tracing = false
      pprof-enabled = false
      https-enabled = false
      https-certificate = "/etc/ssl/influxdb.pem"
      https-private-key = ""
      max-row-limit = 10000
      max-connection-limit = 0
      shared-secret = ""
      realm = "InfluxDB"
      unix-socket-enabled = false
      bind-socket = "/var/run/influxdb.sock"

    [[graphite]]
      enabled = false
      bind-address = ":2003"
      database = "graphite"
      retention-policy = ""
      protocol = "tcp"
      batch-size = 5000
      batch-pending = 10
      batch-timeout = "1s"
      consistency-level = "one"
      separator = "."
      udp-read-buffer = 0

    [[collectd]]
      enabled = false
      bind-address = ":25826"
      database = "collectd"
      retention-policy = ""
      batch-size = 5000
      batch-pending = 10
      batch-timeout = "10s"
      read-buffer = 0
      typesdb = "/usr/share/collectd/types.db"

    [[opentsdb]]
      enabled = false
      bind-address = ":4242"
      database = "opentsdb"
      retention-policy = ""
      consistency-level = "one"
      tls-enabled = false
      certificate = "/etc/ssl/influxdb.pem"
      batch-size = 1000
      batch-pending = 5
      batch-timeout = "1s"
      log-point-errors = true

    [[udp]]
      enabled = false
      bind-address = ":8089"
      database = "udp"
      retention-policy = ""
      batch-size = 5000
      batch-pending = 10
      read-buffer = 0
      batch-timeout = "1s"
      precision = ""

    [continuous_queries]
      log-enabled = true
      enabled = true
      run-interval = "1s"
```

**创建ConfigMap文件，将`[admin]接口中的enabled=false`改为`enabled=true`，从而开启influxdb中的UI界面。该yaml文件需要在其他插件创建前创建**

- influxdb-deployment.yaml

代码下载：[influxdb-deployment.yaml](/download/Deploy-Monitoring-With-K8s/influxdb-deployment.yaml)

``` yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: monitoring-influxdb
  namespace: kube-system
spec:
  replicas: 1
  template:
    metadata:
      labels:
        task: monitoring
        k8s-app: influxdb
    spec:
      containers:
      - name: influxdb
        image: gcr.io/google_containers/heapster-influxdb-amd64:v1.1.1
        volumeMounts:
        - mountPath: /data
          name: influxdb-storage
        - mountPath: /etc/
          name: influxdb-config
      volumes:
      - name: influxdb-storage
        emptyDir: {}
      - name: influxdb-config
        configMap:
          name: influxdb-config

```

- influxdb-service.yaml

代码下载：[influxdb-service.yaml](/download/Deploy-Monitoring-With-K8s/influxdb-service.yaml)

``` yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    task: monitoring
    kubernetes.io/cluster-service: 'true'
    kubernetes.io/name: monitoring-influxdb
  name: monitoring-influxdb
  namespace: kube-system
spec:
  type: NodePort
  ports:
  - port: 8086
    targetPort: 8086
    name: http
  - port: 8083
    targetPort: 8083
    name: admin
  selector:
    k8s-app: influxdb

```

**含有两个端口，其中8086为influxdb的API端口，8083为influxdb的UI端口**

##### 创建Pod和service

``` sh
kubectl create -f influxdb/influxdb-cm.yaml 
<<'COMMENT'
configmap "influxdb-config" created
COMMENT

kubectl create -f influxdb/

<<'COMMENT'
deployment "monitoring-grafana" created
service "monitoring-grafana" created
deployment "heapster" created
serviceaccount "heapster" created
clusterrolebinding "heapster" created
service "heapster" created
deployment "monitoring-influxdb" created
service "monitoring-influxdb" created
Error from server (AlreadyExists): error when creating "influxdb/influxdb-cm.yaml": configmaps "influxdb-config" already exists
COMMENT

kubectl get pods --all-namespaces -o wide
<<'COMMENT'
NAMESPACE     NAME                                    READY     STATUS    RESTARTS   AGE       IP           NODE
default       my-nginx-3418754612-8rq1j               1/1       Running   0          9m        172.30.7.4   192.168.1.173
default       my-nginx-3418754612-q438g               1/1       Running   0          9m        172.30.7.5   192.168.1.173
default       nginx-ds-dfpmj                          1/1       Running   0          34m       172.30.7.2   192.168.1.173
kube-system   heapster-1554395288-4x2vz               1/1       Running   0          6s        172.30.7.8   192.168.1.173
kube-system   kube-dns-3574069718-f6bwd               3/3       Running   0          10m       172.30.7.3   192.168.1.173
kube-system   kubernetes-dashboard-2970940268-nn9zb   1/1       Running   0          7m        172.30.7.6   192.168.1.173
kube-system   monitoring-grafana-3319647107-bcn3r     1/1       Running   0          6s        172.30.7.7   192.168.1.173
kube-system   monitoring-influxdb-2075516717-s4xqd    1/1       Running   0          6s        172.30.7.9   192.168.1.173
COMMENT

kubectl get svc --all-namespaces -o wide
<<'COMMENT'
NAMESPACE     NAME                   CLUSTER-IP       EXTERNAL-IP   PORT(S)                         AGE       SELECTOR
default       kubernetes             10.254.0.1       <none>        443/TCP                         1h        <none>
default       my-nginx               10.254.232.223   <none>        80/TCP                          9m        run=my-nginx
default       nginx-ds               10.254.74.254    <nodes>       80:48923/TCP                    34m       app=nginx-ds
kube-system   heapster               10.254.228.107   <none>        80/TCP                          13s       k8s-app=heapster
kube-system   kube-dns               10.254.0.2       <none>        53/UDP,53/TCP                   10m       k8s-app=kube-dns
kube-system   kubernetes-dashboard   10.254.173.52    <nodes>       80:38888/TCP                    6m        k8s-app=kubernetes-dashboard
kube-system   monitoring-grafana     10.254.35.229    <none>        80/TCP                          13s       k8s-app=grafana
kube-system   monitoring-influxdb    10.254.61.126    <nodes>       8086:34330/TCP,8083:40268/TCP   12s       k8s-app=influxdb
COMMENT
```

##### Dashboard界面

地址：`192.168.1.173:38888`

![Dashboard界面](/img/in-post/Deploy-Monitoring-With-K8s/dashboard.jpg)


##### Influxdb界面

地址：`192.168.1.173:40268`

其中的Port填写`34330`即可

![Influxdb界面](/img/in-post/Deploy-Monitoring-With-K8s/influxdb.jpg)

##### Grafana界面

非安全地址：`http://192.168.1.171:8080/api/v1/proxy/namespaces/kube-system/services/monitoring-grafana`

![Grafana界面](/img/in-post/Deploy-Monitoring-With-K8s/grafana.jpg)

### 添加邮件

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

