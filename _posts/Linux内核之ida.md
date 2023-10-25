---
title: Linux内核之ida
date: 2020-06-16 09:49:49
tags:
	- Linux

---

--

ida是ID Allocation。就是分配ID的意思。



在 Linux 内核中，ID Allocation（标识分配）通常指的是为进程分配唯一的标识符，通常是进程的 PID（Process ID）。

PID 是一个整数，用于唯一标识系统中的每个进程。

以下是有关 Linux 内核中的 PID 分配的一些介绍：

1. **PID 的分配**：
   - 在 Linux 内核中，PID 是动态分配的。当新的进程创建时，内核会为该进程分配一个唯一的 PID。这是通过查找可用的未分配 PID 来实现的。

2. **PID 范围**：
   - 在 Linux 中，PID 的范围通常是有限的。具体的范围可以在内核配置中进行设置。不同的 Linux 发行版可能具有不同的 PID 范围设置。

3. **PID 重用**：
   - 在某些情况下，已经终止的进程的 PID 可能会在稍后重新分配给新创建的进程。这是为了确保 PID 范围的有效利用，因为系统中可能会有大量的进程。

4. **PID 唯一性**：
   - 尽管 PID 可以被重用，但在任何给定时间点，不同的进程必须具有唯一的 PID。这有助于标识和管理系统中的进程。

5. **进程表**：
   - 内核维护一个进程表，其中包含了系统中所有活动进程的信息，包括它们的 PID、状态、优先级等。进程表的目的是跟踪和管理进程。

6. **进程管理**：
   - PID 是进程管理的关键部分。通过 PID，内核能够识别、管理和通信与各个进程。

总之，PID 分配是 Linux 内核中的一个重要机制，用于标识和管理系统中的进程。内核动态分配唯一的 PID，确保不同进程之间的唯一性。进程的 PID 对于进程管理、通信和资源控制非常重要。



# Linux对pid的回收利用的策略是怎样的

Linux 通过一些策略来回收和重用 PID（进程标识符），以确保 PID 的有效利用和系统的正常运行。以下是一些关于 Linux PID 回收和重用策略的概述：

1. **PID 的有限范围**：
   - Linux 内核为 PID 分配一个有限的范围。PID 号码通常是 16 位或 32 位的整数，具体范围由内核配置决定。这限制了系统中可用的 PID 数量。

2. **PID 循环重用**：
   - 一旦系统中的进程终止，其 PID 号码可能会被回收并在稍后分配给新创建的进程。这是因为 PID 空间是有限的，而系统中的进程数量可能会在运行时不断变化。这种 PID 循环重用有助于有效利用 PID 范围。

3. **进程终止后的 PID 回收**：
   - 当进程终止时，其 PID 号码会被标记为可重用。内核会将这些已终止进程的 PID 标记为可分配状态，以供将来的新进程使用。

4. **等待时间**：
   - 内核通常等待一段时间后才会将已终止进程的 PID 标记为可重用。这是为了确保不会立即将已终止进程的 PID 分配给新进程，以避免潜在的进程状态混乱。

5. **进程状态清理**：
   - 内核会对已终止的进程进行一定的清理操作，例如释放与进程相关的资源和数据结构，然后才将 PID 标记为可重用。

6. **有效利用范围内的 PID 分配**：
   - 内核会努力确保分配给新进程的 PID 在有效范围内，并不会分配已经分配过的 PID，以防止冲突。

7. **配置选项**：
   - 一些内核配置选项可以影响 PID 的回收和重用策略。管理员可以配置 PID 范围和重用行为以适应系统的需求。

总之，Linux 通过有限的 PID 范围、PID 循环重用、等待时间、进程状态清理等策略来回收和重用 PID，以确保系统中的 PID 能够有效利用并避免冲突。这些策略有助于确保进程标识符的唯一性和有效性。



# ID allocation使用举例

Linux 内核中的 ID allocation（标识符分配）通常是由内核自动管理的，

特别是对于 PID（进程标识符）。

程序员通常不需要直接操作或分配 PID，

因为内核负责为新进程自动分配唯一的 PID。

以下是一个简化的示例，演示了 Linux 内核如何为新进程分配 PID：

```c
#include <linux/module.h>
#include <linux/init.h>
#include <linux/sched.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Your Name");

static int __init my_init(void) {
    printk(KERN_INFO "Initializing PID Allocation Example\n");

    // 创建新进程
    struct task_struct *new_task;
    new_task = kthread_create(my_thread_func, NULL, "my_thread");
    
    if (IS_ERR(new_task)) {
        printk(KERN_ERR "Failed to create new process\n");
        return PTR_ERR(new_task);
    }

    wake_up_process(new_task);

    return 0;
}

static void __exit my_exit(void) {
    printk(KERN_INFO "Exiting PID Allocation Example\n");
}

module_init(my_init);
module_exit(my_exit);
```

在这个示例中，我们执行以下操作：

1. 在初始化函数 `my_init` 中，我们创建了一个新的内核线程（kthread），并为该线程指定了一个名称 "my_thread"。**线程的 PID 将由内核自动分配。**

2. 使用 `kthread_create` 函数创建线程，如果成功，将返回指向新线程的指针。

3. 使用 `wake_up_process` 函数启动线程。

这里并没有直接分配 PID，而是由内核自动分配。内核将负责为新进程分配一个唯一的 PID，从而确保进程标识符的唯一性和有效性。

注意：在实际内核开发中，通常不需要显式分配 PID，因为内核会负责处理这些细节。PID 的分配和管理通常在内核的进程调度和创建过程中进行。

# 参考资料

1、ID Allocation

https://www.kernel.org/doc/html/v4.18/core-api/idr.html