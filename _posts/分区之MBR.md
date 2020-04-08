---
title: 分区之MBR
date: 2020-04-08 14:03:51
tags:
	- Linux

---

1

MBR是Master Boot Recorder。主引导记录。

这个在磁盘的第一个扇区。

一个扇区512字节。

MBR只用了其中64个字节。

```
0到445字节：
446到509:64个字节。放MBR。
510到511：最后2个字节。55AA。相当于一个签名。
```

64个字节的MBR分为4个部分，每个部分16字节。

每16个字节代表了一个分区，所以，一个MBR只能描述4个分区的信息。

16字节里的信息有：起始扇区（4字节），扇区数（4字节），其他信息。

一个扇区512字节，4字节的扇区数，这样得到的MBR可以描述的最大的磁盘是2TB。







参考资料

1、

https://thestarman.pcministry.com/asm/mbr/PartTables.htm

2、

https://www.eassos.cn/jiao-cheng/ying-pan/mbr-vs-gpt.php