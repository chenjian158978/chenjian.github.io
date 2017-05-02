---
layout:     post
title:      "MacBook上的优秀软件之第一章节"
subtitle:   "Useful Software On Mac C1"
date:       Mon, Apr 10 2017 17:16:49 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Useful-Software-On-Mac-C1/head_blog.jpg"
catalog:    true
tags:
    - 工作
    - Mac
---

### 摘要

1年前放弃Windows系统，开始使用Ubuntu系统。期间使用过Ubuntu系统的14.04和16.04桌面版本，CentOS7的桌面和服务器版本。写过相关优秀ubuntu系统的软件，如下三篇系列文章：

- [Ubuntu上的优秀软件之第一章节](https://o-my-chenjian.com/2016/04/25/Useful-Software-On-Ubuntu-C1/)
- [Ubuntu上的优秀软件之第二章节](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C2/)
- [Ubuntu上的优秀软件之第三章节](https://o-my-chenjian.com/2017/04/07/Useful-Software-On-Ubuntu-C3/)

半年前开始使用Mac，即macOS系统。这里也会进行总结与分享。

### 系列博文

- [MacBook上的优秀软件之第一章节](https://o-my-chenjian.com/2017/04/10/Useful-Software-On-Mac-C1/)
	- [Homebrew](https://o-my-chenjian.com/2017/04/10/Useful-Software-On-Mac-C1/#homebrew)
	- [Python](https://o-my-chenjian.com/2017/04/10/Useful-Software-On-Mac-C1/#python)
	- [Sublime](https://o-my-chenjian.com/2017/04/10/Useful-Software-On-Mac-C1/#sublime)
	- [Macdown](https://o-my-chenjian.com/2017/04/10/Useful-Software-On-Mac-C1/#macdown)
	- [Chrome](https://o-my-chenjian.com/2017/04/10/Useful-Software-On-Mac-C1/#chrome)
	- [Microsoft Office](https://o-my-chenjian.com/2017/04/10/Useful-Software-On-Mac-C1/#microsoft-office)
	- [Dash](https://o-my-chenjian.com/2017/04/10/Useful-Software-On-Mac-C1/#dash)
	- [Alfred3](https://o-my-chenjian.com/2017/04/10/Useful-Software-On-Mac-C1/#alfred3)
	- [Flux](https://o-my-chenjian.com/2017/04/10/Useful-Software-On-Mac-C1/#flux)
	- [Sequel Pro](https://o-my-chenjian.com/2017/04/10/Useful-Software-On-Mac-C1/#sequel-pro)


### Homebrew

macOS 缺失的软件包管理器。懂了吧！就像ubuntu中的apt-get/apt，就像centos中的yum。

安装：

``` bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

##### wget安装

macOS中没有wget，直接使用homebrew安装

``` bash
brew install wget
```

##### 参考

[Homebrew官网](https://brew.sh/)

### Python

系统内已带python2.7.10，可以通过`python --version`进行查看。但是我还想尝试python2的较新版本2.7.13，或者python3版本。

##### 安装pyenv

``` bash
brew update
brew install pyenv
```

添加到bash_profile: 

- 配置bash

``` bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

- 配置zsh

``` bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

重启shell:

``` bash
exec $SHELL -l
```

##### pyenv基本命令

> 列出所有可以安装的python版本

``` bash
pyenv install --list
```

> 安装某个版本(2.7.13)的python

``` bash
pyenv install 2.7.13
```

安装路径在`~/.pyenv/versions`。可以先进行下载，将其放到`~/.pyenv/cache`中进行安装。

> 更新hash

``` bash
# 为所有已安装的可执行文件 （如：~/.pyenv/versions/*/bin/*） 创建 shims，
# 增删了 Python 版本或带有可执行文件的包（如 pip）以后，都应该执行一次本命令
pyenv rehash
```

> 查看正在使用的python版本

``` bash
pyenv version
```

> 列出所有可以安装的python版本

``` bash
pyenv versions
```

> 卸载某个版本(2.7.13)的python

``` bash
pyenv uninstall 2.7.13
```

> 设置全局python版本

``` bash
pyenv global 2.7.13
```

> 设置局部python版本

``` bash
pyenv local 2.7.13
```

##### 安装pyenv-virtualenv

``` bash
brew update
brew install pyenv-virtualenv
```

配置：

``` bash
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
```

重启shell:

``` bash
exec $SHELL -l
```

##### pyenv-virtualenv基本命令

> 克隆2.7.10版本，目标为my-virtual-env-2.7.10，路径`~/.pyenv/versions`

``` bash
pyenv virtualenv 2.7.13 test-env-2.7.10
```

> 卸载test-env-2.7.10的python

``` bash
pyenv uninstall test-env-2.7.10
```

##### 参考

1. [Python 环境搭建（Mac OS）](http://blog.csdn.net/fdtl01/article/details/63711232)
2. [pyenv管理python版本](https://blog.qiujinfeng.com/book/source/environment/pyenv.html)
3. [使用 pyenv 可以在一个系统中安装多个python版本](http://www.jianshu.com/p/a23448208d9a)

### Sublime

User配置文件如下：

``` bash
{
	"color_scheme": "Packages/Color Scheme - Default/Solarized (Dark).tmTheme",
	"font_size": 12,
	"ignored_packages":
	[
	],
	"open_files_in_new_window": false,
	"soda_folder_icons": true,
	"theme": "Soda SolarizedDark.sublime-theme"
}
```

##### 参考

[sublime官网](https://www.sublimetext.com/)

### Macdown

写markdown使用Macdown(暂时不支持vim)，可以官网上下载。

- 字体：Monaco for Powerline

- 大小：14.0

- 主题：Solarized（Dark）+

- Css：Clearness Dark

- 勾选*Syntax highlighted code block*

- 主题：Okaidia

- 勾选*Show line numbers*

- 勾选*Detect Jekyll front-matter*

##### 参考

[macdown官网](https://macdown.uranusjr.com/)


### Chrome

##### chrome插件

- [AdBlock](https://chrome.google.com/webstore/detail/gighmmpiobklfepjocnamgkkbiglidom) 用来去除广告 
- [Bilibili Helper: Bilibili.com Auxiliary](https://chrome.google.com/webstore/detail/kpbnombpnpcffllnianjibmpadjolanh) B站助手
- [Evernote Web Clipper](https://chrome.google.com/webstore/detail/pioclpoplcdbaefihamjohnefbikjilc) evernote助手
- [Multi-highlight](https://chrome.google.com/webstore/detail/pfgfgjlejbbpfmcfjhdmikihihddeeji) 页面关键字高亮
- [Octotree](https://chrome.google.com/webstore/detail/bkhaagjahfmjljalopjnoealnfndnagc) github左侧文件树
- [One-Click Extensions Manager](https://chrome.google.com/webstore/detail/niemebbfnfbjfojajlmnbiikmcpjkkja) 一键管理chrome插件工具
- [Pinterest Save Button](https://chrome.google.com/webstore/detail/gpdjojdkbbmdfjfahjcgigfpmkopogic) pinterest网页保存
- [Postman](https://chrome.google.com/webstore/detail/fhbjgbiflinjbdggehcddcbncdddomop) 发送请求工具
- [Proxy SwitchyOmega](https://chrome.google.com/webstore/detail/padekgcemlokbadohgkifijomclgjgif) 代理工具
- [SmoothScroll](https://chrome.google.com/webstore/detail/nbokbjkabcmbfdlbddjidfmibcpneigj) 顺滑滚动浏览页面

##### 参考

[chrome官网](https://www.google.com/chrome/browser/desktop/index.html)

### Microsoft Office

可到[这里](https://pan.baidu.com/s/1mhRdC1a)进行下载。
**如果对你有帮助，请在博文下方进行留言表示支持，谢谢！**

### Dash

Dash用来查阅API文档和存储代码片段。

目前升级需要fee，我没有升级，也发现dash的代码片段不能正常使用。

##### 参考

- [dash官网](https://kapeli.com/dash)
- [如何看待 Dash 被 App Store 下架](https://www.zhihu.com/question/51357789)

### Alfred3

mac上**生产力第一**的工具。

包括：

- 文件查询
- 网站查询
- 计算器
- 字典
- 联系人
- 工作流

等等。总结下，就是**神器**。

我已购买终身版。

##### 参考

[Alfred官网](https://www.alfredapp.com/)

### Flux

Flux是一款护眼软件。

杭州经纬度：30.3362，120.117

##### 参考

[Flux官网](https://justgetflux.com/)

### Sequel Pro

数据库客户端

##### 参考

[Sequel Pro官网](https://www.sequelpro.com/)


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/10/Useful-Software-On-Mac-C1/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。