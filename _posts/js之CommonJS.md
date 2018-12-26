---
title: js之CommonJS
date: 2018-12-26 11:19:27
tags:
	- js
---





commonjs是一个规范，这个规范的目的是：

帮助js提高大型软件开发的能力。



commonjs规范规定：

1、一个文件就是一个模块。拥有单独的作用域。

2、普通方式定义的变量、函数、对象都属于该模块内。

3、通过require来加载模块。

4、通过exports和module.exports来暴露模块里的内容。



commonjs是服务器端模块的规范。

nodejs就采用了这套规范。

这套模块方案，对于服务端是可行的，因为require的方式加载模块，是同步的。

对于浏览器，不行，浏览器需要异步的。所以浏览器端，用的是AMD。

AMD的，是通过define这一个函数来做的 。

一个简单的例子是这样。

```
define( [
	"./arr"
], function( arr ) {
	"use strict";

	return arr.indexOf;
} );
```



参考资料

1、CommonJS规范

https://www.cnblogs.com/littlebirdlbw/p/5670633.html

2、JavaScript模块化编程 - CommonJS, AMD 和 RequireJS之间的关系

https://www.cnblogs.com/web-java/p/3506345.html