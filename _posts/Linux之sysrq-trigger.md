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

参考资料

1、/proc/sysrq-trigger详解

https://blog.csdn.net/beckdon/article/details/41313713