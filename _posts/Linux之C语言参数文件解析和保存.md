---
title: Linux之C语言参数文件解析和保存
date: 2018-11-23 14:43:31
tags:
	- Linux

---



需要找到一个比较简单、健壮又通用的参数保存机制。

json是我的首选。

但是一般的Linux程序都是简单的基于行的配置。类似这种。

```
name=xxx
age=10
#this is comment
```

不过这种，一般没有看到保存参数的，都是启动时读取，后面就不管了。

而我现在需要



这个是简单的ini处理的。

https://github.com/brofield/simpleini









