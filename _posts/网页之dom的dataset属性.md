---
title: 网页之dom的dataset属性
date: 2019-03-19 13:43:32
tags:
	- 网页

---





有时候，需要在html元素上附加数据。供js代码使用。

一种解决办法是自定义属性。

```
<div id="mydiv" foo="bar"></div>
```

这样，就是为div定义了一个foo属性，它的值为bar。

可以用getAttribute和setAttribute这2个接口来进行读写。

```
var n = document.getElementById("mydiv");
n.getAttribute("foo");
n.setAttribute("foo", "baz");
```

这种方式虽然可以达到目的，但是会使得html元素不符合标准，使得html代码通不过校验。

更好的解决办法是：使用标准提供的data-*属性。

```
<div id="mydiv" data-foo="bar>
```

操作是这样：

```
var n = document.getElementById("mydiv");
console.log(n.dataset.foo);//get
n.dataset.foo = "baz";//set
```

还可以删除这个属性。

```
delete document.getElementyById("mydiv").dataset.foo;
```

但是用getAttribute("data-foo")也是可以的。

data-后面跟的名字，有一些要求：

一般只用小写字母和连字符就好。

到了js代码里，data-hello-world，会变成dataset.helloWorld。



参考资料

1、Dom模型之dataset属性/Html元素标签的data-*属性

https://blog.csdn.net/wsxujiacheng/article/details/75382075