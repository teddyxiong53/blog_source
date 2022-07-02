---
title: Linux系统之mkbootimg命令
date: 2021-12-15 10:50:25
tags:
	- Linux

---

--

Android 产品中，内核格式是[Linux](https://so.csdn.net/so/search?from=pc_blog_highlight&q=Linux)标准的zImage，

根文件系统采用ramdisk格式。

这两者在Android下是直接合并在一起取名为boot.img,

会放在一个独立分区当中。

这个分区格式是Android自行制定的格式。

Android开发时，最标准的做法是重新编译内核和根文件系统，

然后调用Android给的命令行文件mkbootimg(out/host/linux-x86/bin/)来打包。

在制作手机ROM时，

有时会单独编译内核或抽出根文件进行修改内容，

比如我只编译内核，其余的地方不变。

这样重新安装巨大的Android开发环境实在不划算。

因此很多boot.img解包工具被人开发出来，

这一些工具都是把内核和根文件系统从一个现成的boot.img抽取出来，

修发后再次打包还原。

```
因为boot.img的格式比较简单，它主要分为三大块（有的可能有四块）

+—————–+
| boot header | 1 page
+—————–+
| kernel | n pages
+—————–+
| ramdisk | m pages
+—————–+
| second stage | o pages
+—————–+
n = (kernel_size + page_size – 1) / page_size
m = (ramdisk_size + page_size – 1) / page_size
o = (second_size + page_size – 1) / page_size
```



```
mkbootimg --kernel $OUT/kernel --ramdisk $OUT/ramdisk.img --second kernel/resource.img --output $OUT/boot.img
```



参考资料

1、mkbootimg 打包 特殊参数sencond 说明（爬坑系列）

https://blog.csdn.net/Nyiragongo/article/details/103254684

2、boot.img的生成过程，解析mkbootimg

https://blog.csdn.net/Obsession2015/article/details/85101845