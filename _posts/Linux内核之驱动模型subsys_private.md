---
title: Linux内核之驱动模型subsys_private
date: 2021-02-19 15:59:30
tags:
- Linux
---

--

结构体subsys_private

位于：drivers\base\Base.h

驱动核心的私有数据，只有驱动核心才可以访问。

使用struct subsys_private

**可以将struct bus_type中的部分细节屏蔽掉，**

利于外界使用bus_type。

**struct driver_private和struct device_private都有类似的功能。**



代码注释里写的是

```
struct subsys_private - structure to hold the private to the driver core portions of the bus_type/class structure.
```

是给bus_type和class用的。所以曲面是subsys这样一个抽象的名字。

结构体的成员

```

```

该结构和device_driver中的struct driver_private类似，

device_driver中有提到它，但没有详细说明。

看到结构内部的字段，就清晰多了，没事不要乱起名字嘛！

什么subsys啊，看的晕晕的！

不过还是试着先理解一下为什么起名为subsys吧：

按理说，这个结构就是集合了一些bus模块需要使用的私有数据，

例如kset啦、klist啦等等，命名为bus_private会好点（就像device、driver模块一样）

**【事实上早期版本确实是命名为bus_type_private】。**

不过为什么内核最终抛弃了呢呢？

看看include/linux/device.h中的struct class结构（我们会在下一篇文章中介绍class）就知道了，

因为class结构中也包含了一个一模一样的struct subsys_private指针，

**看来class和bus很相似啊，所以在内核的subsys_private在现在最新版本就是这样。**



想到这里，就好理解了，

无论是bus，还是class，

还是我们会在后面看到的一些虚拟的子系统，

它都构成了一个“子系统（sub-system）”，

**该子系统会包含形形色色的device或device_driver，**

就像一个独立的王国一样，存在于内核中。

**而这些子系统的表现形式，**

**就是/sys/bus（或/sys/class，或其它）目录下面的子目录，**

**每一个子目录，都是一个子系统（如/sys/bus/spi/）。**



参考资料

1、

https://www.cnblogs.com/xinghuo123/p/12872026.html