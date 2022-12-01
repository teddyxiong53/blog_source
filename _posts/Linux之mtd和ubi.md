---
title: Linux之mtd和ubi
date: 2019-12-04 14:55:28
tags:
	- Linux
---

--

ubifs是一个新出现的，应用于mtd之上的文件系统。

可以有效地处理坏块和实现磨损平衡。

同时访问速度更快，消耗内存更小。

还有日志功能。

是jffs2的增强版本。

在mtd设备上存在着partition，在ubi上存在volume，他们之间什么关系？

同时也存在着两个概念mtd device，ubi device，他们之间的区别和联系又是什么？



在Linux下的documentation目录下，ubifs.txt里。

ubi是Unsorted Block Images的缩写。

ubifs是一个flash文件系统。专门为flash设备而设计的。

ubifs跟Linux上传统的文件系统都不一样。

ubifs代表了这样一类文件系统，**它跟mtd设备一起工作，而不是block设备。**

jffs2跟ubifs是一个类型的。



mtd device和block device的区别：

1、mtd device代表flash device，它们由相当大的eraseblock组成（一般是128KB）。

而block device一般是512B。

2、mtd device支持3种操作：

​	在一个eraseblock里，偏移某个值来读取。

​	在一个eraseblock里，偏移某个值来写入。

​	擦除整个eraseblock。

block device支持2种主要操作：

​	读取整个block。

​	写入整个block。

3、eraseblock在写入前需要全部擦除。而block则可以直接写。

4、eraseblock会在多次写入后磨损掉，block则不会。

5、eraseblock可能坏掉（只是对nand），软件必须处理坏块。block则不需要软件处理，硬件会自动处理掉。



ubifs工作在ubi之上。

ubi是一个单独的软件层，代码在drivers/mtd/ubi目录。

ubi提供的volume概念是比mtd device更高层的抽象。



**对ubi device的编程模型，跟mtd device的编程模型很像。**

ubi device没有磨损和坏块的限制。

在某种意义上，ubifs是下一代的jffs2 。

但是它跟jffs2很不一样，也不兼容。

下面是ubifs和jffs2的区别：

1、jffs2基于mtd device，而ubifs基于ubi。

2、jffs2没有on-media的index，必须在挂载的时候进行构建。这个就需要进行整个flash的扫描。而ubifs则不需要进行扫描。这样就加快了启动速度。

3、jffs2是write-through模式，而ubifs是write-back模式。所以ubifs更快。



跟jffs2类似，ubifs支持实时压缩，这样就占用很小的空间。

跟jffs2一样，ubifs也可以很好地应对意外断电。

**不需要fsck.ext2这样的处理。**

**ubifs自动根据日志进行恢复。保证flash上数据的完整性。**



ubifs是对数性能的，因为底层数据结构主要是树。

所以挂载时间和内存消耗，不是随着大小线性递增的。

jffs2也是如此。

这是因为ubifs在flash上维护了文件系统索引。

但是，ubifs是基于ubi的，而ubi是线性的。

所以整体上还是线性的。

但是比jffs2还是要好多了。



**ubifs的作者相信，开发完全对数性能的ubi2是可能的。**



编译时的ubi处理：



运行时的ubi处理：

```
 # ls /dev/ubi* -lh
crw-rw----    1 root     root      235,   0 Jan  1 00:00 /dev/ubi0
crw-rw----    1 root     root      235,   1 Jan  1 00:00 /dev/ubi0_0
crw-rw----    1 root     root      234,   0 Jan  1 00:00 /dev/ubi1
crw-rw----    1 root     root      234,   1 Jan  1 00:00 /dev/ubi1_0
crw-rw----    1 root     root       10,  55 Jan  1 00:00 /dev/ubi_ctrl
```



# ubiattach

a tool to attach MTD device to UBI.

这个工具的源代码在：mtd-2.1.1 目录下。

/sys/class/ubi

典型用法：

```
ubiattach /dev/ubi_ctrl -m 5
```

-m 5表示跟哪个mtd设备关联。

```
Creating 7 MTD partitions on "spi-nand0":
0x000000000000-0x000000200000 : "bootloader"
0x000000800000-0x000001000000 : "tpl"
0x000001000000-0x000001040000 : "misc"
0x000001040000-0x000001d40000 : "recovery"
0x000001d40000-0x000002740000 : "boot"
0x000002740000-0x000006f40000 : "system"
0x000006f40000-0x000008000000 : "data"
```



```
/dev/mtd5 is ready now.
#[ubiattach /dev/ubi_ctrl -m 5]
[    3.573093@1] ubi0: attaching mtd5
[    4.740347@1] ubi0: scanning is finished
[    4.764738@1] ubi0: attached mtd5 (name "system", size 72 MiB)
[    4.764943@1] ubi0: PEB size: 131072 bytes (128 KiB), LEB size: 126976 bytes
[    4.772015@1] ubi0: min./max. I/O unit sizes: 2048/2048, sub-page size 2048
[    4.778974@1] ubi0: VID header offset: 2048 (aligned 2048), data offset: 4096
[    4.786031@1] ubi0: good PEBs: 576, bad PEBs: 0, corrupted PEBs: 0
[    4.792183@1] ubi0: user volume: 1, internal volumes: 1, max. volumes count: 128
[    4.799538@1] ubi0: max/mean erase counter: 2/0, WL threshold: 4096, image sequence number: 4052910
[    4.808551@1] ubi0: available PEBs: 0, total reserved PEBs: 576, PEBs reserved for bad PEB handling: 20
[    4.817957@0] ubi0: background thread "ubi_bgt0d" started, PID 140
```

```
#[ mount -t ubifs /dev/ubi0_0 /mnt ]
[    4.839707@0] UBIFS (ubi0:0): background thread "ubifs_bgt0_0" started, PID 142
[    5.050557@1] UBIFS (ubi0:0): UBIFS: mounted UBI device 0, volume 0, name "rootfs"
[    5.052500@1] UBIFS (ubi0:0): LEB size: 126976 bytes (124 KiB), min./max. I/O unit sizes: 2048 bytes/2048 bytes
[    5.062589@1] UBIFS (ubi0:0): FS size: 68694016 bytes (65 MiB, 541 LEBs), journal size 9023488 bytes (8 MiB, 72 LEBs)
[    5.073161@1] UBIFS (ubi0:0): reserved for root: 0 bytes (0 KiB)
[    5.079127@1] UBIFS (ubi0:0): media format: w4/r0 (latest is w5/r0), UUID FD061054-FD5B-4D42-B118-CC595420E6D6, small LPT model
[    5.886634@0] UBIFS (ubi0:0): background thread "ubifs_bgt0_0" stops
[    6.282854@0] meson_rsv_env_read 856 read 0x2000 bytes from env, ret 0
[    6.340795@1] ubi1: attaching mtd6
[    6.604446@1] factory bad block at 0x7fe0000
[    6.604484@1] ubi1: scanning is finished
[    6.639079@1] ubi1: attached mtd6 (name "data", size 16 MiB)
[    6.639123@1] ubi1: PEB size: 131072 bytes (128 KiB), LEB size: 126976 bytes
[    6.646196@1] ubi1: min./max. I/O unit sizes: 2048/2048, sub-page size 2048
[    6.653100@1] ubi1: VID header offset: 2048 (aligned 2048), data offset: 4096
[    6.660195@1] ubi1: good PEBs: 133, bad PEBs: 1, corrupted PEBs: 0
[    6.666379@1] ubi1: user volume: 1, internal volumes: 1, max. volumes count: 128
[    6.673720@1] ubi1: max/mean erase counter: 2/0, WL threshold: 4096, image sequence number: 1777042946
[    6.682992@1] ubi1: available PEBs: 0, total reserved PEBs: 133, PEBs reserved for bad PEB handling: 19
[    6.692373@0] ubi1: background thread "ubi_bgt1d" started, PID 169
```

上面这个ubiattach是在S02overlayfs里做的。

```
在rcS文件的最前面，提前调用这个overlayfs的。
/etc/init.d/S02overlayfs start
```

里面内容是：

```
start() {
  . /etc/datamount
  . /etc/overlaymount
```



datamount脚本里

```
  #mount data
  ubidetach -p /dev/mtd${data_mtd_number}
  ubiformat -y /dev/mtd${data_mtd_number}
  ubiattach /dev/ubi_ctrl -m ${data_mtd_number}
  #    ubimkvol /dev/ubi1 -s $dataSize"MiB" -N data
  ubimkvol /dev/ubi1 -m -N data
  mount -t ubifs /dev/ubi1_0 /data
```

在overlaymount里

```
do_overlay_mount() { #<overlay dir>
        mkdir -p $1/upper $1/work
        fopivot $1/upper $1/work /rom 1
}
```

# ubi和ubifs关系

UBIFS涉及三个子系统：
\>MTD系统，提供对各种flash芯片的访问接口；drivers/mtd
\>UBI系统，工作在MTD上，提供UBI volume；drivers/mtd/ubi
\>UBIFS文件系统，工作在UBI之上；fs/ubifs

UBI指的是UBI subsystem，其工作在MTD设备上，是MTD设备的高层次表示，对上屏蔽了一些MTD需要处理的问题，如wearing和坏块处理；

而UBIFS指的是UBIFS file system，工作在UBI卷层之上。

# 参考资料

1、

https://blog.csdn.net/oqqyuji12345678/article/details/94616370

2、在Linux下的documentation目录下，ubifs.txt里。