---
title: arm之交叉编译工具链命名规律分析
date: 2019-12-04 13:45:28
tags:
	- arm
---

--

# 基本

常见的工具链命名有这些：

```
arm-linux-gcc
arm-linux-guneabi-gcc
arm-none-linux-eabi-gcc
arm-none-uclinuxeabi-gcc
arm-none-linux-gnueabi-gcc
arm-cortex-a8-linux-gnueabi-gcc
```

有什么区别？

各个部分具体含义是什么？

分别用在什么场合？

命名的组成部分是：

arch-core-kernel-system-language

分为5个部分：

arch：arm、mips这些。

core：指cpu核心。可以没有，也可以是none。

kernel：linux、uclinux。

system：工具链所选择的库函数和目标镜像的规范。如gnu、gnueabi。

​	gnu == glibc + oabi

​	gnueabi == glibc + eabi。

​	也可以留空。

language：gcc、g++。

（上面的规则只是网友的总结，供参考）

arm-none-linux-gnueabi-gcc。这个是最典型的。

这个是Codesourcery公司基于gcc推出的工具链。

可以交叉编译arm相关的所有环节的代码，包括：裸机程序、u-boot、kernel、busybox和应用。



==arm-linux-gnueabihf-gcc==

==这个是Linaro公司推出的arm交叉编译工具链。==

==也可以编译所有环节的代码。==



免费版目前有三大主流工具商提供，

第一是GNU（提供源码，自行编译制作），

第二是 Codesourcery，

第三是Linora。



1、aarch64-linux-gnu-gcc：是由 Linaro 公司基于GCC推出的的ARM交叉编译工具。可用于交叉编译ARMv8 64位目标中的裸机程序、u-boot、Linux kernel、filesystem和App应用程序。

2、arm-none-linux-gnueabi-gcc：是 Codesourcery 公司（目前已经被Mentor收购）基于GCC推出的的ARM交叉编译工具。可用于交叉编译ARM（32位）系统中所有环节的代码，包括裸机程序、u-boot、Linux kernel、filesystem和App应用程序。
3、arm-linux-gnueabihf-gcc：是由 Linaro 公司基于GCC推出的的ARM交叉编译工具。可用于交叉编译ARM（32位）系统中所有环节的代码，包括裸机程序、u-boot、Linux kernel、filesystem和App应用程序。
4、arm-none-elf-gcc：是 Codesourcery 公司（目前已经被Mentor收购）基于GCC推出的的ARM交叉编译工具。可用于交叉编译ARM MCU（32位）芯片，如ARM7、ARM9、Cortex-M/R芯片程序。

5、arm-none-eabi-gcc：是 GNU 推出的的ARM交叉编译工具。可用于交叉编译ARM MCU（32位）芯片，如ARM7、ARM9、Cortex-M/R芯片程序。

https://www.cnblogs.com/carriezhangyan/p/9564669.html

# -march=armv8.2-a

https://gcc.gnu.org/onlinedocs/gcc-9.1.0/gcc/AArch64-Options.html



# 为什么有的地方叫arm64，有的地方叫aarch64？

AArch64 是 Arm 架构的 64 位执行状态。 

AArch64执行状态运行A64指令集。 

AArch32 和 AArch64 执行状态使用非常不同的指令集，

因此许多软件使用两个端口来表示 Arm 架构的两种执行状态。



有“ARM架构”和“ARM指令集”，

导致许多软件项目使用“ARM”或“arm”作为端口名称。

 2011年，ARMv8引入了两种执行状态：AArch32和AArch64。

之前的指令集“ARM”和“Thumb”分别重命名为“A32”和“T32”。 

2017 年，该架构更名为“Arm 架构”，以反映公司名称的重新命名。

因此，“ARMv8-A”架构配置文件现在命名为“Armv8-A”。



对于 AArch64 执行状态，虽然许多项目使用“AArch64”作为端口名称，

但由于遗留原因，macOS、Windows、Linux 内核和一些 BSD 操作系统不幸地使用“arm64”。



（Linux内核在3.7版本中添加了对AArch64的支持。最初，补丁集被命名为“aarch64”，但后来应内核开发者的[请求]（[PATCH 00/36] AArch64 Linux内核移植）进行了更改.)



https://www.cnblogs.com/carriezhangyan/p/9564669.html

# 参考资料

1、交叉编译器的命名规则及详细解释

https://blog.csdn.net/LEON1741/article/details/81537529

