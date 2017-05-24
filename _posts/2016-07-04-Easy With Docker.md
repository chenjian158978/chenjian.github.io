---
layout:     post
title:      "带你玩转Docker"
subtitle:   "Easy With Docker"
date:       Mon, July 4 2016 17:32:07 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Easy-With-Docker/head_blog.jpg"
catalog:     true
tags:
    - 工作
    - Docker
---

### 系列博文

基于Docker容器化上的集群管理，可以使用Kubernetes。以下含有两种部署Kubernetes的方法：

##### 使用Kubeadm工具部署Kubernetes

- [在Linux上使用Kubeadm工具部署Kubernetes](https://o-my-chenjian.com/2016/12/08/Deploy-K8s-by-Kubeadm-on-Linux/)
- [带你玩转Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)
- [Kubernetes集群之搭建ETCD集群](https://o-my-chenjian.com/2017/04/08/Deploy-Etcd-Cluster/)
- [Kubernetes集群之Dashboard](https://o-my-chenjian.com/2017/04/08/Deploy-Dashboard-With-K8s/)
- [Kubernetes集群之Monitoring](https://o-my-chenjian.com/2017/04/08/Deploy-Monitoring-With-K8s/)
- [Kubernetes集群之Logging](https://o-my-chenjian.com/2017/04/08/Deploy-Logging-With-K8s/)
- [Kubernetes集群之Ingress](https://o-my-chenjian.com/2017/04/08/Deploy-Ingress-With-K8s/)
- [Kubernetes集群之Redis Sentinel集群](https://o-my-chenjian.com/2017/02/06/Deploy-Redis-Sentinel-Cluster-With-K8s/)
- [Kubernetes集群之Kafka和ZooKeeper](https://o-my-chenjian.com/2017/04/11/Deploy-Kafka-And-ZP-With-K8s/)


##### 使用二进制方式部署Kubernetes

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


### docker安装

注：docker需在root权限下运行

##### Ubuntu16.04

```bash
wget -qO- https://get.docker.com/ | sh

docker -v
<<'COMMENT'
Docker version 1.12.3, build 6b644ec
COMMENT
```

##### CentOS7之使用wget安装

所需的两个docker的rpm文件的链接：[kubeadm-rpm](https://pan.baidu.com/s/1pLrrlCR)

然后，`sudo yum install * -y`


命令：`wget -qO- https://get.docker.com/ | sh `

查看docker版本：`docker --version`

结果：

```
Docker version 1.11.2, build b9f10c9
```

##### CentOS7之二进制文件安装

该小节主要配合[kubernetes集群的的二进制安装](https://o-my-chenjian.com/2017/04/25/Deploy-K8s-By-Source-Code-On-CentOS7/)。由于环境变量等问题，不支持单独使用，如有需要请进一步阅读相关博文。

> 下载docker二进制文件

``` bash
wget https://get.docker.com/builds/Linux/x86_64/docker-17.04.0-ce.tgz
tar -xvf docker-17.04.0-ce.tgz
cp docker/{docker,docker*} /root/local/bin
```

> docker.service

``` bash
cat > docker.service <<EOF
[Unit]
Description=Docker Application Container Engine
Documentation=http://docs.docker.io

[Service]
Environment="PATH=/root/local/bin:/bin:/sbin:/usr/bin:/usr/sbin"
EnvironmentFile=-/run/flannel/docker
ExecStart=/root/local/bin/dockerd --log-level=error \$DOCKER_NETWORK_OPTIONS
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=on-failure
RestartSec=5
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
Delegate=yes
KillMode=process

[Install]
WantedBy=multi-user.target
EOF
```

- dockerd运行时会调用其它docker命令，如docker-proxy，所以需要将docker命令所在的目录加到PATH环境变量中

- flanneld启动时将网络配置写入到`/run/flannel/docker`文件中的变量`DOCKER_NETWORK_OPTIONS`，dockerd命令行上指定该变量值来设置`docker0`网桥参数。由此可以看出docker服务的启动在需要此参数的前提下，需要先安装Flanneld服务

- 不能关闭默认开启的`--iptables`和`--ip-masq`选项；

- 如果内核版本比较新，建议使用`overlay`存储驱动；

- docker从`1.13`版本开始，可能将`iptables FORWARD chain`的默认策略设置为DROP，从而导致ping其它Node上的Pod IP失败，遇到这种情况时，需要手动设置策略为 ACCEPT：

``` bash
# 设置iptalbes
iptables -L
<<'COMMENT'
Chain FORWARD (policy DROP)
target     prot opt source               destination         
DOCKER-ISOLATION  all  --  anywhere             anywhere            
ACCEPT     all  --  anywhere             anywhere             ctstate RELATED,ESTABLISHED
DOCKER     all  --  anywhere             anywhere            
ACCEPT     all  --  anywhere             anywhere            
ACCEPT     all  --  anywhere             anywhere            
COMMENT

iptables -P FORWARD ACCEPT

iptables -L
<<'COMMENT'
Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         
DOCKER-ISOLATION  all  --  anywhere             anywhere            
ACCEPT     all  --  anywhere             anywhere             ctstate RELATED,ESTABLISHED
DOCKER     all  --  anywhere             anywhere            
ACCEPT     all  --  anywhere             anywhere            
ACCEPT     all  --  anywhere             anywhere          
COMMENT
```

> 启动 docker

``` bash
sudo cp docker.service /etc/systemd/system/docker.service
sudo systemctl daemon-reload
#sudo iptables -F && sudo iptables -X && sudo iptables -F -t nat && sudo iptables -X -t nat
sudo systemctl enable docker

<<'COMMENT'
Created symlink from /etc/systemd/system/multi-user.target.wants/docker.service to /etc/systemd/system/docker.service.
COMMENT

sudo systemctl start docker
sudo systemctl status docker

<<'COMMENT'
● docker.service - Docker Application Container Engine
   Loaded: loaded (/etc/systemd/system/docker.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2017-04-24 15:30:01 CST; 8s ago
     Docs: http://docs.docker.io
 Main PID: 19017 (dockerd)
   Memory: 14.9M
   CGroup: /system.slice/docker.service
           ├─19017 /root/local/bin/dockerd --log-level=error
           └─19023 docker-containerd -l unix:///var/run/docker/libcontainerd/docker-containerd.sock --metrics-interval=0 --start-timeout 2m --state-dir ...

Apr 24 15:30:01 192-168-1-173.node systemd[1]: Started Docker Application Container Engine.
Apr 24 15:30:01 192-168-1-173.node systemd[1]: Starting Docker Application Container Engine...
COMMENT
```

> 查看docker版本

``` bash
docker version

<<'COMMENT'
Client:
 Version:      17.04.0-ce
 API version:  1.28
 Go version:   go1.7.5
 Git commit:   4845c56
 Built:        Wed Apr  5 23:33:17 2017
 OS/Arch:      linux/amd64

Server:
 Version:      17.04.0-ce
 API version:  1.28 (minimum version 1.12)
 Go version:   go1.7.5
 Git commit:   4845c56
 Built:        Wed Apr  5 23:33:17 2017
 OS/Arch:      linux/amd64
 Experimental: false
COMMENT
```

### 查看images列表

`docker images`


### 创建一个image

`docker build -t chenjian158978/wmcluster_sitealive .` 

#### 删除一个image

`docker rmi image_id`

#### 删除所有的images

`docker rmi $(docker images -q)`


### 查看当前运行中的容器

`docker ps`

### 查看当前的容器

`docker ps -a`

### 运行一个image

进入容器的命令行：`docker run -it image_name /bin/bash`

退出容器命令行：`exit`

再次进入命令行（在容器运行才行）：`docker exec -it container_id /bin/bash`

后台运行容器：`docker run -idt image_name`

### 查看docker(images/container)详细信息

`docker inspect images_id/container_id` 

### 由改变后的container生成image

`docker commit -m='change server.xml' container_id tomcat-process:test`

### 登录到docker

`docker login` 

### 推送到dockerhub上

`docker push username/imagename`

### 搜索dockerhub上的一个镜像

`docker search docker_name`

### 下载一个镜像

`docker pull docker_image_name`

*默认是官网dockerhub，但是如果经常pull和push，建议建立私有仓库*

### 建立docker私有仓库

##### 搭建私有库

例如在`192.168.1.78`上，创建私有仓库

1. 下载registry镜像：`docker pull registry`

2. 启动registry容器： `docker run -d -p 5000:5000 registry`

3. 浏览器输入： `http://127.0.0.1:5000/v2`

内容如下：

```bash
{}
```

则运行正常

在`192.168.1.157`上，上传image到私有仓库

##### 添加--insecure-registry参数

对于各种系统和各种docker版本的解决https问题的方法：

- 用于ubuntu14.04，docker1.11：
    
``` bash
echo "DOCKER_OPTS=\"\$DOCKER_OPTS --insecure-registry=192.168.1.78:5000\"" >> /etc/default/docker
```

- 用于ubuntu16.04，docker1.12：

``` bash
echo { \"insecure-registries\":[\"10.0.0.153:5000\"] } > /etc/docker/daemon.json
```

- 用于Centos7, docker1.10:

``` bash
echo "INSECURE_REGISTRY='--insecure-registry 10.0.0.153:5000'" >> /etc/sysconfig/docker
```
	
- 用于Centos7，docker1.12：

``` bash
sudo vim /usr/lib/systemd/system/docker.service

ExecStart=/usr/bin/dockerd 
ExecStart=/usr/bin/dockerd --insecure-registry 10.0.0.153:5000
```

- 重启docker服务：`sudo service docker restart`

##### 私有库的基本操作

- 更换镜像的tag：`docker tag 40a673399858 192.168.1.78:5000/docker-whale`

- 上传镜像： `docker push 192.168.1.78:5000/docker-whale`

- 下载镜像： `docker pull 192.168.1.78:5000/docker-whale`

- 浏览器输入： `http://192.168.1.78:5000/v2/_catalog`

``` bash
{"repositories":["docker-whale","test_docker"]}
```

- 查询镜像tag： 

``` bash
curl http://192.168.1.78:5000/v2/heapster/tags/list
	
"name":"heapster","tags":["v1","canary","latest"]}
```

**建立私有仓库，不仅能保护docker的安全性，有助于下载与上传，同时对于使用kubernets更加方便**

### 从容器中拷贝出文件

`docker cp container_id:/run.sh /home/administrator/run.sh`

### 将外部文件拷贝到容器中

`docker cp /home/administrator/run.sh container_id:/run.sh`

### 保存(save)docker镜像

`sudo docker save image > /home/chenjian/save.tar`

### 导入save.tar文件

`docker load < /home/chenjian/save.tar`   

### 导出(export)docker容器

`sudo docker expot container_id > /home/chenjian/export.tar`

### 导入export.tar

`sudo docker import /home/chenkjian/export.tar`

#### save vs export 

从文件大小(size)中可知
saveed-loaded：没有丢失历史与层(layer)，可以回滚
exported-imported：丢失所有历史,无法进行回滚

### 给镜像添加仓库名称与tag

有时会遇见repository与tag都为`<none>`

可用：`sudo docker tag image_id repository_name:tag_name`

如果tag_name没有的话，tag为`latest`


### 清理所有的镜像与容器

摧毁：`docker kill $(docker ps -a -q)`

移除容器： `docker rm $(docker ps -a -q)`

移除镜像： `docker rmi $(docker ps -a -q)`

其中`“$()”`可以与`“``”`互换

### docker环境变量

命令：`docker run -e "CHENJIAN=chenjian" image_id`

1. 查看全部：`env`

2. 查看某一个：`echo $CHENJIAN` 或者 `env | grep CHENJIAN`

3. 设置：`export CHENJIAN="chenjian"`， 只在当前终端中

4. 删除： `unset $CHENJIAN`

* 系统级设置环境变量：

操作：

1. `sudo vim /etc/profile`, 在尾行中添加`export CHENJIAN="chenjian"`

2. `source /etc/profile`

3. 重启电脑

* python中获得系统环境变量

``` python
# -*- coding:utf8 -*-

__author__ = 'chenjian'

import commands
status, result = commands.getstatusoutput("echo $CHENJIAN")
print status, result  # 0 chenjian

import os
os_res = os.environ["CHENJIAN"]
print os_res  # chenjian
```

### docker网络模式

- --set=host

如果启动容器的时候使用host模式，那么这个容器将不会获得一个独立的Network Namespace，而是和宿主机共用一个Network Namespace。容器将不会虚拟出自己的网卡，配置自己的IP等，而是使用宿主机的IP和端口。

命令：`sudo docker run -idt --net=host image`

### docker容器数目限制问题

docker信息：`sudi docker info`

``` bash
<<'COMMENT'
Containers: 7
 Running: 7
 Paused: 0
 Stopped: 0
Images: 9
Server Version: 1.12.1
Storage Driver: aufs
 Root Dir: /var/lib/docker/aufs
 Backing Filesystem: extfs
 Dirs: 147
 Dirperm1 Supported: true
Logging Driver: json-file
Cgroup Driver: cgroupfs
Plugins:
 Volume: local
 Network: null host bridge overlay
Swarm: inactive
Runtimes: runc
Default Runtime: runc
Security Options: apparmor
Kernel Version: 4.2.0-27-generic
Operating System: Ubuntu 14.04.5 LTS
OSType: linux
Architecture: x86_64
CPUs: 8
Total Memory: 125.9 GiB
Name: administrator68
ID: PYF6:LI5A:MGX2:QSE7:SF7X:ADHR:ZT2V:CUKR:OCI7:MGGO:V7JC:IFW6
Docker Root Dir: /var/lib/docker
Debug Mode (client): false
Debug Mode (server): false
Registry: https://index.docker.io/v1/
WARNING: No swap limit support
Insecure Registries:
 127.0.0.0/8
COMMENT
```

**问题**
当容器开到40-50个的时候，开始出现：
`docker: Error response from daemon: containerd: container did not start before the specified timeout`

##### 具体操作

```shell
sudo mkdir -p /etc/systemd/system/docker.service.d/

sudo tee /etc/systemd/system/docker.service.d/tasksmax.conf <<-'EOF'
[Service]
TasksMax=infinity
EOF

# ubuntu 16+ / Centos7
sudo systemctl stop docker
sudo systemctl daemon-reload 
sudo systemctl enable docker
sudo systemctl start docker

# ubuntu 14.04
sudo service docker restart
# 或者
/etc/init.d/docker restart
```

**效果**
开了100个测试了下，较为正常


P.S. **项目中的DNShj，由于网络链接一直不行，则采用了host模式。由于没有其他机器进行访问dnshj的worker机器，所以开启两个host模式下面的dnshj的worker暂无问题**

- brige(defult)
bridge模式是Docker默认的网络设置，此模式会为每一个容器分配Network Namespace、设置IP等，并将一个主机上的Docker容器连接到一个虚拟网桥上。 

##### wmcluster中celery.py

添加C_FORCE_ROOT：

```python
from celery import Celery, platforms

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wmcluster.settings')

from django.conf import settings  # noqa

app = Celery('missions')

platforms.C_FORCE_ROOT = True
```

### Shipyard的安装及使用

安装
* 安装curl：
命令：

1. `wget --no-check-certificate curl.haxx.se/download/curl-7.20.0.tar.gz`

2. `tar zvxf curl-7.20.0.tar.gz`

3. `cd curl-7.20.0`

4. `./configure --with-ssl`

问题：**undefined reference to "SSLv2_client_method"**

1.解决博文：[linux 编译 curl 出错](https://segmentfault.com/q/1010000003987744)

命令:`which openssl`,将结果`--with-ssl=/usr/bin/openssl`添加到后面

注：此解决方法，后期使用curl处理https时，出现问题。解决方法如下一个。

2.解决：在curl-7.20.0/lib/ssluse.c中注释掉以下内容：

``` c
  case CURL_SSLVERSION_SSLv2:
    req_method = SSLv2_client_method();
    use_sni(FALSE);
    break;
```

5. `make`

6. `sudo make install`

7. `curl --version`

结果：

``` bash
curl 7.20.0 (i686-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3
Protocols: dict file ftp ftps gopher http https imap imaps ldap pop3 pop3s rtmp rtsp smtp smtps telnet tftp 
Features: GSS-Negotiate IDN IPv6 Largefile NTLM SSL libz 
```

问题：**curl 不能链接https**

1. `locate libcurl.so.4`

``` bash
/home/administrator/apps/curl-7.20.0/lib/.libs/libcurl.so.4
/home/administrator/apps/curl-7.20.0/lib/.libs/libcurl.so.4.2.0
/usr/lib/x86_64-linux-gnu/libcurl.so.4
/usr/lib/x86_64-linux-gnu/libcurl.so.4.3.0
/usr/local/lib/libcurl.so.4
/usr/local/lib/libcurl.so.4.2.0
```

2. `sudo rm -rf /usr/local/lib/libcurl.so.4`

3. `sudo ln -s /usr/lib/x86_64-linux-gnu/libcurl.so.4.3.0 /usr/local/lib/libcurl.so.4`

* 安装shipyard

命令：`curl -sSL https://shipyard-project.com/deploy | bash -s`

添加节点：

文章：[shipyard如何做集群节点](http://blog.csdn.net/cuisongliu/article/details/49818199)

命令：`curl -sSL https://shipyard-project.com/deploy | ACTION=node DISCOVERY=etcd://$host-ip:4001  bash -s`

$host-ip 是主的shipyard节点的IP，该脚本需要运行在从node的主机上,不是主机节点的机器上。

### 参考

1. [Docker私有仓库Registry的搭建验证](http://www.cnblogs.com/lienhua34/p/4922130.html)
2. [Linux查看环境变量当前信息和查看命令](http://os.51cto.com/art/201005/202463.htm)
3. [ubuntu 环境变量设置方法](https://my.oschina.net/qinlinwang/blog/29167)
4. [在Linux里设置环境变量的方法（export PATH）](http://www.cnblogs.com/amboyna/archive/2008/03/08/1096024.html)
5. [Docker容器内不能联网的6种解决方案](http://blog.csdn.net/yangzhenping/article/details/43567155)
6. [Docker网络详解及pipework源码解读与实践](http://www.infoq.com/cn/articles/docker-network-and-pipework-open-source-explanation-practice/)
7. [docker的四种网络方式](http://blog.csdn.net/halcyonbaby/article/details/42112141)
8. [docker 1.12 daemon crashed after launched 40+ busybox containe](https://github.com/docker/docker/issues/22690)
9. [Control and configure Docker with systemd](https://docs.docker.com/engine/admin/systemd/)
10. [Docker网络详解及pipework源码解读与实践](http://www.infoq.com/cn/articles/docker-network-and-pipework-open-source-explanation-practice/)
11. [http://www.shipyard-project.com/](http://www.shipyard-project.com/)
 
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
