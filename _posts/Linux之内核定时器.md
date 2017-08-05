---
title: Linux之内核定时器
date: 2017-08-03 23:33:27
tags:

	- Linux

---

# 1. 关于定时器

1、定时器是管理内核时间的基础。

2、依赖全局变量jiffies。是unsigned long类型。

3、定时器的注册函数是只执行一次的，不是循环执行的。

# 2. 使用定时器

1、定义一个定时器变量struct timer_list mytimer;

2、初始化定义的定时器变量。有好几个函数可以实现这个目的。一般我们用setup_timer。

3、增加定时器并且激活。用add_timer函数。

4、删除定时器，用del_timer函数。

5、修改定时器的超时时间，并启动。用mod_timer函数。

# 3. 一个示例

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





