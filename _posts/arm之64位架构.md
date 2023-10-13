---
title: arm之64位架构
date: 2018-04-13 21:15:41
tags:
	- arm

---



# 发展历史

真正的64位计算在1990年代才出现。

首先是mips的R4000，然后是DEC的Alpha处理器。

到了1990年代中期，Intel和sun都有了自己的64位设计。

对于消费者来说，熟悉的是AMD在2003年发布的64位pc处理器。

随着语音识别、3D游戏、高分辨率显示屏的普及，32位处理器的能力已经推到了极限。

arm看到了64位处理器的需求，很早就开始了新的设计。

arm的新款64位架构跟自己的32位架构全面兼容。32位的可执行文件，不需要修改，就可以在上面跑。

这对于安卓来说，意义就是，内核被移植到64位后，系统的其余部分，核心库、应用、游戏，都可以在32位和64位之间切换。

苹果从iPhone 5s上用的A7处理器，就是64位的。A7采用的就是armv8的架构 。

是双核的，2个64K的一级缓存（一个核心一个），1一个1M的二级缓存（2个核心共用）。1个4M的三级缓存（整个soc共用）。

苹果拥有arm架构授权，它可以自己从头设计自己的处理器，但是必须保证对arm的兼容。

arm自己有一套测试套件，来测试处理器是否兼容。



树莓派3B就是64位的A53核心。但是上面跑32位系统完全没有问题。

骁龙845是A75的，骁龙835是A73的。



对于系统编程来说，64位又什么需要注意的地方？



# aarch64是什么？

```
Features    : fp asimd aes pmull sha1 sha2 crc32
CPU implementer : 0x41
CPU architecture: AArch64
CPU variant : 0x0
CPU part    : 0xd03
CPU revision    : 2
```

aarch64是armv8架构的一种执行状态。

还有aarch32的执行状态。

#arm64和aarch64的区别

```
So it makes sense, iPad calls itself ARM64, as Apple is using LLVM, and Edge uses AARCH64, as Android is using GNU GCC toolchain.
```

苹果什么都喜欢自己搞一套。





# 参考资料

1、ARM 64位处理器架构ARMv8技术浅析

https://blog.csdn.net/u011279649/article/details/46128495

2、64 位 ARM 处理器意味着什么？

https://www.oschina.net/news/55263/64bit-arm

3、五分钟打造ARM 64位最小系统

https://community.arm.com/cn/b/blog/posts/arm-64

4、AArch64: ARM’s 64-bit architecture

https://llvm.org/devmtg/2012-11/Northover-AArch64.pdf

5、AArch64 是什么

https://blog.csdn.net/rd_w_csdn/article/details/53841018

6、Differences between arm64 and aarch64

https://stackoverflow.com/questions/31851611/differences-between-arm64-and-aarch64