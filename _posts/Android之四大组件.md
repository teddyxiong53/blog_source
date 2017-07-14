---
title: Android 4大组件
date: 2017-07-14 20:29:01
tags:

	- Android

---

Android的4大组件是Activity、Service、BroadcastReceiver、ContentProvider。

分别是一个前台（Activity），一个后台，一个给（ContentProvider），一个拿（BroadcastReceiver）。

# 1. Activity

## 1.1 函数

生命周期里是3对（6个）函数。

onCreate和onDestroy

onStart和onStop

onPause和onResume

这个是一个符合正常思考方式的设置。

启动Activity：先onCreate，然后onStart，然后onResume，Activity进入到运行状态。

如果一个Activity被其他的Activity覆盖（例如出现确认窗口）或者手机被锁屏，则onPause被调用。

如果一个Activity回到最上层或者手机解锁了，则onResume被调用。

如果你进入到一个新的Activity，或者按Home键回到主屏了，则当前的Activity会先onPause，在onStop。



# 2. Service

# 2.1 本地服务

本地服务LocalService，是指调用者和Service在同一个进程里，运行在主进程的main线程里，所以不能太耗时。不涉及进程间通信。

有两种启动方法，一种是是以start的方式来开启服务。另一种是用bind来启动。

### 2.1.1 start启动服务

1、定义一个类，继承Service类。

2、在manifest.xml里配置service。

3、使用context的startService(Intent)方法来启动service。

4、不用的时候，调用stopService来停止service。

这个的特点是，即使开启者退出了，service还是可以继续运行。

### 2.1.2 bind启动服务

特点是开启者退出了，服务也会跟着退出的。

onBind启动，onUnbind停止。

