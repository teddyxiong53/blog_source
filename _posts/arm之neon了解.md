---
title: arm之neon了解
date: 2019-12-04 13:34:28
tags:
	- arm
---

--

VFP(Vector Floating Point)指令

该指令用于向量化加速浮点运算。

自ARMv7开始正式引入NEON指令，

NEON性能远超VFP，因此VFP指令被废弃。

类似于Intel CPU下的MMX/SSE/AVX/FMA指令，

ARM CPU的NEON指令同样是通过向量化来进行速度优化。



熟悉arm processor的朋友应该知道arm的Cortex-A是带有FPU和NEON的，

FPU用来做浮点数运算的，

而NEON是SIMD指令做并行运算的。

在现有Cortex-A的设计里，NEON和FPU是不可分的，也就是不能单独只有NEON或是FPU。

在比较高性能的Cortex-A CPU（比如Cortex-A15/A57/A72/A73/A75)中，NEON和FPU是不能在RTL配置里去掉的，

在高能效的Cortex－A的CPU（比如Cortex-A7/A53/A55)中NEON和FPU是可以在RTL配置里面配置有或是没有。



NEON和FPU毕竟是占面积的，也许你会认为你的应用可能用不到NEON或是FPU，所以你可以配置RTL没有NEON／FPU，以减少面积die size或功耗。



这在Armv7里可能不是问题，但是在armv8 64位里需要非常小心，

也许因为这个配置导致你的芯片称为无用的废片，有些客户因此遭受损失，虽然我们已经尽可能地告知客户们。





# 参考资料

1、

https://blog.csdn.net/weixin_41965270/article/details/89150413

2、Armv8上不弃不离的NEON／FPU

https://www.jianshu.com/p/a19cc2ca59da