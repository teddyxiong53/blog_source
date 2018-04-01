---
title: Linux内核之时间子系统（一）
date: 2018-03-31 22:48:01
tags:
	- Linux内核
---



Linux内核的时间子系统主要是围绕低精度定时器和基于它的tick时钟周期来展开的。

但是随着Linux在嵌入式方向的发展，引入了2个新的功能：

1、高精度时钟。hr_timer。为了更加精准的定时。

2、tickless系统。这个是为了低功耗。



硬件层，我们用armv8架构的情况来分析。

在armv8上，对应的模块是arm generic timer。

这个模块有这些特点：

1、System Counter。全局共享。

2、Timer。每个核心有一个。

3、Virtual Counter。这个不关注。



GMT时间：我们日常用的。因为地球的自转在变慢。

UTC时间：为了让UTC时间跟GMT保持一致，需要设置闰秒。



linux里的时间起点是1970年1月1日0时0分0秒。

# 代码文件

时间子系统的文件在kernel/time目录下，文件及对应的作用如下：

| 文件名                                      | 描述                                       |
| ---------------------------------------- | ---------------------------------------- |
| time.c、timeconv.c                        | time.c是用来向用户提供api的文件。例如stime、gettimeofday。timeconv提供了时间转换的工具函数。 |
| timer.c                                  | 低精度定时器。timer_init、modify_timer这些函数。      |
| time_list.c、timer_status.c               | 向用户空间提供的调试API。用户空间可以用/proc/timer_list、/proc/timer_stats来查看。 |
| hrtimer.c                                | 高精度定时器。                                  |
| itimer.c                                 | 内部定时器。                                   |
| posix-timer.c、posix-cpu-timers.c、posix-clock.c |                                          |
| ...                                      |                                          |
|                                          |                                          |
|                                          |                                          |
|                                          |                                          |
|                                          |                                          |
|                                          |                                          |
|                                          |                                          |
|                                          |                                          |
|                                          |                                          |
|                                          |                                          |
|                                          |                                          |
|                                          |                                          |
|                                          |                                          |
|                                          |                                          |

# 用户API

站在App的角度，内核要提供的和时间相关的服务有：

1、和系统时间相关的服务。例如记录时间戳。

2、让进程sleep。

3、和定时器相关的任务。



## 秒级别的函数

```
#include <time.h>
time_t time(time_t *t);//从1970年来的秒数。
int stime(time_t *t);//设置时间。
```

## 微秒级别的函数

```
#include <sys/time.h>
int gettimeofday(struct timeval *tv, struct timezone *tz);
int settimeofday(struct timeval *tv, struc timezone *tz);
```

tz参数是历史遗留，内核并没有对时区进行支持。

## 纳秒级别的函数

```
#include <time.h>
int clock_gettime(clockid_t clk_id, struct timespec *tp);
int clock_settime(clockid_t clk_id, struct timespec *tp);
```

clockid_t的取值有这些：

```
CLOCK_REALTIME//这个表示是墙上时钟。大家最习惯的那个时间。
clock_monotonic
clock_monotoinc_raw
clock_process_cputime_id
clock_thread_cputime_id
```

## 进程睡眠函数

也分为秒级、微秒级、纳秒级。

```
#include <unistd.h>
unsigned int sleep(unsigned int seconds);
unsigned int usleep(useconds_t usec);//比较老了。不建议用。建议用nanosleep。
```

```
#include <time.h>
int nanosleep(const struct timespec *req, struct timespec *rem);
```

## 和定时器相关的函数

1、alarm函数。

2、内部定时器函数。

3、更高级的定时器函数。

# timekeeping

timekeeping是一个提供时间服务的基础模块。



# mini2440里的bsp代码

调用流程。

```
start_kernel
	time_init
		只调用了machine_desc->init_time()
		就是mini2440_init_time
			s3c2440_init_clocks(12000000);
				s3c2410_common_clk_init(NULL, xtal, 1, S3C24XX_VA_CLKPWR);
					ctx = samsung_clk_init(np, reg_base, NR_CLKS);
					s3c2410_common_clk_register_fixed_ext(ctx, xti_f);
					samsung_clk_register_pll
					samsung_clk_register_mux
					samsung_clk_register_div
					samsung_clk_register_gate
					samsung_clk_register_alias
					s3c2410_clk_sleep_init
```



# 参考资料

1、 Linux时间子系统(一) -- 原理

https://blog.csdn.net/flaoter/article/details/77413163

2、Linux时间子系统之（一）：时间的基本概念

这个是一个系列，有14篇文章。

http://www.wowotech.net/timer_subsystem/time_concept.html