---
title: nodejs之exports和module.exports区别
date: 2019-04-16 14:00:28
tags:
	 - nodejs
---



```
1、module.exports初始值为一个空对象{}
2、exports是指向module.exports的引用。
3、require()函数返回的是module.exports。
```

我们经常看到这种写法：

```
exports = module.exports = xxx;
```



每一个nodejs文件，都自动创建了一个module对象。

同时，module对象会创建一个叫exports的属性。初始化值为{}



node在编译js模块的，对我们写的代码进行了包装，将整个文件的代码放进了一个函数里，是这个样子：

```
(function(exports,require,module,__filename,__dirname){ var bar = function(){ console.log(‘it is bar’); } module.exports = bar; });
```

从这里可以看出模块变量总共有5个：

```
exports
require
module
__filename
__dirname
```



exports的常用模式

```
我们可以选择exports这些东西：
1、命名空间。
	fs模块就是这种用法。
	怎么做的？
	var fs = exports;
	这样fs就等价于module.exports了。
	也可以给module.exports赋值一个对象。
2、一个工厂方法。
	express就是这么干的。
	
3、一个偏函数。
	偏函数就是返回函数的函数。
	
4、构造函数。
	这个也很常用。
5、单例。
	mongoose就是这样做的。
	module.exports = exports = new Mongoose();
6、扩展全局对象。
	一般不这么做。
7、实现猴子补丁。
	就是运行时动态给模块打补丁。
	
```



参考资料

1、exports 和 module.exports 的区别

https://cnodejs.org/topic/5231a630101e574521e45ef8

2、module.exports与exports？？关于exports的总结

https://cnodejs.org/topic/52308842101e574521c16e06

3、exports的用法：Node.js模块的接口设计模式

https://gywbd.github.io/posts/2014/11/using-exports-nodejs-interface-design-pattern.html