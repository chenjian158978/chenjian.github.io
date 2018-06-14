---
layout:     post
title:      "Prometheus和Grafana在Kubernetes上的使用"
subtitle:   "Deploy Prometheus And Grafana On Kubernetes"
date:       Sat, Jan 27 2018 00:00:41 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Prometheus-And-Grafana-On-Kubernetes/head_blog.jpg"
catalog:    true
tags: [工作, Kubernetes]
---

### 集群版本信息说明

| 组件名称 | 版本号 |
| :-----: | :---: |
| kubernetes | 1.8.1 |
| golang | 1.8.3 |
| docker | 17.06.2-ce |
| prometheus | v2.0.0 |
| grafana | 4.2.0 |
| kube-state-metrics | v1.2.0 |
| altermanager | v0.12.0 |

> 更改版本后，后续配置信息可能发生改变，需对照文档进行修改与更新

### 镜像信息说明

| 镜像名称 | tag号 |
| :-----: | :---: |
| prom/prometheus | v2.0.0 |
| prom/node-exporter | v0.15.2 |
| dockermuenster/caddy | 0.9.3 |
| giantswarm/tiny-tools | latest |
| gcr.io/google_containers/kube-state-metrics | v1.2.0 |
| grafana/grafana | 4.6.3 |
| quay.io/prometheus/alertmanager | v0.12.0 |

### yaml文件说明

yaml原版来自于[giantswarm/kubernetes-prometheus](https://github.com/giantswarm/kubernetes-prometheus)。

经过改动，问题可以查看项目的`Issues`。

| YAML文件 | 下载链接 |
| :-----: | :-----: |
| alertmanager-configmap.yaml | [点击下载](/download/Deploy-Prometheus-And-Grafana-On-Kubernetes/alertmanager-configmap.yaml) |
| alertmanager-templates.yaml | [点击下载](/download/Deploy-Prometheus-And-Grafana-On-Kubernetes/alertmanager-templates.yaml) |
| alertmanager.yaml | [点击下载](/download/Deploy-Prometheus-And-Grafana-On-Kubernetes/alertmanager.yaml) |
| grafana-import-dashboards-configmap.yaml | [点击下载](/download/Deploy-Prometheus-And-Grafana-On-Kubernetes/grafana-import-dashboards-configmap.yaml) |
| grafana-import-dashboards.yaml | [点击下载](/download/Deploy-Prometheus-And-Grafana-On-Kubernetes/grafana-import-dashboards.yaml) |
| grafana.yaml | [点击下载](/download/Deploy-Prometheus-And-Grafana-On-Kubernetes/grafana.yaml) |
| kube-state-metrics-rbac.yaml | [点击下载](/download/Deploy-Prometheus-And-Grafana-On-Kubernetes/kube-state-metrics-rbac.yaml) |
| kube-state-metrics.yaml | [点击下载](/download/Deploy-Prometheus-And-Grafana-On-Kubernetes/kube-state-metrics.yaml) |
| node-directory-size-metrics.yaml | [点击下载](/download/Deploy-Prometheus-And-Grafana-On-Kubernetes/node-directory-size-metrics.yaml) |
| prometheus-configmap.yaml | [点击下载](/download/Deploy-Prometheus-And-Grafana-On-Kubernetes/prometheus-configmap.yaml) |
| prometheus-node-exporter.yaml | [点击下载](/download/Deploy-Prometheus-And-Grafana-On-Kubernetes/prometheus-node-exporter.yaml) |
| prometheus-rbac.yaml | [点击下载](/download/Deploy-Prometheus-And-Grafana-On-Kubernetes/prometheus-rbac.yaml) |
| prometheus-rules.yaml | [点击下载](/download/Deploy-Prometheus-And-Grafana-On-Kubernetes/prometheus-rules.yaml) |
| prometheus.yaml | [点击下载](/download/Deploy-Prometheus-And-Grafana-On-Kubernetes/prometheus.yaml) |

### Prometheus模块

#### args问题

采用版本`v2.0.0`，其中注意`args`里的参数与老版本不同，具体可以运行`./prometheus -h`来参考，例如：

``` shell
--storage.tsdb.retention=12h
--storage.tsdb.path=/prometheus
--config.file=/etc/prometheus/prometheus.yaml
```

#### prometheus-configmap文件

采用configmap挂载到`/etc/prometheus/prometheus.yaml`，可以参考官方文档[CONFIGURATION](https://prometheus.io/docs/prometheus/2.0/configuration/configuration/#configuration)

- - scrape_interval默认参数为15s，该参数需要小与查询语句中的范围值(例如，1m)

- - scrage_configs为抓取对象，以`job_name`为单位。这里包含以下抓取对象（均以/metrics结尾）：

``` shell
1.  app为prometheus，component为core，端口为9090；
2.  app为prometheus，component为node-exporter，端口为9100；
3.  app为kube-state-metrics，端口为8080；
4.  app为alertmanager，端口为9093；
5.  app为kubelet，端口为10255；
6.  app为node-directory-size-metric， 端口为9102；
7.  app为cadvisor，端口为4194。

备注：      
1. kubelet的启动参数"--cadvisor-port=0"可以关闭cadvisor的4194端口；
2. kubelet以10255端口的抓取种类较少；
3. kubelet的“ip:10255/metrics/cadvisor”与cadvisor的"ip:4194/metrics"抓取种类数量类似，但前者仍然偏少（例如：“process_start_time_seconds”）；
4. 具体可通过浏览器查看`ip:4194/metrics`来查看当前所有的query语句与其结果
```

#### prometheus-rules文件

`prometheus`采用`altermanager`来进行报警监控。

其中rules文件需要参考官方文档[ALERTING RULES](https://prometheus.io/docs/prometheus/2.0/configuration/alerting_rules/#alerting-rules)进行修改与编写。

同时其对应的配置在`prometheus-config.yaml`中如下：

``` yaml
...
    rule_files:
      - "/etc/prometheus-rules/alert-rules.yaml"
    alerting:
      alertmanagers:
        - static_configs:
          - targets:
            - "alertmanager:9093"
```

#### Prometheus界面

- Alerts

展示的便是写在`alert-rules.yaml`中，采用`yaml格式`。例如判断服务器是否启动，可以使用查询语句中的`up`，如下：

``` yaml
{% raw %}
- name: instance-down
  rules:
  - alert: InstanceDown
    expr: up{job="kubernetes-nodes"} == 0
    for: 1m
    labels:
      severity: page
    annotations:
      summary: "Instance {{ $labels.instance }} down"
      description: "{{ $labels.instance }} of job {{ $labels.job }} has been down for more than 1 minute."
{% endraw %}
```

- Status / Targets

可以看到抓取对象的地址(Endpoint)，状态(State)为UP，便签(Labels)，最近一次抓取时间(Last Scrape)等等

- Graph

输入查询语句进行查询，该功能非常重要，后续会讲到。

### Grafana模块

- 启动顺序

`grafana-import-dashboards-configmap.yaml`类型为`Job`，需在grafana启动后执行，执行前先挂载上`configmap`。

``` shell
kubectl create -f grafana.yaml
kubectl create -f grafana-import-dashboards-configmap.yaml
kubectl create -f grafana-import-dashboards.yaml
```

> 启动后，数据库自动导入，Dashboard自动建立

- 登录账户密码

`admin/admin`

### 自定义Dashboard

其实从网上下载别人做好的`yaml`文件，然后`kubectl create -f xxx.yaml`一下，就全部成功，并且bashboard也能正常显示，**这是再好不过的事情了**。

> 但是，很多问题让这种情况难以实现。我们不得不掌握一定基础的技术来摆脱对他人的依靠。

#### Grafana添加数据库

> 先大致看下[官方Using Prometheus in Grafana](http://docs.grafana.org/features/datasources/prometheus/)

> url根据具体情况进行改变

> grafana支持多种数据库，可从Grafana UI / Plugins /  Data source中查看

- Grafana UI / Data Sources / Add data source

- - Name: prometheus

- - Type: Prometheus

- - Url: http://prometheus:9090

- Add



#### Dashboard

dashboard可以通过导入`json`文件，操作：Grafana UI / Dashboards / Import / Upload .json File。

本文自动导入的json文件便在`grafana-import-dashboards-configmap.yaml`中。其实有很多做好的dashboard的json文件，可以从[官网与社区构建Dashboards](https://grafana.com/dashboards)上面寻找合适的，可以以数据库类型为分类，然后点击`Download JSON`来下载。当然这些做好的模板和组件版本相关，不一定适合使用者当前的版本。

在当前Dashboard中进行修改与更新，可以查看当前的配置，操作为菜单栏上的设置栏(齿轮状图标)中的`View JSON`。也可以保存当前的json文件，操作为菜单栏上的分享栏(分发状图标)中的`Export`。

从json文件中来看，grafana是按照`id`编号来划分各个种类，因为查看对应的json数据，便可查看id。例如希望整个模板都是`5s刷新`一次，便可填写以下内容：

``` json
...
"id": 1,
"links": [],
"refresh": "5s",
...
```

##### Templating

> 先大致看下[官方Templating](http://docs.grafana.org/reference/templating/)

在菜单栏上的设置栏(齿轮状图标)中选择：`Templating` / +New

以显示kubernetes的`node`值为例：

- Name: node

- Label: Node

- Type: Query

- Data source: prometheus

- Refresh: On Dashboard Load

- Query: label\_values(kube\_node\_info{app="kube-state-metrics"},node)

- Sort: Alphabetical(asc)

- Include All option: √

从query语句中能获得`master2，master1，master3`三个数据，通过sort对其进行排序。而include all option提供一个`All`值来全选所有数据。

Name中的`node`很重要，后续查询语句可以通过当前的值为条件再进行查询,例如

``` shell
# namespace值
label_values(namespace)

# 通过当前的namespace值，选出namespace中的pod
label_values(kube_pod_info{namespace="$namespace"},pod)

# 通过当前选的pod值，选出pod内的container
label_values(kube_pod_container_info{pod="$pod"},container)
```

### 查询语句

> 先大致看下[官方QUERYING PROMETHEUS](https://prometheus.io/docs/prometheus/2.0/querying/basics/)

**查询语句非常重要**，困难之处也在此处。

#### 查询语句变量

| Name | Description |
| :--: | :---------: |
|label_values(label) | Returns a list of label values for the label in every metric. |
|label_values(metric, label) | Returns a list of label values for the label in the specified metric.|
|metrics(metric)| Returns a list of metrics matching the specified metric regex.|
|query_result(query)|Returns a list of Prometheus query result for the query.|

例如：

``` shell
kube_pod_info{...xxx...,kubernetes_name="kube-state-metrics",kubernetes_namespace="kube-system",namespace="chenjian",...xxx...}
```
- - 其中`kube_pod_info`便为**metric值**;

- - 其中的`kubernetes_name`，`kubernetes_namespace`，`namespace`等均为`kube_pod_info`中**label值**；

- - 某些metric中还包含metric，或者metric中的label值来自其他metric的label值，便可使用**metrics(metric)**

`查询语句`可以通过以下方法查询到：

1. 通过浏览器访问各个抓取器(例如cadvisor，kube-state-metrics等)的地址，以cadvisor为例，地址则为`http://ip:4194/metrics`；

2. 通过浏览器进入prometheus界面，操作如：Prometheus UI / Graph。例如你需要知晓容器的cpu信息，便可输入`container cpu`，便可得到很多查询语句。

``` shell
# 从以上结果中选取一个查询语句，举例说明：
container_cpu_usage_seconds_total

# 可以获得很多结果，选择namespace为kube-system，则为：
container_cpu_usage_seconds_total{namespace="kube-system"}

# 可以获得很多结果，选择container_name为prometheus，则为：
container_cpu_usage_seconds_total{container_name="prometheus",namespace="kube-system"}

# 此时结果定位便比较清晰。
```

#### Querying OPERATORS & FUNCTIONS

> 先大致看下[官方OPERATORS](https://prometheus.io/docs/prometheus/latest/querying/operators/), 以及[官方FUNCTIONS](https://prometheus.io/docs/prometheus/latest/querying/functions/)

使用比较多的是：

-  使用正则表达式；

``` shell
# 可查询到namespace以“chenjian-”为开头，后续随意的所有字段
container_cpu_usage_seconds_total{namespace=~"^chenjian-.*"}
```

- 使用运算符；

``` shell
# 便可查询到image与pod_name均不为空的结果
container_cpu_usage_seconds_total{image!="",pod_name!=""}
```
        

- 一定时间段；

``` shell  
# 便可查询到1分钟内的结果
container_cpu_usage_seconds_total{instance="master1",container_name!="POD",pod_name=~"^prometheus.*"}[1m]
```
        

- rate与sum；

``` shell
# 便可查询到1分钟内每秒的平均值
rate(container_cpu_usage_seconds_total{instance="master1",container_name!="POD",pod_name=~"^prometheus.*"}[1m])
        

#  便可查询到1分钟内每秒平均值的总和
sum(rate(container_cpu_usage_seconds_total{instance="master1",container_name!="POD",pod_name=~"^prometheus.*"}[1m]))
```

- 在grafana中结合Templating使用：

``` shell
# 其中的"$node"便是Templating中的node，当选择“master1”时，查询语句便显示master1的memory数据结果
sum(container_memory_working_set_bytes{id="/",instance=~"^$node$"})
```    
        



### 参考博文

1. [Prometheus入门教程](http://caosiyang.github.io/2017/10/27/prometheus/)
2. [Prometheus入门](https://www.hi-linux.com/posts/25047.html)
3. [使用Prometheus监控kubernetes(k8s)集群](http://www.do1618.com/archives/595)
4. [Prometheus报警AlertManager实战](https://blog.qikqiak.com/post/alertmanager-of-prometheus-in-practice/)
5. [使用prometheus自定义监控](https://www.jianshu.com/p/1f05476ebcee)
6. [prometheus官方文档](https://prometheus.io/docs/introduction/overview/)
7. [grafana官方文档](http://docs.grafana.org/)
8. [cAdvisor container_network_* metrics are coming with container_name="POD" instead of container_name="real name of container"](https://github.com/kubernetes/kubernetes/issues/43560)


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2018/01/27/Deploy-Prometheus-And-Grafana-On-Kubernetes/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
