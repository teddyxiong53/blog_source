---
title: qemu之使用经验
date: 2018-03-26 20:54:33
tags:
	- qemu

---



1、加上`-serial stdio`和不加的区别。

在带图形界面启动的时候，就不一样了。

不加：命令行卡住了。

加上：命令行可以继续输入。

2、指定内存大小。

这样：

```
qemu-system-arm -M vexpress-a9 -m 1G 
```

这样就指定了1G的内容。如果指定超出了。就会报错：

```
vexpress-a9: cannot model more than 1GB RAM
```



