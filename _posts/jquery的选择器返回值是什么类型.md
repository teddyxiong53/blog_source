---
title: jquery的选择器返回值是什么类型
date: 2019-03-04 10:12:03
tags:
	- jquery
---





例如选择所有的li元素。得到的并不是一个js数组。不能forEach循环遍历。

实际上返回的是一个jquery对象。

类似数组，有length属性。

可以用[]来进行索引 。

对于js数组，可以用find函数来过滤元素，也可以用filter函数。

jquery里也有这2个函数，但是不一样了。

```
而一个更通用的方法是使用选择器，比如：$(“div”).filter(“.rain”) 等同于 $(“div .rain”)。
```



可以把jquery对象转成数组。

```
var obj = $("li")
var arr = $.makeArray(obj)

```



参考资料

1、jQuery选择器的返回值

http://nferzhuang.com/jquery选择器的返回值/