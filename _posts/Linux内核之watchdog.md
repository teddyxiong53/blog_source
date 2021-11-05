---
title: Linux内核之watchdog
date: 2021-11-04 19:46:17
tags:
	- Linux内核

---

--

内核的watchdog是在kernel/watchdog.c里。

注释里写着：

```
Detect hard and soft lockups on a system
```

lockup_detector_init 在内核init的后面部分调用。

```
CONFIG_WATCHDOG=y
CONFIG_WATCHDOG_CORE=y
```

```
watchdog_enable_all_cpus
	smpboot_register_percpu_thread_cpumask
		给每一个cpu核心创建一个内核线程。
		
```

传递给线程的数据是这样的：

```
static struct smp_hotplug_thread watchdog_threads = {
	.store			= &softlockup_watchdog,
	.thread_should_run	= watchdog_should_run,
	.thread_fn		= watchdog,
	.thread_comm		= "watchdog/%u",
	.setup			= watchdog_enable,
	.cleanup		= watchdog_cleanup,
	.park			= watchdog_disable,
	.unpark			= watchdog_enable,
};
```

这个跟硬件的watchdog怎么配合呢？



参考资料

1、

https://blog.csdn.net/yhb1047818384/article/details/70833825