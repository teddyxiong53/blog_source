---
title: js之Array
date: 2018-12-22 14:37:17
tags:
	- js
---



属性有3个：

1、constructor。

2、length。

3、prototype。



对象方法有：

```
concat：把2个数组连起来。

```



日常使用：

```
//拿到长度
console.log("length:", arr.length)
//遍历数组
arr.forEach(function(item, index, array) {
  console.log(item, index)
})
```



参考资料

1、JavaScript Array 对象

http://www.runoob.com/jsref/jsref-obj-array.html

2、常用操作

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Array