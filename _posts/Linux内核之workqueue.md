---
title: Linux内核之workqueue
date: 2018-04-09 10:36:38
tags:
	- Linux内核

---

1

在内核驱动里，一般小型的任务（work）都不会自己起一个线程来处理，而是扔到workqueue里去处理。**workqueue的主要工作就是用进程上下文来处理内核中大量的小任务。**

工作队列是内核2.6版本引入的，工作队列使用起来更加方便。它把工作推后，交给一个内核thread去执行。这个thread总是在进程上下文执行，所以很方便持有sem，也可以允许sleep。

工作队列和tasklet，都是属于底半段机制。

每个workqueue就是一个内核进程。

所以，workqueue的主要设计思想就是：

1、要并行，多个work不要相互阻塞。

2、要节省资源，多个work尽量共享资源。

工作队列workqueue**不是通过软中断实现**的，它是**通过内核进程实现**的

内核进程worker_thread做的事情很简单，死循环而已，不停的执行workqueue上的work_list.



为了实现这个设计思想，workqueue的设计实现也经历了多个版本。最新的workqueue实现叫做CMWQ（Concurrency Managed Workqueue），也就是更加智能的算法来实现并行和节省。

相关概念：

1、work。最小单位。核心就是一个函数指针。

2、workqueue。work的集合。



涉及的数据结构：

```
struct work_struct
struct cpu_workqueue_struct
struct workqueue_struct

struct worker_pool
struct pool_workqueue 
```



workqueue系统的初始化：

```
start_kernel
	do_basic_setup
		init_workqueues
			keventd_wq = create_workqueue("events");
				create_workqueue_thread
					kthread_create(worker_thread, cwq, fmt, wq->name, cpu);
```





workqueue是对内核线程封装的用于处理各种工作项的一种处理方法，

由于处理对象是用链表拼接一个个工作项， 

依次取出来处理， 然后从链表删除，

就像一个队列排好队依次处理一样， 所以也称工作队列，

**所谓封装可以简单理解一个中转站，** 

一边指向“合适”的内核线程， 一边接受你丢过来的工作项， 

用结构体 workqueue_srtuct表示， 

而所谓工作项也是个结构体 --  work_struct， 

里面有个成员指针， 指向你最终要实现的函数，



当然使用者在实现自己函数功能后可以直接调用，

或者通过kthread_create()把函数当做新线程的主代码，

 或者add_timer添加到一个定时器延时处理



那为何要弄个work_struct工作项先封装函数， 然后再丢到workqueue_srtuct处理呢？

 这就看使用场景了， 如果是一个大函数， 处理事项比较多， 且需要重复处理，

 可以单独开辟一个内核线程处理； 对延时敏感的可以用定时器； 

如果只是简单的一个函数功能，  且函数里面有延时动作的， 

就适合放到工作队列来处理了， 

毕竟定时器处理的函数是在中断上下文，不能delay或者引发进程切换的API，  

而且开辟一个内核线程是耗时且耗费资源的， 一般用于函数需要while(1) 不断循环处理的，

一个简单的使用workqueue和work_struct的例子如下。

```
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/delay.h>
#include <linux/workqueue.h>

struct workqueue_struct *workqueue_test;

struct work_struct work_test;

void work_test_func(struct work_struct *work)
{
    printk("%s()\n", __func__);

    //mdelay(1000);
    //queue_work(workqueue_test, &work_test);
}


static int test_init(void)
{
    printk("Hello,world!\n");

    /* 1. 自己创建一个workqueue， 中间参数为0，默认配置 */
    workqueue_test = alloc_workqueue("workqueue_test", 0, 0);

    /* 2. 初始化一个工作项，并添加自己实现的函数 */
    INIT_WORK(&work_test, work_test_func);

    /* 3. 将自己的工作项添加到指定的工作队列去， 同时唤醒相应线程处理 */
    queue_work(workqueue_test, &work_test);
    
    return 0;
}

static void test_exit(void)
{
    printk("Goodbye,cruel world!\n");
    destroy_workqueue(workqueue_test);
}

module_init(test_init);
module_exit(test_exit);

MODULE_AUTHOR("Vedic <FZKmxcz@163.com>");
MODULE_LICENSE("Dual BSD/GPL");
```

不过一般情况下，我们是不需要自己另外新建的workqueue的，内核默认提供了一些。

所以上面的代码，可以进一步简化。

```
static int test_init(void)
{
    printk("Hello,world!\n");

    /* 2. 初始化一个工作项，并添加自己实现的函数 */
    INIT_WORK(&work_test, work_test_func);

    /* 3. 将自己的工作项添加到指定的工作队列去， 同时唤醒相应线程处理 */
    queue_work(system_wq, &work_test);
    
    return 0;
}

如果workqueue对象是 system_wq， 可以使用另一个封装函数schedule_work(&work_test)
static inline bool schedule_work(struct work_struct *work)
{
　　return queue_work(system_wq, work);
}
```

将自己的工作项挂到已有的工作队列

需要注意的是由于这些队列是共享的，

 各个驱动都有可能将自己的工作项放到同个队列， 

会导致队列的项拥挤，

 当有些项写的代码耗时久或者调用delay()延时特别久， 你的项将会迟迟得不到执行！ 

所以早期很多驱动开发人员都是自己创建workqueue， 添加自己的work。 

在Linux-2.XXX时代， 创建workqueue时会创建属于workqueue自己的内核线程，

 这些线程是“私有的”， 虽然是方便了驱动开发人员，

 但每个驱动都“一言不合”就创建workqueue导致太多线程，

 严重占用系统资源和效率，

所以在Linux-3.XXX时代， 社区开发人员将workqueue和内核线程剥离！ 

**内核会自己事先创建相应数量的线程**（后面详解）， 被所有驱动共享使用。  

用户调用alloc_workqueue()只是创建workqueue这个空壳，

 其主要作用：

　　a. 兼容Linux-2.XXX时代代码

　　b. 新增flag字段表明这个workqueue的属性（普通优先级还是高优先级等）， 方便在queue_work()时寻找“合适的”线程， 因为事先创建的线程分普通优先级、高优先级、绑定CPU线程， 非绑定CPU线程等

当然这对驱动开发人员是透明的， 

驱动人员只需关注调用queue_work()让线程执行自己的工作项， 

至于是这个workqueue的私有线程还是现在的共享线程， 不重要！

 **这样就限制了系统工作线程的暴涨**， 

唯一的缺点就是前面提到的， **跟别人共享会增加自己的工作项被执行的不确定性。**

**只能说各个驱动开发人员自我约束**， 尽量使得工作项函数简短快速， 

**如果我们需要等自己的工作项被执行完才能处理其他事情， 可以调用flush_work() 等待work被执行完**





参考资料

1、Linux workqueue工作原理 

https://www.cnblogs.com/sky-heaven/p/5847519.html

2、Linux-workqueue讲解

这篇很好。

https://www.cnblogs.com/vedic/p/11069249.html