---
title: python之读取网页的方法
date: 2018-10-21 11:04:06
tags:
	- python

---



Python读取网页的方法，好像有很多的库，这些库的区别是什么？分别适合什么场景？

官方自带的是urllib

# 注意

如果只使用Python3的话，只需要知道有urllib这一个就够了。

在python2里有这些库可以用：

1、urllib

2、urllib2

3、urllib3

4、httplib

5、httplib2

6、requests

在python3里，有这些库可以用：

1、urllib

2、urllib3

3、httplib2

4、requests。



urllib3和requests都不是标准库，是第三方的。

urllib3提供了线程安全的连接池和文件post支持，和urllib及urllib2的关系不大。



# urllib和urllib2的区别（python2才有）

1、urllib2可以接受Request对象为URL设置header信息。

2、urllib提供了一些原始基础方法，而urllib2没有。



# python3里的urllib的改变

在python3里，urllib被分成了几个模块。

1、urllib.request：用来打开和读取url。

2、urllib.error：用来处理request引起的异常。

3、urllib.parse：用来解析url。

4、urllib.robotparser：用来解析robots.txt文件。



# 参考资料

1、python中urllib, urllib2,urllib3, httplib,httplib2, request的区别

https://blog.csdn.net/permike/article/details/52437492