---
title: Android之Intent
date: 2017-07-14 22:44:33
tags:

	- Android

---

Intent在Android里的作用和地位是什么？它是四大组件的联系纽带。

# 1. 作用和主要函数

Intent可以启动一个Activity，也可以启动一个Service，也可以发起一个Broadcast。

对应的函数分别是：

startActivity

startService

bindService

sendBroadcasts

sendOrderedBroadcasts

sendStickyBroadcasts

