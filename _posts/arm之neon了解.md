---
title: arm之neon了解
date: 2019-12-04 13:34:28
tags:
	- arm
---

--

# 简介

VFP(Vector Floating Point)指令

该指令用于向量化加速浮点运算。

自ARMv7开始正式引入NEON指令，

**NEON性能远超VFP，因此VFP指令被废弃。**

类似于Intel CPU下的MMX/SSE/AVX/FMA指令，

ARM CPU的NEON指令同样是通过向量化来进行速度优化。



熟悉arm processor的朋友应该知道arm的Cortex-A是带有FPU和NEON的，

==FPU用来做浮点数运算的，==

==而NEON是SIMD指令做并行运算的。==

==在现有Cortex-A的设计里，NEON和FPU是不可分的，也就是不能单独只有NEON或是FPU。==

在比较高性能的Cortex-A CPU（比如Cortex-A15/A57/A72/A73/A75)中，NEON和FPU是不能在RTL配置里去掉的，

==在高能效的Cortex－A的CPU（比如Cortex-A7/A53/A55)中NEON和FPU是可以在RTL配置里面配置有或是没有。==



NEON和FPU毕竟是占面积的，也许你会认为你的应用可能用不到NEON或是FPU，所以你可以配置RTL没有NEON／FPU，以减少面积die size或功耗。



这在Armv7里可能不是问题，但是在armv8 64位里需要非常小心，

也许因为这个配置导致你的芯片称为无用的废片，有些客户因此遭受损失，虽然我们已经尽可能地告知客户们。



# arm neon指令汇编举例

NEON（Advanced SIMD）指令集是 ARM 处理器上的一组 SIMD（Single Instruction, Multiple Data）指令，用于高效地执行并行数据处理。

以下是一些 NEON 指令的简单汇编示例：

1. **加法指令（VADD）：**

   ```assembly
   // 向量加法
   vadd.i32 q0, q1, q2   // q0 = q1 + q2
   ```

2. **减法指令（VSUB）：**

   ```assembly
   // 向量减法
   vsub.i32 q0, q1, q2   // q0 = q1 - q2
   ```

3. **乘法指令（VMUL）：**

   ```assembly
   // 向量乘法
   vmul.f32 q0, q1, q2   // q0 = q1 * q2 (单精度浮点数)
   ```

4. **累加指令（VADDL）：**

   ```assembly
   // 向量累加并扩展为长整型
   vaddl.s16 q0, d1, d2   // q0 = (int32_t)d1 + (int32_t)d2
   ```

5. **比较指令（VQABS）：**

   ```assembly
   // 向量绝对值（饱和）
   vqabs.s32 q0, q1   // q0 = abs(q1) 饱和到 int32_t 范围
   ```

6. **加载/存储指令（VLD1 / VST1）：**

   ```assembly
   // 加载/存储单精度浮点数向量
   vld1.f32 {d0-d3}, [r0]!   // 从地址 r0 加载 4 个单精度浮点数到寄存器 d0-d3，并递增地址
   vst1.f32 {d4-d7}, [r1]!   // 将寄存器 d4-d7 存储到地址 r1，并递增地址
   ```

7. **运算指令（VRECPS）：**

   ```assembly
   // 逆元素运算
   vrecps.f32 q0, q1   // q0 = 1.0 / q1
   ```

8. **向量运算指令（VDIV）：**

   ```assembly
   // 向量除法
   vdiv.f32 q0, q1, q2   // q0 = q1 / q2
   ```

这些只是 NEON 指令的一小部分，NEON 还包括了许多其他指令，用于执行不同类型的操作，如位运算、逻辑运算等。具体的 NEON 指令使用取决于所执行的任务和数据类型。要深入了解 NEON 指令集，请参考 ARM 的文档和参考资料。

# 参考资料

1、

https://blog.csdn.net/weixin_41965270/article/details/89150413

2、Armv8上不弃不离的NEON／FPU

https://www.jianshu.com/p/a19cc2ca59da