---
layout:     post
title:      "Kubernetes之Pause容器"
subtitle:   "The Pause Container Of Kubernetes"
date:       Tue, Oct 17 2017 00:06:37 GMT+8
author:     "ChenJian"
header-img: "img/in-post/The-Pause-Container-Of-Kubernetes/head_blog.jpg"
catalog:    true
tags: [工作, Kubernetes, Docker]
---

### pause根容器

在接触Kubernetes的初期，便知道集群搭建需要下载一个`gcr.io/google_containers/pause-amd64:3.0`镜像，然后每次启动一个容器，都会伴随一个pause容器的启动。

但这个`pause`容器的功能是什么，它是如何做出来的，以及为何都伴随容器启动等等。这些问题一直在我心里，如今有缘学习相关内容。

`pause`源码在kubernetes项目(**v1.6.7版本**)的`kubernetes/build/pause/`中。

``` sh
git clone -b v1.6.7 https://github.com/kubernetes/kubernetes.git

ll kubernetes/build/pause
<<'COMMENT'
Dockerfile  Makefile  orphan.c  pause.c
COMMENT
```

##### pause的源码

四个文件中，`pause.c`是`pause`的源码，用`c语言`编写，如下(除去注释):

``` c
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

static void sigdown(int signo) {
  psignal(signo, "Shutting down, got signal");
  exit(0);
}

static void sigreap(int signo) {
  while (waitpid(-1, NULL, WNOHANG) > 0)
    ;
}

int main() {
  if (getpid() != 1)
    /* Not an error because pause sees use outside of infra containers. */
    fprintf(stderr, "Warning: pause should be the first process in a pod\n");

  if (sigaction(SIGINT, &(struct sigaction){.sa_handler = sigdown}, NULL) < 0)
    return 1;
  if (sigaction(SIGTERM, &(struct sigaction){.sa_handler = sigdown}, NULL) < 0)
    return 2;
  if (sigaction(SIGCHLD, &(struct sigaction){.sa_handler = sigreap,
                                             .sa_flags = SA_NOCLDSTOP},
                NULL) < 0)
    return 3;

  for (;;)
    pause();
  fprintf(stderr, "Error: infinite loop terminated\n");
  return 42;
}
```

可以看出来很简单。目前这段代码讲什么，还是没看懂。

##### pause的Dockerfile

剩余的文件`orphan.c`是个测试文件，不用管。`Makefile`用于制作`pause`镜像，制作镜像的模板便是`Dockerfile`。先看看这个`Dockerfile`(除去注释)：

``` docker
FROM scratch
ARG ARCH
ADD bin/pause-${ARCH} /pause
ENTRYPOINT ["/pause"]
```

- FROM scratch

    基础镜像是一个空镜像(an explicitly empty image)

- ARG ARCH

    等待在docker build --build-arg时提供的ARCH参数

- ADD bin/pause-${ARCH} /pause

    添加外部文件到内部

- ENTRYPOINT ["/pause"]

    开启容器，运行命令

可以看出这个`bin/pause-${ARCH}`非常关键，但是如何制作出来呢？

##### pause的Makefile

- ARCH值

``` makefile
# Architectures supported: amd64, arm, arm64, ppc64le and s390x
ARCH ?= amd64

ALL_ARCH = amd64 arm arm64 ppc64le s390x
```

可以看出架构支持很多类型，默认为`amd64`

- 制作pause二进制文件

``` makefile
TAG = 3.0
CFLAGS = -Os -Wall -Werror -static
BIN = pause
SRCS = pause.c
KUBE_CROSS_IMAGE ?= gcr.io/google_containers/kube-cross
KUBE_CROSS_VERSION ?= $(shell cat ../build-image/cross/VERSION)

bin/$(BIN)-$(ARCH): $(SRCS)
	mkdir -p bin
	docker run --rm -u $$(id -u):$$(id -g) -v $$(pwd):/build \
		$(KUBE_CROSS_IMAGE):$(KUBE_CROSS_VERSION) \
		/bin/bash -c "\
			cd /build && \
			$(TRIPLE)-gcc $(CFLAGS) -o $@ $^ && \
			$(TRIPLE)-strip $@"
```

可以看出这分为两步，

- - 运行`gcr.io/google_containers/kube-cross:xxxx`容器

        这个镜像的制作，可在kubernetes/build/build-image/cross路径下，
        其中的Makefile很简单。Dockerfile的基础镜像是golang:1.7.6，
        可以看出这个镜像目的是This file creates a standard build environment for building 
        cross platform go binary for the architecture kubernetes cares about.
        该镜像也包含后续所需的gcc工具。

- - 制作二进制文件

        通过挂载，在容器内部制作pause二进制文件。

- 制作pause镜像

``` makefile
TAG = 3.0
REGISTRY ?= gcr.io/google_containers
IMAGE = $(REGISTRY)/pause-$(ARCH)

.container-$(ARCH): bin/$(BIN)-$(ARCH)
	docker build --pull -t $(IMAGE):$(TAG) --build-arg ARCH=$(ARCH) .
```

一个很简单的制作过程。

### 制作pause镜像

这里绕开制作`cross`镜像，直接做`pause`镜像。

``` sh
cd kubernetes/build/pause
mkdir -p bin

sudo gcc -Os -Wall -Werror -static -o pause pause.c

ls -hl
<<'COMMENT'
total 876K
drwxr-xr-x. 2 root root    6 Oct 16 19:13 bin
-rw-r--r--. 1 root root  679 Oct 11 15:19 Dockerfile
-rw-r--r--. 1 root root 2.9K Oct 11 15:19 Makefile
-rw-r--r--. 1 root root 1.1K Oct 11 15:19 orphan.c
-rwxr-xr-x. 1 root root 858K Oct 16 19:11 pause
-rw-r--r--. 1 root root 1.6K Oct 11 15:19 pause.c
COMMENT

file pause
<<'COMMENT'
pause: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, for GNU/Linux 2.6.32, BuildID[sha1]=5a2385a62d252571c959bc5453569e60866baf53, not stripped
COMMENT

nm pause
<<'COMMENT'
00000000004183d0 T abort
00000000006c2860 B __abort_msg
00000000004530c0 W access
00000000004530c0 T __access
0000000000492a50 t add_fdes
0000000000461bb0 t add_module.isra.1
00000000004569a0 t add_name_to_object.isra.3
00000000006c1728 d adds.8351
0000000000418ea0 T __add_to_environ
000000000048aac0 t add_to_global
00000000006c2460 V __after_morecore_hook
0000000000416350 t alias_compare
0000000000409120 W aligned_alloc
00000000006c24d0 b aligned_heap_area
00000000004523f0 T __alloc_dir
000000000049dd50 r archfname
...
COMMENT

# 开始Strip
strip pause

ls -lh pause
<<'COMMENT'
-rwxr-xr-x. 1 root root 781K Oct 16 19:22 pause
COMMENT

file pause
<<'COMMENT'
pause: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, for GNU/Linux 2.6.32, BuildID[sha1]=5a2385a62d252571c959bc5453569e60866baf53, stripped
COMMENT

nm pause
<<'COMMENT'
nm: pause: no symbols
COMMENT

cp pause bin/pause-amd64

docker build --pull -t gcr.io/google_containers/pause-amd64:3.0 --build-arg ARCH=amd64 .

<<'COMMENT'
Sending build context to Docker daemon  1.612MB
Step 1/4 : FROM scratch
 ---> 
Step 2/4 : ARG ARCH
 ---> Running in 6eec4bcd21b7
 ---> 30b135219bee
Removing intermediate container 6eec4bcd21b7
Step 3/4 : ADD bin/pause-${ARCH} /pause
 ---> acda3361fddc
Removing intermediate container 79a21fb7baca
Step 4/4 : ENTRYPOINT /pause
 ---> Running in dd1d266bb882
 ---> 18620a113848
Removing intermediate container dd1d266bb882
Successfully built 18620a113848
Successfully tagged gcr.io/google_containers/pause-amd64:3.0
COMMENT

docker images

<<'COMMENT'
REPOSITORY                             TAG                 IMAGE ID            CREATED             SIZE
gcr.io/google_containers/pause-amd64   3.0                 18620a113848        4 minutes ago       799kB
busybox                                latest              2b8fd9751c4c        15 months ago       1.09MB
COMMENT
```

- strip

    通过上面的对比，可以看出strip后，pause文件由858K瘦身到781K。strip执行前后，不改变程序的执行能力。在开发过程中，strip用于产品的发布，调试均用未strip的程序。

- file

    通过file命令可以看到pause的strip状态

- nm

    通过nm命令，可以看到strip后的pause文件没有符号信息

### pause容器的工作

可知kubernetes的pod抽象基于Linux的namespace和cgroups，为容器提供了良好的隔离环境。在同一个pod中，不同容器犹如在localhost中。

在Unix系统中，PID为1的进程为init进程，即所有进程的父进程。它很特殊，维护一张进程表，不断地检查进程状态。例如，一旦某个子进程由于父进程的错误而变成了“孤儿进程”，其便会被init进程进行收养并最终回收资源，从而结束进程。

或者，某子进程已经停止但进程表中仍然存在该进程，因为其父进程未进行wait syscall进行索引，从而该进程变成“僵尸进程”，这种僵尸进程存在时间较短。不过如果父进程只wait，而未syscall的话，僵尸进程便会存在较长时间。 

同时，init进程不能处理某个信号逻辑，拥有“信号屏蔽”功能，从而防止init进程被误杀。

容器中使用pid namespace来对pid进行隔离，从而每个容器中均有其独立的init进程。例如对于寄主机上可以用个发送SIGKILL或者SIGSTOP(也就是docker kill 或者docker stop)来强制终止容器的运行，即终止容器内的init进程。一旦init进程被销毁， 同一pid namespace下的进程也随之被销毁，并容器进程被回收相应资源。

kubernetes中的pause容器便被设计成为每个业务容器提供以下功能：

- 在pod中担任Linux命名空间共享的基础； 

- 启用pid命名空间，开启init进程。

### 实践操作

已有刚做好的`pause`镜像和`busybox`镜像

``` sh
docker images

<<'COMMENT'
REPOSITORY                             TAG                 IMAGE ID            CREATED             SIZE
gcr.io/google_containers/pause-amd64   3.0                 18620a113848        4 minutes ago       799kB
busybox                                latest              2b8fd9751c4c        15 months ago       1.09MB
COMMENT

docker run -idt --name pause gcr.io/google_containers/pause-amd64:3.0
<<'COMMENT'
7f6e459df5644a1db4bc9ad2206a0f99e40312de1892695f8a09d52faa9c1073
COMMENT

docker ps -a
<<'COMMENT'
CONTAINER ID        IMAGE                                      COMMAND             CREATED             STATUS              PORTS               NAMES
7f6e459df564        gcr.io/google_containers/pause-amd64:3.0   "/pause"            11 seconds ago      Up 11 seconds                           pause
COMMENT

docker run -idt --name busybox --net=container:pause --pid=container:pause --ipc=container:pause busybox
<<'COMMENT'
ad3029c55476e431101473a34a71516949d1b7de3afe3d505b51d10c436b4b0f
COMMENT

docker ps -a
<<'COMMENT'
CONTAINER ID        IMAGE                                      COMMAND             CREATED             STATUS              PORTS               NAMES
ad3029c55476        busybox                                    "sh"                36 seconds ago      Up 35 seconds                           busybox
7f6e459df564        gcr.io/google_containers/pause-amd64:3.0   "/pause"            2 minutes ago       Up 2 minutes                            pause
COMMENT

docker exec -it ad3029c55476 /bin/sh
<<'COMMENT'
/ # ps aux
PID   USER     TIME   COMMAND
    1 root       0:00 /pause
    5 root       0:00 sh
    9 root       0:00 /bin/sh
   13 root       0:00 ps aux
COMMENT
```

可以看出来，busybox中的`PID 1`由`pause`容器提供。

### 参考博文

1. [scratch镜像](https://hub.docker.com/r/library/scratch/)
2. [gcc参数问题](https://zhidao.baidu.com/question/501561674.html)
3. [linux中的strip命令简介](http://blog.csdn.net/stpeace/article/details/47090255)
4. [Kubernetes中的Pod的到底是什么](http://dockone.io/article/2682)
5. [Kubernetes之“暂停”容器](http://dockone.io/article/2785)


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/10/17/The-Pause-Container-Of-Kubernetes/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。