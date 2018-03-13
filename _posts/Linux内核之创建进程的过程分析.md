---
title: Linux内核之创建进程的过程分析
date: 2018-03-13 16:54:09
tags:
	- Linux内核

---



fork函数分析。

对应arch/arm/kernel/sys_arm.c里的sys_fork。里面实际就是调用了do_fork。

类似的函数还有：

```
sys_fork
	do_fork(SIGCHLD
sys_clone
	do_fork(clone_flags,
sys_vfork
	do_fork(CLONE_VFORK | CLONE_VM | SIGCHLD
```



do_fork在kernel/fork.c里。

```
do_fork
	copy_process//复制进程描述符，返回创建的task_struct指针。
		p = dup_task_struct(current);
	get_task_pid。
	//如果是vfork，用complete来保证父进程后执行。
	wake_up_new_task(p);//把子进程加入到调度器队列，使得子进程由机会运行。
	
```





# 参考文章

1、分析Linux内核创建一个新进程的过程

https://www.cnblogs.com/Nancy5104/p/5338062.html