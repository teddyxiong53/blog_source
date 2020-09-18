---
title: Android之Service分析
date: 2019-03-29 17:46:32
tags:
	- Android

---



1

先从 Service 生命周期看起，Service 的生命周期比较有趣的一点是，它的生命周期会根据调用不同的方法启动有不同的表现，具体有两种形式。



1. 通过 startService(Intent intent) 启动 Service

   生命周期是这样的： `onCreate()`  、`onStartCommand()`、`onStart()(已经过时)` 、`onDestroy()`

2. 通过 bindService(Intent intent,ServiceConnection conn,int flags) 启动 Service

   生命周期是这样的：`bindService()`、`onCreate()` 、`IBinder onBind(Intent intent)`、`unBindService()`、`onDestroy()` 方法。

snapdroid这个程序里，两种方式都用到了。

既然通过 startService 启动的 Service 和 Activity 没有建立联系，那么通过 bindService 来启动 Service，就可以和 Activity 建立联系了，相当于 Service 绑定到了这个 Activity 中了。

Activity 在没有 bindService 的情况下，调用 unBindService(ServiceConnection serviceConnection) 是会 crash 的。无论在什么情况下，对于某个 Activity，只能够执行一次 unBindService。



参考资料

1、Android Service 详解（上）

https://www.jianshu.com/p/d88020de60b1