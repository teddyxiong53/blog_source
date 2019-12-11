---
title: Linux驱动之LDD3源代码分析
date: 2018-03-07 22:43:42
tags:
	- Linux

---



LDD3是本经典，但是翻译实在是读不下去。我直接看源代码。看书为辅。

LDD3是基于linux2.6的。比较老了。有人移植了相关例程到linux新版本上，最新已经支持到4.9了。

代码在这里。https://github.com/duxing2007/ldd3-examples-3.x

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

还是创建节点，对设备节点进行echo操作。

查看dmesg。

```
[460514.119114] BUG: unable to handle kernel NULL pointer dereference at           (null)
[460514.119384] IP: faulty_write+0x8/0x20 [faulty]
[460514.119528] PGD 8000000011189067 
[460514.119530] P4D 8000000011189067 
[460514.119755] PUD b53a8067 
[460514.119868] PMD 0 

[460514.120229] Oops: 0002 [#1] SMP PTI
[460514.120342] Modules linked in: faulty(OE) xt_nat xt_tcpudp veth ipt_MASQUERADE nf_nat_masquerade_ipv4 xfrm_user xfrm_algo iptable_nat nf_conntrack_ipv4 nf_defrag_ipv4 nf_nat_ipv4 xt_addrtype iptable_filter ip_tables xt_conntrack x_tables nf_nat br_netfilter bridge stp llc overlay aufs cfg80211 nf_conntrack_netlink vboxsf(OE) nf_conntrack libcrc32c nfnetlink binfmt_misc crct10dif_pclmul crc32_pclmul ghash_clmulni_intel pcbc snd_intel8x0 snd_ac97_codec ac97_bus aesni_intel aes_x86_64 crypto_simd glue_helper cryptd joydev snd_pcm snd_seq_midi snd_seq_midi_event snd_rawmidi snd_seq snd_seq_device snd_timer snd vboxvideo(OE) soundcore input_leds intel_rapl_perf ttm serio_raw i2c_piix4 drm_kms_helper vboxguest(OE) drm fb_sys_fops syscopyarea sysfillrect sysimgblt mac_hid ib_iser rdma_cm iw_cm ib_cm ib_core
[460514.121650]  iscsi_tcp libiscsi_tcp libiscsi scsi_transport_iscsi parport_pc ppdev lp parport nfsd auth_rpcgss nfs_acl lockd grace sunrpc autofs4 hid_generic usbhid hid video e1000 psmouse ahci libahci pata_acpi [last unloaded: complete]
[460514.122430] CPU: 3 PID: 31590 Comm: zsh Tainted: G           OE   4.13.0-45-generic #50~16.04.1-Ubuntu
[460514.122694] Hardware name: innotek GmbH VirtualBox/VirtualBox, BIOS VirtualBox 12/01/2006
[460514.122980] task: ffff8b0287a68000 task.stack: ffffaa1dc2b2c000
[460514.123125] RIP: 0010:faulty_write+0x8/0x20 [faulty]
[460514.123329] RSP: 0018:ffffaa1dc2b2feb0 EFLAGS: 00010246
[460514.123452] RAX: 0000000000000000 RBX: 0000000000000002 RCX: ffffaa1dc2b2ff18
[460514.123591] RDX: 0000000000000002 RSI: 00000000006c21e0 RDI: ffff8b032d640500
[460514.123720] RBP: ffffaa1dc2b2fec0 R08: ffffffffc0717000 R09: ffff8b032da8e428
[460514.123860] R10: 0000000000000001 R11: ffff8b0287a68000 R12: ffffaa1dc2b2ff18
[460514.123989] R13: 00000000006c21e0 R14: ffff8b032d640500 R15: 0000000000000001
[460514.124127] FS:  00007fe3b4476700(0000) GS:ffff8b033b380000(0000) knlGS:0000000000000000
[460514.124376] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[460514.124532] CR2: 0000000000000000 CR3: 0000000006d6c006 CR4: 00000000000606e0
[460514.124669] DR0: 0000000000000000 DR1: 0000000000000000 DR2: 0000000000000000
[460514.124870] DR3: 0000000000000000 DR6: 00000000fffe0ff0 DR7: 0000000000000400
[460514.124999] Call Trace:
[460514.126666]  ? __vfs_write+0x1b/0x40
[460514.128139]  vfs_write+0xb8/0x1b0
[460514.129640]  ? entry_SYSCALL_64_after_hwframe+0xb1/0x139
[460514.131149]  SyS_write+0x55/0xc0
[460514.132179]  ? entry_SYSCALL_64_after_hwframe+0x79/0x139
[460514.133142]  entry_SYSCALL_64_fastpath+0x24/0xab
[460514.134119] RIP: 0033:0x7fe3b36822c0
[460514.135104] RSP: 002b:00007ffef4644698 EFLAGS: 00000246 ORIG_RAX: 0000000000000001
[460514.136071] RAX: ffffffffffffffda RBX: 0000000000000004 RCX: 00007fe3b36822c0
[460514.137024] RDX: 0000000000000002 RSI: 00000000006c21e0 RDI: 0000000000000001
[460514.137991] RBP: 0000000000000004 R08: 00007fe3b3951780 R09: 00007fe3b4476700
[460514.138927] R10: 0000000000000001 R11: 0000000000000246 R12: 0000000000000000
[460514.139874] R13: 0000000000000000 R14: 0000000000000000 R15: 0000000000000000
[460514.140773] Code: <c7> 04 25 00 00 00 00 00 00 00 00 48 89 e5 5d c3 0f 1f 84 00 00 00 
[460514.141751] RIP: faulty_write+0x8/0x20 [faulty] RSP: ffffaa1dc2b2feb0
[460514.142606] CR2: 0000000000000000
[460514.143475] fbcon_switch: detected unhandled fb_set_par error, error code -16
[460514.145795] fbcon_switch: detected unhandled fb_set_par error, error code -16
[460514.148135] ---[ end trace 81f268ce846bc754 ]---
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

