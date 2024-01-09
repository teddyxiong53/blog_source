---
title: arm之aarch64
date: 2020-07-23 17:36:51
tags:
	- arm

---

--

# 寄存器分布

AArch拥有31个通用寄存器，系统运行在64位状态下的时候名字叫Xn，运行在32位的时候就叫Wn；



![](../images/random_name/20170509190238235.png)



# aarch64为什么不是eabi

在 ARM 架构中，早期的 ARM 处理器使用的是 Embedded Application Binary Interface（EABI）。EABI 是一种标准化的 ABI（Application Binary Interface），定义了一套规范，用于指导编译器、链接器和运行时库等工具，确保不同的软件模块能够在嵌入式系统中正确地相互操作。

然而，在 64 位 ARM 架构（即 AArch64）中，ARM 开发者采用了一个新的 ABI，称为 ARM 64-bit Architecture Procedure Call Standard（AArch64 PCS）。AArch64 PCS 是针对 64 位 ARM 架构的新 ABI 标准，与传统的 EABI 有一些区别。

主要的一些区别和原因包括：

1. **64 位体系结构的改变：** AArch64 是一种全新的 64 位体系结构，因此在设计 ABI 时考虑了新的体系结构特性，如寄存器数量和使用方式等，与传统的 EABI 不同。

2. **对齐和数据结构的变化：** 64 位体系结构带来了对数据对齐和数据结构的变化，为了更好地利用硬件性能和支持更大的地址空间，AArch64 PCS 在数据对齐和数据结构方面有所调整。

3. **向后兼容性考虑：** AArch64 PCS 考虑到与现有 32 位 ARM 代码的兼容性，但在一些设计上与传统的 EABI 有所不同，以更好地适应 64 位架构的特性。

虽然 AArch64 采用了新的 ABI 标准，但它仍然致力于保持与旧有的 ARM 32 位架构的兼容性，并在新的架构特性下进行了调整，以便更好地利用 64 位 ARM 架构的性能优势。

# 参考资料

1、ARMv8-AArch64寄存器和指令集

https://blog.csdn.net/tanli20090506/article/details/71487570