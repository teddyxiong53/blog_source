---
title: Linux内核之设备模型（二）
date: 2018-03-20 16:40:30
tags:
	- Linux内核

---



前面没有分析过Bus这个东西。现在看看。

首先，bus是一种特殊的设备，所以它算是device的子类。

在linux里，bus是一种连接CPU跟其他device的通道。

为了统一设备模型的实现，linux规定，所有的其他device都要挂在一个bus上。

所以就有了platform bus这种虚拟总线。也就有了platform device这一系列的概念。



bus对应的结构体是struct bus_type。

```
struct bus_type {
  char *name
  char *dev_name 注意这个。跟device结构体里的init_name有关系。对于usb批量设备，设计者懒得起名字了。
  	内核也允许这种行为。允许设备的名字为空。这样当device注册到内核后，用bus->dev_name +id来给设备取名。
  struct device *dev_root;这个只跟subsystem这个有关系。
};
```



class、bus都会形成一个虚拟的子系统。

subsys_private结构体。



class这个东西，跟前面讨论的bus、device、device_driver不太一样，因为前面那些都是实实在在存在的实体。

而class是完全抽象的。

我们可以取class这个单词的一个含义，班级的含义，来帮助理解。

一个班级由很多的学生组成，就是class由device组成。

这个class有个名字，例如一班。

这个班上如果没有学生，那么这个班就没有存在的意义。

有班级好处是什么？就是一个老师讲课，只讲一次，班里的学生就都知道了。

不然需要跟每个学生单独讲一遍。

在内核里，就是有些相似的device（知识水平差不多的学生）。需要向用户空间提供相似的接口（课程）。

如果每个设备的驱动都是实现一遍的话，就太麻烦了。

所以class就说，我来帮你们实现吧。你们调用我的接口就好了。





内核的启动过程中，要完成一定的初始化操作之后，才会开始处理device的probe这些。

在这之前，常规的platform device是没法用的。

但是又有这种需求，例如console设备。

所以就单独提供了early platform这一套东西。

不过，我看我的mylinuxlab里的配置的，并没有用到early platform的东西。



# 出错释放资源的技巧

一般在写probe函数的时候，会申请各种资源，然后一个出错，就要把前面申请的释放掉。然后就是各种goto。

这种写法很繁琐。

但是linux考虑到这种情况了。

提供了一套devm_xxx的接口给我们用。这个出错了，它会帮我们去释放对应的资源的。

