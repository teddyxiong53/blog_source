---
title: Linux驱动之LDD3源代码分析
date: 2018-03-07 22:43:42
tags:
	- Linux

---



LDD3是本经典，但是翻译实在是读不下去。我直接看源代码。看书为辅。

LDD3是基于linux2.6的。比较老了。有人移植了相关例程到linux新版本上，最新已经支持到4.9了。

代码在这里。https://github.com/duxing2007/ldd3-examples-3.x

这个是更新的版本。

https://github.com/martinezjavier/ldd3

在ubuntu20.04上测试。插入会失败。

看dmesg。

```
[6218933.591005] Lockdown: insmod: unsigned module loading is restricted; see man kernel_lockdown.7
[6218951.737022] Lockdown: insmod: unsigned module loading is restricted; see man kernel_lockdown.7
[6218986.801836] Lockdown: insmod: unsigned module loading is restricted; see man kernel_lockdown.7
[6219370.083498] Lockdown: insmod: unsigned module loading is restricted; see man kernel_lockdown.7
```

需要这样处理一下

```
To get the module loading, disable kernel lockdown via sys-rq:

# echo 1 > /proc/sys/kernel/sysrq
# echo x > /proc/sysrq-trigger
```

也还是不行。



书的目录结构：

```
1、设备驱动简介
2、建立和运行模块。
3、字符驱动
	scull。实现了这些设备。
		1、scull0到scull3 。
		2、scullpipe0到scullpipe3.
		3、scullsingle
		4、scullpriv
		5、sculluid
		6、scullwuid
		
4、调试技术
	
5、并发
6、高级字符驱动
7、时间
8、分配内存。
9、操作硬件。
10、中断
11、内核里的数据类型。
12、PCI驱动。
13、usb
14、linux设备模型。
15、内存映射和dma
16、块设备。
17、网络驱动。
18、tty驱动。
```

代码和章节的对应关系。

```
.
├── Chapter 2
│   ├── hello.c：就是一个HelloWorld程序，init和exit函数。在misc-modules目录下。
│   └── hellop.c：加上了moduleparam。
├── Chapter 3
│   └── scull.c
├── Chapter 4
│   ├── faulty.c
│   ├── gdbline
│   ├── seq.c
│   ├── setconsole.c
│   └── setlevel.c
├── Chapter 5
│   └── complete.c
├── Chapter 6
│   ├── asynctest.c
│   ├── nbtest.c
│   ├── polltest.c
│   └── sleepy.c
├── Chapter 7
│   ├── jiq.c
│   ├── jit.c
│   └── load50.c
├── Chapter 8
│   └── scullc
│       ├── Makefile
│       ├── main.c
│       ├── mmap.c
│       ├── scullc.h
│       ├── scullc_load
│       └── scullc_unload
├── Chapter 9
│   ├── inp.c
│   ├── outp.c
│   └── silly.c
├── Chapter 10
│   ├── short
│   │   ├── Makefile
│   │   ├── short.c
│   │   ├── short_load
│   │   └── short_unload
│   └── shortprint
│       ├── Makefile
│       ├── shortprint.c
│       ├── shortprint.h
│       ├── shortprint_load
│       └── shortprint_unload
├── Chapter 11
│   ├── dataalign.c
│   ├── datasize.c
│   ├── kdataalign.c
│   └── kdatasize.c
├── Chapter 12
│   ├── pci
│   │   ├── Makefile
│   │   └── pci_skel.c
│   └── skull
│       ├── Makefile
│       ├── skull_clean.c
│       └── skull_init.c
├── Chapter 13
│   └── usb
│       ├── Makefile
│       ├── readme.txt
│       ├── test_with_g_zero.patch
│       └── usb-skeleton.c
├── Chapter 14
│   ├── lddbus
│   │   ├── Makefile
│   │   ├── lddbus.c
│   │   └── lddbus.h
│   └── sculld
│       ├── Makefile
│       ├── main.c
│       ├── mmap.c
│       ├── sculld.h
│       ├── sculld_load
│       └── sculld_unload
├── Chapter 15
│   ├── mapcmp.c
│   ├── mapper.c
│   ├── scullv
│   │   ├── Makefile
│   │   ├── main.c
│   │   ├── mmap.c
│   │   ├── scullv.h
│   │   ├── scullv_load
│   │   └── scullv_unload
│   ├── simple
│   │   ├── Makefile
│   │   ├── simple.c
│   │   ├── simple_load
│   │   └── simple_unload
│   └── scullp
│       ├── Makefile
│       ├── main.c
│       ├── mmap.c
│       ├── scullp.h
│       ├── scullp_load
│       └── scullp_unload
├── Chapter 16
│   └── sbull
│       ├── Makefile
│       ├── sbull.c
│       ├── sbull.h
│       ├── sbull_load
│       └── sbull_unload
├── Chapter 17
│   ├── netifdebug.c
│   └── snull
│       ├── Makefile
│       ├── snull.c
│       ├── snull.h
│       ├── snull_load
│       └── snull_unload
└── Chapter 18
    └── tty
        ├── Makefile
        ├── tiny_serial.c
        └── tiny_tty.c
```



# 环境准备

我是打算在我的树莓派上做实验的。

我的树莓派对应的源代码版本是4.14.y。

把scull文件夹拷贝到树莓派上。

```
pi@raspberrypi:~/test/ldd/scull$ make KERNELDIR=/home/pi/linux_src/linux-rpi-4.14.y
```

编译正常。

插入看看。

```
pi@raspberrypi:~/test/ldd/scull$ sudo ./scull_load 
pi@raspberrypi:~/test/ldd/scull$ lsmod
Module                  Size  Used by
scull                  24576  0 
```

也正常。

看看设备情况：

```
pi@raspberrypi:~/test/ldd/scull$ ls /dev/scull* -l
lrwxrwxrwx 1 root root        6 Mar 12 13:37 /dev/scull -> scull0
crw-rw-r-- 1 root staff 242,  0 Mar 12 13:37 /dev/scull0
crw-rw-r-- 1 root staff 242,  1 Mar 12 13:37 /dev/scull1
crw-rw-r-- 1 root staff 242,  2 Mar 12 13:37 /dev/scull2
crw-rw-r-- 1 root staff 242,  3 Mar 12 13:37 /dev/scull3
lrwxrwxrwx 1 root root       10 Mar 12 13:37 /dev/scullpipe -> scullpipe0
crw-rw-r-- 1 root staff 242,  4 Mar 12 13:37 /dev/scullpipe0
crw-rw-r-- 1 root staff 242,  5 Mar 12 13:37 /dev/scullpipe1
crw-rw-r-- 1 root staff 242,  6 Mar 12 13:37 /dev/scullpipe2
crw-rw-r-- 1 root staff 242,  7 Mar 12 13:37 /dev/scullpipe3
crw-rw-r-- 1 root staff 242, 11 Mar 12 13:37 /dev/scullpriv
crw-rw-r-- 1 root staff 242,  8 Mar 12 13:37 /dev/scullsingle
crw-rw-r-- 1 root staff 242,  9 Mar 12 13:37 /dev/sculluid
crw-rw-r-- 1 root staff 242, 10 Mar 12 13:37 /dev/scullwuid
```

就这个驱动就生成了这么多的设备。

我们看看源代码。

先看看目录构成：

```
pi@raspberrypi:~/test/ldd/scull$ tree
.
├── access.c：user access的意思。具体怎么用不知，要先看懂才知道。
├── main.c：module_init在这里定义。
├── Makefile
├── pipe.c：定义对应的pipe设备。
├── scull.h：定义scull_dev结构体等。
├── scull.init：
├── scull_load：加载驱动的脚本。
└── scull_unload
```

先把加载驱动的脚本scull_load看一遍。

```
1、定义变量device和module，都是scull。定义权限为644 。
2、insmod。
3、从/proc/devices里取得major为242 。
4、删除/dev/scull*设备。
5、mknod /dev/scull0到3，minor依次为0到3，建立软链接，让/dev/scull指向/dev/scull0
6、建立scullpipe设备。minor为4到7
7、建立single、uid、wuid、priv这4个设备。minor为8到11 。
```

测试设备的读写。

我试了一下，用sudo都不行，一定要切换到root用户，才能进行读写操作。

```
# ls > /dev/scull
# cat /dev/scull
```

pipe则是：

```
cat /dev/scullpipe
卡住。
```

另外开一个窗口，

```
echo "123" > /dev/scullpipe
```



# 按章节来看代码

为了加快测试速度，我还是在我的虚拟机里运行。

但是有个错误。就是linux/sched/signal.h这个头文件在我的虚拟机里不存在。我要把文件里的这一行注释掉就好了。



1、hello。

insmod，看dmesg。

```
[63655.636880] hello: module verification failed: signature and/or required key missing - tainting kernel
[63655.638111] Hello, world
```

签名错误不管。

2、hellop。

输入：

```
sudo insmod ./hellop.ko whom=teddy howmany=3
```

得到：

```
[63915.354825] (0) Hello, teddy
[63915.354842] (1) Hello, teddy
[63915.354861] (2) Hello, teddy
```

3、faulty。

这个是故意在驱动里加一个写空指针的语句。

```
测试方法：
insmod faulty.ko
cat /proc/devices # 查看主设备号是多少
mknod -m 644 /dev/faulty c 244 0 # 上一步看到主设备号是244
cat /dev/faulty # 这样可以进行读取。
echo 1 > /dev/faulty # 这个会挂掉。因为write函数里直接写空指针。
```

dmesg看到的信息：

```
[101943.290727] BUG: unable to handle kernel NULL pointer dereference at           (null)
[101943.290856] IP: faulty_write+0x8/0x20 [faulty]
[101943.290939] PGD 800000008a272067 
[101943.290940] P4D 800000008a272067 
[101943.291020] PUD 4f64c067 
[101943.291124] PMD 0 
```



4、seq。

这个是演示通过seq来输出内容到用户空间。

你可以cat /proc/sequence来输出。是连续输出整数的效果。

5、complete。

这个是用一个complete来同步自己对自己的读写。

6、scullc。c表示cache。基于缓存的scull设备。

把kmalloc改成了kmem_cache_alloc

7、scullp。p代表page，表示使用整页内存的。

用`__get_free_pages`来分配内存。

8、short。这个是演示中断的。short是缩写。Simple Hardware Operations and Raw Tests

用的是串口的例子。

9、lddbus。为了讲解设备驱动模型。

新建了一种虚拟总线。这个值得仔细看看。

10、sculld。挂在lddbus上的scull设备。

11、scullv。v表示使用虚拟地址。

12、snull。网络设备。

# scull

scullpipe，这个才有阻塞的读和写。算是比较实用的。

开2个shell参考，一个cat /dev/scullpipe0 ，另外一个echo 123 > /dev/scullpipe0.

dmesg查看得到：

```
[106110.555422] scull: "cat" reading: going to sleep
[106120.494907] scull: Going to accept 4 bytes to ffff8970d9d40000 from 00000000006c21e0
[106120.494924] scull: "zsh" did write 4 bytes
[106120.494979] scull: "cat" did read 4 bytes
[106120.495004] scull: "cat" reading: going to sleep
```





# jit

jit是just in time模块的意思。

在misc-modules目录下。

插入模块：

```
sudo insmod ./jit.ko
```

产生了这些proc节点：

```
hlxiong@hlxiong-VirtualBox:/proc$ ls jit* -lh
-r--r--r-- 1 root root 0 12月  7 16:25 jitasklet
-r--r--r-- 1 root root 0 12月  7 16:25 jitasklethi
-r--r--r-- 1 root root 0 12月  7 16:25 jitbusy
-r--r--r-- 1 root root 0 12月  7 16:25 jitimer
-r--r--r-- 1 root root 0 12月  7 16:25 jitqueue
-r--r--r-- 1 root root 0 12月  7 16:25 jitsched
-r--r--r-- 1 root root 0 12月  7 16:25 jitschedto
```

还有一个currentime

```
hlxiong@hlxiong-VirtualBox:/proc$ cat currentime 
0x106d345ab 0x0000000106d345ab 1575707177.097970
                              1575707177.092723152
```

依次是：jiffies、64位的jiffies、timeval、timespec。

# complete

这个是用来演示complete的用法的。

先插入模块：

```
sudo insmod ./complete.ko
```

查看/proc/devices，看到分配到的设备号是244 。

然后创建设备节点：

```
sudo mknod c /dev/complete 244 0
```

一个shell窗口：

```
cat /dev/complete
```

会阻塞住。按ctrl+C都无法停止的。

另外开一个shell窗口：

```
su root # 需要切换到root用户采用权限。
echo "123" > /dev/complete
```

这个时候，cat命令执行完。

查看dmesg：

```
[459639.868842] process 31585 (cat) going to sleep
[459669.054363] process 31594 (echo) awakening the readers...
[459669.054372] awoken 31585 (cat)
```

dmesg里的pid和命令名字，是这样获取到的：

```
current->pid, current->comm
```

整个代码很简单。

```
定义一个complete：
DECLARE_COMPLETION(comp);
等待：
wait_for_completion(&comp);
发送：
complete(&comp);
```

# faulty

这个是用来演示错误的。

在write函数里，故意对指向NULL的指针进行写操作。

```
ssize_t faulty_write (struct file *filp, const char __user *buf, size_t count,
		loff_t *pos)
{
	/* make a simple fault by dereferencing a NULL pointer */
	*(int *)0 = 0;
	return 0;
}
```



# hellop

这个是演示模块参数传递的。

```
hlxiong@hlxiong-VirtualBox:~/work/test/ldd3/ldd3-examples-3.x/misc-modules$ sudo insmod ./hellop.ko 
hlxiong@hlxiong-VirtualBox:~/work/test/ldd3/ldd3-examples-3.x/misc-modules$ dmesg
[460725.310139] (0) Hello, world
```

带上参数：

```
sudo insmod ./hellop.ko howmany=10 whom=teddy
dmesg
[460833.250284] (0) Hello, teddy
[460833.250289] (1) Hello, teddy
[460833.250291] (2) Hello, teddy
[460833.250293] (3) Hello, teddy
[460833.250295] (4) Hello, teddy
[460833.250297] (5) Hello, teddy
[460833.250299] (6) Hello, teddy
[460833.250301] (7) Hello, teddy
[460833.250303] (8) Hello, teddy
[460833.250305] (9) Hello, teddy
```

# jiq

jiq是just in queue的意思。



# snull

这是一个net device的示例。

先看看使用。

```
sudo insmod ./snullko
```

这样会产生2个网卡，sn0和sn1。

我们用ifconfig给这2个网络配置地址。

```
sudo ifconfig sn0 192.168.1.10/24
sudo ifconfig sn1 192.168.1.20/24
```

可以ping通。

这里需要看一下书上的描述，因为这个环境准备相对来说麻烦一点。



# sbull

这个是块设备驱动的演示。

sbull_load脚本，需要修改一下。insmod那里。不要用-f参数。直接insmod就好。

不然insmod会失败。

