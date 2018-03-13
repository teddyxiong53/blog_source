---
title: Linux内核之内存之mm_struct
date: 2018-03-13 15:59:10
tags:
	- Linux

---



每个进程自己的虚拟地址空间，都是通过一个mm_struct的结构体来进行描述。

1、每个进程都有一个task_struct来描述。

2、task_struct里有一个mm_struct。

在内核的start_kernel里，有这样的语句：

```
mm_init_owner(&init_mm, &init_task);
init_mm就是内核看到的虚拟内存布局。
init_task就是第一个task_struct。
```



