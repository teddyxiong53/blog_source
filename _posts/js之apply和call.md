---
title: js之apply和call
date: 2019-08-22 16:45:03
tags:
	- js
---

--

js给所有的函数都定义了call和apply这2个方法。

这2个方法的作用是一样的。

只是传递参数的形式有点区别。



apply

需要2个参数

```
参数1：
	作为函数上下文的一个对象。
参数2：
	一个数组，放传递给函数的参数。
```

举例：

```
var obj = {
    name: "xhl"
}
function func(fisrtName, lastName) {
    console.log(fisrtName + this.name + lastName)
}
func.apply(obj, ['aa', 'bb'])
```

call

参数个数不固定。除了第一个参数，后面的都是传递给函数的参数。

相当于把apply的数组去掉了。

```
var obj = {
    name: "xhl"
}
function func(fisrtName, lastName) {
    console.log(fisrtName + this.name + lastName)
}
func.call(obj, 'aa', 'bb')
```



主要应用场景

1、改变this的指向。

2、借用别的对象的方法。



参考资料

1、JavaScript 中 apply 、call 的详解

https://github.com/lin-xin/blog/issues/7