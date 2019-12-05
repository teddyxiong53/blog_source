---
title: arm之neon了解
date: 2019-12-04 13:34:28
tags:
	- arm
---

1

VFP(Vector Floating Point)指令
该指令用于向量化加速浮点运算。
自ARMv7开始正式引入NEON指令，NEON性能远超VFP，因此VFP指令被废弃。
类似于Intel CPU下的MMX/SSE/AVX/FMA指令，ARM CPU的NEON指令同样是通过向量化来进行速度优化。

参考资料

1、

https://blog.csdn.net/weixin_41965270/article/details/89150413