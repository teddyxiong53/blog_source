---
title: cpp之实现回调的方式
date: 2018-09-28 11:07:17
tags:
	- cpp

---



# callback方式

callback的本质是设置一个函数指针进去。Windows的消息处理函数就是这样做的。

面向过程的，适合在C语言里用。



# sink方式

sink的本质是你按照对方的要求实现一个cpp接口。

然后把你设置接口设置给对方。COM里的连接点就是使用这种方式。

其实就是一个观察者方式。



# delegate方式

跟观察者类似。



sink和delegate的区别：

sink以类为单位，delegate以函数为单位。



参考资料

1、C++ 回调函数的几种策略

https://www.cnblogs.com/maniford/p/6905317.html