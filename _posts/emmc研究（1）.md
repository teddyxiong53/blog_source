---
title: emmc研究（1）
date: 2022-11-24 11:05:32
tags:
	- emmc

---

--

# eMMC 里 DDR52 HS200 HS400 等的含义

DDR52就是最高 52M clock，数据速率就是 52 x 2 = 104
HS200 就是最高 200M clock，单[通道](https://so.csdn.net/so/search?q=通道&spm=1001.2101.3001.7020)，数据速率也是 200
HS400 也是最高 200M clock，但是是双通道，所以数据速率是 200 x 2 = 400

HS200和HS400 是 5.0 协议才有的。

# emmc和nand flash的关系

emmc是在nand的基础上增加了控制器，自动管理坏块。

写emmc的驱动比写nand的驱动要简单。



# 参考资料

1、

https://blog.csdn.net/boyemachao/article/details/109227536

2、

https://linux-sunxi.org/Replace_NAND_with_eMMC_howto