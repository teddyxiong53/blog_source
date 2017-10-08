---
title: CPU绑定技术
date: 2017-10-05 12:01:14
tags:
	- Linux

---



# 1. 概念

什么是CPU Affinity？Affinity是进程的一个属性。这个属性指明了调度器可以把这个进程指定到哪些CPU上。

在Linux中，我们可以利用CPU Affinity把进程和CPU之间建立多对多的绑定关系。

CPU Affinity分为两种：soft和hard。soft的建议是建议，不能保证一定可以调度达到预期。hard则可以保证。

为什么需要指定CPU Affinity呢？

1、增加CPU缓存的命中率。

CPU之间是不共享缓存的。如果进程在各个CPU之间频繁切换，需要不断地设置旧CPU的cache失效。这个肯定影响运行效率。另外，有多个进程是共享了很多的相同数据的，那么如果把这些进程指定到同一个CPU上，则也可以提高CPU缓存的命中率。

2、保证某一个进程的运行独占一个CPU。

这个是典型用法，这样这个进程就相当于一个很高的优先级。



# 2. 编码示例

函数原型是：

```
long sched_setaffinity(pid_t pid, const struct cpumask *in_mask)
```

in_mask这个跟select的fd_set比较类似。

针对线程级别的示例如下。

```
#define _GNU_SOURCE
#include <stdio.h>
#include <math.h>
#include <pthread.h>
cpu_set_t cpuset,cpuget;
double waste_time(long n)
{
	double res = 0;
	long i = 0;
	while (i <n * 200000000)
	{
		i++;
		res += sqrt(i);
	}
	return res;
}
void *thread_func(void *param)
{
	CPU_ZERO(&cpuset);
	CPU_SET(0, &cpuset); /* cpu 0 is in cpuset now */
	/* bind process to processor 0 */
	if (pthread_setaffinity_np(pthread_self(), sizeof(cpu_set_t), &cpuset) !=0)
	{
		perror("pthread_setaffinity_np");
	}
	printf("Core 0 is running!\n");
	/* waste some time so the work is visible with "top" */
	printf("result: %f\n", waste_time(5));
	pthread_exit(NULL);
}
int main(int argc, char *argv[])
{
	pthread_t my_thread;
	time_t startwtime, endwtime;
	startwtime = time (NULL);
	if (pthread_create(&my_thread, NULL, thread_func,NULL) != 0)
	{
		perror("pthread_create");
	}
	pthread_join(my_thread,NULL);
	endwtime = time (NULL);
	printf ("wall clock time = %d\n", (endwtime - startwtime));
	return 0;
}
```

运行上面的程序，打开Ubuntu的system monitor，可以看到运行期间，CPU0的占用率一直是100% 。





