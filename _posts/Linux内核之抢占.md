---
title: Linux内核之抢占
date: 2018-03-23 16:35:28
tags:
	- Linux内核

---



内核实现了几种抢占模型。在menuconfig里配置。

1、不强制抢占。英文是No Forced Preemption（server）。这个是传统的模型。适合在服务器上用。针对高吞吐量。

系统调用返回和中断是会导致抢占的原因。

2、自愿抢占。英文是Voluntary Kernel Preemption（Desktop）。适合桌面系统。方法是在一些代码位置上添加抢占代码。

3、可抢占。Preemptible Kernel（Desktop） 适合桌面系统。这个是随时可能被抢占。

4、可抢占。Preemptible Kernel（Basic RT）。跟第三个类似。

5、完全抢占。Fully Preemptible Kernel（RT）。除了一些保护的临界点不能被抢占，其余都可以被抢占。



# 参考资料

1、https://wiki.linuxfoundation.org/realtime/documentation/technical_basics/preemption_models

