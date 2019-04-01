---
title: Android之系统启动过程
date: 2019-04-01 14:38:32
tags:
	- Android
---





一个跟Linux不同的一点，就是多一个zygote进程，这个进程由init进程创建。

是其余用户态进程的父进程。

zygote的字面含义是受精卵。

zygote进程在启动时会创建一个dalvik虚拟机实例。

当zygote孵化一个新的进程时，会把自己的dalvik虚拟机复制过去。

这样每个进程都有自己独立的dalvik虚拟机。



参考资料

1、Android启动过程图解.md

https://github.com/helen-x/AndroidInterview/blob/master/android/Android%E5%90%AF%E5%8A%A8%E8%BF%87%E7%A8%8B%E5%9B%BE%E8%A7%A3.md

2、Android Zygote Startup

https://elinux.org/Android_Zygote_Startup

3、Dalvik虚拟机的启动过程分析

https://blog.csdn.net/luoshengyang/article/details/8885792

4、Android runtime机制（一）init进程

https://blog.csdn.net/dodod2012/article/details/80988414