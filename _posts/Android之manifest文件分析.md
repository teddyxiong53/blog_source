---
title: Android之manifest文件分析
date: 2019-04-08 10:19:30
tags:
	- Android

---



#MAIN和LAUNCHER

我们经常看到在MainActivity里写MAIN和LAUNCHER。这2个代表的内涵是什么？

MAIN表示打开应用的第一个界面。

LAUNCHER则表示在手机上显示安装图标。你可以指定多个LAUNCHER。就会显示多个图标。但是这样没有什么价值。

# meta-data

在manifest文件里，有时候会看到meta-data标签。

例如这样：

```
<meta-data
                android:name="android.support.PARENT_ACTIVITY"
                android:value="com.danielkim.soundrecorder.activities.MainActivity" />
```

meta-data可以出现在这些元素里面：

```
1、application
2、Activity
3、service
4、provider
```

一般在xml文件里指定，在java代码里获取。

一般就是配置某些sdk的appid这样的用途的。其实就是配置文件。



参考资料

1、理解android.intent.action.MAIN 与 android.intent.category.LAUNCHER

https://blog.csdn.net/Marvel__Dead/article/details/72822677

2、Android学习之 Manifest中meta-data扩展元素数据的配置与获取

https://blog.csdn.net/janice0529/article/details/41583587

3、Android meta-data知识介绍及应用

https://www.jianshu.com/p/d0d82e5d66f6