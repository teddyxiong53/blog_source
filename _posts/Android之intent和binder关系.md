---
title: Android之intent和binder关系
date: 2019-04-04 17:37:30
tags:
	- Android
typora-root-url: ../
---



Intent贯穿Android应用层，是Android平台的经脉。

Intent具有跨进程特性。

相比于桌面系统，手机系统的各个部分的联系更加紧密。

Intent具有更大的灵活性。



Intent的灵活，但是效率不那么高。

主要在应用层用。

而Binder则效率高。主要在系统层用。

![](./images/android之intent和binder关系.png)



intent实际上是对Binder的封装。



参考资料

1、Android中Intent与Binder

http://blog.sina.com.cn/s/blog_72819b170101bliy.html

2、IPC、Binder、AIDL与Intent之间区别与联系

https://danlov.iteye.com/blog/2191704