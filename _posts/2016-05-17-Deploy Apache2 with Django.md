---
layout:     post
title:      "Deploy Apache2 with Django"
subtitle:   " \"Hello World, Hello Blog\""
date:       Tue, May 17 15:16:04 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Deploy-Apache2-With-Django/head_blog.png"
tags:
    - 工作
    - Python
---

## Django项目

- 参考于[《自强学堂——django后台》](http://www.ziqiangxuetang.com/django/django-admin.html)

- 项目名称：zqxt_admin

- 项目path： `/home/chenjian/PycharmProjects/zqxt_admin`

----------

## 安装 apache2 和 mod_wsgi   

```sh
sudo apt-get install apache2
 
# Python 2
sudo apt-get install libapache2-mod-wsgi
 
# Python 3
sudo apt-get install libapache2-mod-wsgi-py3
```


## 确认apache版本


```sh
apachectl -v

Server version: Apache/2.4.18 (Ubuntu)
Server built:   2016-04-15T18:00:57
```

## 遇到的问题

### 处理使用virtualenv带来的问题

参考：[部署apache，使用virtualenv，遇到的no module named django.core.wsgi](http://www.thinksaas.cn/topics/0/349/349343.html)

在wsgi.py中修改为以下：

```python
# -*- coding:utf-8 -*-

import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cluster.settings")
# sys.path.append(r'C:\Apache2\Apache2.2\htdocs\cluster')
# 添加自己的项目路径
sys.path.append(r'/home/chenjian/PycharmProjects/qgs/cluster')
# 添加virtualenv中的python所依赖的包
sys.path.append(r'/home/administrator/.venv/python2.7/local/lib/python2.7/site-packages')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

```

### 处理Permission denied

具体内容如下：

```sh
Permission denied: [client 192.168.1.243:46572] AH00035: access to /mon/ denied (filesystem path '/home/usr/webvul') because search permissions are missing on a component of the path
```

- 解决方法：

将相应的文件权限改掉：

命令：`sudo chmod -R 777 webvul/`


## 创建zqxt_admin的apache配置

命令：`sudo vim /etc/apache2/sites-available/zqxt.conf`

输入内容：

```
# 访问的服务器名称，localhost就是127.0.0.1，也可自己编写
ServerName 192.168.1.68
Listen 8003
# 
DocumentRoot /home/chenjian/PycharmProjects/zqxt_admin

#LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so
# wsgi.py文件位置，其中第二个'/'是指最后127.0.0.1/admin中的“/”；
# 如果第二个写成'/admin',则访问地址为：127.0.0.1/admin/admin/
WSGIScriptAlias / /home/chenjian/PycharmProjects/zqxt_admin/zqxt_admin/wsgi.py
# 让脚本找到项目的位置
WSGIPythonPath /home/chenjian/PycharmProjects/zqxt_admin
# 或者WSGIPythonPath如下
# sys.path.append(r'/home/administrator/.venv/python2.7/local/lib/python2.7/site-packages')

# wsgi.py文件位置，并设置权限
<Directory /home/chenjian/PycharmProjects/zqxt_admin/zqxt_admin>
<Files wsgi.py>
    Require all granted
</Files>
</Directory>
```

上面安装mod_wsgi时，会自动在`/etc/apache2/mods-enabled/`目录下生成：wsgi.load和wsgi.conf；如果没有，也可以手动载入模块：`LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so`


## 激活网站

命令：`sudo a2ensite zqxt.conf`


## 停止与启动apache服务器

命令：`sudo service apache2 start`与`sudo service apache2 stop`

p.s. 如果apache2总是失败，除了看error.log日志，勿忘重启apache服务！


## 重启apache服务器

命令:`sudo service apache2 restart`

## 访问网站

chrome浏览器中输入：[http://127.0.0.1/admin/](http://127.0.0.1/admin/)

页面显示：![访问网站](/img/in-post/Deploy-Apache2-With-Django/1481300896123_4.png)

说明：可能有些static或者其他内容没有配置，所以和平时的runserver不一样。



## 错误查看

1. 将settings.py文件修改：`DEBUG = True`
2. 重启apache服务器：`sudo service apache2 restart`
3. 查看apache错误日志：`cat /var/log/apache2/error.log `


## 其他

1. 修改settings.py文件中ALLOWED_HOSTS改为：`['127.0.0.1']`或者`'*'`，后者表示全部
2. 编码问题，在wsgi.py中加入`#-*- coding:ut-8 -*-`


## 参考：
[《自强学堂——Django 部署(Apache)》](http://www.ziqiangxuetang.com/django/django-deploy.html)