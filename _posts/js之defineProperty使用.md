---
title: js之defineProperty使用
date: 2019-03-14 17:00:11
tags:
	- js

---



1

defineProperty，是给对象定义属性。

在js里，我们有这么几种方法来给对象定义属性。

```
//方法1：用点号。
xx.name = "xhl"
//方法2：用索引
xx['name'] = "xhl"
//方法3：用defineProperty
Object.defineProperty(xx, "name", {
    value: "xhl"
})
```

看起来defineProperty这种方式，比较麻烦。

那么为什么还存在这种方式呢？



defineProperty这个函数会返回对象本身。

语法格式是：

```
Object.defineProperty(object, propertyName, descriptor)
```

3个参数都是必须的。

description是重点。

```
可以设置的属性有：
value
writable
configurable
enumable
get
set
```



在vue、react等框架里，经常看一看看到这个函数的使用。



参考资料

1、不会Object.defineProperty你就out了

https://imweb.io/topic/56d40adc0848801a4ba198ce