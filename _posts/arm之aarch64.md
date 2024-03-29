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



# 汇编

新建hello.s文件。

```
.text

.global main
main:
        ldr x0, addr_of_keep_x30
        str x30, [x0]

        ldr x0, addr_of_msg
        bl puts

        ldr x0, addr_of_keep_x30
        ldr x30, [x0]

        mov w0, #0
        ret


addr_of_msg: .dword msg
addr_of_keep_x30: .dword keep_x30
.data
msg: .asciz "hello world!\n"
keep_x30: .dword 0

```

Makefile这样写。

```
all:
	aarch64-linux-gnu-as   hello.s -o hello.o
	aarch64-linux-gnu-gcc -static hello.o -o hello

```

运行：

```
hlxiong@hlxiong-VirtualBox:~/work/test/asm$ qemu-aarch64 ./hello
hello world!

```

arm公司有推出一个叫DS-5的工具（基于eclipse的）。可以进行汇编模拟调试。



ARMv8拥有两种执行模式： 
AArch64执行A64指令，使用64bit的通用寄存器； 
AArch32执行A32/T32指令，使用32bit的通用寄存器；



```
x0到x30 
	通用寄存器。可以当32位寄存器用。这个时候写做w0到w30
plr
	就是x30寄存器。保存返回地址。
	produce link register, 连接寄存器
SP_EL0到3
	栈指针寄存器。
ELR_EL1到3
	exception link registers，异常链接寄存器
SPSR_EL1到3
	保存进入ELx状态时的状态寄存器。
V0到V31
	浮点寄存器。128位的。
PC
	
```



![1595905853484](images/random_name/1595905853484.png)

EL0为普通用户程序 
EL1是操作系统内核相关 
EL2是Hypervisor, 可以理解为上面跑多个虚拟OS 
EL3是Secure Monitor(ARM Trusted Firmware)



参考资料

1、这个系列文章不错

https://blog.csdn.net/yhb1047818384/article/details/80382783

# 参考资料

1、ARMv8-AArch64寄存器和指令集

https://blog.csdn.net/tanli20090506/article/details/71487570