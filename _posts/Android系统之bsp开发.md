---
title: Android系统之bsp开发
date: 2020-09-14 09:48:32
tags:
	- Android系统

---

1

将android移植到特定硬件平台上，其核心是bsp的搭建工作，bsp是板级支持包，并不是特定某个文件，而是从功能上理解的一种硬件适配软件包，它的核心就是： 

1、linux内核硬件相关部分（主要是linux device drivers）; 

2、android用户空间的硬件抽象层。（HAL，hardware abstract layer）. 
linux驱动程序工作在内核空间，**android的HAL工作在用户空间**，有了这两个部分的结合，就可以让庞大的android系统运行在特定的硬件平台上。 

目前一般的处理器或者硬件平台的BSP（board support package）都是**由芯片厂商统一完成**的，并且已经趋于成熟。

**因此开发者的主要工作不再是构建完整的BSP，而是调试和修改现有的BSP**。

其实每个芯片厂家都会有一个硬件平台的参考设计，如PMU，EMMC,WIFI，CODEC，CTP等。

如果没有太大的改动，原厂的BSP一般都是可以跑起来的，针对某一块的硬件变化修改驱动和HAL就可以了，对于新增加的硬件，编写相关的驱动程序，**然后提供给JAVA的本地框架层的接口就可以了。**

对于一些简单的设备驱动，可以不用写HAL的代码，实际上很多时候也不用去写，

一种常见的情况是由**JNI的部分代码直接调用驱动程序的设备节点或者使用sys文件系统。**

也可以直接把/sys/的属性文件（可以通过cat和echo读写）的文件接口直接提供给java层代码调用。



android的主要驱动有： 
1. 显示驱动 display driver：常用于基于linux的帧缓冲frame buffer 驱动程序。 
2. flash内存驱动flash memory driver :基于MTD的flash驱动程序。 
3. 照相机驱动camera driver :基于linux的v4l video for linux驱动。 
4. 音频驱动 audio driver ：基于ALSA advanced linux sound architechure驱动。 
5. wifi驱动：基于IEEE801.31标准的驱动程序。 
6. 键盘驱动keyboard driver：作为输入设备的键盘驱动。 
7. 蓝牙驱动 bluetooth diver :基于IEEE801.35.1标准的无限传输技术。 
8. **binder IPC驱动：android一个特殊的驱动程序，具有单独的设备节点，提供进程间通信的功能。** 
9. power management能源管理：管理电池电量等信息。 



![img](../images/random_name/20160105124704644)

其中system.img可以理解为android的本体部分。

System.img最终会挂在ramdisk的/system目录下面，

system/app     

这个里面主要存放的是常规下载的应用程序，可以看到都是以APK格式结尾的文件。在这个文件夹下的程序为系统默认的组件，自己安装的软件将不会出现在这里，而是/data/文件夹中。

 system/framework  

主要是一些核心的文件，从后缀名为jar可以看出是是系统平台框架。

**system/lib       **

**lib目录中存放的主要是系统底层库，如hardware层库。**

system/media  

铃声音乐文件夹，除了常规的铃声外还有一些系统提示事件音

system/usr      

用户文件夹，包含共享、键盘布局、时间区域文件等。



在"/system/lib/hw"下面定义了硬件抽象层编译的动态库文件。

![img](../images/random_name/20160105124559685)



# aosp/device/samples目录分析

这个给了一个例子，非常全面，涉及了app、jni、库。



# aosp 适配



为什么开发者试图将AOSP ROM移植到设备上时会出这么多问题？ 

简单的答案是，由于功能在不同版本的Android上发生了变化，所以打包成BLOB的旧驱动文件无法支持较新版本的Android，即使是原版的AOSP。

 为了克服这个问题，开发者一般会使用一种叫”shim”（垫片）的手段进行适配，

但是这个过程很棘手，耗时，有时还很难调试。

在本文中，我们将科普这个”shim”技术的原理，特别是关于相机部分的适配。

我们将以OnePlus 3T为例。但请注意，现实中不同的设备适配过程中可能遇到的问题是各不相同的。

一个重大原因：让手机的摄像头能正常工作的驱动程序，主要是Camera HAL (Hardware Abstraction Layer 硬件抽象层)也不是开源的。

相机HAL和官方ROM都是闭源的最大问题是，负责ROM移植的开发者几乎等于在盲操作了。

官方ROM之所以能够正常调用相机是因为官方有HAL的源代码。

HAL是让ROM与硬件之间能正常互相通信的关键部分——没有它，相机是没法用的。

可以把HAL比作一辆车的油门和方向盘，这两个东西为车辆内部的复杂结构提供了一个可以让外部用简单方法进行操作的“界面”。

随着相机硬件上变得越来越复杂（比如出现了各种双摄），假如有HAL的源码就可以让移植第三方ROM变得简单很多。

然而由于各种原因，OEM厂商并不公开提供HAL源码。

首先，如果他们本身也不完全拥有相机HAL的所有权（比如可能相机功能用了其他公司授权的知识产权），那他们是没法开源的。

其次，开放HAL源码可能会危及他们自己的知识产权。

而且这些公司并没有义务提供源代码（不像他们所用到的Linux内核由于GPL协议而必须开源）。

所以没有HAL源码，开发人员要怎么才能让相机能用？答案是用BLOB和”shim”技术，加大量的调试。

一个设备BLOB文件包括了打包编译好的二进制文件。

**在本例中，相机HAL是厂商编译好后以二进制形式存储在设备中出货的。**

开发者指的BLOB就是这些在设备里存储的，他们能够提取的文件。

相机BLOB的相关问题一直困扰了一加手机相关开发很长时间了，但好在至少开发者总是能提取这些BLOB文件。

HAL源代码可以说是开发者解决问题的金钥匙了，但由于知识产权的问题，估计它永远不会被开源。

因此想要移植AOSP的开发者唯一能用的就是没有源代码的这些BLOB文件。

很少有人能把这些BLOB直接套用在原版系统上直接正常使用，所以为了修正两者之间的问题，开发人员需要开发一个”shim”垫片。

这是因为厂商编译的相机BLOB可能需要调用OxygenOS中特有的一些功能函数，但在AOSP中并不存在，或者名字不一样，这就会导致错误。这就可以通过我们的shim来进行弥补修复。





参考资料

1、android BSP与硬件相关子系统读书笔记（1）android BSP移植综述

https://blog.csdn.net/eliot_shao/article/details/50242681

2、例说Android 硬件抽象层

https://blog.csdn.net/eliot_shao/article/details/50461738

3、谈第三方Android ROM开发者是如何适配硬件的

https://blog.toby.moe/android-shim/