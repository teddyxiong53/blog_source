---
title: Linux内核之dump_stack
date: 2021-02-19 14:22:30
tags:
- Linux
---

--

对于大型驱动，想要知道某个回调函数由谁调用，非常困难。

到底有没有办法知道呢？

回答是肯定的，

通过内核提供的接口dump_stack()可以满足要求。

其实能够想到使用dump_stack()来跟踪，

是根据当内核发生panic时候，也会主动调用该接口，

所以我们可以在调试过程中**主动调用该接口来进行测试。**





参考资料

1、dump_stack()使用方法

https://blog.csdn.net/yanlaifan/article/details/51462497

2、linux内核中打印栈回溯信息 - dump_stack()函数分析

https://blog.csdn.net/jasonchen_gbd/article/details/45585133