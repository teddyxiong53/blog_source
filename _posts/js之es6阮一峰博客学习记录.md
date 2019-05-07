---
title: js之es6阮一峰博客学习记录
date: 2019-05-07 14:25:28
tags:
	- js

---



博客在这里。

http://es6.ruanyifeng.com/#docs/intro

```
0、前言
1、es简介
2、let和const
3、变量的解构赋值
4、字符串的扩展
5、字符串的新增方法
6、正则的扩展
7、数值的扩展
8、函数的扩展
9、数组的扩展
10、对象的扩展
11、对象的新增方法
12、Symbol
13、Set和Map
14、Proxy
15、Reflect
16、Promise
17、Iterator和for-of循环。
18、Generator函数的语法
19、Generator函数的异步应用
20、async函数
21、Class的基本语法。
22、Class的继承
23、Module的语法
24、Module的加载实现。
25、编程风格
26、读懂规格
27、ArrayBuffer
28、最新提案
29、Decorator
30、参考
```

# 1.es简介

查看node对es6的支持情况。

```
node --v8-options | grep harmony
```

# 2.let和const

let定义的，在大括号外面不可见。

```
{
    var a = 1;
    let b =2;
}

a
b
```

for循环里的i，很适合用let来定义。

以前在es5里，只有全局作用域和函数作用域，没有块级作用域。

这个带来了很多的问题。

1、变量覆盖。

2、循环计数变量泄露到外面。

```
let a = 1
{
    let a = 2;
    console.log(a);
}
```

这个用babel转码，得到这样：

```
"use strict";

var a = 1;
{
    var _a = 2;
    console.log(_a);
}
```

顶层对象，在浏览器环境指的是window对象，在 Node 指的是global对象。ES5 之中，顶层对象的属性与全局变量是等价的。



顶层对象跟全局变量挂钩，被认为是js最大的设计败笔之一。

从 ES6 开始，全局变量将逐步与顶层对象的属性脱钩。

用let定义的全局变量，不会被自动添加到顶层对象（浏览器的window，nodejs的global）。

```
let xx = 1
window.xx //不存在的。
var yy = 2
window.yy //是存在的
```

# 3.解构赋值

主要作用：

```
1、交换变量的值。
	let x = 1;
	let y = 2;
	[x, y] = [y, x]
2、从函数返回多个值。
	返回数组
	function func() {
		return [1,2,3]
	}
	let [a,b,c] = func()
	返回对象
	function func() {
		return {
			a: 1,
			b: 2
		}
	}
	let {a, b} = func()
3、函数参数的定义。
	参数有顺序
	function func([x,y,z]) {
		
	}
	func([1,2,3])
	参数没有顺序
	function func({x,y,z}) {
	
	}
	func({z:3,y:2,x:1})
4、提取json数据。
	let jsonData = {
		id: 42,
		status: "ok"
	}
	let {id, status} = jsonData;
5、函数参数的默认值
	function func(arg, {a=1, b=2}) {
	
	}
	这样就可以避免在函数内部这样写了
	let xx = xx || "default param"
6、获取模块的指定方法
	const { SourceMapConsumer, SourceNode } = require("source-map");
```

