---
title: uboot之bootm和go的区别
date: 2018-03-16 12:49:40
tags:
	- uboot

---



go和bootm的区别就是：

1、go只是修改了pc的值。go用来引导没有使用mkimage制作过的内核。

2、bootm除了修改pc值，还传递了R0/R1/R2的值过去。



假设kernel的链接地址是0x2000 8000 。

# 用未压缩内核Image

1、让运行地址，不等于链接地址。

```
tftp 0x21000000 Image; go 0x21000000
```

不能运行。



# 用压缩内核zImage

1、让运行地址，不等于链接地址。

```
tftp 0x21000000 Image; go 0x21000000
```

可以解压成功。因为解压代码是地址无关的。

解压后的内核不能运行。

2、让运行地址，等于链接地址。

```
tftp 0x20008000 Image; go 0x20008000
```



对于不是用gzip压缩的内核，bootm命令会先判断bootm xxx这个xxx地址跟mkimage的-a参数指定的地址一样。

如果一样，就原封不动放在那里。

如果不一样，就会从xxx这个地址提取64字节 头部。把去掉头部的内部，复制到-a指定的地址上运行。



**bootm** 用于将内核镜像加载到[内存](https://so.csdn.net/so/search?q=内存&spm=1001.2101.3001.7020)的指定地址处，

如果有需要还要解压镜像，

然后根据操作系统和体系结构的不同给内核传递不同的启动参数，最后启动内核。



# 参考资料

1、uboot 命令分析(一) — bootm

https://blog.csdn.net/g_salamander/article/details/8463854