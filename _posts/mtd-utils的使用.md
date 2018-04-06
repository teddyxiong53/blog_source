---
title: mtd-utils的使用
date: 2017-05-03 22:02:59
tags:
	- mtd

---

用软件模拟出一个mtd设备。具体方法查看我的文章《Linux上模拟mtd设备》。

# 1. mtdinfo

```
teddy@teddy-ubuntu:~$ mtdinfo /dev/mtd0
mtd0
Name:                           NAND simulator partition 0
Type:                           nand
Eraseblock size:                131072 bytes, 128.0 KiB
Amount of eraseblocks:          1024 (134217728 bytes, 128.0 MiB)
Minimum input/output unit size: 2048 bytes
Sub-page size:                  512 bytes
OOB size:                       64 bytes
Character device major/minor:   90:0
Bad blocks are allowed:         true
Device is writable:             true
```



# 2.  mtd_debug

这个命令要用sudo来运行，不然会出错。

```
teddy@teddy-ubuntu:~$ sudo mtd_debug info /dev/mtd0
[sudo] teddy 的密码： 
mtd.type = MTD_NANDFLASH
mtd.flags = MTD_CAP_NANDFLASH
mtd.size = 134217728 (128M)
mtd.erasesize = 131072 (128K)
mtd.writesize = 2048 (2K)
mtd.oobsize = 64 
regions = 0
```

# 3. flash_erase

基本语法是：`flash_erase /dev/mtd0 0x40000 5`。这个表示从0x40000这个地址开始，擦除5块的内容。一块的大小是128KB。

```
teddy@teddy-ubuntu:~$ sudo flash_erase /dev/mtd0 0x40000 5
Erasing 128 Kibyte @ c0000 -- 100 % complete 
```

类似命令有flash_eraseall。

```
teddy@teddy-ubuntu:~$ sudo flash_eraseall /dev/mtd0
flash_eraseall has been replaced by `flash_erase <mtddev> 0 0`; please use it
Erasing 128 Kibyte @ 7fe0000 -- 100 % complete 
```

# 4. flashcp

一般是用来把镜像文件直接拷贝到分区里。举例如下：

先生成一个img文件。

```
# cd test/mtd-test
# mkdir paramfs
# cd paramfs
# touch 1.txt
# cd ../
# mkfs.jffs2 -e 0x20000 -d paramfs -o paramfs.img
```

然后使用flashcp。

```
# flashcp -v ./paramfs.img /dev/mtd0
```

但是出错了。

```
teddy@teddy-ubuntu:~/test/mtd-test$ sudo flashcp ./paramfs.img /dev/mtd0 -v
Erasing blocks: 1/1 (100%)
Writing data: 0k/0k (0%)
While writing data to 0x00000000-0x00000080 on /dev/mtd0: Invalid argument
```

先不管错误。

上面的操作等价于

```
dd if=./paramfs.img of=/dev/mtd0
```

# 5. nandwrite

```
teddy@teddy-ubuntu:~/test/mtd-test$ sudo nandwrite -p /dev/mtd0 ./paramfs.img 
Writing data to block 0 at offset 0x0
```

# 6. nanddump

```
sudo nanddump -p -f ./nand.txt /dev/mtd0
```

p表示pretty，表示把打印弄漂亮一点。

dump出来非常大。

```
teddy@teddy-ubuntu:~/test/mtd-test$ ls -lh
总用量 481M
-rw-r--r-- 1 root  root  480M  5月  3 23:35 nand.txt
drwxrwxr-x 2 teddy teddy 4.0K  5月  3 23:33 paramfs
-rw-r--r-- 1 teddy teddy  268  5月  3 23:33 paramfs.img
```





