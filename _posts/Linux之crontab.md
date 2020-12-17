---
title: Linux之crontab
date: 2017-08-02 23:44:24
tags:

	- Linux

---

Linux里的定时任务要靠crontab来做。这个表格由crond这个守护进程来负责解析执行。

crontab里的条目的格式分为6段：

A B C D E F。

A：分钟。

B：小时。

C：Day。

D：Month

E：星期几。

F：执行的命令或者脚本。

执行的最小间隔是1分钟。



下面是一些常用的例子。

1、每分钟执行一次：

```
* * * * * cmd
```

用crontab命令来添加新的定时任务。

crontab -e，这样会打开编辑器，你进行编辑就好。

crontab -l，查看当前用户的定时任务。

