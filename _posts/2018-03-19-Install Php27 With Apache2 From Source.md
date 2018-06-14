---
layout:     post
title:      "PHP27和Apache2的源码安装"
subtitle:   "Install Php27 With Apache2 From Source"
date:       Mon, Mar 19 2018 23:21:35 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Install-Php27-With-Apache2-From-Source/head_blog.jpg"
catalog:    true
tags: [工作, Linux]
---

### 操作系统

``` shell
cat /etc/redhat-release
<<'COMMENT'
CentOS Linux release 7.4.1708 (Core)
COMMENT
```

### Apache2源码安装

Apache2主要依赖以下三个组件：

- Apache Portable Runtime(APR)
- Apache Portable Runtime Util(APR-Util)
- Perl-Compatible Regular Expressions Library (PCRE)

##### 解决编译工具gcc依赖

``` shell
ls gcc-dep/

<<'COMMENT'
cpp-4.8.5-16.el7_4.2.x86_64.rpm
gcc-c++-4.8.5-16.el7_4.2.x86_64.rpm
libgomp-4.8.5-16.el7_4.2.x86_64.rpm]
libstdc++-devel-4.8.5-16.el7_4.2.x86_64.rpm
gcc-4.8.5-16.el7_4.2.x86_64.rpm 
libgcc-4.8.5-16.el7_4.2.x86_64.rpm
libstdc++-4.8.5-16.el7_4.2.x86_64.rpm
COMMENT

cd gcc-dep/
yum install -y *
```

##### 解决expat-devel依赖

``` shell
yum install -y expat-devel-2.1.0-10.el7_3.x86_64.rpm
```

##### apr源码安装

``` shell
wget http://archive.apache.org/dist/apr/apr-1.5.2.tar.gz
cd apr-1.5.2
sed -i '/$RM "$cfgfile"/d' configure
./configure --prefix=/usr/local/apr
make && make install
```

##### apr-util源码安装

``` shell
wget http://archive.apache.org/dist/apr/apr-util-1.5.2.tar.gz
cd ${cur_path}/apache2
tar -zxvf apr-util-1.5.2.tar.gz
cd apr-util-1.5.2
./configure --prefix=/usr/local/apr-util --with-apr=/usr/local/apr
make && make install
```

##### pcre源码安装

``` shell
wget https://ftp.pcre.org/pub/pcre/pcre-8.41.tar.gz
tar -zxvf pcre-8.41.tar.gz
cd pcre-8.41
./configure --prefix=/usr/local/pcre
make && make install
```

##### Apache2源码安装

``` shell
wget https://mirrors.tuna.tsinghua.edu.cn/apache/httpd/httpd-2.4.29.tar.gz
tar -zxvf httpd-2.4.29.tar.gz
cd httpd-2.4.29
./configure --prefix=/usr/local/apache2 --with-apr=/usr/local/apr --with-apr-util=/usr/local/apr-util --with-pcre=/usr/local/pcre --enable-so
make && make install
```


##### 检查httpd.conf的php模块

``` shell
grep 'LoadModule php7_module modules/libphp7.so' /usr/local/apache2/conf/httpd.conf
```


##### Apr和Apr-Util版本问题

原先采用`Apr-1.6.3`和`Apr-Util-1.6.1`版本，在`Apache2`的编译过程出现：

``` shell
/usr/local/apr-util/lib/libaprutil-1.so: undefined reference to `XML_GetErrorCode'
/usr/local/apr-util/lib/libaprutil-1.so: undefined reference to `XML_SetEntityDeclHandler'
/usr/local/apr-util/lib/libaprutil-1.so: undefined reference to `XML_ParserCreate'
/usr/local/apr-util/lib/libaprutil-1.so: undefined reference to `XML_SetCharacterDataHandler'
/usr/local/apr-util/lib/libaprutil-1.so: undefined reference to `XML_ParserFree'
/usr/local/apr-util/lib/libaprutil-1.so: undefined reference to `XML_SetUserData'
/usr/local/apr-util/lib/libaprutil-1.so: undefined reference to `XML_StopParser'
/usr/local/apr-util/lib/libaprutil-1.so: undefined reference to `XML_Parse'
/usr/local/apr-util/lib/libaprutil-1.so: undefined reference to `XML_ErrorString'
/usr/local/apr-util/lib/libaprutil-1.so: undefined reference to `XML_SetElementHandler'
collect2: error: ld returned 1 exit status
make[2]: *** [htpasswd] Error 1
make[2]: Leaving directory `/usr/local/httpd-2.4.29/support'
make[1]: *** [all-recursive] Error 1
make[1]: Leaving directory `/usr/local/httpd-2.4.26/support'
make: *** [all-recursive] Error 1
```

查询后无解，便更换了这两个部件的版本，从而成功。


### PHP源码安装

##### 解决rpm包依赖

``` shell
ls php-dep/

<<'COMMENT'
bzip2-1.0.6-13.el7.x86_64.rpm 
krb5-devel-1.15.1-8.el7.x86_64.rpm
libsepol-devel-2.5-6.el7.x86_64.rpm
pcre-8.32-17.el7.x86_64.rpm
bzip2-devel-1.0.6-13.el7.x86_64.rpm
libcom_err-devel-1.42.9-10.el7.x86_64.rpm
libverto-devel-0.2.5-4.el7.x86_64.rpm
pcre-devel-8.32-17.el7.x86_64.rpm
epel-release-7-11.noarch.rpm
libkadm5-1.15.1-8.el7.x86_64.rpm
libxml2-devel-2.9.1-6.el7_2.3.x86_64.rpm
xz-devel-5.2.2-1.el7.x86_64.rpm
keyutils-libs-devel-1.5.8-3.el7.x86_64.rpm
libselinux-devel-2.5-11.el7.x86_64.rpm
openssl-devel-1.0.2k-8.el7.x86_64.rpm
zlib-devel-1.2.7-17.el7.x86_64.rpm
COMMENT

cd php-dep/
yum install -y *
```

##### php72源码安装

> php安装前必须安装Apache2，因为需要参数"--with-apxs2"

``` shell
wget http://cn2.php.net/get/php-7.2.3.tar.gz/from/this/mirror
tar -zxvf php-7.2.3.tar.gz
cd php-7.2.3
./configure --with-apxs2=/usr/local/apache2/bin/apxs
make && make install
cp php.ini-development /usr/local/lib/php.ini

cat >> /usr/local/apache2/conf/httpd.conf <<'EOF'
<FilesMatch "\.ph(p[2-6]?|tml)$">
    SetHandler application/x-httpd-php
</FilesMatch>
EOF

```


### 开启Apache2

```
/usr/local/apache2/bin/apachectl start
```

### 丢入php文件

``` shell
cp hereisphp.php /usr/local/apache2/htdocs
```

便可在`http://ip:80/hereisphp.php`访问php页面。

更改端口的操作：

``` shell
# 更改配置文件
sed -i 's/Listen 80/Listen 8855/g' /usr/local/apache2/conf/httpd.conf

# 重启apache2服务
/usr/local/apache2/bin/apachectl restart
```


### 参考文献

1. [centos7安装apache](https://www.cnblogs.com/subendong/p/7746999.html)
2. [CentOS7 源码安装apache遇到的坑](https://segmentfault.com/a/1190000013760266)
3. [Unix系统下的Apache 2.x](http://php.net/manual/zh/install.unix.apache2.php)
4. [PHP undefined reference to ts_resource_ex](https://stackoverflow.com/questions/29528699/php-undefined-reference-to-ts-resource-ex)


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2018/03/19/Install-Php27-With-Apache2-From-Source/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
