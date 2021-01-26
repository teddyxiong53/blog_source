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



# 不要滥用$(this)

如果不了解javasrcipt中基本的DOM属性和方法的话，很容易滥用jQuery对象。比如：

```
$(‘#someAnchor’).click(function() {

    alert( $(this).attr(‘id’) );

});
```

 

如果你只是通过jQ对象**获取简单的dom元素的属性比如id**，那么你**完全可以使用js原生的方法**：

```
$(‘#someAnchor’).click(function() {

    alert( this.id );

});
```

# 参考资料

1、jQuery中的this用法

https://blog.csdn.net/xuwenpeng/article/details/6461125

2、jquery中this与$(this)的用法区别

https://my.oschina.net/rouchongzi/blog/111987

3、jQuery中this与$(this)的区别总结

https://www.cnblogs.com/gfl123/p/8080484.html