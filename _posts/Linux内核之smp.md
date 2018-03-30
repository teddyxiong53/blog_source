---
title: Linux内核之smp
date: 2018-03-30 09:35:08
tags:
	- Linux内核
typora-root-url: ..\
---



smp是对称多处理器的意思。

smp起源于1950年代。开始的时候，因为单个处理器的性能不行，所以这个还是有很多公司在研究，不过后面到了80年代，单个处理器的性能提升了，大家的研究热情就下降了。

但是到了现在，这个又流行起来了。

有个Amdahl法则，就是核不是越多越好。管理多核的开销。

最早的linux smp是松耦合smp系统。实际上是多台机器，通过高速以太网连接起来。

对应的项目叫Linux Beowulf（贝奥武夫）。这个是一个集群。

这种就是架构起来容易，但是占用空间大，耗电。

紧耦合smp

这个就是一般说的smp了。是芯片级的。

![Linux内核之smp-图1](/images/Linux内核之smp-图1.png)

Linux内核在早期，是通过大内核锁来进行串行化。所以对smp的支持非常不好。

到了2.6版本的时候，才慢慢好起来。



#smp的内核变量保护

就是per-cpu变量。

这样来定义。

```
DEFINE_PER_CPU(int, cpu_state) = {0};
```

它是把变量定义在特别的位置。

```
#define PER_CPU_BASE_SECTION ".data..percpu"
```



# 参考资料

1、Linux 和对称多处理

https://www.ibm.com/developerworks/cn/linux/l-linux-smp/