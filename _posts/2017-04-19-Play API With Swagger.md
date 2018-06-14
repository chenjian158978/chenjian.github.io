---
layout:     post
title:      "玩转API框架之Swagger"
subtitle:   "Play API With Swagger"
date:       Wed, Apr 19 2017 10:13:44 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Play-API-With-Swagger/head_blog.jpg"
catalog:    true
tags: [工作, Python]
---

### DIY搭建Swagger-UI

##### 下载Swagger-UI项目

``` sh
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

``` sh
git clone https://github.com/swagger-api/swagger-editor
```

该项目需要`Node 6.x`和`NPM 3.x`

运行：

``` sh
npm start
```

便会开启3001端口。在浏览器中进行编译。编译以`YAML`格式进行，很简单。编译完后，可以导出成`JSON`格式／`YAML`格式，例如导出为`swagger.yml`

##### DIY搭建UI

可以参考博文

1. SwaggerUI教程API文档神器搭配Node使用[^2]
2. swagger环境的搭建[^3]

或者跟着我做：



``` sh
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

``` sh
node index.js
```

打开浏览器`http://127.0.0.1:3000/static/`即可访问


### Docker搭建Swagger-UI

##### 官方docker搭建

没玩过**Docker**，来看[带你玩转Docker](https://o-my-chenjian.com/2016/07/04/Easy-With-Docker/)吧！

``` sh
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

``` sh
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

``` sh
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

``` sh
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

代码下载：[view.py](/download/Play-API-With-Swagger/view.py)

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

代码下载：[urls.py](/download/Play-API-With-Swagger/apidoc/urls.py)

``` python
#!/usr/bin/python
# -*- encoding=utf-8 -*-

from django.conf.urls import url
from qgsprocessor2017.apps.apidoc.views import api_documents

urlpatterns = [
    url(r'^$', api_documents),
]
```

##### 整个项目的urls.py

代码下载：[urls.py](/download/Play-API-With-Swagger/urls.py)

``` python
#!/usr/bin/python
# -*- encoding=utf-8 -*-

from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/doc/', include("mouprojects.apps.apidoc.urls")),
]
```

##### 修改index.html

代码下载：[index.html](/download/Play-API-With-Swagger/index.html)

``` html
{% raw %}{% load staticfiles %}
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/2000/svg">
<head>
    <meta charset="UTF-8">
    <title>Swagger UI</title>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,700|Source+Code+Pro:300,600|Titillium+Web:400,600,700" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="{% static 'dist/swagger-ui.css' %}" >
    <link rel="icon" type="image/png" href="{% static 'dist/favicon-32x32.png' %}" sizes="32x32" />
    <link rel="icon" type="image/png" href="{% static 'dist/favicon-16x16.png' %}" sizes="16x16" />
    <style>
        html
        {
            box-sizing: border-box;
            overflow: -moz-scrollbars-vertical;
            overflow-y: scroll;
        }
        *,
        *:before,
        *:after
        {
            box-sizing: inherit;
        }
        body {
            margin:0;
            background: #fafafa;
        }
    </style>
</head>
<body>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="position:absolute;width:0;height:0">
    <defs>
        <symbol viewBox="0 0 20 20" id="unlocked">
            <path d="M15.8 8H14V5.6C14 2.703 12.665 1 10 1 7.334 1 6 2.703 6 5.6V6h2v-.801C8 3.754 8.797 3 10 3c1.203 0 2 .754 2 2.199V8H4c-.553 0-1 .646-1 1.199V17c0 .549.428 1.139.951 1.307l1.197.387C5.672 18.861 6.55 19 7.1 19h5.8c.549 0 1.428-.139 1.951-.307l1.196-.387c.524-.167.953-.757.953-1.306V9.199C17 8.646 16.352 8 15.8 8z"></path>
        </symbol>
        <symbol viewBox="0 0 20 20" id="locked">
            <path d="M15.8 8H14V5.6C14 2.703 12.665 1 10 1 7.334 1 6 2.703 6 5.6V8H4c-.553 0-1 .646-1 1.199V17c0 .549.428 1.139.951 1.307l1.197.387C5.672 18.861 6.55 19 7.1 19h5.8c.549 0 1.428-.139 1.951-.307l1.196-.387c.524-.167.953-.757.953-1.306V9.199C17 8.646 16.352 8 15.8 8zM12 8H8V5.199C8 3.754 8.797 3 10 3c1.203 0 2 .754 2 2.199V8z"/>
        </symbol>
        <symbol viewBox="0 0 20 20" id="close">
            <path d="M14.348 14.849c-.469.469-1.229.469-1.697 0L10 11.819l-2.651 3.029c-.469.469-1.229.469-1.697 0-.469-.469-.469-1.229 0-1.697l2.758-3.15-2.759-3.152c-.469-.469-.469-1.228 0-1.697.469-.469 1.228-.469 1.697 0L10 8.183l2.651-3.031c.469-.469 1.228-.469 1.697 0 .469.469.469 1.229 0 1.697l-2.758 3.152 2.758 3.15c.469.469.469 1.229 0 1.698z"/>
        </symbol>
        <symbol viewBox="0 0 20 20" id="large-arrow">
            <path d="M13.25 10L6.109 2.58c-.268-.27-.268-.707 0-.979.268-.27.701-.27.969 0l7.83 7.908c.268.271.268.709 0 .979l-7.83 7.908c-.268.271-.701.27-.969 0-.268-.269-.268-.707 0-.979L13.25 10z"/>
        </symbol>
        <symbol viewBox="0 0 20 20" id="large-arrow-down">
            <path d="M17.418 6.109c.272-.268.709-.268.979 0s.271.701 0 .969l-7.908 7.83c-.27.268-.707.268-.979 0l-7.908-7.83c-.27-.268-.27-.701 0-.969.271-.268.709-.268.979 0L10 13.25l7.418-7.141z"/>
        </symbol>
        <symbol viewBox="0 0 24 24" id="jump-to">
            <path d="M19 7v4H5.83l3.58-3.59L8 6l-6 6 6 6 1.41-1.41L5.83 13H21V7z"/>
        </symbol>
        <symbol viewBox="0 0 24 24" id="expand">
            <path d="M10 18h4v-2h-4v2zM3 6v2h18V6H3zm3 7h12v-2H6v2z"/>
        </symbol>
    </defs>
</svg>
<div id="swagger-ui"></div>
<script src="{% static 'dist/swagger-ui-bundle.js' %}"></script>
<script src="{% static 'dist/swagger-ui-standalone-preset.js' %}"></script>
<script>
    window.onload = function() {
        // Build a system
        const ui = SwaggerUIBundle({
            url: "{% static 'dist/swagger.yaml' %}",
            dom_id: '#swagger-ui',
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIStandalonePreset
            ],
            plugins: [
                SwaggerUIBundle.plugins.DownloadUrl
            ],
            layout: "StandaloneLayout"
        });
        window.ui = ui
    }
</script>
</body>
</html>{% endraw %}
```

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

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/04/19/Play-API-With-Swagger/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。