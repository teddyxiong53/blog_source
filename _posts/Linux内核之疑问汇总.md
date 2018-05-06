---
title: Linux内核之疑问汇总
date: 2018-05-02 09:43:52
tags:
	- Linux内核

---



# down_interruptible被打断是指被什么打断？

http://blog.chinaunix.net/uid-20801390-id-1839286.html

被打断是指被信号打断。

如果获得信号，程序可以继续运行，否则休眠。

这里的信号是指标准的posix信号。例如ctrl+c杀死进程。

也就是说，这个down_interruptible的等待，可以被用户取消掉。

虽然这个代码写在