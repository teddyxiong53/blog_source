---
title:
 Linux上模拟mtd设备
date: 2017-05-03 22:08:46
tags:

	- linux

	- mtd

---

要学习mtd-utils的使用，但是手头没有带mtd设备的板子，怎么办？模拟一个呗。

模拟方法如下：

```
1. 先安装mtd-utils
 sudo apt-get install mtd-utils
2.  sudo modprobe mtd  
3.  sudo modprobe mtdblock
4. sudo modprobe nandsim first_id_byte=0xec second_id_byte=0xa1 third_id_byte=0x00 fourth_id_byte=0x15 
```

现在就可以在查看到对应的mtd设备了。

```
teddy@teddy-ubuntu:/usr/include$ cat /proc/mtd
dev:    size   erasesize  name
mtd0: 08000000 00020000 "NAND simulator partition 0"
```

