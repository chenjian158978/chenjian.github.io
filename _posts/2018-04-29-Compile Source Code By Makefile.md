---
layout:     post
title:      "通过Makefile编译源码"
subtitle:   "Compile Source Code By Makefile"
date:       Sun, Apr 29 2018 18:31:37 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Compile-Source-Code-By-Makefile/head_blog.jpg"
catalog:    true
tags:
    - 工作
---

### 编译和链接

- 编译(compile): 将源码(Source Code)编译成中间代码文件(Object File，Windows下的obj文件，Unix下的o文件)

- 打包(pack): 将中间代码文件打包， Windows下的lib文件(库文件, Library File)，Unix下的a文件(Archive)

- 链接(link): 将中间代码文件合成执行文件

### 参考Makefile文件

[libnvidia-container之Makefile](https://raw.githubusercontent.com/NVIDIA/libnvidia-container/master/Makefile)

### 规则

Makefile的规则如下：

``` makefile
<target> : <prerequisites> 
[tab]  <commands>
```

- target: 目标，*必需项。一个目标构成一条规则；
- prerequisites: 前置条件。指定“目标”是否要重建构建的判断标准，只要一个前置文件不存在或者有过更新(前置文件的last-modification时间戳比目标的时间戳新)，“目标”就需重新构建；
- \[tab]: TAB键，第二行必须以TAB键开头；
- commands：命令行，运行结果通常是目标文件。

### 伪目标

例如：

``` makefile 
.PHONY: all tools shared static deps install uninstall dist depsclean mostlyclean clean distclean
```

在使用**伪目标**时，当文件路径下有个`all`文件，如果使用命令`make all`，则会执行对应目标命令。


### 关键字Include

例如：

``` makefile
include $(MAKE_DIR)/common.mk
```

在文件`common.mk`中包含**全局变量定义**和**函数定义**

在Makefile使用include关键字可以把别的 Makefile 包含进来，这很像C语言的`#include`，被包含的文件会原模原样的放在当前文件的包含位置。

### 内置变量

Make命令提供一系列内置变量，比如，$(CC) 指向当前使用的编译器，$(MAKE) 指向当前使用的Make工具。这主要是为了跨平台的兼容性，详细的内置变量清单见[手册](https://www.gnu.org/software/make/manual/html_node/Implicit-Variables.html)

``` makefile
$(LIB_OBJS): %.lo: %.c | deps
	$(CC) $(LIB_CFLAGS) $(LIB_CPPFLAGS) -MMD -MF $*.d -c $(OUTPUT_OPTION) $<

deps: $(LIB_RPC_SRCS) $(BUILD_DEFS)
	$(MKDIR) -p $(DEPS_DIR)
	$(MAKE) -f $(MAKE_DIR)/nvidia-modprobe.mk install
```

### 函数

Makefile提供了许多内置函数，可供调用。

- shell函数

``` makefile
UID      := $(shell id -u)
GID      := $(shell id -g)
```

- call函数

call函数是唯一一个可以用来创建新的参数化的函数

在makefile中：

``` makefile
ARCH    ?= $(call getarch)
```

其对应的`getarch`函数在`common.mk`中

``` makefile
getarch = $(shell [ -f /etc/debian_version ] && echo "amd64" || echo "x86_64")
```

### 忽略错误

``` makefile
ifeq ($(WITH_LIBELF), no)
	-$(MAKE) -f $(MAKE_DIR)/elftoolchain.mk clean
```

在`$(MAKE)`前面加`-`，表示出现错误时不停止，继续执行下去。

### 赋值运算符

``` shell
# 在执行时扩展，允许递归扩展。
VARIABLE = value

# 在定义时扩展。
VARIABLE := value

# 只有在该变量为空时才设置值。
VARIABLE ?= value

# 将值追加到变量的尾端。
VARIABLE += value
```

区别可查看[What is the difference between the GNU Makefile variable assignments =, ?=, := and +=?
](https://stackoverflow.com/questions/448910/what-is-the-difference-between-the-gnu-makefile-variable-assignments-a)

### 循环

Makefile使用 Bash 语法，完成判断和循环。

``` makefile
ifeq ($(WITH_LIBELF), no)
	-$(MAKE) -f $(MAKE_DIR)/elftoolchain.mk clean
endif
ifeq ($(WITH_TIRPC), yes)
	-$(MAKE) -f $(MAKE_DIR)/libtirpc.mk clean
endif
```

### 使用docker编译

> 命令：make docker-centos:7 TAG=beta.1

``` makefile
docker-%: SHELL:=/bin/bash
docker-%:
	image=$* ;\
	$(MKDIR) -p $(DIST_DIR)/$${image/:} ;\
	$(DOCKER) build --network=host \
                    --build-arg IMAGESPEC=$* \
                    --build-arg USERSPEC=$(UID):$(GID) \
                    --build-arg WITH_LIBELF=$(WITH_LIBELF) \
                    --build-arg WITH_TIRPC=$(WITH_TIRPC) \
                    --build-arg WITH_SECCOMP=$(WITH_SECCOMP) \
                    -f $(MAKE_DIR)/Dockerfile.$${image%%:*} -t $(LIB_NAME):$${image/:} . ;\
	$(DOCKER) run --rm -v $(DIST_DIR)/$${image/:}:/mnt:Z -e TAG -e DISTRIB -e SECTION $(LIB_NAME):$${image/:}
```

- docker-%: 目标(target)。可以使用`make docker-centos:7`；

- %: 匹配符。上述`%为centos:7`;

- SHELL:=/bin/bash： 前置条件(prerequisites)。意思为`当符合前置条件的情况下，执行目标。或者先执行前置条件，再执行目标`，该句意思为，在当前SHELL为`/bin/bash`时，会执行目标`docker-%`

- 第二个docker-%，则为目标的主体。
- - 第二行必须由一个`TAB键`起首，后续跟着命令(commands)
- - 命令中每行在不同进程执行。若要保持连续性，命令之间需要添加`;`。为编写方便，可添加反斜杠转义`\`

- \$\*: 指代匹配符`%`匹配的部分， 比如`%`匹配`docker-centos:7`中的`centos:7` ，$\*就表示`centos:7`;

- \$\${image/:}: 在makefile中要引用shell命令中的变量，要使用`$${VAR}`格式



### 参考文献


1. [Makefile中使用$$的使用](http://makaidong.com/LiuYanYGZ/664768_4491452.html)
2. [Make命令教程](http://www.ruanyifeng.com/blog/2015/02/make.html)


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2018/04/29/Compile-Source-Code-By-Makefile/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。