---
title: html之urlrewrite
date: 2018-08-28 22:37:00
tags:
	- html

---



url rewrite是url重写，就是把传递进来的web请求重定向到其他url的过程。

url rewrite的主要用途是url伪静态化。这个是一种把动态页面显示为静态页面的一种技术。

例如：

```
http://www.xxx.com/news/index.asp?id=123
```

使用url rewrite转换后显示为：

```
http://www.xxx.com/news/123.html
```



1、满足观感的要求。

对于追求完美的网站设计师，希望网页的网址看起来也是简单直接的。

2、可以隐藏网站使用的编程语言，还可以提高网站的可移植性。

3、最重要的是，方便搜索引擎来抓取你的网站的内容。



mod_rewrite是Apache的一个非常强大的功能。

我们可以在phpinfo里可以搜索到Apache的loaded modules。



是靠web server里定义的规则来做的。

规则写在.htaccess文件里。



# 参考资料

1、什么是URL Rewrite？URL Rewrite有什么用？

https://blog.csdn.net/shimiso/article/details/8594885

2、php 伪静态(url rewrite)apache配置！

https://blog.csdn.net/liumf2005/article/details/45224727