---
title: uboot（1）
date: 2022-11-28 19:06:32
tags:
	- uboot

---

--

# 基本信息

这些信息是从https://github.com/u-boot/u-boot readme的内容总结得到的。

## summary

uboot的开发跟Linux紧密相关。

有些代码是直接从Linux kernel那边拿过来的。

有一些公用的头文件。

还有些特殊代码用来支持Linux的启动。

## 项目由来

1、最早是8xxrom的代码。

2、创建了PPCboot project。PPC是PowerPC的缩写。

3、然后增加了对其他的板子的支持。

4、创建ARMBoot project。

5、增加其他CPU支持。

6、创建u-boot project。

## 软件配置

make xx_defconfig

## sandbox环境

## 板子init flow

首先是架构相关的start.S汇编是入口。

```
lowlevel_init
board_init_f
board_init_r
```

## image format

两种格式：

1、New uImage format (FIT)。基于 Flattened Image Tree 。文档在 doc/uImage.FIT 

2、Old uImage format。

## Linux支持



# sandbox

在这个doc\driver-model\README.txt文件里。

看到有这样的说明：

```
   make sandbox_defconfig
   make
   ./u-boot -d u-boot.dtb
```

看来是一个类似于qemu的可以在本机执行进行测试的配置。

看看。

# FIT image

Linux kernel在ARM架构中引入device tree（全称是flattened device tree，后续将会以FDT代称）的时候[1]，

其实怀揣了一个Unify Kernel的梦想----同一个Image，可以支持多个不同的平台。

随着新的ARM64架构将FDT列为必选项，并将和体系结构有关的代码剥离之后，这个梦想已经接近实现：



本文将基于嵌入式产品中普遍使用的u-boot，

**以其新的uImage格式（FIT image，Flattened uImage Tree）为例，**

介绍达到此目标的步骤，以及背后的思考和意义。



为了解决上述缺点，u-boot自定义了一种Image格式----uImage。

最初的时候，uImage的格式比较简单，

就是为二进制文件加上一个header（具体可参考“[include/image.h](https://github.com/wowotechX/u-boot/blob/x_integration/include/image.h)”中的定义），

标示该文件的特性。

然后在boot该类型的Image时，从header中读取所需的信息，按照指示，进行相应的动作即可。

这种原始的Image格式，称作Legacy uImage，其特征可总结为：

1）使用mkimage工具（位于u-boot source code的tools/mkimage中）生成。

2）支持OS Kernel Images、RAMDisk Images等多种类型的Image。

3）支持gzip、bzip2等压缩算法。

4）支持CRC32 checksums。

5）等等。

最后，之所以称作Legacy，说明又有新花样了，这种旧的方式，我们就不再过多关注了，拥抱新事物去吧。



device tree在ARM架构中普及之后，u-boot也马上跟进、大力支持，

毕竟，美好的Unify kernel的理想，需要bootloader的成全。

为了支持基于device tree的unify kernel，u-boot需要一种新的Image格式，这种格式需要具备如下能力：

1）Image中需要包含多个dtb文件。

2）可以方便的选择使用哪个dtb文件boot kernel。



综合上面的需求，u-boot推出了全新的image格式----FIT uImage，

其中FIT是flattened image tree的简称。

是不是觉得FIT和FDT（flattened device tree）有点像？

没错，它利用了Device Tree Source files（DTS）的语法，

生成的image文件也和dtb文件类似（称作itb），下面我们会详细描述。

为了简单，我们可以直接把FIT uImage类比为device tree的dtb文件，其生成和使用过程为[2]：

> image source file    mkimage + dtc              transfer to target
>       \+        -----------------------------> image file -----------------------------------> bootm
> image data file(s)

其中image source file(.its)和device tree source file(.dts)类似，

负责描述要生成的image file的信息（上面第2章描述的信息）。

mkimage和dtc工具，可以将.its文件以及对应的image data file，打包成一个image file。

我们将这个文件下载到么memory中，**使用bootm命令就可以执行了。**



image source file的语法和device tree source file完全一样（可参考[3][4][5]中的例子），只不过自定义了一些特有的节点，包括images、configurations等。说明如下：



参考资料

1、u-boot FIT image介绍

http://www.wowotech.net/u-boot/fit_image_overview.html



# 重要的文件

```
include\image.h
include\bootstage.h
```



# 参考资料

1、

