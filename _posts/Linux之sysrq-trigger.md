---
title: Linux之sysrq-trigger
date: 2021-12-16 14:45:11
tags:
	- Linux

---

--

通过这样来控制

```
echo x > /proc/sysrq-trigger
```

x的取值可以是这些：

```
b：马上重启
o：马上关闭
m：导出内存分配信息，在/var/log/message里查看
c：故意让系统崩溃。这个常用。
```

在内核的sysrq.c里。

还可以用来查内存泄漏相关的问题。

查看帮助信息

```
echo h > /proc/sysrq-trigger

loglevel(0-9) 
reboot(b) 
crash(c) 
terminate-all-tasks(e) 
memory-full-oom-kill(f) 
kill-all-tasks(i) 
thaw-filesystems(j) 
sak(k) 
show-backtrace-all-active-cpus(l) 
show-memory-usage(m) 
nice-all-RT-tasks(n) 
poweroff(o) 
show-registers(p) 
show-all-timers(q) 
unraw(r) 
sync(s) 
show-task-states(t) 
unmount(u) 
show-blocked-tasks(w) 
dis intr to trigger wdt rst(x) 
dump-ftrace-buffer(z) 
```



参考资料

1、/proc/sysrq-trigger详解

https://blog.csdn.net/beckdon/article/details/41313713

2、/proc/sysrq-trigger说明

https://blog.csdn.net/silenttung/article/details/8084136