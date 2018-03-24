---
title: qemu之mini2440环境搭建（二）
date: 2018-03-24 23:12:33
tags:
	- qemu

---



这个采用buildroot来做。

定制的qemu是一样。不再重新下载。

buildroot下载非常卡，只能用ssr翻墙了。



编译过程中还碰到几个错误。

```
conftest.c:14625: must be after `@defmac' to use `@defmacx'
Makefile:241: recipe for target 'autoconf.info' failed
```

https://blog.csdn.net/laohuang1122/article/details/44098291/

参考这篇文章来修改。

就macro ovar和macro dvar要去掉最后面的`@`。

