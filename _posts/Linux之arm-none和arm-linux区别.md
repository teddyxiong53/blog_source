---
title: Linux之arm-none和arm-linux区别
date: 2018-03-13 21:07:53
tags:
	- Linux

---



arm工具链，有的叫arm-none-eabi，有的叫arm-none-linux-eabi，区别是什么？



命名规则是：

```
arch-vendor-os-eabi
```

**命名规则:**

交叉编译工具链的命名规则为：arch [-vendor] [-os] [-(gnu)eabi]

- arch - 体系架构，如ARM，MIPS
- verdor - 工具链提供商
- os - 目标操作系统
- eabi - 嵌入式应用二进制接口

根据对操作系统的支持与否，ARM GCC可分为支持和不支持操作系统，如

- arm-none-eabi：这个是没有操作系统的，自然不可能支持那些跟操作系统关系密切的函数，比如fork(2)。他使用的是newlib这个专用于嵌入式系统的C库。

- arm-none-linux-eabi：用于Linux的，使用Glibc





参考资料

1、

https://www.cnblogs.com/deng-tao/p/6432578.html