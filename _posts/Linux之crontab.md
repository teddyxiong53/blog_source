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

记忆就是”分时日月星“。



执行的最小间隔是1分钟。



下面是一些常用的例子。

1、每分钟执行一次：

```
* * * * * cmd
```

用crontab命令来添加新的定时任务。

crontab -e，这样会打开编辑器，你进行编辑就好。

crontab -l，查看当前用户的定时任务。



这样指定定时任务文件

```
crontab ${JD_DIR}/config/crontab.list
```

修改了文件里的内容，重新执行一下上面一行命令，就可以重新载入任务。



# 任务没有执行

我加的任务，感觉没有执行，手动执行命令是没有错误的。

但是定时没有执行效果。应该怎么调试定时任务呢？

查看日志是/var/log/cron.log

默认没有这个文件。

ubuntu默认没有开启cron日志

> :sudo nano /etc/rsyslog.d/50-default.conf

把cron对应的那一行注释打开。

重启syslog。

```
sudo service rsyslog restart
```

随便往crontab -e里写一个每分钟执行的任务。

然后看日志。的确有执行。

我的任务也有执行。

那么可能就是长期cron生效了。



# 参考资料

1、

https://blog.csdn.net/wuqi5328/article/details/101674718