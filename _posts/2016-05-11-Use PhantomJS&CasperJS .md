---
layout:     post
title:      "Use PhantomJS&CasperJS"
subtitle:   "O Lord our Lord,
how excellent is thy name in all the earth! Psa 8:9"
date:       Wed, May 18 14:42:29 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Use-PhantomJS&CasperJS/head_blog.jpg"
tags:
    - 工作
    - javascript
---

## 摘要

CasperJS是一个开源的导航脚本处理和测试工具，基于PhantomJS（前端自动化测试工具）编写。CasperJS简化了完整的导航场景的过程定义，提供了用于完成常见任务的实用的高级函数、方法和语法。

可以处理网页动态产生的数据爬取问题。

## 安装

### PhantomJS

- PhantomJS安装：`sudo apt-get install phantomjs`

- 检测：`phantomjs --version`

### Casperjs

- Casperjs安装：去 [Casperjs官网](http://casperjs.org/)下载，解药到对应的目录中，
- 做个链接：
`sudo ln -sf /home/chenjian/App/casperjs-1.1.1/bin/casperjs /usr/local/bin/casperjs`
- 检测：`casperjs --version`


## CasperJS实例

目标：![淘宝一物品](/img/in-post/Use-PhantomJS-CasperJS/1482053889447_2.png)

`casperjs amzoe.js`的代码：

```javascript
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

## 参考

1. [Ubuntu 14.04 下安装 Phantomjs + Casperjs](http://gaoke0820.blog.163.com/blog/static/2166496520152310371358/)
2. [萌萌CasperJS第1篇 1分钟写完爬虫 拿亚马逊商品数据](http://blog.csdn.net/sagomilk/article/details/20800543)
3. [getElementsByTagName和getElementById 的区别](http://zhidao.baidu.com/link?url=ZLMMj-mkU9b_aHFjEjPmXhHhbGgdosAXekXZgaf3UfYDToiAjkUNUSMz6UBRzMrhwgiw8WWNYIzHr2COeGBAoK)