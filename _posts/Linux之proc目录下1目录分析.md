---
title: Linux之proc目录下1目录分析
date: 2018-01-28 09:07:44
tags:
	- Linux

---

1

# 进程目录

以init进程的为主，进行分析。进程id为1 。

```
auxv 
	这个是传递给进程的ELF解释器信息。
	可以用hexdump -x auxv来查看。
	128字节。
clear_refs
	只写。
	清除用于估算内存使用量的PG_Referenced和ACCESSED/YOUNG。
	可以写入1到4这4个值，表示4种不同的策略。
cmdline
	表示进程被启动的命令。
comm
	进程的名字。一个进程的不同的线程有不同的名字。
coredump_filter
	coredump过滤器。写入bitmap数据。
	表示不同的策略。
environ
	进程的环境变量。
	init进程的是这样：
	HOME=/ TERM=linux storagemedia=nand /proc/1
fd
	这个目录下，放了fd对应的文件名的情况。
	init进程下的是这样：
	lrwx------    1 root     root          64 Dec 12 14:29 0 -> /dev/console
	lrwx------    1 root     root          64 Dec 12 14:29 1 -> /dev/console
	lrwx------    1 root     root          64 Dec 12 14:29 2 -> /dev/console
	某个业务进程是这样：
	是后台运行的。
	/proc/1/fd # ls /proc/376/fd -lh                                                   
    lr-x------    1 root     root          64 Dec 12 14:29 0 -> /dev/null              
    lrwx------    1 root     root          64 Dec 12 14:29 1 -> /dev/console           
    lr-x------    1 root     root          64 Dec 12 14:29 10 -> pipe:[1293]           
    l-wx------    1 root     root          64 Dec 12 14:29 11 -> pipe:[1293]           
    lrwx------    1 root     root          64 Dec 12 14:29 12 -> anon_inode:[eventpoll]
    lrwx------    1 root     root          64 Dec 12 14:29 13 -> socket:[206519]       
    lr-x------    1 root     root          64 Dec 12 14:29 14 -> /dev/input/event1     
fdinfo
	也是个目录，包含fd的信息。
	文件都是只读的。
io
	嵌入式设备上没有这个。
	电脑上有。内容是io的字节数。
	rchar: 1745997628
    wchar: 1394133136
    syscr: 808933
    syscw: 515287
    read_bytes: 14208813056
    write_bytes: 1169547264
    cancelled_write_bytes: 20025344
limits
	就是ulimit操作的那些信息。
map_files
	mmap的一些文件情况。
	二进制文件、so文件。
maps
	映射的具体情况。
mem
	用来通过open、read/write来访问进程的内存页。
mountinfo
	挂载信息。
mounts
	挂载信息。
mountstat
	挂载信息。
ns/
	目录。namespace信息。
oom_adj
	默认为0，表示继承父进程的设置。
	谁的分数高，在oom的时候，优先杀掉谁。
oom_score
	分数。
	这个只读。要写入，写oom_score_adj。
oom_score_adj
	调整分析。范围-1000到1000 。
pagemap
	当前进程的虚拟内存映射情况。
	不能cat，是二进制的。
personality
	不知道具体什么用途。
root
	软链接。指向进程的根目录。
smaps
	内存映射文件。每一个区域的详细情况。
stat
	进程的详细状态。很多数字。
statm
	进程的内存统计。
status
	可读性好的stat。跟stat的内容是一致的，但是人可以理解。
syscall
	信息看不懂。
	反正就是系统调用相关。
task/
	就是本进程下的线程。init进程是单线程的，所以下面只有一个目录1 。
	而我另外那个376的业务进程。下面就有20来个文件夹。说明有这么的的线程。
	/proc/376/task/396 # cat comm 
	monitor_work_ro               
```







## 内存相关

proc下面的跟内存相关的文件

```
/proc/1/statm
/proc/1/maps
```

statm里面的内容是这样：

```
# init进程的
599 105 93 164 0 75 0
# 某个业务进程的
499103 6955 3653 28 0 492573 0
```

总共7个数字，他们的单位都是page（4KB），分别是：

```
1、size。虚拟空间地址大小。
2、resident。正在使用的物理内存大小。
3、shared。共享页数。
4、trs。程序所拥有的可执行的虚拟内存大小。
5、lrs。被映射到进程的虚拟地址空间的库的大小。
6、drs。进程的数据段和用户栈的大小。
7、脏页数量。
```

```
/proc/1 # cat maps
00400000-004a4000 r-xp 00000000 1f:06 3                 /bin/busybox
004b3000-004b4000 r--p 000a3000 1f:06 3                 /bin/busybox
004b4000-004b5000 rw-p 000a4000 1f:06 3                 /bin/busybox
004b5000-004b6000 rw-p 00000000 00:00 0
3f0b3000-3f0d4000 rw-p 00000000 00:00 0                 [heap]
7f84f17000-7f85048000 r-xp 00000000 1f:06 514              /lib/libc-2.26.so
7f85048000-7f85057000 ---p 00131000 1f:06 514              /lib/libc-2.26.so
7f85057000-7f8505b000 r--p 00130000 1f:06 514              /lib/libc-2.26.so
7f8505b000-7f8505d000 rw-p 00134000 1f:06 514              /lib/libc-2.26.so
7f8505d000-7f85061000 rw-p 00000000 00:00 0
7f85061000-7f8507e000 r-xp 00000000 1f:06 505              /lib/ld-2.26.so
7f85089000-7f8508b000 rw-p 00000000 00:00 0
7f8508b000-7f8508c000 r--p 00000000 00:00 0               [vvar]
7f8508c000-7f8508d000 r-xp 00000000 00:00 0               [vdso]
7f8508d000-7f8508e000 r--p 0001c000 1f:06 505              /lib/ld-2.26.so
7f8508e000-7f85090000 rw-p 0001d000 1f:06 505              /lib/ld-2.26.so
7fc11a9000-7fc11ca000 rw-p 00000000 00:00 0               [stack]
```



以一行的数据来分析。

```
00400000-004a4000 r-xp 00000000 1f:06 3                                  /bin/busybox   
```

有6列。

```
1、虚拟地址。
2、权限。r/w/x，读写执行。p表示private，s表示share。
3、偏移量。
4、映射文件的主设备号和次设备号。
	从/proc/devices里看到，主设备号是1f，就是十进制的31，对应的是rkflash。
	次设备号为6的，对应的是rootfs对应的分区。
5、文件的inode。
6、可执行文件的路径。
```



参考资料

1、

https://www.cnblogs.com/klb561/p/11062129.html

2、

https://my.oschina.net/victorlovecode/blog/344264?p={{currentPage-1}}

3、Linux /proc/$pid部分内容详解

https://www.cnblogs.com/likui360/p/6181927.html

4、Linux proc文件系统说明

https://blog.csdn.net/ZYC88888/article/details/80194088