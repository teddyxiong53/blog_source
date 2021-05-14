---
title: Linux之给网卡分配0.0.0.0这个ip的作用
date: 2021-04-29 15:46:34
tags:
	- Linux
---

--

在有些脚本里，经常看到这样用：

```
ifconfig wlan0 0.0.0.0
```

这个有什么意义呢？

相当于C语言里内存操作memset吧。先清空一下当前的ip地址。

方便从dhcp重新获取。



参考资料

1、

https://serverfault.com/questions/713884/what-does-the-command-ifconfig-interface-0-0-0-0-do