---
title: http之url中的符号用途
date: 2018-02-28 10:48:21
tags:
	- http

---



# #1.问号

问号有2个作用：

1、连接作用。例如：

```
http://www.xxx.com/show.jsp?id=123&name=xxx&page=1
```

2、清除缓存。

```
http://www.xxx.com/index.html
http://www.xxx.com/index.html?test123
```

这个2个url打开的页面一样，但是后面一个有问号，表示不调用缓存的内容。重新读取。



# 2. 与号

不同参数的间隔符。

