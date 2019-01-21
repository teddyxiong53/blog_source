---
title: html之localStorage
date: 2019-01-21 17:16:12
tags:
	- html
---



在html5里，加入了一个localStorage的特性。

这个特性主要是用来做本地存储的。

解决了cookie存储空间不足的问题。cookie的大小限制是4K。

localStorage的一般是5M。

查看浏览器是否支持localStorage。

```
document.write(window.localStorage);
```

设置值的三种方式：

```
var storage = window.localStorage;
storage["a"] = 1;
storage.b = 2;
storage.setItem("c", 3);
console.log(typeof storage["a"]);
console.log(typeof storage["b"]);
console.log(typeof storage["c"]);
```

可以看到都是string的了。本来是int的。

因为localStorage只支持string类型。

相应的，有3种读取方式。

```
storage.a
storage["a"]
storage.getItem("a")
```

官方推荐getItem和setItem。

删除。

```
storage.clear();//全部清空
storage.removeItem("a");
```



我们一般和json一起用。



参考资料

1、localStorage使用总结

https://www.cnblogs.com/st-leslie/p/5617130.html