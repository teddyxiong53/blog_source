---
title: Android之进程间通信
date: 2019-03-30 11:49:32
tags:
	- Android
typora-root-url: ../
---



1

Android里如何使用多进程？

在manifest里注册四大组件的时候，加上`android:process`属性就可以了。

```
<Activity
	android:name=".Process1Activity"
	android:process=".process1"
/>

```

主进程的名字用的是包名。



默认情况下，同一个app里的所有组件都是在一个进程里运行的。这个是够用了的。



binder是Android特有的一种进程间通信方式。

和传统的ipc不同，它融合了rpc的概念，而且是一种面向对象的rpc。

在unix ipc机制里，通信双方必须处理线程同步、内存管理等复杂问题。不但工作量大，而且容易出错。

除了socket、pipe之外，fifo、semaphore、消息队列多被从Android里去掉了。

Android在架构上一直希望模糊进程的概念。用组件来取代。

app不应该关心组件存放的位置、组件的生命周期。

随时随地，只要拥有binder对象，就能使用组件的功能。

因此，Android系统的服务都是利用binder构建的。binder是整个系统运行的中枢。



在内核里，有一个/dev/binder设备节点。本质上是封装的共享内存。

提供给用户态的是libbinder库。



binder的优点：

```
1、使用简单。速度快。
2、消耗的内存更小。

```



参考资料

1、Android 进程间通信

http://wuxiaolong.me/2018/02/15/AndroidIPC/

2、android:process 的坑，你懂吗？

http://www.rogerblog.cn/2016/03/17/android-proess/

3、Android系统在新进程中启动自定义服务过程（startService）的原理分析

https://blog.csdn.net/luoshengyang/article/details/6677029

4、Android进程间通信--Binder

https://zhuanlan.zhihu.com/p/27344402

5、Android为什么选择binder，及Binder设计与实现初步讲解

https://blog.csdn.net/daogepiqian/article/details/50757082