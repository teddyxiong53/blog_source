---
title: rt-thread（十九）pipe分析
date: 2018-02-13 15:21:37
tags:
	- rt-thread

---



 之前一直没有看rt-thread的pipe。因为没有看到哪个模块用到这个东西。现在看mqtt的代码。发现有用到这个，所以就分析一下。

pipe还同时涉及了ringbuffer。

pipe是一个device。

对应的dev的open是rt_ringbuffer_create，对应的close是rt_ringbuffer_destroy。

read、write都是对这个ringbuffer进行操作。

除了rt_device的一套open/close/read/write接口。rt_device还包括了dfs_fs_ops的一套open/close/read/write。



入口函数是pipe(int fd[2])，有个static的pipeno，每次调用这个接口，这个值就加1.

然后得到/dev/pipe0这种名字的设备。

对这个设备打开两次，一次只读、一次只写。



