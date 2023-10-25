---
title: Linux之内核中的同步机制辨析
date: 2018-03-08 17:04:13
tags:
	- Linux

---

# 同步机制

## mutex

mutex相当于一个厕所坑位，只能一个人上。后面要用的人得排队等前面的一个人出来才行。

## semaphore

这个是一个教室，可以容纳多人，还有座位就能进去。

## 二值semaphore和mutex区别

1、有的系统是没有区别的。

2、有的系统有区别。mutex谁拿着谁释放。而semaphore可以由其他人释放。

mutex用来保护，semaphore用来同步。分工明确。

## spinlock和semaphore区别

1、spinlock是一直占用CPU的等。

2、semaphore会sleep让出CPU。

3、只有多CPU的内核态非进程空间，才会用到spinlock。

结论：spinlock很少用。

# linux内核同步机制有哪些

Linux 内核使用多种同步机制来管理并发访问共享资源，以确保数据的一致性和防止竞争条件。以下是一些常见的 Linux 内核同步机制：

1. **自旋锁（Spinlock）**：
   - 自旋锁用于短时间内的互斥同步。它会循环等待资源，直到锁可用，适用于在中断上下文中获取锁的情况。自旋锁的特点是快速获取，但会导致 CPU 自旋。

2. **互斥锁（Mutex）**：
   - 互斥锁用于长时间内的互斥同步。它会将等待的线程阻塞，直到锁可用。互斥锁适用于进程上下文的同步，也可以在中断上下文使用 spinlock。

3. **信号量（Semaphore）**：
   - 信号量用于资源计数和同步。它允许多个线程访问资源，但在资源耗尽时会阻塞等待。信号量通常用于进程间通信。

4. **读写锁（Reader-Writer Lock）**：
   - 读写锁允许多个读操作同时进行，但只允许一个写操作进行。这对于读多写少的场景非常有用。

5. **自旋信号量（Spinlock-based Semaphores）**：
   - 自旋信号量是一种类似于信号量的机制，但使用自旋锁来进行同步。它通常用于轻量级同步，适用于中断上下文等环境。

6. **条件变量（Condition Variables）**：
   - 条件变量用于线程间的协作，它允许一个线程等待某个条件的满足，另一个线程在条件满足时通知等待线程继续执行。

7. **屏障（Barriers）**：
   - 屏障用于线程同步，确保一组线程在达到某个点之前都停止执行，然后在所有线程都达到该点后同时继续执行。

8. **计数器（Counters）**：
   - 计数器通常用于跟踪某种资源的数量，例如等待队列中的任务数量，以便根据需要进行调度。

9. **RCU（Read-Copy Update）**：
   - RCU 是一种用于读优化的同步机制，它允许无锁访问共享数据结构，而不需要锁定读取操作。RCU 通常用于高性能数据结构。

10. **内核线程间通信（Kernel-to-Kernel Communication）**：
    - Linux 内核还提供了各种用于内核线程间通信的同步机制，如工作队列、等待队列等。

这些同步机制在 Linux 内核中用于不同的情况和需求，以确保内核的稳定性、性能和正确性。选择正确的同步机制对于内核开发非常重要，因为它直接影响到系统的性能和可靠性。

## spinlock举例

在 Linux 内核中，自旋锁（Spinlock）通常用于临界区的短时间互斥同步，因为它不会导致线程切换（不会使线程进入休眠状态），适合在中断上下文中使用。下面是一个简单的示例，演示如何在内核模块中使用自旋锁：

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/spinlock.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Your Name");

static spinlock_t my_spinlock; // 声明自旋锁变量

static int my_data = 0; // 共享资源

static int my_init(void) {
    printk(KERN_INFO "Spinlock Example: Module init\n");
    spin_lock_init(&my_spinlock); // 初始化自旋锁

    // 模拟两个线程尝试访问共享资源
    spin_lock(&my_spinlock); // 获取自旋锁

    // 临界区：在这里访问共享资源
    my_data++;
    printk(KERN_INFO "Shared resource incremented: %d\n", my_data);

    spin_unlock(&my_spinlock); // 释放自旋锁

    return 0;
}

static void my_exit(void) {
    printk(KERN_INFO "Spinlock Example: Module exit\n");
}

module_init(my_init);
module_exit(my_exit);
```

这个示例演示了如何在内核模块中使用自旋锁。首先，使用`spin_lock_init`初始化了自旋锁。然后，在`my_init`函数中，两个线程尝试获取自旋锁，只有一个线程能够成功获取锁，进入临界区，对共享资源（`my_data`）进行操作，最后释放自旋锁。自旋锁确保了在临界区内的操作是互斥的，从而避免竞争条件。

需要注意的是，自旋锁适用于短时间的互斥同步，因为它会让线程在获取锁失败时忙等待，不会主动放弃 CPU 时间片。在某些情况下，如果临界区的代码执行时间过长，自旋锁可能会导致系统性能下降。因此，选择适当的同步机制对于内核开发非常重要，根据具体需求选择自旋锁、互斥锁或其他同步机制。

## mutex举例

在 Linux 内核中，互斥锁（Mutex）通常用于长时间的互斥同步，阻塞等待资源可用。以下是一个示例，演示如何在内核模块中使用互斥锁：

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/mutex.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Your Name");

static DEFINE_MUTEX(my_mutex); // 声明互斥锁变量

static int my_data = 0; // 共享资源

static int my_init(void) {
    printk(KERN_INFO "Mutex Example: Module init\n");

    // 临界区：在这里获取互斥锁，访问共享资源，然后释放锁
    mutex_lock(&my_mutex); // 获取互斥锁

    // 访问共享资源
    my_data++;
    printk(KERN_INFO "Shared resource incremented: %d\n", my_data);

    mutex_unlock(&my_mutex); // 释放互斥锁

    return 0;
}

static void my_exit(void) {
    printk(KERN_INFO "Mutex Example: Module exit\n");
}

module_init(my_init);
module_exit(my_exit);
```

在这个示例中，首先使用`DEFINE_MUTEX`宏定义了一个互斥锁变量`my_mutex`。然后，在`my_init`函数中，通过`mutex_lock`获取互斥锁，进入临界区，在临界区内对共享资源（`my_data`）进行操作，最后使用`mutex_unlock`释放互斥锁。互斥锁确保在临界区内的操作是互斥的，只有一个线程可以访问临界区，从而避免竞争条件。

互斥锁适用于需要长时间的互斥同步，其中线程可能需要等待资源的情况。互斥锁会使等待的线程进入休眠状态，直到锁可用。这有助于避免在忙等待自旋锁时浪费 CPU 时间。同样，选择适当的同步机制对于内核开发非常重要，根据具体需求选择自旋锁、互斥锁或其他同步机制。



## sem举例

在 Linux 内核中，信号量（Semaphore）通常用于资源计数和同步，允许多个线程访问资源，但在资源耗尽时会阻塞等待。以下是一个示例，演示如何在内核模块中使用信号量：

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/semaphore.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Your Name");

static struct semaphore my_semaphore; // 声明信号量变量

static int my_data = 0; // 共享资源

static int my_init(void) {
    printk(KERN_INFO "Semaphore Example: Module init\n");

    // 初始化信号量为1，表示资源初始可用
    sema_init(&my_semaphore, 1);

    // 临界区：在这里获取信号量，访问共享资源，然后释放信号量
    if (down_interruptible(&my_semaphore) == 0) {
        // 获取信号量成功
        // 访问共享资源
        my_data++;
        printk(KERN_INFO "Shared resource incremented: %d\n", my_data);
        up(&my_semaphore); // 释放信号量
    } else {
        printk(KERN_INFO "Failed to obtain the semaphore (interrupted)\n");
    }

    return 0;
}

static void my_exit(void) {
    printk(KERN_INFO "Semaphore Example: Module exit\n");
}

module_init(my_init);
module_exit(my_exit);
```

在这个示例中，首先使用`sema_init`初始化了信号量`my_semaphore`，并将其设置为1，表示资源初始可用。然后，在`my_init`函数中，通过`down_interruptible`尝试获取信号量，如果获取成功，就进入临界区，在临界区内对共享资源（`my_data`）进行操作，最后使用`up`释放信号量。

信号量允许多个线程同时进入临界区，但在资源耗尽时会阻塞等待。如果资源已经被其他线程占用，`down_interruptible`将会将当前线程置于休眠状态，直到信号量可用。这有助于避免竞争条件。

需要注意的是，内核中的信号量通常用于进程间同步，以确保对共享资源的访问是有序和安全的。选择适当的同步机制对于内核开发非常重要，根据具体需求选择自旋锁、互斥锁、信号量或其他同步机制。

## rwlock举例

在 Linux 内核中，读写锁（Reader-Writer Lock）通常用于允许多个读操作同时进行，但只允许一个写操作进行的场景。下面是一个示例，演示如何在内核模块中使用读写锁：

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/rwlock.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Your Name");

static rwlock_t my_rwlock; // 声明读写锁变量

static int my_data = 0; // 共享资源

static int my_init(void) {
    printk(KERN_INFO "Reader-Writer Lock Example: Module init\n");

    // 初始化读写锁
    rwlock_init(&my_rwlock);

    // 读操作：多个线程可以同时进行读操作
    read_lock(&my_rwlock);
    printk(KERN_INFO "Read operation: Shared resource value is %d\n", my_data);
    read_unlock(&my_rwlock);

    // 写操作：只允许一个线程进行写操作
    write_lock(&my_rwlock);
    my_data++;
    printk(KERN_INFO "Write operation: Shared resource incremented to %d\n", my_data);
    write_unlock(&my_rwlock);

    return 0;
}

static void my_exit(void) {
    printk(KERN_INFO "Reader-Writer Lock Example: Module exit\n");
}

module_init(my_init);
module_exit(my_exit);
```

在这个示例中，首先使用`rwlock_init`初始化了读写锁`my_rwlock`。然后，在`my_init`函数中，使用`read_lock`进行读操作，允许多个线程同时进行读操作，然后使用`read_unlock`释放读锁。接下来，使用`write_lock`进行写操作，只允许一个线程进行写操作，然后使用`write_unlock`释放写锁。

读写锁允许多个线程同时进行读操作，但只允许一个线程进行写操作，这对于读多写少的场景非常有用。读写锁可以提高并发性，因为多个读操作可以同时进行而不会相互干扰。

需要注意的是，内核中的读写锁通常用于保护对共享资源的读和写操作，以确保数据的一致性和避免竞争条件。选择适当的同步机制对于内核开发非常重要，根据具体需求选择自旋锁、互斥锁、读写锁或其他同步机制。

# kernel workqueue和waitqueue的关系

内核中的 Workqueue 和 Wait Queue 是两个不同的概念，它们用于不同的目的，但在某些情况下可以相互关联，用于实现复杂的同步和异步操作。

1. **Workqueue**：

   - Workqueue 是 Linux 内核中的一种机制，用于在后台执行工作，而不阻塞当前执行线程。工作是一组任务或函数，它们可以异步执行，通常用于执行非实时和需要长时间处理的任务，以避免阻塞内核中的主线程。

   - Workqueue 通常使用工作队列（Work Queue）来组织和管理工作项。工作项是要执行的任务，它们被提交到工作队列，然后由工作队列线程异步执行。Workqueue 的使用有助于提高内核的响应性和性能，因为它避免了阻塞主线程。

2. **Wait Queue**：

   - Wait Queue 是一种同步机制，用于在内核中等待某个条件满足时被唤醒。通常，它与进程或线程的休眠和唤醒有关。当条件尚未满足时，线程可以通过 `wait_event` 等待在等待队列上，当条件满足时，其他线程可以通过 `wake_up` 唤醒等待的线程。

   - Wait Queue 通常用于实现同步原语，如信号量、互斥锁和条件变量。它们用于线程之间的协作，以等待某些事件的发生。

虽然 Workqueue 和 Wait Queue 是不同的机制，但它们可以在一些情况下相互关联，以实现更复杂的操作。例如，内核中的工作项可以与等待队列一起使用，以等待某些条件的发生，然后在条件满足时执行工作。这种情况下，Workqueue 可能会在某些条件满足时触发工作项的执行，从而唤醒等待队列上的线程。

总之，Workqueue 和 Wait Queue 都是内核中用于管理同步和异步操作的机制，它们有不同的用途，但在某些情况下可以结合使用，以实现复杂的内核任务。