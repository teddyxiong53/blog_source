---
title: jquery之$(this)用法
date: 2019-03-03 21:26:03
tags:
	- jquery
---



根据$()返回的是jquery对象这个原则。

我们可以得到结论：

$(this)得到的是一个jquery对象。

用来把当前对象转成一个jquery对象。

```
console.log("this:",this)
console.log("$(this)", $(this))
```

表示的都是同一个radio元素。



# 参考资料

1、jQuery中的this用法

https://blog.csdn.net/xuwenpeng/article/details/6461125

2、jquery中this与$(this)的用法区别

https://my.oschina.net/rouchongzi/blog/111987