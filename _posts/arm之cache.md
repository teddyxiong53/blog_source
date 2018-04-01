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





# 参考资料

1、cache为什么分为i-cache和d-cache以及Cache的层次设计

https://blog.csdn.net/bytxl/article/details/50275377

2、ARM-I/Dcache, MMU关系

https://blog.csdn.net/jijiagang/article/details/8913459