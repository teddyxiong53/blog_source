---
title: linux的中断处理
date: 2016-11-30 21:06:49
tags:
	- linux驱动
---



# 中断分类

根据中断的来源，

1、内部中断。内部中断来自于cpu内部，如软中断指令、溢出、除法错误。

2、外部中断。外部中断，由外设发出的中断。



根据中断入口的跳转方法

1、向量中断。采用向量中断的cpu为不同的中断分配不同的中断号，不同中断号对应不同的入口地址。

2、非向量中断。非向量中断则是共用一个入口地址，然后用代码来判断中断标志来区分处理。



中断一般是很频繁的，而中断的处理对于系统的影响非常大。所以希望中断处理的时间尽量短，但是中断往往伴随着很大的数据量，处理数据是要花时间的。怎么解决这个问题呢？

linux的驱动框架提供了中断的分段处理机制：把中断的处理过程分为上半段和底半段。也就是top half和bottom half。
上半段只处理中断标志。主要工作由底半段来完成。
底半段在处理过程中可以被新的中断打断。而顶半段是不可以被新的中断打断的，处理期间是禁止中断的。
当然，如果某个中断处理的事情并不多，也可以不分段处理。

linux提供的底半段机制有：tasklet、工作队列、软中断。

# 1. tasklet
使用模板：
```
void xxx_do_tasklet(unsigned long );
DECLARE_TASKLET(xxx_tasklet, xxx_do_tasklet, 0);

//buttom half
void xxx_do_tasklet(unsigned long )
{

}
//top half
irqreturn_t xxx_interrupt(int irq, void *dev_id)
{
	...
	tasklet_schedule(&xxx_tasklet);
}
int xxx_init()
{
	ret = request_irq();
}
void xxx_exit()
{
	free_irq();
}
```
# 2. 工作队列 
和tasklet模板基本一致。

使用模板：
```
struct work_struct xxx_wq;
//buttom half
void xxx_do_work(unsigned long)
{
	
}

irqreturn_t xxx_interrupt(...)
{
	...
	schedule_work(&xxx_wq);
}

int xxx_init()
{
	request_irq();
	INIT_WORK(&xxx_wq, xxx_do_work, NULL);
}
void xxx_exit()
{
	free_irq();
}
```
# 3. 软中断
tasklet就是基于软中断来实现的。tasklet和软中断的处理函数里，不能sleep，工作队列的处理函数是可以的。

软中断上下文属于原子上下文的一种。

驱动编写者，不应该直接使用软中断。这个主要是提供给内核用的。

系统调用那里所说的软中断，和这里的软中断，不是一个概念，系统调用那个软中断是指软件上写特殊寄存器来人为触发一个中断。





# 工作队列和tasklet的比较

1、tasklet在软件中断上下文运行，所以tasklet代码必须是原子的。而工作队列函数是在一个特殊的内核进程上下文运行，可以休眠。

2、tasklet只能在最初被提交的处理器上运行。

3、tasklet还是需要尽快完成的，工作队列则时间上很宽松。



# 参考文章

http://blog.chinaunix.net/uid-20528014-id-3068412.html

