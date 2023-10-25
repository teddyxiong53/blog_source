---
title: Linux之内核定时器
date: 2017-08-03 23:33:27
tags:

	- Linux

---

--

# kernel 定时器介绍

在 Linux 内核中，定时器是一种非常重要的机制，

用于执行定期或延迟的任务。

这些任务可以是周期性的，也可以是一次性的。

内核使用定时器来执行各种操作，如处理中断、调度任务、资源回收等。

以下是有关内核定时器的介绍：

1. **定时器类型**：
   - 内核中有两种主要类型的定时器：硬件定时器和软件定时器。
     - **硬件定时器**：硬件定时器通常由底层硬件提供，用于生成硬件中断，例如处理系统时钟。
     - **软件定时器**：软件定时器是由内核代码管理的，用于触发特定事件或任务。

2. **内核定时器的用途**：
   - 内核定时器可用于多种用途，包括：
     - 调度任务：内核可以使用定时器来触发任务的执行，例如在特定时间执行定期任务。
     - 中断处理：硬件定时器可用于生成时钟中断，以便内核能够跟踪时间和执行时间相关的操作。
     - 资源管理：内核可以使用定时器来回收未使用的资源，以提高系统的效率。
     - 延迟操作：定时器可以用于实现延迟执行，例如延迟删除或释放资源。

3. **内核定时器的API**：
   - 在 Linux 内核中，定时器通常使用 `struct timer_list` 结构表示，该结构包含了定时器的信息和回调函数。内核提供了一组函数，如 `init_timer`、`add_timer`、`mod_timer`、`del_timer` 以及相应的回调函数来操作和使用定时器。

4. **实现细节**：
   - 定时器可以实现为定时器事件队列，当定时器到期时，相关回调函数会被触发。
   - 内核使用硬件定时器来触发定时器事件。硬件定时器会定期触发中断，然后内核在中断处理程序中检查和触发到期的定时器事件。

5. **定时器的精度**：
   - 定时器的精度取决于硬件和内核实现。硬件定时器通常提供高精度的定时，而软件定时器的精度受到内核调度器的影响。

总之，内核定时器是 Linux 内核中的重要机制，用于管理各种与时间相关的任务和事件。这些定时器可用于实现调度、中断处理、资源管理和延迟操作等多种目的，从而为内核提供了强大的时间管理能力。内核定时器的正确使用对于系统的性能和可靠性至关重要。



# 关于定时器

1、定时器是管理内核时间的基础。

2、依赖全局变量jiffies。是unsigned long类型。

3、定时器的注册函数是只执行一次的，不是循环执行的。

# 使用定时器

1、定义一个定时器变量struct timer_list mytimer;

2、初始化定义的定时器变量。有好几个函数可以实现这个目的。一般我们用setup_timer。

3、增加定时器并且激活。用add_timer函数。

4、删除定时器，用del_timer函数。

5、修改定时器的超时时间，并启动。用mod_timer函数。

# 一个示例

```
#include <linux/timer.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/init.h>

#define MY_TIMER_MAJOR 222
#define MY_TIMER_NAME "mytimer"
//step 1
struct timer_list mytimer;

struct file_operations mytimer_ops =
{
	.owner = THIS_MODULE,
};
static void mytimer_func(unsigned long data)
{
	//step 4
	mod_timer(&mytimer, jiffies + HZ);
	printk("current jiffies:%ld \n", jiffies);
	
}
static int __init mytimer_init(void)
{
	register_chrdev(MY_TIMER_MAJOR, MY_TIMER_NAME, &mytimer_ops);
	//step 2
	setup_timer(&mytimer, mytimer_func, 0);
	//step 3
	add_timer(&mytimer);
	printk("mytimer init \n");
	return 0;
}


static void __exit mytimer_exit(void)
{
	printk("mytimer exit");
	del_timer(&mytimer);
	unregister_chrdev(MY_TIMER_MAJOR, MY_TIMER_NAME);
}
module_init(mytimer_init);
module_exit(mytimer_exit);
```

# 代码举例

以下是一个简单的示例，展示如何在 Linux 内核模块中创建和使用软件定时器。这个示例创建一个定时器，每隔一秒触发一次，然后在定时器回调函数中打印消息。

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/timer.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Your Name");

static struct timer_list my_timer;

static void my_timer_callback(unsigned long data) {
    printk(KERN_INFO "Timer callback: One second passed!\n");

    // 重新设置定时器，以便下一次触发
    mod_timer(&my_timer, jiffies + msecs_to_jiffies(1000));
}

static int my_init(void) {
    printk(KERN_INFO "Timer Example: Module init\n");

    // 初始化定时器
    setup_timer(&my_timer, my_timer_callback, 0);

    // 设置定时器的初始触发时间，这里是 1秒后触发
    mod_timer(&my_timer, jiffies + msecs_to_jiffies(1000));

    return 0;
}

static void my_exit(void) {
    printk(KERN_INFO "Timer Example: Module exit\n");

    // 删除定时器
    del_timer(&my_timer);
}

module_init(my_init);
module_exit(my_exit);
```

在这个示例中，我们执行以下操作：

1. 定义了一个名为 `my_timer` 的 `struct timer_list` 结构，该结构用于表示定时器。

2. 编写了 `my_timer_callback` 回调函数，当定时器触发时，这个函数将被调用。在本示例中，回调函数简单地打印一条消息，并重新设置定时器以在下一秒触发。

3. 在 `my_init` 函数中，初始化定时器并设置其初始触发时间为 1 秒后。我们使用 `setup_timer` 来初始化定时器，并使用 `mod_timer` 来设置定时器的初始触发时间。

4. 在 `my_exit` 函数中，删除定时器以确保在模块卸载时不再触发定时器事件。

您可以使用 `insmod` 命令加载内核模块，然后使用 `rmmod` 命令卸载它，观察定时器事件的触发和回调函数的执行。这个示例演示了如何在内核中创建和使用软件定时器。



