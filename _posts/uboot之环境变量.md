---
title: uboot之环境变量
date: 2018-03-04 11:51:08
tags:
	- uboot
typora-root-url: ..\
---



本文是根据这篇文章总结的。

https://nnc3.com/mags/LJ_1994-2014/LJ/246/11725.html



uboot带有一个命令行，这个命令行有基本的脚本特性。

脚本特性跟环境变量结合，就可以创造很强大的引导功能。

initrd镜像在ddr的顶部，kernel可能无法访问。你可以让uboot把initrd放在ddr的低地址上。你只需要设置initrd_high这个环境变量就可以了。



# 什么是环境变量

简单的说法就是一组键值对。

值可以是：

```
1、字符串。
2、十六进制。
3、bool
4、其他。
```

在介质上存储的都是字符串。

![环境变量存储](/images/环境变量存储.jpg)



# 环境变量的存储

1、default。是写死在代码里的。

2、用户定义的。存储在介质里。

uboot提供了工具，来生成环境变量块。这样就避免了一个一个输入sentenv的过程了。

```
./tools/mkenvimage -s 16384 -o my_env_blob myenvdata.txt
```

# 增加一个环境变量



# uboot在内存里

在内存里是一个hashtable。

setenv就是对这个table进行操作。saveenv的时候才写入到介质里。

