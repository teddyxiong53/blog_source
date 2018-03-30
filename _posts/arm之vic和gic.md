---
title: arm之vic和gic
date: 2018-03-30 11:16:47
tags:
	- arm

---



vic和gic是arm架构下的两种中断控制器。

另外，还有一个nvic。

这三者是什么关系？



多核系统只能用gic。因为只有gic才支持多核。

一般的芯片都会使用vic，因为是向量中断处理器，处理中断的速度非常快。

nvic是对vic的改进，支持中断嵌套。





# 参考资料

1、Arm Generic Interrupt controler(通用中断GIC)

https://wenku.baidu.com/view/7d9318d75022aaea998f0f2b.html?rec_flag=default&mark_pay_doc=2&mark_rec_page=1&mark_rec_position=3&mark_rec=view_r_1&clear_uda_param=1

2、中断控制器GIC、VIC和NVIC的区别和联系，以及他们主要用于那些场合？？？

http://www.embsky.com/forum.php?mod=viewthread&tid=267