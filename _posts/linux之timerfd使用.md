---
title: linux之timerfd使用
date: 2019-02-23 17:11:17
tags:
	- Linux

---



是Linux为用户态程序提供的接口。基于文件描述符进行操作。

主要用于select和poll。

timerfd是Linux为用户程序提供的一个定时器接口。这个接口基于文件描述符，通过文件描述符的可读事件进行超时通知，因此可以配合select/poll/epoll等使用。



我在看muduo的代码里看到这个东西。所以了解一下。

主要有3个接口。

```
timerfd_create
timerfd_settime
timerfd_gettime
```

## timerfd_create

```
原型：
	int timerfd_create(int clockid, int flags);
参数1：
	clockid：
		CLOCK_MONOTONIC 
			单调时间。是相对时间，表示从系统开机以来的时间。
			所以是单调递增的一个数。
			修改系统时间，对这个没有影响。
		CLOCK_REALTIME
			这个是真实时间。从1970以来的时间值。修改系统时间，对这个有影响。
			这个时间不是单调递增的，ntp同步等操作，都会导致时间发生变化。
参数2：
	flags
		TFD_NONBLOCK
		TFD_CLOEXEC
			一般我们都把这2个标志都写上。
返回值：
	一个fd。
```

## timerfd_settime

```
原型：
	int timerfd_settime(int fd, int flags, const struct itimerspec *new_value, struct itimerspec *old_value);
参数1：
	fd：就是timerfd_create得到的返回值。
参数2：
	flags：
		0表示相对时间，1表示绝对时间。
		1是TFD_TIMER_ABSTIME 。
参数3：
	new_value：表示超时时间和间隔（这个结构体里有2个timespec）。
		struct itimerspec {
            struct timespec it_interval;//这个不为0，则表示循环触发。
            struct timespec it_value;//这个是触发的时间点。
        };
        如果2个timespec都是0，表示停止定时器。
参数4：
	old_value：经常是设置为NULL.
```

## timerfd_settime

```
原型：
	int timerfd_gettime(int fd, struct itimerspec *curr_value);
参数1：
	fd。
参数2：
	
作用：
	得到距离下次超时的时间间隔。
```



对timerfd的fd的操作，可以进行read。

```
uint64_t expire_times = 0;
read(fd, &expire_times, sizeof(uint64_t));
```

read得到的值，表示这个定时器超时的次数。



下面看timerfd配合epoll的例子。

```

```





参考资料

1、linux新定时器：timefd及相关操作函数

https://www.cnblogs.com/mickole/p/3261879.html

2、linux timerfd系列函数总结

https://www.cnblogs.com/wenqiang/p/6698371.html

3、CLOCK_MONOTONIC与CLOCK_REALTIME区别

https://www.jianshu.com/p/1861a844a2fb