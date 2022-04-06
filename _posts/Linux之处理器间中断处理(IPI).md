---
title: Linux之处理器间中断处理(IPI)
date: 2022-03-25 19:39:25
tags:
	- Linux

---

--

处理器间中断允许一个CPU向系统其他的CPU发送中断信号，

处理器间中断（IPI）不是通过IRQ线传输的，

而是作为信号直接放在连接所有CPU本地APIC的总线上。

在多处理器系统上，Linux定义了下列三种处理器间中断：

在多处理器系统上，Linux定义了下列三种处理器间中断：

**CALL_FUNCTION_VECTOR** （*向量0xfb*）

发往所有的CPU，但不包括发送者，强制这些CPU运行发送者传递过来的函数，相应的中断处理程序叫做*call_function_interrupt()*，例如，地址存放在群居变量*call_data*中来传递的函数，可能强制其他所有的CPU都停止，也可能强制它们设置内存类型范围寄存器的内容。通常，这种中断发往所有的CPU，但通过*smp_call_function()*执行调用函数的CPU除外。

**RESCHEDULE_VECTOR** （*向量0xfc*）

当一个CPU接收这种类型的中断时，相应的处理程序限定自己来应答中断，当从中断返回时，所有的重新调度都自动运行。

**INVALIDATE_TLB_VECTOR** （*向量0xfd*）

发往所有的CPU，但不包括发送者，强制它们的转换后援缓冲器TLB变为无效。相应的处理程序刷新处理器的某些TLB表项。



Linux有一组函数使得发生处理器间中断变为一件容易的事：

| 函数                  | 说明                               |
| :-------------------- | :--------------------------------- |
| send_IPI_all()        | 发送一个IPI到所有CPU，包括发送者   |
| send_IPI_allbutself() | 发送一个IPI到所有CPU，不包括发送者 |
| send_IPI_self()       | 发送一个IPI到发送者的CPU           |
| send_IPI_mask()       | 发送一个IPI到位掩码指定的一组CPU   |



大家知道，在做内核调试器的时候，为了不影响当前环境，当[中断](https://so.csdn.net/so/search?q=中断&spm=1001.2101.3001.7020)产生的时候必须将非当前cpu外的其他cpu
的运行中断下来。那么内核调试器是怎么做到的呢？实际上这是APIC的ipi（处理器间中断）。





参考资料

1、处理器间中断处理(IPI)

https://blog.csdn.net/fishmai/article/details/99593954

2、浅谈APIC的IPI机制

https://blog.csdn.net/weixin_34097242/article/details/92488657

3、

https://blog.csdn.net/vito_bin/article/details/52986011