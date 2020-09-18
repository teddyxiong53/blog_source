---
title: Android之framework代码分析
date: 2019-04-03 13:58:04
tags:
	- Android

---

1

 Framework开发是一项非常繁琐复杂的工作，需要阅读大量的源代码，

分析及其多的LOG信息来定位错误位置。

这个时候如果使用一些工具或者知道如何定位重要LOG信息，就可以使一些复杂的工作变的简单很多，

使我们分析问题的效率变得更快，不再为阅读大量的源代码而感到一筹莫展。

本文将针对一些场景讲解如何分析系统LOG信息，如何添加LOG定位错误信息，以及常用工具以及使用方法。



使用命令adb shell input keyevent + 对应的键值，可以模拟对应的操作。

# **am命令**

有时候我们在调试系统时可以在终端使用am命令来发送广播，打开Activity，启动Service等操作，十分方便。

am的详细操作如下，我们可以通过adb shell am + 对应命令，就可操作。

打开设置：

```
rpi3:/ # am start com.android.settings
Starting: Intent { act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] pkg=com.android.settings }
```



# **pm命令**

当要查询系统中某个应用是否存在，或者存在路径，就可以根据对应的包名来查找对应的apk信息。

查看系统里的package。

```
pm list packages
```

# 查看系统日志

直接执行logcat就好了。



# dumpsys 

adb shell dumpsys activity

这个是查看activity信息。

可以查看的信息

```
account
alarm 查看闹钟情况
audio 查看音频情况
battery
cpuinfo
diskstats
```

# getprop

后面不跟参数，则是打印出所有的属性的值。

本质上是读取/default.prop、/init.rc、/system/build.prop这3个文件里的内容。



参考资料

1、Framework常用工具及LOG调试方法

https://blog.csdn.net/fu_kevin0606/article/details/79616216

2、Android实用技巧之adb命令：getprop，setprop，watchprops命令的使用

https://blog.csdn.net/heqiangflytosky/article/details/69432749



