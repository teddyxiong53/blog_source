---
title: Linux之内核栈
date: 2020-07-17 13:29:51
tags:
	- Linux

---

1

一个用户态进程/线程在内核中都是用一个task_struct的实例描述的，这个有点类似设计模式里面的桥接模式(handle-body), 用户态看到的进程PID，线程TID都是handle, task_struct是body。

用户空间的堆栈，在task_struct->mm->vm_area里面描述，都是属于进程虚拟地址空间的一个区域。

而内核态的栈在task_struct->stack里面描述，**其底部是thread_info对象**，thread_info可以用来快速获取task_struct对象。**整个stack区域一般只有一个内存页(可配置)，32位机器也就是4KB。**

所以说，一个进程的内核栈，也是进程私有的，只是在task_struct->stack里面获取。



参考资料

1、怎么理解linux内核栈？

https://www.zhihu.com/question/57013926

