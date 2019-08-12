---
title: Linux之时间系统
date: 2019-06-20 14:23:37
tags:
	- Linux
---

1

什么是单调递增时钟？



Linux下写应用，有时候需要使用高精度的时间间隔，例如定时100ms。

应该用哪个函数来达到这个目的呢？

time

```
这个函数是从1970年开始算的秒数，精度不够。
不符合我们的需求。
```

gettimeofday

```
这个精度可以到us。
精度是够了。
但是如果ntp时间发生了跳变，那么会出问题的。所以也不符合需求。
```

clock_gettime

```
CLOCK_MONOTONIC
	单调递增时间。
	这个表示系统开机后的秒数和纳秒数。
	ntp调整时间会影响它，所以不是真正的单调递增。
CLOCK_MONOTONIC_RAW
	这个是真正的单调递增时间。不受ntp时间调整的影响。
```





参考资料

1、Linux系统下的单调时间函数

https://blog.csdn.net/sollor525/article/details/74202550