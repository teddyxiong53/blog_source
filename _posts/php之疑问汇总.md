---
title: php之疑问汇总
date: 2018-08-15 22:23:10
tags:
	- php

---



## header函数

用途是向客户端发送原始的http包头。

```
header("location:index.php");//表示重定向到index.php。
```



## <?php 没有结束配对

这个对于纯php文件是没有关系的，如果是在html里嵌入php代码，则必须配对。

https://zhidao.baidu.com/question/1702574186544998580.html

如果是一个纯粹的PHP页面，最后的结束符?>最好一定不要添加。

## ob_start();函数

是用来控制浏览器的cache的。

ob是out buffer的缩写。

这个函数是打开缓冲区的意思。

https://www.cnblogs.com/w10234/p/5480670.html

## self和this的区别

https://blog.csdn.net/tancy_weipj/article/details/50971230

self表示当前类。

this表示当前对象。

所以self一般用来引用属于类的东西，例如静态的东西。

## @符号的作用

阻止警告的输出。

叫做错误控制运算符。

## require_once

是为了避免重复加载文件。



## session_start

https://www.cnblogs.com/hyt-jinhua/p/6404632.html