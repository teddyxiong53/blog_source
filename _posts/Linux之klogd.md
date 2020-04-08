---
title: Linux之klogd
date: 2018-04-03 21:43:50
tags:
	- Linux

---



# 什么是klogd

klogd是一个用来截获并记录内核消息的守护进程。

不运行也没有任何关系。我的mylinuxlab默认就没有运行。

在标准的linux系统上，klogd从/proc/kmsg里获取内容，再通过syslogd守护进程把它们保存到系统日志文件里。



```
start-stop-daemon -b -S -q -m -p /var/run/klogd.pid --exec /sbin/klogd -- -n
```

klogd默认是把内核打印转发给syslogd。所以可以从/var/log/messages里看到内核的打印。

Klogd的输出结果会传送给syslogd进行处理,syslogd会根据/etc/syslog.conf的配置把log，信息输出到/var/log/下的不同文件中。



klogd就是把printk打印的东西转发给syslogd。



# busybox里的klogd实现

先看帮助信息。

```
~ # klogd -h
klogd: invalid option -- 'h'
BusyBox v1.27.2 (2018-03-21 13:02:08 CST) multi-call binary.

Usage: klogd [-c N] [-n]

Kernel logger

        -c N    Print to console messages more urgent than prio N (1-8)
        -n      Run in foreground
```

可以有2个选项，-c指定日志级别。-n表示前台运行。

我现在的mylinuxlab里，输入klogd，就一直狂打印下面的内容，都没法停止。

```
EXT2-fs (mmcblk0): error: ext2_lookup: deleted inode referenced: 14500
EXT2-fs (mmcblk0): error: ext2_lookup: deleted inode referenced: 14500
EXT2-fs (mmcblk0): error: ext2_lookup: deleted inode referenced: 14500
EXT2-fs (mmcblk0): error: ext2_lookup: deleted inode referenced: 14500
EXT2-fs (mmcblk0): error: ext2_lookup: deleted inode referenced: 14500
```

我用`klogd -n`前台的方式运行，可以用ctrl+c的方式停掉。

cat /proc/kmsg输出内容也是一样的。



#printk的实现

```
printk
	vprintk
	在这个函数里，禁止调度，锁中断。还有spinlock。
```

对于printk来说，一共有2个缓冲区，printk_buf和log_buf。

printk_buf是临时的，log_buf用来存储要输出的字符串。

printk_time，这个变量是用来控制是否加上时间打印的。

printk_cpu_id，这个是看算法加上CPU号的打印的。

最后在console_unlock这个函数里，做了不少的事情。这个函数名字起得真不怎么样。

```
call_console_drivers
if (wake_klogd)
		wake_up_klogd();
```

console_unlock注释里写着：

```
may be called from any context.
```

内核的log buffer。就是这么定义的，一个全局的数组。挺大的。是环形处理的。

```
#define __LOG_BUF_LEN	(1 << CONFIG_LOG_BUF_SHIFT)//1<<17
static char __log_buf[__LOG_BUF_LEN] __nosavedata;
static char *log_buf = __log_buf;
```



# 参考资料

1、klogd

https://baike.baidu.com/item/klogd/13681310?fr=aladdin