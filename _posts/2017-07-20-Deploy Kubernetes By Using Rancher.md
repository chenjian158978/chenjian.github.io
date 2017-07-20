---
layout:     post
title:      "秒搭Kubernetes之使用Rancher"
subtitle:   "Deploy Kubernetes By Using Rancher"
date:       Thu, Jul 20 2017 11:02:38 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Kubernetes-By-Using-Rancher/head_blog.jpg"
catalog:    true
tags:
    - 工作
    - Kubernetes
    - Docker
---

### Rancher

在接触Docker和K8s的前阶段就耳闻目睹到Rancher，但是没有进一步接触过。直到将K8s搭建完成。才进一步了学习与实践Rancher。

Rancher是简便易用的容器管理。其中Rancher对Kubernetes的支持与维护特别用心，使其在生产环境中的基础设置里更易于搭建与使用。

**但实话实说，其一对于k8s的小白能通过rancher方便部署k8s，但在其封装下，不易理解k8s的内部实现。对于更多专业人士，推荐自己亲自搭建K8s；其二，对于生产中使用Rancher，建议需要更为专业的人士，不能将Rancher只是作为一个搭建平台而已。**

### 环境与版本说明

##### Rancher

Rancher 版本： v1.6.2

其中所需镜像：

|  镜像名称  | 镜像tag | 镜像备注 |
| :------: | :------: | :------: |
| rancher/server | stable | 服务镜像稳定版本 |
| rancher/agent | v1.2.2 | 代理镜像，每个节点都需要 |
| rancher/healthcheck | v0.3.1 | 健康查询镜像 |
| rancher/net | v0.11.2 | IPSEC网络 |
| rancher/net | holder | IPSEC网络 |
| rancher/metadata | v0.9.2 | network-services |
| rancher/dns | v0.15.1 | network-services |
| rancher/network-manager | v0.7.4 | network-services |
| rancher/scheduler | v0.8.2 | scheduler |

##### Docker

Docker 版本： 1.12.5

**Rancher对支持的Docker版本有相关规定，请仔细阅读官网文档**

##### Kubernetes

Kubernetes 版本: v1.5.4

其中所需镜像：

|  镜像名称  | 镜像tag | 镜像备注 |
| :------: | :------: | :------: |
| rancher/k8s  | v1.5.4-rancher1-4 | K8s基础镜像，包含kubelet，kube-controller-manager，kube-apiserver，kube-proxy，kube-scheduler  |
| rancher/etcd | v2.3.7-11 | Etcd镜像 |
| rancher/kubectld | v0.6.0 | kubectl镜像 |
| rancher/etc-host-updater | v0.0.2 | HOST升级 |
| rancher/lb-service-rancher | v0.6.1 | 负载均衡 |
| rancher/kubernetes-agent | v0.5.4 | K8s代理 |
| gcr.io/google_containers/heapster-influxdb-amd64 | v1.1.1 | heapster-influxdb |
| gcr.io/google_containers/heapster-grafana-amd64 | v4.0.2 | heapster-grafana |
| gcr.io/google_containers/heapster-amd64 | v1.3.0-beta.1 | heapster |
| gcr.io/kubernetes-helm/tiller | v2.1.3 | helm | 
| gcr.io/google_containers/kubernetes-dashboard-amd64 | v1.5.0 |kubernetes-dashboard |
| gcr.io/google_containers/kubedns-amd64 | 1.9 | kubedns |
| gcr.io/google_containers/dnsmasq-metrics-amd64 | 1.0 | dnsmasq-metrics |
| gcr.io/google_containers/kube-dnsmasq-amd64 | 1.4 | kube-dnsmasq |
| gcr.io/google_containers/pause-amd64 | 3.0 | 根容器 |

这些镜像均需加载到所需的寄主机中

##### 寄主机

操作系统： Centos7

|  寄主机名称  | 寄主机IP | 备注 |
| :------: | :------: | :------: |
| 192-168-1-175 | 192.168.1.175 | Rancher-Server |
| 192-168-1-176 | 192.168.1.176 | K8s-node-1 |
| 192-168-1-179 | 192.168.1.179 | K8s-node-2 |
| 192-168-1-180 | 192.168.1.180 | K8s-node-3 |

### Rancher启动

在寄主机`192-168-1-175`上操作：

``` sh
sudo docker run -d --restart=unless-stopped -p 8080:8080 rancher/server:stable
```

过一段时间，访问地址(http://192.168.1.175:8080/) 便可进入Rancher的界面。

随后在`系统管理-访问控制`中添加本地账户

### Rancher搭建配置原理

Rancher搭建以Kubernetes模版为基础，其定义以`rancher-catalog`中的`docker-compose.yml`和`rancher-compose.yml`为基础。

默认官方的`rancher-catalog`如下图所示：

![kube-system](/img/in-post/Deploy-Kubernetes-By-Using-Rancher/catalog.png)

这些yml文件当然也可以自己编写，通过在Rancher界面中的第四栏选择`系统管理-系统设置-应用商店`中，停用官方认证的Rancher，或者社区贡献，添加自定义的可以`git clone`的URl。名称填写`library`,地址填写`https://xxxxx.git`,分支选择你需要的分支即可。

**如果对Rancher和Kubernetes不是特别深入的学习，请勿随意修改这里面的值。当然这里面会涉及到相关镜像，可以修改为自己的，方便拉取**

命名空间kube-system中的`dashboard，heapster，grafana，helm`等等，其配置文件都在`镜像rancher/k8s:v1.5.4-rancher1-4`中的`/etc/kubernetes/addons/`中，这些服务的启动就依靠这些配置文件。

如果你想修改这些YAML配置问题——例如我想把其中的`imagePullPolicy: Always`这条去掉，避免始终去拉取相关镜像——你们需要重新制作这个镜像，则可以在`rancher/kubernetes-package`这个GitHub项目，需要clone到相对应分支或者tag的源码，加以修改，并创建镜像，其创建的镜像就是**rancher/k8s:v1.5.4-rancher1-4**

> 以上操作本人实践过，耗时较长，还没有成功过。主要是卡死在某些步骤上，涉及到一些插件或者依赖包。解决不重建镜像，又能修改配置的方法，可以在Kubernetes-UI中实现，修改完yaml文件，然后进行UPDATE

### 添加环境

在Rancher界面中的第一栏选择`环境管理-添加环境`中，填写`环境名称(k8stest)`和`环境模版(Kubernetes)`，然后点击`创建`，如下图

![添加环境](/img/in-post/Deploy-Kubernetes-By-Using-Rancher/add-env.jpg)

### 添加主机

在Rancher界面中的第三栏选择`基础框架-主机-添加主机`，认真阅读添加过程中的每一条，再将第五点的shell命令复制到每一台寄主机(192-168-1-176,192-168-1-179,192-168-1-180)上

``` sh
sudo docker run --rm --privileged -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/rancher:/var/lib/rancher rancher/agent:v1.2.2 http://192.168.1.175:8080/v1/scripts/02328C47DE9B1D32FEFD:1483142400000:JnFPIlUBltDshvrqejKH29ZpZE

<<'COMMENT'
INFO: Running Agent Registration Process, CATTLE_URL=http://192.168.1.175:8080/v1
INFO: Attempting to connect to: http://192.168.1.175:8080/v1
INFO: http://192.168.1.175:8080/v1 is accessible
INFO: Inspecting host capabilities
INFO: Boot2Docker: false
INFO: Host writable: true
INFO: Token: xxxxxxxx
INFO: Running registration
INFO: Printing Environment
INFO: ENV: CATTLE_ACCESS_KEY=122073EFDD6FFB401BE0
INFO: ENV: CATTLE_HOME=/var/lib/cattle
INFO: ENV: CATTLE_REGISTRATION_ACCESS_KEY=registrationToken
INFO: ENV: CATTLE_REGISTRATION_SECRET_KEY=xxxxxxx
INFO: ENV: CATTLE_SECRET_KEY=xxxxxxx
INFO: ENV: CATTLE_URL=http://192.168.1.175:8080/v1
INFO: ENV: DETECTED_CATTLE_AGENT_IP=192.168.1.176
INFO: ENV: RANCHER_AGENT_IMAGE=rancher/agent:v1.2.2
INFO: Deleting container rancher-agent
INFO: Launched Rancher Agent: 1c03d064165c071f64226dbce86365267300bc98094523272a381a3f3947b31b
COMMENT
```

如此完成后，等所有服务启动完成，即**Kubernetes的集群搭建完成**。

主机信息图如下图：

![主机信息](/img/in-post/Deploy-Kubernetes-By-Using-Rancher/host_info.jpg)

### 基础设施应用

在Rancher界面中的第二栏选择`KUBERNETES-基础设施应用`中，可以看到所有的基础应用。如下图所示：

![基础设施应用](/img/in-post/Deploy-Kubernetes-By-Using-Rancher/Infrastructure_apps.jpg)

在`应用kubernetes`中可以列表形式，链接图形式和编排文件形式(docker-compose.yml和rancher-compose.yml)来查看应用。

以链接图形式查看如下图所示：

![链接图形式](/img/in-post/Deploy-Kubernetes-By-Using-Rancher/linkmap.png)

*命名空间kube-system*中的服务这里并不能找到。需要在上述的`应用`中找，如下图所示：

![kube-system](/img/in-post/Deploy-Kubernetes-By-Using-Rancher/kube_system.png)

可以看出这里的镜像标签是端口号，内置的API是错误的。

### Kubernete仪表板

在Rancher界面中的第二栏选择`KUBERNETES-仪表板-Kubernete UI`，直接就跳入Dashboard的界面，如下图所示：

![Dashboard](/img/in-post/Deploy-Kubernetes-By-Using-Rancher/dashboard.jpg)

### Rancher重启

对于某些节点的清扫，一般用到以下命令：

``` sh
# 暂停所有容器
sudo docker stop `docker ps -aq`

# 删除所有容器
sudo docker rm `docker ps -aq`

# 删除所有容器volume
sudo docker volume rm $(docker volume ls -qf dangling=true)
```

### 参考

1. [Rancher-k8s加速安装文档](https://mp.weixin.qq.com/s/z9Xz84eDbXU3_lJl_KGw2w)
2. [Rancher使用入门](http://tonybai.com/2016/04/14/an-introduction-about-rancher/)
3. [CentOS7上Docker安装与卸载](http://www.cnblogs.com/w2206/p/7080498.html)
4. [Rancher实现的内部DNS基础服务](http://www.dockerinfo.net/278.html)
5. [如何hack一下Rancher Kubernetes](https://segmentfault.com/a/1190000007656432)


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/07/20/Deploy-Kubernetes-By-Using-Rancher/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。


































