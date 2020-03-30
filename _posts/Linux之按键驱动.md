---
title: Linux之按键驱动
date: 2018-05-08 23:11:49
tags:
	- Linux

---



对于gpio不能配置为中断方式的，怎么处理？

input子系统提供了input-polldev.c来处理这种情况。

这个是kernel提供的一个新的架构，基于原有的input子系统。

在input设备外增加了一层轮询设备的封装。

我们只需给polldev提供一个轮询间隔时间。

在我们把这个input设备关闭后，这个轮询就会停止。

这个polldev架构还提供了一些sysfs节点。其中比较有用的就是poll节点。

我们可以用cat poll来查询到当前的轮询频率。也可以用echo 一个值进去来进行修改。



要实现的效果：类似桌面打开记事本，按下键盘后有输入，按住按键不放的话就连续输入。

环境：嵌入式Linux系统，键盘有GPIO扫描实现，模拟成标准键盘，界面用QT4的LineEdit显示。



长按检测

https://blog.csdn.net/songyulong8888/article/details/80572126



# 参考资料

1、关于input设备的多次打开

http://www.xuebuyuan.com/830860.html

2、EV_REP，input_repeat_key，键盘重复，GPIO键盘

https://blog.csdn.net/lanmanck/article/details/6326802