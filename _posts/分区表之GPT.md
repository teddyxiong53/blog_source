---
title: 分区表之GPT
date: 2020-04-08 14:01:51
tags:
	- Linux

---



看rk3308的分区表，是使用GPT的方式。了解一下这个。

GPT被存放在介质的LBA0到LBA64。

LBA是Logic Block Address的意思。逻辑块地址。



uboot支持标准的GPT格式。

GPT是EFI标准的一部分。特点是使用UUID作为磁盘分区的代号。

GPT的第一个扇区，还是放MBR信息，这样来保持对MBR 的兼容。





参考资料

1、

https://thestarman.pcministry.com/asm/mbr/PartTables.htm

2、

http://rockchip.wikidot.com/partitions

3、GPT在uboot里的文档

https://github.com/rockchip-linux/u-boot/blob/android/doc/README.gpt

4、

https://blog.csdn.net/haiross/article/details/38659825

5、逻辑区块地址

https://baike.baidu.com/item/%E9%80%BB%E8%BE%91%E5%8C%BA%E5%9D%97%E5%9C%B0%E5%9D%80/22660818?fromtitle=LBA&fromid=2025827

6、MBR 与 GPT，关于分区表你应该知道的一些知识 - 硬盘使用知识大全（8）

https://www.eassos.cn/jiao-cheng/ying-pan/mbr-vs-gpt.php