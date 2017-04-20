---
layout:     post
title:      "Play API With Swagger"
subtitle:   "The Lord is my shepherd; I shall not want. Psa 23:1"
date:       Wed, Apr 19 2017 10:13:44 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Play-API-With-Swagger/head_blog.jpg"
catalog:    true
tags:
    - 工作
    - Python
---

### DIY搭建Swagger-UI

##### 下载Swagger-UI项目

``` git
git clone https://github.com/swagger-api/swagger-ui.git
```

我们需要关注`/dist/index.html`中的下一段：

``` javascript
 // Build a system
  const ui = SwaggerUIBundle({
    url: "http://petstore.swagger.io/v2/swagger.json",
    dom_id: '#swagger-ui',
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ],
    plugins: [
      SwaggerUIBundle.plugins.DownloadUrl
    ],
    layout: "StandaloneLayout"
  })
```

可参考说明文档中的*SwaggerUIBundle*[^1]

##### 下载Swagger-Editor项目

``` git
git clone https://github.com/swagger-api/swagger-editor
```

该项目需要`Node 6.x`和`NPM 3.x`

运行：

``` bash
npm start
```

便会开启3001端口。在浏览器中进行编译。编译以`YAML`格式进行，很简单。编译完后，可以导出成`JSON`格式／`YAML`格式，例如导出为`swagger.yml`

##### DIY搭建UI

可以参考博文

1. SwaggerUI教程API文档神器搭配Node使用[^2]
2. swagger环境的搭建[^3]

或者跟着我做：



``` bash
node -v
v6.9.5

npm -v
3.10.10

mkdir swapperApi
cd swapperApi

npm init

# 以下随意编写
name: (node_app) node_app
version: (1.0.0)
description:
entry point: (index.js)
test command:
git repository:
keywords:
author:
license: (ISC)
# 以上随意编写

# 安装express
npm install express --save

cat << EOF > index.js 
var express = require('express');
var app = express();
app.get('/', function (req, res) {
    app.use('/static', express.static('docs'));
    res.send('Hello World!');
});

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});
EOF

mkdir docs
cd docs

# 将clone好的Swagger-UI项目下的`dist/`目录下的所有文件复制到该文件夹docs下；
# 将导出的`swagger.yml`文件放到文件夹docs下
# 修改`docs/index.html`中的内容
# 将
# url: "http://petstore.swagger.io/v2/swagger.json",
# 改为
# url: "/static/swagger.yml",
```

运行：

``` bash
node index.js
```

打开浏览器`http://127.0.0.1:3000/static/`即可访问


### Docker搭建Swagger-UI

##### 官方docker搭建

没玩过**Docker**，来看[Easy With Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)吧！

``` bash
# 在Swagger-UI项目下
docker build -t swagger-ui .
docker run -idt -p 80:8080 swagger-ui
```

通过浏览器访问`http://127.0.0.1`即可

#### DIY实用docker搭建

- 添加swagger.yaml文件到Swagger-UI目录下（同样JSON格式也可以）

- 修改Dockfile文件夹,添加以下两行

``` docker
# 将swagger.yaml的路径写入环境变量中
ENV SWAGGER_YAML "/usr/share/nginx/html/swagger.yaml"

# 将swagger.yaml文件加入到含有index.html的文件夹中
ADD swagger.yaml /usr/share/nginx/html/swagger.yaml
```

- 修改docker-run.sh文件夹

``` bash
# 该句含义很简单。就是判断${SWAGGER_YAML},即
# /usr/share/nginx/html/swagger.yaml 
# 这个文件是否存在
# 如果存在，则会修改index.html文件中的一句话，即
# 将
# http://petstore.swagger.io/v2/swagger.json
# 替换为
# swagger.yaml
if [[ -f $SWAGGER_YAML ]]; then
  sed -i "s|http://petstore.swagger.io/v2/swagger.json|swagger.yaml|g" $INDEX_FILE
  sed -i "s|http://example.com/api|swagger.yaml|g" $INDEX_FILE
else
  sed -i "s|http://petstore.swagger.io/v2/swagger.json|$API_URL|g" $INDEX_FILE
  sed -i "s|http://example.com/api|$API_URL|g" $INDEX_FILE
fi
```

- 创建镜像与运行

``` bash
# 在Swagger-UI项目下
docker build -t swagger-ui-diy .
docker run -idt -p 80:8080 swagger-ui-diy
```

通过浏览器访问`http://127.0.0.1`即可

### Django加入Swagger-UI

通过上面两个章节，我们可以看出来，第一个基于nodejs，一个基于nginx。在Django中也可以植入swagger，将其改造为一个app即可。

最初看到这样一篇博客：一个简便的django-app将swagger-ui搬到项目中展示[^4]，然后找到其Github上的源码[cocoakekeyu/swaggerdoc](https://github.com/cocoakekeyu/swaggerdoc)，clone下来学习了一番。

总结如下：

- 该项目将swagger-ui变成Django中的swaggerdoc这个app
- 一些Django的基础知识：
	- templates中放html文件
	- static中放dist文件夹
	- dist中存放所需的css，js和image等等
	- docs中存放swagger需要读入的yaml文件
- 较为有特色的是修改了html文件，加入了个性化的页面设定

运行其源码很顺利，也很直观。

接下来，根据最新的Swagger-UI项目来做。

##### 创建app

``` bash
# 在Django项目的app文件夹下
mkdir apidoc

cd apidoc

mkdir static
mkdir templates
```

##### 修改setting配置

``` python
INSTALLED_APPS = (
    'qgsprocessor2017.apps.apidoc',
)

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'apps/apidoc/static'),
)
```

##### 导入dist文件夹

- 将项目Swagger-UI中的dist文件夹直接放在`/app/apidoc/static/`下面

- 将`dist`文件夹下的`index.html`文件放到`templates`文件夹下

- 保证`dist`文件夹下有已经生成好的`swaggger.yaml`文件

##### view.py

``` python
#!/usr/bin/python
# -*- encoding=utf-8 -*-

from django.shortcuts import render

def api_documents(request):
    """

    :param request:
    :return:
    """
    return render(
        request=request,
        template_name='index.html'
    )
```

##### apidoc/urls.py

``` python
from django.conf.urls import url
from qgsprocessor2017.apps.apidoc.views import api_documents

urlpatterns = [
    url(r'^$', api_documents),
]
```

##### 整个项目的urls.py

``` python
from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/doc/', include("mouprojects.apps.apidoc.urls")),
]
```

##### 修改index.html

由于博客中的Liquid会读取markdown下面的html，会与一些django内部的html语言发生冲突，而是只能是有图片形式

![index1](/img/in-post/Play-API-With-Swagger/index1.png)

![index2](/img/in-post/Play-API-With-Swagger/index2.png)


##### 访问api/doc

浏览器输入`http://127.0.0.1:8000/api/doc/`即可

### Issues

在UI中的`Try it out`后`Execute`没有反应。
看了下，貌似curl语句有问题。
暂时放弃解决这个问题。在此记录


[^1]: [SwaggerUIBundle](https://github.com/swagger-api/swagger-ui#swaggeruibundle)
[^2]: [SwaggerUI教程API文档神器搭配Node使用](http://www.cnblogs.com/weixing/p/6264310.html)
[^3]: [swagger环境的搭建](http://blog.csdn.net/ron03129596/article/details/53559803)
[^4]: [一个简便的django-app将swagger-ui搬到项目中展示](http://www.ctolib.com/swaggerdoc.html)

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2016/04/19/Play-API-With-Swagger/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。