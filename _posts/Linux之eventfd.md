---
title: Linux之eventfd
date: 2019-08-08 11:05:19
tags:
	- Linux

---

--

eventfd函数，用来创建一个用于做事件通知的文件描述符。

函数原型：

```
#include <sys/eventfd.h>
int eventfd(unsigned int initval, int flags);
参数1：
	initval。
参数2：
	flags。
	可能的取值：
	EFD_CLOEXEC
	EFD_NONBLOCK
	EFD_SEMAPHORE
	
返回值：
	一个文件描述符。
	针对这个fd，可以做的操作有：
	read
		返回的是一个uint64的证书。如果你给的buffer小于8字节，错误码会被设置为EINVAL
		返回的值，是host order的。
		读的行为，跟EFD_SEMAPHORE有关系。
		如果EFD_SEMAPHORE设置了，那么读到的值就是1，读完后，自动变为0 。
		如果EFD_SEMAPHORE没有设置，读取的是非零值，读完后，变成0 
		如果read的时候，发现值是0，则可能阻塞（如果EFD_NONBLOCK没有设置）。或者返回EAGIN（如果设置了EFD_NONBLOCK）。
	write
		也是写入8个字节的整数。
	poll/select操作
	close
```

是内核通知应用程序。

例子就看man手册里带的那个。

一般函数eventfd(0,0)。我们给2个参数传递0就好了。



类似eventfd的，还有一个timerfd。

这个的函数原型，有3个。

```
#include <sys/timerfd.h>

int timerfd_create(int clockid, int flags);

int timerfd_settime(int fd, int flags,
const struct itimerspec *new_value,
struct itimerspec *old_value);

int timerfd_gettime(int fd, struct itimerspec *curr_value);
```

内核的定时系统调用有：

setitimer

timer_create

timerfd_create跟他们的不同，在于可以跟select结合起来使用。



可以看到，eventfd实现的资源是一次性消耗品，只允许一次read。



# 用pipe来模拟eventfd

我看bluealsa里，有个这样的用法：

创建一个pipe：

```
	if (pipe(config.ctl.evt) == -1)
		goto fail;
	config.ctl.pfds[CTL_IDX_EVT].fd = config.ctl.evt[0];
```

这样写内容来触发事件：

```
int bluealsa_ctl_event(enum event event) {
	return write(config.ctl.evt[1], &event, sizeof(event));
}

```



# 参考资料

1、让事件飞 ——Linux eventfd 原理与实践

https://cloud.tencent.com/developer/article/1171508

2、man手册。

3、

https://blog.csdn.net/shuxiaogd/article/details/45914615