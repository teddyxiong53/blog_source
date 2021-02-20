---
title: arm之cache
date: 2018-04-01 10:53:44
tags:
	- arm
typora-root-url: ..\
---



# 什么是cache

出于CPU和ddr之间的一级存储器，是SRAM，特点是，快但是很贵。

ddr是sdram。

sram使用的MOS管比较多，占用硅片的面积大，因此功耗大，集成度低。

dram则使用MOS管少，功耗低，集成度高。



# 为什么需要cache

1、因为CPU和ddr内存的速度相差太大。ddr会拖慢CPU的。



# cache为什么要分级

对cache的需求，当然是越大越好。但是cache实在是贵。

分级是为了提高效率，分为两级，比单纯加大一级的cache，性价比要高很多。

现在的Intel core cpu已经有了三级cache了。

下面是我的电脑的情况。

二级缓存1M，三级缓存6M。

```
CPU详情
CPU厂商  GenuineIntel
CPU  (英特尔)Intel(R) Core(TM) i5-6500 CPU @ 3.20GHz
CPU核心数  4
CPU默认频率  3201 MHz
CPU外频  100 MHz
CPU当前频率  3201 MHz
二级缓存  1024 KB
三级缓存  6144 KB
CPU电压  1.000 V
CPU序列号  BFEBFBFF000506E3
数据宽度  64bit
指令集  MMX,SSE,SSE2,SSE3,SSSE3,SSE4.1,SSE4.2,EM64T
扩展版本  Ext.Family 0  Ext.Model 5
```

![arm之cache-图1](/images/arm之cache-图1.jpg)



可以看到，三级cache是所有核心共享的，跟一级和二级的不同。



# cache和mmu的关系

配置是下面这样的关系。

```
ICache 		| DCache 		| MMU 		| Allowed?
================================
Off			|	Off			|	Off		|	Yes
On			|	Off			|	Off		|	Yes
Off			|	On			|	Off		|	No
Off			|	Off			|	On		|	Yes
On			|	On			|	Off		|	No
Off			|	On			|	On		|	Yes
On			|	Off			|	On		|	Yes
On			|	On			|	On		|	Yes
```

总结；

mmu禁止的时候，dcache不能打开。icache可以打开。



数据在主存和缓存之间以固定大小的”块（block）”为单位传递，也就是每次从main memory读取的最小数据的单元。每个块的大小可能是4，8，16 Bytes或其他值，不同的CPU不尽相同，目前的x86 CPU cache line基本都是64 bytes。通常，人们更习惯称之为cache行，或者cache line。根据前一篇文章的描述，每个cache line除了包含数据，还包含TAG（地址信息）和状态信息。



# 关联方式

Cache的**替换策略**决定了主存中的数据块会**拷贝到cache中的哪个位置**，

如果对于一块数据（大小为一个cache line ），只有一个cache line与之对应，我们称之为”直接映射 (Direct map)”；

如果该数据块可以和cache中的任意一个cache line对应，则称之为”全相联（Full-Associative）”

而目前更多的实现方式是采用”N路组相连（N Way Set-Associative）”的方式，即内存中的某一块数据可能在

cache中的N个位置出现，N可能是2，4，8，12，或其他值。

## 直接关联

![img](/images/random_name/285001-112cc05b03c1970e.webp)



这是一种多对一的映射关系，在这种映射方式下，主存中的每个数据块只能有一个cache line与之对应，因此直接映射也称为”**单路组相联**”。

在1990年代初期，直接映射是当时最流行的机制

它所需的硬件资源非常有限，每次对主存的访问都固定到一个指定的cache line，

这种简单明了有一系列的好处，最大的优点是在200～300MHz CPU主频的情况下，Load-Use Latency可以快到只需要1个cycle！



随着CPU主频的提高，Load-Use Latency也在相对缩小，**直接映射方式的优势也就显得不那么明显**，同时，成平方级别**增长的主存容量使得cache的容量显得越来越小。**



由于没有替换策略，主存的数据能存在哪个cache line根本没得选 ，

**这也意味着当两个变量映射到同一个cache line时，他们会不停地把对方替换出去。**

由于严重的冲突，**频繁刷新cache将造成大量的延时**，而且在这种机制下，如果没有足够大的cache，**程序几乎无时间局部性可言。**



如今直接映射机制正在逐渐退出舞台。



单核处理器，使用Dcache 只存在一个问题，即与 DMA 会数据不一致的问题。

CPU 读取 RAM 数据，如果 Dcache 命中，则读取 Dcache 中的值，未命中则读取 RAM 中的值。写数据时，有两种方式： write through 和 write back。

write through 方式：CPU 将数据同时写回到 Dcache 和 RAM 中，这个过程与不开 Dcache 消耗的时间一样。

write back 方式： CPU 将数据写到 Dcache 中，并将该数值标志为 dirty， 当 Dcache 释放该数据时，将值写回到 RAM 中。这个过程是比较快捷的。



DMA 通常负责外设与 RAM 的通信，是不经过 CPU 的。

当 DMA 修改 RAM 中的数据时，CPU 是不知道的。



Cache的容量很小，它保存的内容只是主存内容的一个子集，且Cache与主存的数据交换是以块为单位的。

**为了把信息放到Cache中，必须应用某种函数把主存地址定位到Cache中，这称为地址映射**。

在信息按这种映射关系装入Cache后，CPU执行程序时，会将程序中的主存地址变换成Cache地址，这个变换过程叫做地址变换。



Cache的地址映射方式有直接映射、全相联映射和组相联映射。假设某台计算机主存容量为1MB，被分为2048块，每块512B；Cache容量为8KB，被分为16块，每块也是512B。下面以此为例介绍三种基本的地址映射方法。



直接映射，是dram里的一个块只能映射到cache里的某一个特定块。

```
第0块、第16块、第32块等等dram，只能映射到第0块cache。
第1块、第17块、第33块等等dram，只能映射到第1块cache。
依次类推。
```

这个存在的问题是，例如你的程序，重复使用了dram的第0块和第16块，就会导致这2个反复被换入换出。



全相联映射

是dram里的任何一个块，都可以映射到cache里的任何一个块上。

这个电路设计复杂。也不合适。



所以选择折中的方案，组相联映射。

具体是这么做的，先对dram和cache都进行分组。

dram一个组内的块数跟cache的分组数相同。

**组间采用直接映射，组内采用全相联映射。**

例如，dram分为256组，每组8块，cache分为8组，每组2块。



存储设备的速度对比



![å¾ç4.jpg](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/3d2f1556803040.jpg)

cache的共享关系

![å¾ç5.png](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/95101556803041.png)



在Cortex-A53架构上，

L1 cache分为单独的instruction cache（ICache）和data cache（DCache）。

L1 cache是CPU私有的，每个CPU都有一个L1 cache。

一个cluster 内的所有CPU共享一个L2 cache，L2 cache不区分指令和数据，都可以缓存。

所有cluster之间共享L3 cache。

L3 cache通过总线和主存相连。





# 参考资料

1、cache为什么分为i-cache和d-cache以及Cache的层次设计

https://blog.csdn.net/bytxl/article/details/50275377

2、ARM-I/Dcache, MMU关系

https://blog.csdn.net/jijiagang/article/details/8913459

3、内存类型中SRAM和DRAM什么区别？

https://zhidao.baidu.com/question/135827484.html

4、Cache基本原理之：结构

https://www.jianshu.com/p/2b51b981fcaf

5、（试图）深入理解 Cache

https://jcf94.com/2018/09/04/2018-09-04-cache/

6、Cache控制器设计

https://blog.csdn.net/Zhongzi_L/article/details/51607457

7、MMU、Icache、Dcache

https://blog.csdn.net/iodoo/article/details/8954014

8、Cache直接映射、组相连映射以及全相连映射（转载）

https://www.cnblogs.com/east1203/p/11572500.html

9、

这篇文章图文并茂，很好。

http://www.wowotech.net/memory_management/458.html