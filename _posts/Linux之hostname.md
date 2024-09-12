---
title: Linux之hostname
date: 2020-06-18 14:37:49
tags:
	- Linux

---



hostname哪些地方有：

```
/etc # cat hostname
rockchip
/etc #
/etc # cat /proc/sys/kernel/hostname
rockchip
/etc # sysctl kernel.hostname
kernel.hostname = rockchip
```

如果修改了hostname，会导致我正在运行的程序调用了gethostbyname失败。

```
gethostbyname fail, reason:Connection timed out
```



参考资料

1、

https://www.cnblogs.com/kerrycode/p/3595724.html