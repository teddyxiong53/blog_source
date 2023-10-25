---
title: Linux内核之workqueue
date: 2018-04-09 10:36:38
tags:
	- Linux内核

---

--

# 简介

在内核驱动里，一般小型的任务（work）都不会自己起一个线程来处理，

而是扔到workqueue里去处理。

**workqueue的主要工作就是用进程上下文来处理内核中大量的小任务。**



工作队列是内核2.6版本引入的，工作队列使用起来更加方便。

它把工作推后，交给一个内核thread去执行。

这个thread总是在进程上下文执行，所以很方便持有sem，也可以允许sleep。



工作队列和tasklet，都是属于底半段机制。

每个workqueue就是一个内核进程。



所以，workqueue的主要设计思想就是：

1、要并行，多个work不要相互阻塞。

2、要节省资源，多个work尽量共享资源。

工作队列workqueue**不是通过软中断实现**的，它是**通过内核进程实现**的

内核进程worker_thread做的事情很简单，死循环而已，不停的执行workqueue上的work_list.



为了实现这个设计思想，workqueue的设计实现也经历了多个版本。

最新的workqueue实现叫做CMWQ（Concurrency Managed Workqueue），

也就是更加智能的算法来实现并行和节省。



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

**所以早期很多驱动开发人员都是自己创建workqueue， 添加自己的work。** 

在Linux-2.XXX时代， 创建workqueue时会创建属于workqueue自己的内核线程，

 这些线程是“私有的”， 虽然是方便了驱动开发人员，

 **但每个驱动都“一言不合”就创建workqueue导致太多线程，**

 **严重占用系统资源和效率，**

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



# 介绍

Kernel workqueue（内核工作队列）是 Linux 内核中用于异步执行内核任务的一种机制。

它允许内核代码在后台执行任务，而不会阻塞当前进程或线程。

工作队列通常用于执行与设备管理、定时任务、中断处理、系统维护等相关的工作。

以下是关于内核工作队列的一些重要信息：

1. **异步执行**：工作队列允许内核代码将工作推入后台执行，而不需要阻塞当前执行流。这对于需要较长时间来完成的任务非常有用，以避免阻塞主要的系统进程。

2. **类型**：内核工作队列有两种主要类型：普通工作队列（workqueue）和延迟工作队列（delayed workqueue）。普通工作队列通常在工作项添加后立即执行，而延迟工作队列则可以设置延迟时间后再执行工作项。

3. **创建和初始化**：要使用工作队列，你需要先创建和初始化一个工作队列对象。这通常在模块初始化期间完成。

4. **添加工作项**：你可以使用`queue_work`或`queue_delayed_work`函数将工作项添加到工作队列中。这些工作项是函数指针，通常指向你希望在工作队列中执行的函数。

5. **执行工作项**：工作队列中的工作项将由内核的工作线程池执行。内核会自动创建和管理这些工作线程，以异步执行工作项。

6. **取消工作项**：你可以使用`cancel_work_sync`或`cancel_delayed_work_sync`函数来取消已经添加到工作队列中的工作项。

7. **销毁工作队列**：在不再需要工作队列时，应该销毁它以释放资源。这通常在模块卸载期间完成。

内核工作队列的主要目的是提高系统的响应性和性能，同时允许内核执行一些需要长时间运行的任务，而不会影响系统的实时性能。

这在处理设备管理、文件系统操作、中断处理等方面非常有用。

它是内核中的一种重要的异步执行机制。

# workqueue的发展历史

Workqueue 是 Linux 内核中的一个重要子系统，用于管理异步工作任务。

其历史可以追溯到 Linux 内核的早期版本，经历了多个阶段的发展和改进。

以下是 Workqueue 的发展历史的主要里程碑：

1. **早期的内核版本**：早期的 Linux 内核没有专门的工作队列机制，开发人员通常使用内核定时器和其他手动管理的方式来执行异步任务。

2. **2.6 内核系列**：Workqueue 子系统首次引入于 Linux 2.6 内核系列。它引入了 `kernel/workqueue.c` 文件，为内核开发人员提供了一个标准的接口来创建和管理工作队列。这是 Workqueue 子系统的初始版本。

3. **2.6.20 内核**：在 Linux 2.6.20 内核版本中，`work_struct` 结构体（代表工作项）的设计和 API 进行了一些改进，以提供更好的灵活性和性能。

4. **2.6.36 内核**：在 Linux 2.6.36 内核版本中，引入了可延迟的工作队列 (delayed workqueue)。这允许开发人员将工作项设置为在一定延迟后执行，而不是立即执行。

5. **4.15 内核**：在 Linux 4.15 内核版本中，引入了 Unified Workqueue (unbound workqueues)。这一变化允许工作项在多个 CPU 核心上并行执行，以提高性能。此版本还引入了 `alloc_workqueue` 函数以简化工作队列的创建。

6. **5.5 内核**：在 Linux 5.5 内核版本中，引入了基于 CPU 的 Workqueue，这允许开发人员将工作项绑定到特定的 CPU 核心上执行。

7. **5.11 内核**：在 Linux 5.11 内核版本中，引入了 WQ_MEM_RECLAIM 类型的工作队列，用于执行内存回收相关的工作。

Workqueue 的不断发展和改进旨在提高内核的性能、可维护性和可扩展性。它是 Linux 内核中的一个核心组件，用于处理异步任务，如设备管理、磁盘操作、文件系统任务等。内核开发人员依赖于 Workqueue 来确保这些任务能够以非阻塞的方式进行，提高了整个系统的响应性。因此，Workqueue 子系统在内核开发中一直处于不断发展和改进的状态。

# workqueue的常用flag介绍

在 Linux 内核中使用 Workqueue 时，可以指定不同的标志（flags），以定制工作队列的行为。以下是一些常用的 Workqueue 标志以及它们的介绍：

1. **WQ_FREEZABLE**：这个标志表示工作队列支持系统的冻结（suspend-to-ram）操作。当系统进入冻结状态时，工作队列中的工作项将被冻结，直到系统恢复。这可以确保工作队列的工作不会在系统休眠期间执行。

2. **WQ_UNBOUND**：这个标志表示工作队列是无绑定的，工作项可以在任何可用的 CPU 核心上执行。这对于并行化工作非常有用，以提高性能。

3. **WQ_HIGHPRI**：这个标志表示工作队列是高优先级的，其工作项将在普通工作队列之前执行。这可以用于确保高优先级的工作能够及时执行。

4. **WQ_CPU_INTENSIVE**：这个标志表示工作队列用于 CPU 密集型工作。在这种情况下，工作队列会尽量将工作项绑定到请求的 CPU 核心上，以减少上下文切换的开销。

5. **WQ_RESCUER**：这个标志用于创建一个救援工作队列，用于处理其他工作队列中的工作项。这可以帮助避免死锁情况，当一个工作队列在等待其他工作队列的工作项时，救援工作队列可以处理它们。

6. **WQ_MEM_RECLAIM**：这个标志用于工作队列执行内存回收相关的工作。它通常用于确保内存管理操作不会导致内存耗尽。

7. **WQ_POWER_EFFICIENT**：这个标志用于表示工作队列是用于执行省电工作的。它通常用于移动设备和节能优化的场景。

8. **WQ_SYSFS**：这个标志用于创建一个可通过 sysfs 接口控制的工作队列。这允许用户空间程序配置和管理工作队列。

这些标志可用于在创建工作队列时定义工作队列的行为。你可以根据你的特定需求选择适当的标志来控制工作队列的性能和行为。注意，标志的可用性和行为可能会根据内核版本有所不同，因此查阅你所使用的内核版本的文档以获取详细信息是很重要的。

# workqueue的常用api说明

Workqueue 是 Linux 内核中用于管理异步工作任务的子系统，

提供了一组 API 函数来创建、管理和处理工作队列。

以下是一些常用的 Workqueue API 函数以及它们的简要说明：

1. **`create_workqueue(const char *name)`**：
   - 用于创建一个新的工作队列。
   - `name` 参数是工作队列的名称。
   - 返回一个指向新创建工作队列的指针。

2. **`create_singlethread_workqueue(const char *name)`**：
   - 创建一个单线程工作队列，只有一个线程在队列中处理工作项。
   - 通常用于需要严格顺序执行的工作。

3. **`queue_work(struct workqueue_struct *wq, struct work_struct *work)`**：
   - 将工作项添加到工作队列中，立即执行。
   - `wq` 是工作队列指针。
   - `work` 是指向工作项的指针。

4. **`queue_delayed_work(struct workqueue_struct *wq, struct work_struct *work, unsigned long delay)`**：
   - 将工作项添加到工作队列中，并设置延迟时间后执行。
   - `delay` 是延迟的时间（以 jiffies 为单位）。
   
5. **`cancel_work_sync(struct work_struct *work)`**：
   - 取消指定的工作项，并等待它的执行完成。
   
6. **`flush_workqueue(struct workqueue_struct *wq)`**：
   - 等待工作队列中的所有工作项执行完成，然后返回。
   
7. **`destroy_workqueue(struct workqueue_struct *wq)`**：
   - 销毁工作队列，释放相关资源。
   
8. **`flush_scheduled_work()`**：
   - 立即执行所有已调度的工作项。

9. **`schedule_work(struct work_struct *work)`**：
   - 将工作项调度到当前 CPU 核心的工作队列中，等待执行。

10. **`schedule_delayed_work(struct work_struct *work, unsigned long delay)`**：
    - 将工作项调度到当前 CPU 核心的工作队列中，并设置延迟时间后执行。

这些 API 函数是用于创建和操作工作队列的常用函数。它们允许内核开发人员创建异步工作任务，将它们提交到工作队列，等待它们执行完成，或取消它们的执行。这些函数是 Linux 内核中实现异步操作和并发任务的重要工具，以提高系统的响应性和性能。在内核编程中，熟练使用这些 API 函数对于实现复杂的内核功能非常重要。





# 参考资料

1、Linux workqueue工作原理 

https://www.cnblogs.com/sky-heaven/p/5847519.html

2、Linux-workqueue讲解

这篇很好。

https://www.cnblogs.com/vedic/p/11069249.html