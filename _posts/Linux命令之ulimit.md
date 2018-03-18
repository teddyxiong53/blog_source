---
title: Linux命令之ulimit
date: 2018-03-17 23:05:03
tags:
	- Linux命令

---



在树莓派上，查看：

```
pi@raspberrypi:~$ ulimit -a
core file size          (blocks, -c) 0  //core文件大小，默认是0，括号里的-c表示可以用ulimit -c来设置。
data seg size           (kbytes, -d) unlimited//数据段，无限大。
scheduling priority             (-e) 0  //调度优先级。默认是0
file size               (blocks, -f) unlimited //文件大小，无限大。
pending signals                 (-i) 7345 //
max locked memory       (kbytes, -l) 64    //最大锁定内存。64K？
max memory size         (kbytes, -m) unlimited //最大内存使用，无限大。
open files                      (-n) 65536 //最多打开65536个文件。
pipe size            (512 bytes, -p) 8  //
POSIX message queues     (bytes, -q) 819200 //mq尺寸。
real-time priority              (-r) 0   //实时优先级。
stack size              (kbytes, -s) 8192  //堆栈，默认8M。
cpu time               (seconds, -t) unlimited 
max user processes              (-u) 7345  //最大用户进程个数，7345个。
virtual memory          (kbytes, -v) unlimited 
file locks                      (-x) unlimited
```

