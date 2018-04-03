---
title: Linux内核之时间子系统（二）
date: 2018-04-03 09:58:26
tags:
	- Linux内核

---



这篇文章主要是对《Linux内核设计与实现》第11章的总结。



#tick处理了什么内容

linux在tick处理函数里，做了这些事情：

1、更新系统运行时间。

2、在smp系统上，均衡调度程序中各处理器上的运行队列，尽量使得负载均衡。

3、检查当前进程是否已经用尽了自己的时间片，如果用尽了，就重新调度。

4、运行注册的定时器。

5、更新资源消耗和处理器时间的统计值。



#HZ值

提高HZ值的好处有：

1、更高的时间精度。

2、对poll、select这种函数很有用，本来是10ms检查一次，如果你提高了，1ms就检查一次，就更加及时。

提高HZ值的坏处：

1、中断更加频繁，系统负载更重。

不过，对于现在的CPU来说，1000HZ还可以接受。所以linux还是运行你自己改的。

# 不要tick？

在os的发展历史里，一直都有tick这个东西存在。

现在的linux加入了五tick的选项，就是为了降低功耗。

# jiffies

jiffies是一个全局变量，用来统计开机以来的tick计数。

jiffy这个单词的意思是“一会儿”。这个词起源于18世纪的英国。

在科学应用里，jiffy一般是指10ms。

32位的jiffies变量，如果时钟频率是100HZ，那么会在497天之后溢出。

如果是64位的，那么就不用考虑溢出的问题。也许人类灭亡了，还没有溢出呢。

为了保持兼容，jiffies还是用的unsigned long定义。

这个对于32位机器，溢出的风险还是存在的。

不过内核开发者设计一种巧妙的方法来规避。

```
u64 jiffies_64;
```

在链接脚本里，arch/x86/kernel/vmlinux.lds.S里。

```
#ifdef CONFIG_X86_32
OUTPUT_ARCH(i386)
ENTRY(phys_startup_32)
jiffies = jiffies_64;
#else
OUTPUT_ARCH(i386:x86-64)
ENTRY(phys_startup_64)
jiffies_64 = jiffies;
#endif
```

jiffies的回绕。

为了避免jiffies的回绕导致的时间比较错误。linux提供了几个宏来进行处理。

```
unsigned long timeout = jiffies + HZ/2; //500ms
//... 这里可能产生溢出
if(time_before(jiffies, timeout)) {
  //没有超时
} else {
  //超时了。
}
```



#tick处理函数

tick_periodic函数。

里面就调用了

1、do_timer(1)。对jiffies_64加1 。

2、update_process_times



# BogoMIPS

这个是开机的时候计算的，就是用来给udelay这种函数来用的。

