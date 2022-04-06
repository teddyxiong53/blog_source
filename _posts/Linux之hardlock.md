---
title: Linux之hardlock
date: 2022-03-14 15:48:25
tags:
	- Linux

---

--

*soft lockup*：检测调度异常， 一般是驱动禁止调度或者阻塞比如while(1)， 导致无法调度其他线程，

*hard lockup*：检测中断异常， 一般是禁止中断或者某个中断函数内阻塞， 导致其他中断无法得到执行， 中断是系统得以运行的重要保证， 出了异常系统不可控！

由于不可屏蔽中断是10秒产生一次， 而定时器中断每4秒产生一次， 所以hrtimer_interrupts必然不等于hrtimer_interrupts_saved， 且将hrtimer_interrupts赋值到hrtimer_interrupts_saved进行更新，



hard lockup依赖处理器有没有NIM中断， 没有的话无法实现



参考资料

1、Linux soft lockup 和 hard lockup

https://blog.csdn.net/weixin_30512785/article/details/99746494