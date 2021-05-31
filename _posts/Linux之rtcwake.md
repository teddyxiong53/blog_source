---
title: Linux之rtcwake
date: 2021-05-27 11:35:11
tags:
	- Linux

---

--

enter a system sleep state until specified wakeup time

作用是：进入休眠状态，知道指定的时间再唤醒。

**使用方法**

 standby

普通待机模式，为默认选项，对应ACPI  state S1

 mem

待机到内存，即内存之外把其他设备都进入低功耗模式，对应ACPI state S3

 disk

待机到硬盘，即休眠，把电脑的当前状态保存到硬盘，几乎不消耗外部电源，对应ACPI state S4

off 

通过调用系统的关机命令来休眠， 对应ACPI state S5



可以通过以下命令查阅当前系统支持的休眠模式

```
cat /sys/power/state
standby mem disk
```



systime和rtctime



参考资料

1、Linux 下使用rtcwake实现定时休眠和唤醒设备

https://www.cnblogs.com/runtimeexception/p/12170200.html