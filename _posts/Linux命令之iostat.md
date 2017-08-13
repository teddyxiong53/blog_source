---
title: Linux命令# 之iostat
date: 2017-08-11 23:32:10
tags:

	- Linux命令

---

iostat可以统计当前系统读写磁盘等的状态，在调试性能的时候，是非常有用的工具。

# 1. iostat基本使用

```
teddy@teddy-ubuntu:~$ iostat
Linux 4.2.0-16-generic (teddy-ubuntu)   2017年08月11日  _i686_  (4 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           0.16    0.02    0.28    1.47    0.00   98.07

Device:            tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
sda              18.65       166.85        13.68     783143      64196
```

分析上面的内容：

总共分为3大部分

1、系统信息。就第一行。

2、cpu信息。第2、3行。

3、磁盘信息。第4、5行。

# 2. 加一点高级选项

```
teddy@teddy-ubuntu:~$ iostat -k -d 1 3
Linux 4.2.0-16-generic (teddy-ubuntu)   2017年08月11日  _i686_  (4 CPU)

Device:            tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
sda              18.13       162.16        13.30     783155      64244

Device:            tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
sda               0.00         0.00         0.00          0          0

Device:            tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
sda               0.00         0.00         0.00          0          0
```

上面命令加了-k、-d、1、3这4个选项或者参数。含义如下：

-k：以KB为单位。

-d：别打印cpu信息了。

1：每秒打印一次。

3：打印3次。

tps表示times per second，一秒里有几次读写。

从上面看，第一次的数据比较大，它表示的是从Linux系统启动到目前的统计平均值。



