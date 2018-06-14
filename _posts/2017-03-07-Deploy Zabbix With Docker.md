---
layout:     post
title:      "使用Docker部署Zabbix"
subtitle:   "Deploy Zabbix With Docker"
date:       Tue, Mar 7 2017 15:40:58 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Zabbix-With-Docker/head_blog.jpg"
catalog:    true
tags: [工作, Docker]
---

### 镜像berngp

名称： berngp/docker-zabbix

GitHub： [berngp/docker-zabbix](https://github.com/berngp/docker-zabbix)

##### 在Docker中使用Zabbix 进行监控

> Zabbix Server 端口号10051.

> Zabbix Java Gateway 端口号 10052.

> Zabbix Web UI 端口号 80 (例子 http://$container_ip/zabbix )

> Zabbix Agent .

> MySQL实例支持 Zabbix , 用户名密码都是 zabbix .

> Monit管理在这里 (http://$container_ip:2812, user 'myuser' and password 'mypassword').  monit是一款进程、文件、目录和设备的监测软件，用于Unix平台。

##### 如何使用

你可以执行以下命令运行Zabbix服务.

`docker run -d -P --name zabbix  berngp/docker-zabbix`

上面的命令要求在*docker*跑*berngp/docker-zabbix*镜像的时候开放所有Zabbix指定所有本地端口去运行实例。 运行`docker ps -f name=zabbix`检查端口映射到容器的'80'端口, Zabbix Web UI .

**打开http://docker实例的ip地址:docker指定的端口默认是80/zabbix**

一个将端口 80 映射到 49184 端口的例子。

``` bash
sudo docker ps -f name=zabbix

CONTAINER ID        IMAGE                         COMMAND                CREATED             STATUS              PORTS                                                                                                NAMES
970eb1571545        berngp/docker-zabbix:latest   "/bin/bash /start.sh   18 hours ago        Up 2 hours          0.0.0.0:49181->10051/tcp, 0.0.0.0:49182->10052/tcp, 0.0.0.0:49183->2812/tcp, 0.0.0.0:49184->80/tcp   zabbix
```

如果你想在Docker主机绑定容器特定的端口，你可以执行以下命令：

``` bash
docker run -d \
           -p 10051:10051 \
           -p 10052:10052 \
           -p 80:80       \
           -p 2812:2812   \
           --name zabbix  \
           berngp/docker-zabbix
```

上面的命令会* Zabbix服务*通过* 10051 端口启动，而Web界面则通过80端口运行名字是 Zabbix 的实例。 要有耐心的花一两分钟配置MySQL实例启动服务。你可以使用`docker logs -f $contaienr_id`记录日志。

以上都做完了*Zabbix Web UI* 就已经运行了 你可以通过 http://$container_ip/zabbix 访问. 用户名是**admin**密码是**zabbix**.

##### Apparmor细节 (仅仅在Debian和Ubuntu)

如果你想容器使用Monit控制和监视各个进程, 你需要配置Docker的默认Apparmor配置文件. 目前，唯一的办法就是添加 trace 能力和运行的容器通过AppArmor，使用下面的标识 RUN command:

--cap-add SYS_PTRACE  --security-opt apparmor:unconfined
如果添加*vast*号日志信息写入你得你的系统日志，并每10秒跟踪一次进程！

##### 挖掘Docker Zabbix 容器

如果你想查看部署运行容器的内容, 你可以通过如下命令 bash shell through docker's exec . 执行以下命令.

`docker exec -i -t zabbix /bin/bash`


##### 进入容器构建代码目录

`cd /docker/docker-zabbix`

##### 构建容器

`docker build -t berngp/docker-zabbix .`

##### CentOS7 mini上搭建zabbix-agent

``` bash
# 安装网络工具
yum install net-tools

# 关闭selinux
sed -i "s/SELINUX=enforcing/SELINUX=disabled/" /etc/selinux/config
setenforce 0  

# 安装zabbix 软件源
rpm -ivh http://repo.zabbix.com/zabbix/2.4/rhel/7/x86_64/zabbix-release-2.4-1.el7.noarch.rpm

# 安装zabbix-agent
yum install zabbix-sender zabbix-agent zabbix

# 查看已安装的zabbix-agent版本 
rpm -qa|grep zabbix

zabbix-release-2.4-1.el7.noarch
zabbix-2.4.8-1.el7.x86_64
zabbix-sender-2.4.8-1.el7.x86_64
zabbix-agent-2.4.8-1.el7.x86_64

# 配置zabbix-agent agent机器ip为10.0.0.171，server机器ip为10.0.0.41
sed -i "s/Server=127.0.0.1/Server=10.0.0.41/" /etc/zabbix/zabbix_agentd.conf
sed -i "s/ServerActive=127.0.0.1/ServerActive=10.0.0.41/" /etc/zabbix/zabbix_agentd.conf
sed -i "s/Hostname=Zabbix server/Hostname=10.0.0.171/" /etc/zabbix/zabbix_agentd.conf 

# 启动并设置开机自启
systemctl restart zabbix-agent.service
systemctl enable zabbix-agent.service
systemctl status zabbix-agent.service
```

zabbix界面添加agent主机

### 镜像million12

名称：
 
- million12/zabbix-server
- million12/mariadb
- million12/zabbix-agent

GitHub： 

- [docker-zabbix-agent](https://github.com/million12/docker-zabbix-agent)
- [docker-zabbix-server](https://github.com/million12/docker-zabbix-server)

##### 如何使用

##### mariadb

``` bash
docker run \
    -d \
    --name zabbix-db \
    -p 3306:3306 \
    --env="MARIADB_USER=username" \
    --env="MARIADB_PASS=my_password" \
    million12/mariadb
```

##### zabbix-server

``` bash
docker run \
    -d \
    --name zabbix \
    -p 80:80 \
    -p 10051:10051 \
    --link zabbix-db:zabbix.db \
    --env="ZS_DBHost=zabbix.db" \
    --env="ZS_DBUser=username" \
    --env="ZS_DBPassword=my_password" \
    --env="ZABBIX_ADMIN_EMAIL=qgssoft@163.com" \
    --env="ZABBIX_SMTP_SERVER=smtp.163.com:25" \
    --env="ZABBIX_SMTP_USER=qgssoft@163.com" \
    --env="ZABBIX_SMTP_PASS=qwer1234" \
    million12/zabbix-server
```

##### zabbix-agent

``` bash
docker run \
	-d \
	--name zabbix-agent \
	-p 10050:10050 \
	-v /proc:/data/proc \
	-v /sys:/data/sys \
	-v /dev:/data/dev \
	-v /var/run/docker.sock:/var/run/docker.sock \
	-e ZABBIX_SERVER=10.0.0.171 \
	-e HOSTNAME=my.zabbix \
	--restart=always \
	million12/zabbix-agent
```

### - 参考博文

1. [Git@OSC 项目推荐 —— Zabbix 的 Docker 映像](http://www.tuicool.com/articles/MFrAZf6)
2. [centos7 安装zabbix-agent](http://blog.csdn.net/linglong0820/article/details/48196895)
3. [Centos7 安装zabbix-server](http://blog.csdn.net/linglong0820/article/details/48194315)


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/03/07/Deploy-Zabbix-With-Docker/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。