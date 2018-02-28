---
title: Linux驱动之常用头文件
date: 2018-02-28 12:42:45
tags:
	- Linux驱动

---



```
<linux/module.h>：定义了EXPORT_SYMBOL等宏。HelloWorld的驱动只需要包含这个就够了。
<linux/fs.h>：定义了inode、file、file_operations、inode_operations等结构体。
<linux/errno.h>：错误码。
<linux/types.h>：定了dev_t等xx_t数据类型。
<linux/cdev.h>：cdev结构体和接口。40行左右。
<linux/wait.h>：定义了wait_queue_head_t和相关函数。
<linux/init.h>：定义了__init等宏。
<linux/kernel.h>：各种print、trace。
<linux/slab.h>：kmalloc、kmem_cache_create等接口。
<linux/uaccess.h>：copy_from_user等接口。
<linux/device.h>：device、driver等结构体定义。
<linux/io.h>：ioremap等函数。
<linux/miscdevic.h>：miscdev定义。60行左右。
<linux/interrupt.h>：tasklet和中断。
<linux/bitops.h>：set_bit等函数。
<linux/semaphore.h>：50行左右。
<linux/sched.h>：
<linux/kfifo.h>：环形队列。
<linux/timer.h>：timer_list相关操作。200行。
<linux/input.h>：
<linux/delay.h>：msleep、ndelay等。
```



