---
title: Linux之ps命令卡住
date: 2019-08-23 09:51:03
tags:
	- Linux
---

1

我的Ubuntu很长一段时间以来，执行ps aux后，就卡住无法退出。

现在看看是怎么回事。

用strace ps aux。

可以看到是卡在这里：

```
open("/proc/4050/status", O_RDONLY)     = 6
read(6, "Name:\tXorg\nUmask:\t0022\nState:\tD "..., 2048) = 1296
close(6)                                = 0
open("/proc/4050/cmdline", O_RDONLY)    = 6
read(6, 
```

网上说是因为有进程处于不可中断的sleep状态。

在ps的输出里，显示状态为D的就是。

如果重启没有用，那么就是你的磁盘有坏的扇区，进程在启动的时候试图读取那里的文件。

我当前看到的进程是pidof。有很多这个进程，都是D状态的。

进入D状态，一般是io访问出问题了导致的。

要解决只能通过重启。

还有修改内核的方式来解决。但是这个就太高级了点。



参考资料

1、Suggestions needed to debug why ps -ef gets stuck

https://unix.stackexchange.com/questions/10980/suggestions-needed-to-debug-why-ps-ef-gets-stuck

2、Linux进程状态：D

https://blog.csdn.net/djskl/article/details/44887017

3、Linux杀掉D状态进程

https://blog.csdn.net/RegretPain/article/details/78215227