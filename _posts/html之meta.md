---
title: html之meta
date: 2018-08-22 21:22:35
tags:
	- html

---



meta标签是head区里的一个关键标签。一个辅助性标签。



提供：

1、字符集。

2、语言。

3、作者信息。

4、关键词和网页等级。

最大的作用是SEO 。

```
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
```



http-equiv的取值可以是：

1、content-type。

2、default-style。

3、refresh。指定自动刷新的时间间隔。



为了让搜索引擎搜索到你的网页。

代码里可以这样写。

```
<meta name="keywords" content="xx yy">
<meta name="description" content="aa bb">
```



下面这个是为了说明网页是怎么生成的。可以是FrontPage。

```
<meta name="generator" content="emlog" />
```



# 参考资料

1、html meta标签使用总结

https://www.cnblogs.com/moyingliang/p/5748043.html

2、`HTML <meta> http-equiv 属性`

http://www.runoob.com/tags/att-meta-http-equiv.html