---
title: Linux内核之进程（一）
date: 2018-03-29 16:12:19
tags:
	- Linux内核

---



先对比一下2.6.35和4.4的task_struct。看看有什么改动。

1、smp新增了一些成员。

```
struct llist_node wake_entry;
	int on_cpu;//这个都有。其余是新增。
	unsigned int wakee_flips;
	unsigned long wakee_flip_decay_ts;
	struct task_struct *last_wakee;

	int wake_cpu;
```

2、cgroup的新增。

```
#ifdef CONFIG_CGROUP_SCHED
	struct task_group *sched_task_group;
#endif
```

3、task state这里的位域变量，增加了几个。







