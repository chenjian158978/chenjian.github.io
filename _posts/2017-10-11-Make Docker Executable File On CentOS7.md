---
layout:     post
title:      "centos7下docker二进制文件编译"
subtitle:   "Make Docker Executable File On CentOS7"
date:       Wed, Oct 11 2017 22:36:37 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Make-Docker-Executable-File-On-CentOS7/head_blog.jpg"
catalog:    true
tags:
    - 工作
    - Golang
    - Docker
---

### 相关博文

1. [带你玩转Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)

### 系统环境与软件版本

- OS：Centos7 64bit
- Kernel Version：3.10.0-693.2.2.el7.x86_64
- Golang Version: go1.8.4 linux/amd64
- Docker: 17.05.0-ce

### 浅谈docker源码编译

官方提供编译步骤依次为：`make build`和`make binary`。先看懂`Makefile`会帮助理解docker基本结构。

- make build
    
    其实就是`docker build`，于是要看`Dockerfile`文件。其制作一个叫`docker-dev`的镜像，镜像中会生成源码编译的环境。

- make binary

    其实就是`docker run docker-dev`，即运行`docker-dev`一个容器，并在容器中的bundles文件夹下生成dockers所需的二进制文件。

通过查看`Dockerfile`以下内容：

``` docker
# Install tomlv, vndr, runc, containerd, tini, docker-proxy
# Please edit hack/dockerfile/install-binaries.sh to update them.
COPY hack/dockerfile/binaries-commits /tmp/binaries-commits
COPY hack/dockerfile/install-binaries.sh /tmp/install-binaries.sh
RUN /tmp/install-binaries.sh tomlv vndr runc containerd tini proxy bindata
```

可以看出具体的binary来自脚本`install-binaries.sh`。

- install-binaries.sh

    此脚本涉及到`docker-containerd系列`，`docker-runc`，`docker-init`和`docker-proxy`等组件的源码地址，以及编译命令

- binaries-commits
    
    此文件涉及到各类组件的commit编号，使用`git checkout -q xxxxxxxx`来切换到相对应的tree上

**以下内容，实际便是抽出install-binaries.sh中的内容，独立完成，从而获得docker所有编译后的二进制文件。如要生成rpm文件，需进一步研究**

### Golang的安装与配置

可以在[下载 - Golang中国](https://www.golangtc.com/download)中下载相对应的安装包。安装包`go1.9.linux-amd64.tar.gz`和脚本`install_go.sh`放在同一个目录下。

代码下载： [install_go.sh](/download/Make-Docker-Executable-File-On-CentOS7/install_go.sh)

``` sh
#!/bin/bash

cur_path=`pwd`

# 解压go包
sudo tar zxvf ${cur_path}/go1.8.4.linux-amd64.tar.gz -C /usr/local

# 创建GOPATH文件夹
sudo mkdir -p /home/mygo

# 设置go环境变量
sudo echo "export GOROOT=/usr/local/go" >> /etc/profile
sudo echo "export GOPATH=/home/mygo" >> /etc/profile
sudo echo "export PATH=\$PATH:\$GOROOT/bin" >> /etc/profile
. /etc/profile

# 安装wget
sudo yum install -y wget

# 更新为aliyun源
sudo wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo

# 安装git
sudo yum install -y git

# 安装go包管理工具govendor
go get -u github.com/kardianos/govendor
cp ${GOPATH}/bin/govendor /usr/local/go/bin/
```

结果如下：

``` sh
go version
<<'COMMENT'
go version go1.8.4 linux/amd64
COMMENT

ls /home/mygo/ /home/mygo/src/ /home/mygo/src/github.com/ /usr/local/go/bin/

<<'COMMENT'
/home/mygo/:
bin  pkg  src

/home/mygo/src/:
github.com

/home/mygo/src/github.com/:
kardianos

/usr/local/go/bin/:
go  godoc  gofmt  govendor
COMMENT
```

### docker编译二进制文件

##### 安装依赖软件

``` sh
yum install -y gcc make cmake device-mapper-devel btrfs-progs-devel libarchive libseccomp-devel glibc-static
```

##### 编译docker等二进制文件

组件：

- docker: docker-client端
- dockerd: docker-server端

操作：

``` sh
cd $GOPATH/src/github.com/

mkdir docker && cd docker

# 下载相关版本的docker源码
git clone -b v17.05.0-ce https://github.com/moby/moby.git

cp -R moby/ docker && rm -rf moby/

# docker编译
cd  $GOPATH/src/github.com/docker/docker/cmd/docker
go build
cp docker /usr/local/bin/

# dockerd编译
cd  $GOPATH/src/github.com/docker/docker/cmd/dockerd
go build
cp dockerd /usr/local/bin/
```

##### 编译containerd等二进制文件

组件：

- docker-containerd
- docker-containerd-ctr
- docker-containerd-shim

操作：

``` sh
# 下载相关版本的container源码
git clone https://github.com/containerd/containerd.git "${GOPATH}/src/github.com/docker/containerd"
cd "${GOPATH}/src/github.com/docker/containerd"
git checkout -q 9048e5e50717ea4497b757314bad98ea3763c145

# 组件编译
cd  ${GOPATH}/src/github.com/docker/containerd

make static
<<'COMMENT'
cd ctr && go build -ldflags "-w -extldflags -static -X github.com/docker/containerd.GitCommit=9048e5e50717ea4497b757314bad98ea3763c145 " -tags "" -o ../bin/ctr
cd containerd && go build -ldflags "-w -extldflags -static -X github.com/docker/containerd.GitCommit=9048e5e50717ea4497b757314bad98ea3763c145 " -tags "" -o ../bin/containerd
cd containerd-shim && go build -ldflags "-w -extldflags -static -X github.com/docker/containerd.GitCommit=9048e5e50717ea4497b757314bad98ea3763c145 " -tags "" -o ../bin/containerd-shim
COMMENT

cp bin/containerd /usr/local/bin/docker-containerd
cp bin/containerd-shim /usr/local/bin/docker-containerd-shim
cp bin/ctr /usr/local/bin/docker-containerd-ctr
```

##### 编译docker-runc二进制文件

组件：

- docker-runc

操作：

``` sh
cd $GOPATH/src/github.com/

mkdir opencontainers && cd opencontainers

# 下载相关版本的runc源码
git clone -b v1.0.0-rc2 https://github.com/opencontainers/runc.git "${GOPATH}/src/github.com/opencontainers/runc"

# runc编译
cd  ${GOPATH}/src/github.com/opencontainers/runc

make BUILDTAGS="${RUNC_BUILDTAGS:-"selinux"}" static

<<'COMMENT'
CGO_ENABLED=1 go build -i -tags "selinux cgo static_build" -ldflags "-w -extldflags -static -X main.gitCommit="c91b5bea4830a57eac7882d7455d59518cdf70ec-dirty" -X main.version=1.0.0-rc2" -o runc .
COMMENT

cp runc /usr/local/bin/docker-runc
```

##### 编译docker-init二进制文件

组件：

- docker-init

操作：

``` sh
cd $GOPATH/src/github.com/

mkdir krallin && cd krallin

# 下载相关版本的tini源码
git clone https://github.com/krallin/tini.git "$GOPATH/tini"
cd "$GOPATH/tini"
git checkout -q 949e6facb77383876aeff8a6944dde66b3089574

cmake .
<<'COMMENT'
-- The C compiler identification is GNU 4.8.5
-- Check for working C compiler: /usr/bin/cc
-- Check for working C compiler: /usr/bin/cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Performing Test HAS_BUILTIN_FORTIFY
-- Performing Test HAS_BUILTIN_FORTIFY - Failed
-- Configuring done
-- Generating done
-- Build files have been written to: /home/mygo/tini
COMMENT

make tini-static
<<'COMMENT'
Scanning dependencies of target tini-static
[100%] Building C object CMakeFiles/tini-static.dir/src/tini.c.o
Linking C executable tini-static
[100%] Built target tini-static
COMMENT

cp tini-static /usr/local/bin/docker-init
```

##### 编译docker-proxy二进制文件

组件：

- docker-proxy

操作：

``` sh
cd $GOPATH/src/github.com/docker

# 下载相关版本的proxy源码
git clone https://github.com/docker/libnetwork.git "$GOPATH/src/github.com/docker/libnetwork"
cd "$GOPATH/src/github.com/docker/libnetwork"
git checkout -q 7b2b1feb1de4817d522cc372af149ff48d25028

# proxy编译
go build -ldflags="$PROXY_LDFLAGS" -o /usr/local/bin/docker-proxy github.com/docker/libnetwork/cmd/proxy
```

### 运行docker

``` sh
ll /usr/local/bin/docker*

<<'COMMENT'
-rwxr-xr-x. 1 root root 25845680 Oct 10 14:00 /usr/local/bin/docker
-rwxr-xr-x. 1 root root 12474568 Oct 10 14:01 /usr/local/bin/docker-containerd
-rwxr-xr-x. 1 root root 11435336 Oct 10 14:03 /usr/local/bin/docker-containerd-ctr
-rwxr-xr-x. 1 root root  3858880 Oct 10 14:04 /usr/local/bin/docker-containerd-shim
-rwxr-xr-x. 1 root root 55072232 Oct 10 14:02 /usr/local/bin/dockerd
-rwxr-xr-x. 1 root root   824568 Oct 10 14:59 /usr/local/bin/docker-init
-rwxr-xr-x. 1 root root  2528043 Oct 10 15:10 /usr/local/bin/docker-proxy
-rwxr-xr-x. 1 root root 10894408 Oct 10 14:16 /usr/local/bin/docker-runc
COMMENT

groupadd docker

dockerd
<<'COMMENT'
INFO[0000] libcontainerd: new containerd process, pid: 9024 
WARN[0000] containerd: low RLIMIT_NOFILE changing to max  current=1024 max=4096
WARN[0001] failed to rename /var/lib/docker/tmp for background deletion: %!s(<nil>). Deleting synchronously 
INFO[0001] [graphdriver] using prior storage driver: overlay 
INFO[0001] Graph migration to content-addressability took 0.00 seconds 
INFO[0001] Loading containers: start.
INFO[0001] Default bridge (docker0) is assigned with an IP address 172.17.0.0/16. Daemon option --bip can be used to set a preferred IP address 
INFO[0001] Loading containers: done.
INFO[0001] Daemon has completed initialization
INFO[0001] Docker daemon                                 commit=library-import graphdriver=overlay version=library-import
INFO[0001] API listen on /var/run/docker.sock
COMMENT

ps aux|grep docker
<<'COMMENT'
root     11753  0.2  2.8 343472 28860 pts/1    Sl+  14:09   0:00 dockerd
root     11756  0.0  0.6 267908  6240 ?        Ssl  14:09   0:00 docker-containerd -l unix:///var/run/docker/libcontainerd/docker-containerd.sock --metrics-interval=0 --start-timeout 2m --state-dir /var/run/docker/libcontainerd/containerd --shim docker-containerd-shim --runtime docker-runc
root     11890  0.0  0.0 112660   976 pts/2    R+   14:10   0:00 grep --color=auto docker
COMMENT

docker version
<<'COMMENT'
Client:
 Version:      library-import
 API version:  1.29
 Go version:   go1.8.4
 Git commit:   library-import
 Built:        library-import
 OS/Arch:      linux/amd64

Server:
 Version:      library-import
 API version:  1.29 (minimum version 1.12)
 Go version:   go1.8.4
 Git commit:   library-import
 Built:        library-import
 OS/Arch:      linux/amd64
 Experimental: false
COMMENT

docker pull busybox

docker run -idt busybox
<<'COMMENT'
b6f61b4b5ec9ce2b4331a47a1e8a3552b2162ca0f152ec2e02dfbf169d64a80a
COMMENT

docker ps -a
<<'COMMENT'
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
b6f61b4b5ec9        busybox             "sh"                27 minutes ago      Up 27 minutes                           loving_noether
COMMENT
```

可以看到，在启动`dockerd`后，会启动另一个程序`docker-containerd`。

### 制作docker的systemd-unit

##### docker.service

``` sh
cat > docker.service <<EOF
[Unit]
Description=Docker Application Container Engine
Documentation=http://docs.docker.io

[Service]
Environment="PATH=/usr/local/bin:/bin:/sbin:/usr/bin:/usr/sbin"
EnvironmentFile=-/run/flannel/docker
ExecStart=/usr/local/bin/dockerd --log-level=error $DOCKER_NETWORK_OPTIONS
ExecReload=/bin/kill -s HUP $MAINPID
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

##### 启动docker服务

``` sh
sudo cp docker.service /etc/systemd/system/docker.service
sudo systemctl daemon-reload

sudo systemctl enable docker
<<'COMMENT'
Created symlink from /etc/systemd/system/multi-user.target.wants/docker.service to /etc/systemd/system/docker.service.
COMMENT

sudo systemctl start docker

sudo systemctl status docker
<<'COMMENT'
● docker.service - Docker Application Container Engine
   Loaded: loaded (/etc/systemd/system/docker.service; enabled; vendor preset: disabled)
   Active: active (running) since Wed 2017-10-11 15:27:51 CST; 3s ago
     Docs: http://docs.docker.io
 Main PID: 1152 (dockerd)
   Memory: 67.2M
   CGroup: /system.slice/docker.service
           ├─1152 /usr/local/bin/dockerd --log-level=error
           └─1156 docker-containerd -l unix:///var/run/docker/libcontainerd/docker-containerd.sock --metrics-interval=0 --start-timeout 2m --state-dir /var/run/docker/libcontainerd/containerd...

Oct 11 15:27:51 localhost.localdomain systemd[1]: Started Docker Application Container Engine.
Oct 11 15:27:51 localhost.localdomain systemd[1]: Starting Docker Application Container Engine...
COMMENT
```

### TroubleShooting

##### /bin/bash^M: bad interpreter:没有那个文件或目录

参考： [bad interpreter](http://blog.csdn.net/yongan1006/article/details/8142527)

##### Linux环境下gcc静态编译/usr/bin/ld: cannot find -lc错误

参考： [lc错误](http://blog.csdn.net/shudaqi2010/article/details/32938715)


### 参考文献

1. [编译Docker源码](http://blog.csdn.net/zhonglinzhang/article/details/76180059)
2. [docker源代码编译](http://www.ybojj.com/docker%E6%BA%90%E4%BB%A3%E7%A0%81%E7%BC%96%E8%AF%91/?d=1)

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/10/11/Make-Docker-Executable-File-On-CentOS7/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。