---
title: nodejs之常用工具
date: 2018-12-24 14:54:17
tags:
	- nodejs
---





util是一个nodejs核心模块，提供常用函数的集合。

用来弥补核心js功能不足的缺点。

```
util.inherits：实现对象之间的原型继承。
util.inspect：用来把任意对象转成字符串。用来调试。
util.isArray
util.isRegExp
util.isDate
util.isError
```



js的面向对象是基于原型的，这个跟一般面向对象的基于类的机制是不一样的。

js没有提供语言级别的继承机制，是通过原型复制来实现的。

```
var util = require('util')
function Base() {
	this.name = "base"
	this.base = 1991
	this.sayHello = function() {
		console.log("hello " + this.name)
	}
}

Base.prototype.showName = function() {
	console.log(this.name)
}

function Sub() {
	this.name = "sub"
}

util.inherits(Sub, Base)
var objBase = new Base()
objBase.sayHello()
objBase.showName()
console.log(objBase)
var objSub = new Sub()
//objSub.sayHello()
objSub.showName()
console.log(objSub)
```



```
D:\work\test
λ  node test.js
hello base
base
Base { name: 'base', base: 1991, sayHello: [Function] }
sub
Sub { name: 'sub' }
```



参考资料

1、Node.js 常用工具

http://www.runoob.com/nodejs/nodejs-util.html