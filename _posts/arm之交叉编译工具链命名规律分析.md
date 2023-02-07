---
title: arm之交叉编译工具链命名规律分析
date: 2019-12-04 13:45:28
tags:
	- arm
---



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



arm-linux-gnueabihf-gcc

这个是Linaro公司推出的arm交叉编译工具链。

也可以编译所有环节的代码。





参考资料

1、交叉编译器的命名规则及详细解释

https://blog.csdn.net/LEON1741/article/details/81537529