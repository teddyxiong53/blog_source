---
title: Android系统之zygote
date: 2020-04-15 09:47:51
tags:
	- Android

---

1

在Android系统里存在2个世界。

java世界。谷歌的sdk，主要就是针对这个世界的。都是基于dalvik虚拟机的。

native世界。用C和C++开发的程序。



我们都知道，程序运行，就一定存在一个进程。

但是我们在做Android开发的时候，都是接触的Activity、Service这些概念，它们跟进程是如何关联的呢？

在程序里，我们经常使用系统的service，这些service又在哪里呢？

上面这些疑问，都跟zygote和system_server有关系。这2个东西，就是本文要讨论的重点。

这2个进程，撑起了Android系统里的java世界，任何一个进程崩溃，都导致java世界的崩溃。



zygote

zygote本身是一个native程序。

跟驱动、内核都没有关系。

zygote是init进程根据init.rc的配置创建的。

zygote最初的名字叫app_process。在运行的时候，通过prctrl把自己的名字改成了zygote。

分析的入口文件是app_main.cpp。

```
 set_process_name("zygote");
```

Zygote的这个main函数虽很简单，但其重要功能却是由AppRuntime的start来完成的。下面，我们就来具体分析这个AppRuntime。

//className的值是"com.android.internal.os.ZygoteInit"

//如果环境变量中没有ANDROID_ROOT,则新增该变量，并设置值为“/system"



Zygote是创建Android系统中Java世界的盘古，它创建了第一个Java虚拟机，同时它又是女娲，它成功地繁殖了framework的核心system_server进程。

SystemServer的进程名实际上叫做“system_server”，这里我们可将其简称为SS。SS做为Zygote的嫡长子，其重要性不言而喻。



参考资料

1、第4章  深入理解zygote

https://wiki.jikexueyuan.com/project/deep-android-v1/zygote.html