---
title: usb之gadget
date: 2020-06-23 09:52:49
tags:
	- Linux

---



编写gadget的关键是在于了解udc、gadget、composite三者之间的联系和架构层次，

在实际应用中gadget是不需要我们去编写的，

需要我们自己去编写的是composite层，以及地对udc层的修改，

下面开始详细介绍着三者。

composite英文意思是复合的意思，

估计是编写usb gadget层设备驱动都整合到一起，

通过统一的函数usb_composite_register注册。

功能各异，杂七杂八，所以称为复合层吧。

composite是一个可选的层，在gadget层之上。

**作用是简化构造一个复合设备的步骤，在一个configuration里支持多个功能。**

例如，一个只有一个Configuration的设备，同时支持网络连接和和大容量存储，就是一个复合设备。





关于usb gadget设备function驱动,  最新Linux提供了多种方式。

1. 使用usb_compositor_driver, 注册/实现该驱动即可。
2. 使用configfs进行配置, 用户态可以利用配置文件系统创建相应configuration, interface, endpoint等, 配合内核态的驱动, 即可实现某种功能的usb设备。
3. 使用functionfs进行配置, 最新的安卓相关usb驱动, 如adb, mtp, ptp就是采用这种方式实现。 即内核态提供功能文件系统,  内部可关联多种标准功能,  **具体协议由应用层实现, 即所谓的用户态驱动。**



![img](../images/random_name/20150527111351540)





# 参考资料

1、使用configfs配置usb gadget设备

https://blog.csdn.net/nwpu053883/article/details/100985475

2、Linux usb gadget框架概述

https://www.cnblogs.com/haoxing990/p/8799133.html

3、基于configfs的usb gadget驱动分析

https://blog.csdn.net/chenjiebing2016/article/details/86503215

4、How to enable Android ConfigFS gadgets

https://blog.csdn.net/ztguang/article/details/53106556

5、

https://blog.csdn.net/birdring_0xx0/article/details/128383523