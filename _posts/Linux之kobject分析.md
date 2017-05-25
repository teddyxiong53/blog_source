---
title: Linux之kobject分析
date: 2017-05-25 22:21:12
tags:

	- Linux

	- kobject

---

在Linux内核里，kobject是构成Linux设备模型的基础。一个kobject对应一个sysfs目录。从面向对象的角度来看，kobject可以看做是所有设备对象的基类，但是因为C语言里没有面向对象的语法，所以一般是把kobject作为成员嵌入到其他的结构体里。这里所说的其他结构体，就可以看作是kobject的派生类。

kobject为Linux设备模型提供了很多有用的功能，例如引用计数。

在内核里，没有kobject直接定义的变量，kobject只在其他结构体里存在。

内核里的设备之间是以树状形式来组织的。kobject帮助我们来实现树状结构内部的父子关系。

和kobject一起起作用的另外两个结构体是：kset和ktype。这3个结构体一起构成了Linux设备模型的基础。



kset是kobject的集合。对应到sysfs里，就是/sys目录下的一个目录。

kset本身也是一个kobject，kset之所以可以当成一个容器来用，是因为里面增加了一个双向链表成员。

不是所有的kobject都要在sysfs里有一个对应的东西，但是每个kset在sysfs里一定对应一个文件。





