---
layout:     post
title:      "使用PhantomJS和CasperJS"
subtitle:   "Use PhantomJS&CasperJS"
date:       Wed, May 11 2016 14:42:29 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Use-PhantomJS&CasperJS/head_blog.jpg"
catalog:    true
tags: [工作, JavaScript]
---

### 摘要

CasperJS是一个开源的导航脚本处理和测试工具，基于PhantomJS（前端自动化测试工具）编写。CasperJS简化了完整的导航场景的过程定义，提供了用于完成常见任务的实用的高级函数、方法和语法。

可以处理网页动态产生的数据爬取问题。

### 安装

#### PhantomJS

- PhantomJS安装：`sudo apt-get install phantomjs`

- 检测：`phantomjs --version`

#### Casperjs

- Casperjs安装：去 [Casperjs官网](http://casperjs.org/)下载，解压到对应的目录中，
- 做个链接：
`sudo ln -sf /home/chenjian/App/casperjs-1.1.1/bin/casperjs /usr/local/bin/casperjs`
- 检测：`casperjs --version`


##### CasperJS实例

目标：![淘宝一物品](/img/in-post/Use-PhantomJS&CasperJS/1482053889447_2.jpg)

`casperjs amzoe.js`的代码：

``` javascript
var brower = require('casper').create();
var productPrice;

// 1. 打开浏览器
brower.start();

// 2. 打开页面
brower.thenOpen('https://item.taobao.com/item.htm?spm=a217l.1100141.1998016669-3.3.jUiKPK&id=529573036758');

// 3. 开始搜索价格
brower.then(function getPrice() {
	productPrice = brower.evaluate(function getPriceFromPage() {
		return	price = document.getElementById('J_PromoPriceNum').innerText.trim();
	});
});

// 4. 查看价格
brower.then(function outputProductPrice() {
	console.log(productPrice);
	brower.exit();
});

// 将前面定义的步骤 跑起来
brower.run();
```

- 运行：`casperjs amzoe.js`
	
	结果：`518.00`

### 参考博文

1. [Ubuntu 14.04 下安装 Phantomjs + Casperjs](http://gaoke0820.blog.163.com/blog/static/2166496520152310371358/)
2. [萌萌CasperJS第1篇 1分钟写完爬虫 拿亚马逊商品数据](http://blog.csdn.net/sagomilk/article/details/20800543)
3. [getElementsByTagName和getElementById 的区别](http://zhidao.baidu.com/link?url=ZLMMj-mkU9b_aHFjEjPmXhHhbGgdosAXekXZgaf3UfYDToiAjkUNUSMz6UBRzMrhwgiw8WWNYIzHr2COeGBAoK)

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2016/05/11/Use-PhantomJS&CasperJS/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
