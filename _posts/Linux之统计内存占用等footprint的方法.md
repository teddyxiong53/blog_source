---
title: Linux之统计内存占用等footprint的方法
date: 2021-08-12 19:34:33
tags:
	- Linux

---

--

要对比lvgl和qt的footprint信息。主要是内存和CPU的使用情况。

# 内存统计

统计指定进程的内存使用情况。怎么做是比较准确可靠的？

/proc/xx/status

xx表示对应多进程pid。

里面跟内存相关的部分

```
VmPeak:    30412 kB         
VmSize:    30412 kB         
VmLck:         0 kB         
VmPin:         0 kB         
VmHWM:      1532 kB         
VmRSS:      1532 kB         
RssAnon:             408 kB 
RssFile:            1124 kB 
RssShmem:              0 kB 
VmData:     1404 kB         
VmStk:       132 kB         
VmExe:      2784 kB         
VmLib:      1376 kB         
VmPTE:        72 kB         
VmPMD:         8 kB         
VmSwap:        0 kB         
```

/proc/xx/smaps



在ubuntu上，这个命令可以统计出不错的信息来。

```
ps -eo size,pid,user,command --sort -size | \
    awk '{ hr=$1/1024 ; printf("%13.2f Mb ",hr) } { for ( x=4 ; x<=NF ; x++ ) { printf("%s ",$x) } print "" }' |\
    cut -d "" -f2 | cut -d "-" -f1
```



exmap这个工具可以。

有一个内核模块。exmap.ko。需要插入这个模块，exmap工具才能工作。



vmstat这个工具怎么样？



## gnu time

这个工具不错。可以得出直观的结论。

至于内部的统计是否准确，就不得而知。

作为标准工具，应该不会错的离谱。

不过还是写几个简单的测试程序，来验证一下统计是否准确。

写个while(1)的看CPU占用率。是对的，接近100%。

写个malloc 1M的看内存统计。基本对的。

写个const数组1M的看data统计。这个是统计不出来。



## htop

htop就是通过解析该目录下的/proc/meminfo文件得到CPU的核数以及动态的使用情况。



VmRSS对应的值就是物理内存占用



## procrank

1、Vss
Vss与PS的VSIZE相同是单个进程全部可访问的地址空间
其大小包括可能还尚未在内存中驻留的部分。比如地址空间已经被 malloc 分配，但是还没有实际写入。
对于确定单个进程实际内存使用大小， VSS 用处不大。

2、Rss
RSS是单个进程实际占用的内存大小。
RSS易被误导的原因在于， 它包括了该进程所使用的所有共享库的全部内存大小。对于单个共享库， 尽管无论多少个进程使用，
实际该共享库只会被装入内存一次。
**对于单个进程的内存使用大小， RSS 不是一个精确的描述。**

3、Pss
**PSS 不同于RSS，它只是按比例包含其所使用的共享库大小。**
例如， 三个进程使用同一个占用 30 内存页的共享库。 对于三个进程中的任何一个，PSS 将只包括 10 个内存页。
PSS 是一个非常有用的数字，因为系统中全部进程以整体的方式被统计， 对于系统中的整体内存使用是一个很好的描述。
如果一个进程被终止， 其PSS 中所使用的共享库大小将会重新按比例分配给剩下的仍在运行并且仍在使用该共享库的进程。
此种计算方式有轻微的误差，因为当某个进程中止的时候，PSS没有精确的表示被返还给整个系统的内存大小。

4、Uss
USS 是单个进程的全部私有内存大小。亦即全部被该进程独占的内存大小。
USS 是一个非常非常有用的数字， 因为它揭示了运行一个特定进程的真实的内存增量大小。
如果进程被终止， USS 就是实际被返还给系统的内存大小。
USS 是针对某个进程开始有可疑内存泄露的情况，进行检测的最佳数字。

小结
VSS - Virtual Set Size 虚拟耗用内存（包含共享库占用的内存）
RSS - Resident Set Size 实际使用物理内存（包含共享库占用的内存）
PSS - Proportional Set Size 实际使用的物理内存（比例分配共享库占用的内存）
USS - Unique Set Size 进程独自占用的物理内存（不包含共享库占用的内存）

一般来说内存占用大小有如下规律：VSS >= RSS >= PSS >= USS


# 参考资料

1、

https://stackoverflow.com/questions/131303/how-can-i-measure-the-actual-memory-usage-of-an-application-or-process

2、

https://blog.csdn.net/qinzhonghello/article/details/4058532

3、Android内存分析之procrank命令

https://blog.csdn.net/qinhai1989/article/details/88112715