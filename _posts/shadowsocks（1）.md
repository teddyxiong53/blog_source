---
title: shadowsocks（1）
date: 2018-07-04 21:54:51
tags:
	-shadowsocks

---



现在阅读ss的源代码。

通过写代码的方式来阅读。

往这个地方提交。

https://github.com/teddyxiong53/Python/tree/master/shadowsocks

在pycharm里，新建一个shadowsocks工程。

里面新建一个shadowsocks目录。

新建local.py文件。加入main。

新建shell.py文件。

新建common.py文件。



dns_resolver

这个的作用是什么？

开始引入了lru_cache.py文件。

这里开始设计socket相关协议了。



在windows下的select，只有select是有的。

```
import select

if hasattr(select, 'epoll'):
    print "has epoll"

if hasattr(select, 'kqueue'):
    print "has kqueue"

if hasattr(select, 'select'):
    print "has select"
```

