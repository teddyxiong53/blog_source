---
title: Linux内核之select实现原理
date: 2018-03-26 13:22:33
tags:
	- Linux内核

---



代码调用流程是这样：

```
SYSCALL_DEFINE5(select //在fs/select.c里。
	core_sys_select
		get_fd_set(n, inp, fds.in)) //这里面就是一个copy_from_user。所以说select效率低。
		do_select
			poll_initwait
			
```



select的一种用法分析

看libemqtt里，sub.c里。

```
fd_set readfds;
struct timeval tmv;

// Initialize the file descriptor set
FD_ZERO (&readfds);
FD_SET (socket_id, &readfds);

// Initialize the timeout data structure
tmv.tv_sec = timeout;
tmv.tv_usec = 0;

// select returns 0 if timeout, 1 if input available, -1 if error
if(select(1, &readfds, NULL, NULL, &tmv))
return -2;
```

这里不同普通用法的地方：

1、select的第一个参数，nfds。为什么给1也可以？因为现在只监听一个fd，就是read的。这个没有疑问。

2、第二点就是返回值的判断，为什么返回非0值，就返回错误值呢？大于0不是正常值吗？而0值，不是超时了吗？不过这个超时也无所谓，因为下面还有一个recv在阻塞接收，那么问题来了，这个select意义何在？

而且超时时间是1秒，为什么这1秒内就是没有接收到东西呢？

不是，第一点和第二点要一起看，nfds为1，就注定select的返回值不可能大于0 。

这种用法也是醉了。实际效果等于延时1秒。







