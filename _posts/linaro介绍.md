---
title: linaro介绍
date: 2017-05-07 16:23:21
tags:

	- arm

	- linano

---

在搜索qemu相关的信息的时候，看到了Linaro这个词，觉得有必要了解一下。

Linaro是一家公司的名字，公司的目标是开发可以在不同公司的SOC上运行的通用软件，以给用户和厂商带来价值。这家公司是非盈利性质的，由ARM、IBM、三星等这些半导体厂商联合成立的，时间是2010年3月。后续有很多的大厂家都加入进来了。

有人评论说，Linaro可能对Wintel（微软+英特尔）的模式是一个挑战。

这个公司到目前做出了哪些东西呢？

# 1. 合作开发板

Linaro和三星一起推出了一款低成本的开发板。使用了三星的双核Cortex A9处理器。Exynos4210芯片组，1G的内存。Linaro为这块板子提供了对应的Android和Ubuntu源代码。这块板子可以用来开发平板电脑等产品。

# 2. 工具链 

arm的交叉工具链，免费版本主要是3种：

gnu的、Codesourcery和Linaro。

从工具链的名字上来看，分别的对应关系是这样的：

arm-none-linux-gnueabi-gcc：这个是Codesourcery公司基于gcc推出的arm交叉编译工具。

arm-linux-gnueabi-gcc：这个就是Linaro公司基于gcc推出的工具链。

arm-none-eabi-gcc：这个就是gcc的了。

从上面可以看出，gcc是老祖宗，其余都是基于gcc来改的。



