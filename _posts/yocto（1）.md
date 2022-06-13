---
title: yocto（1）
date: 2019-05-17 13:40:11
tags:
	- Linux
---



yocto是什么？

跟buildroot比较有什么优势？

主要应用的场景？发展的情况如何？

另外还有openwrt，也是一套构建嵌入式Linux系统的工具。

大概看了一些，我觉得还是把buildroot玩好就够用了。

现在需要用yocto来做项目。所以还是研究一下。

先按照公司里的文档把环境搭建起来。

先不用管太多的概念和细节。

编译出镜像，直接分析脚本文件。



这个的确是没有buildroot那么直观简单。

构建是基于bitbake。

就相当于buildroot里的make。

OpenEmbedded（OE）

将BitBake和OE组件组合在一起形成参考构建主机，该主机以前称为 Poky。



Poky两层含义：

含义一：

OpenedHand（公司名）最初开发的开源项目。

该项目可以从现有的OpenEmbedded构建系统中开发出poky，

从而成为对嵌入式Linux商业支持的构建系统。

公司被英特尔收购后，该项目便成为Yocto Project构建系统的基础。

含义二：

在Yocto Project源存储库中， poky作为一个单独的Git存储库存在，

您可以克隆它之后在主机系统上生成本地副本。

**Metadata**：元数据集，所谓元数据集就是发行版内各基本元素的描述与来源 。

**Layers**：即各种meta-xxx目录，将Metadata按层进行分类，有助于项目的维护。
**Bitbake**：一个任务执行引擎，用来解析并执行Metadata。
**Output**：即各种输出image。

总结：假如用烹饪一桌酒席来形容构建发行版，则Yocto就是餐厅名，Poky就是厨房（以及提供作为参考搭配套餐），Metadata就是烹饪资源（.bb表示配方，.bbappend就是配方上的贴士，.conf表示厨房里的管事的小组长），Layers就是菜谱的分类（如川菜谱、粤菜谱），Bitbake就是厨师，Output就是得到的一桌酒席。



BitBake与各种类型的配置文件、任务、执行器一起形成 OpenEmbedded-Core（OE-Core）。

BitBake是OpenEmbedded构建系统的核心工具， 负责解析元数据，从中生成任务列表，然后执行这些任务。

# bitbake基本用法

如您要构建的配方的名称为matchbox-desktop_1.2.3.bb：

```
# 编译对应的镜像
bitbake matchbox-desktop
# 清除
bitbake matchbox-desktop -c clean
# 编译某个包
bitbake optee_example -c compile
# 下载代码
bitback -c fetchall 
# 使用-k忽略过程中的错误
```

## bb文件

带.bb后缀的文件是“配方”文件。这些配方文件为BitBake提供以下内容：

有关软件包的描述性信息（作者，主页，许可证等）
配方版本
现有依赖关系（构建和运行时依赖关系）源代码
所在的位置以及如何获取它
源代码是否需要任何补丁，在哪里可以找到它们以及如何应用它们
如何配置和编译源代码
如何将生成的工件组装到一个或多个可安装的程序包中
在目标计算机上的哪个位置安装软件包或创建的软件包

例如yocto-code/meta-meson/recipes-bsp目录下的u-boot_2019.01.bb文件。

## conf文件



这要从发行版的定制流程说起。

我们的目的很简单，是要得到uboot、kernel、rootfs这三个image；

Yocto的目的也很简单，它要经过一级一级配置，逐步缩小配方，

直至得到uboot、kernel、rootfs这三个image。

每一级需要哪些配方，由该级对应的配置文件（.conf/.bb）决定。

越上级的配置是越笼统的，越下级的配置越细致。

如果下级的配置项相对于上级有补充或者冲突，则以下级的内容为准，可以认为下级会对上级进行“重写”。



有关构建的路线和流程：

对于整个发行版构建，虽然每一级的配方由（.conf/.bb）决定，

但是每一级路线和方向的选择，是由我们最终bitbake的对象决定的，

比如bitbake avi-image-core，我们想要获得rootfs.img，

## bbclass文件

类文件（.bbclass）包含有助于在**配方文件之间共享的信息**。

一个示例是 autotools类，其中包含Autotools使用的任何应用程序的通用设置。

BitBake构建系统过程中必须要包含的一个类是 base.bbclass ,

您可以在classes目录中找到此文件。

base.bbclass类文件是特殊的，

因为它总是被所有的配方和类自动包含。

此类包含用于标准基本任务的定义，

例如获取，解压缩，配置（默认情况下为空），编译（运行存在的任何Makefile），安装（默认情况下为空）和打包（默认情况下为空）。这些任务通常被在项目构建过程中被其它类进行覆盖或者扩展。

## layer

层的可以将不同类型的自定义内容相互隔离。

尽管您可能会发现在单个项目中将所有内容都保留在一层中很诱人，但是元数据的模块化程度越高，应对将来的更改就越容易。

用一句话概括层：

层是组织文件和目录结构的元数据（配置文件、配方）集合。

创建层：
即使你只有一两个配方文件，还是建议你创建自己的层，

而不是把配方添加到OE-Core或者Yocto项目层，

随着你的配方越来越多，这种好处更能体现出来，

且容易迁移到你的其它项目中去。

你可以修改配置文件，使你的层添加到项目中。

还可以用yocto-layer脚本来创建层。



Layer包含了一系列告诉OE构建系统应该做什么的指令，它以仓库的形式存在于你的项目中。

Layer拥有强大的重写功能，以便于你对其他Layer的内容进行修改，使用于你自己的产品。

你可以使用多个Layer，从逻辑上分割你的构建内容，例如，你可以拥有BSP, GUI, distro 配置, 中间件, 应用层这些不同的配置，以帮助你在项目长期运转中灵活的做出任何修改。



参考资料

https://zhuanlan.zhihu.com/p/111688338

## bbappend文件

追加文件是以.bbappend结尾的扩展名文件，

用于扩展或覆盖现有配方文件中的信息。

每个追加文件都应有一个对应的配方文件，且二者具有相同的文件名，

仅后缀不同（例如formfactor_0.0.bb和 formfactor_0.0.bbappend）。



# av400

https://confluence.amlogic.com/display/SW/Yocto+A5+Environment+Setup

yocto-dunfell-a5.xml 

```
$ cd <Your_Local_Path>/Yocto-A5
$ export BUILD_DIR=$PWD/build-av400
$ source meta-meson/aml-setenv.sh mesona5-av400
$ bitbake amlogic-sbr-yocto
```

增加的环境变量是这3个。

```
TARGET_MACHINE=mesona5-av400
BUILDDIR=/mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/build-av400
MESON_ROOT_PATH=/mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code
```

amlogic-sbr-yocto对应的文件是：

```
 find -name "amlogic-sbr-yocto*"
./meta-meson/recipes-core/images/amlogic-sbr-yocto.bb
```



直接看av400当前基础的配置。

从最底层的配置开始看。

```
TUNEVALID[arm] = "Enable ARM instruction set"
```

TUNEVALID代表了什么？

```
TUNECONFLICTS[aarch32] = "armv4 armv5 armv6 armv7 armv7a armv7ve"
```

TUNECONFLICTS有是什么？

```
require conf/machine/include/arm/arch-arm.inc
```

require就是include文件的机制吧。



devtool与bitbake类似，同属于yocto中的构建工具

内核开发最好使用[devtool](https://docs.yoctoproject.org/sdk-manual/extensible.html#using-devtool-in-your-sdk-workflow)来完成， 而不是通过传统的内核工作流方法。



# addtask write_config before do_configure

这句怎么理解？

看了openeuler的yocto分享视频，B站上有。

自定义插入自定义的hook函数的意思。



yocto的版本有些是不兼容的。

好像3.3就跟之前的不兼容。

我现在用的是dunfell。这个版本号是3.1的。

当前最新的是4.0，名字叫kirkstone。



bitbake语法有这样特别的变量操作。

```
.=  这个点号，可以理解为字符串的连接符。这个相当于prepend
=.  这个相当于append。
```

FILESEXTRAPATHS

添加到构建系统的搜索路径里，扩展的是[`FILESPATH`](https://www.yoctoproject.org/docs/1.4.2/ref-manual/ref-manual.html#var-FILESPATH)

一般的用法，就是在bbappend里，写上这个：

```
FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"
```

还有这种用法：

```
FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
```

files对应目录下一个files名字的子目录。



THISDIR



Yocto 变量选择 bb.utils.contains 使用

https://blog.csdn.net/xue1065540183/article/details/105663248

```
ABC = “${@bb.utils.contains('val', 1', 'true', 'false ', d)}"

val = 1 则 ABC 赋值 true，否则 ABC 赋值 false
```



Features

[DISTRO_FEATURES](https://docs.yoctoproject.org/ref-manual/variables.html#term-DISTRO_FEATURES) 

[MACHINE_FEATURES](https://docs.yoctoproject.org/ref-manual/variables.html#term-MACHINE_FEATURES) 

[**IMAGE_FEATURES**](https://docs.yoctoproject.org/ref-manual/variables.html#term-IMAGE_FEATURES) 

[EXTRA_**IMAGE_FEATURES**](https://docs.yoctoproject.org/ref-manual/variables.html#term-EXTRA_IMAGE_FEATURES)



poky/meta/conf/bitbake.conf里定义了PN等变量的。值得看一下。



[**PACKAGECONFIG**](https://docs.yoctoproject.org/ref-manual/variables.html?highlight=packageconfig#term-PACKAGECONFIG)



# virtual provider

https://docs.yoctoproject.org/dev-manual/common-tasks.html#using-virtual-providers

如果你知道不同的配方提供了同一个功能。

那么就可以抽象一个virtual provider。

actual provider会在编译时确定。

例如你有3个kernel配方，分别是kernel-big、kernel-mid、kernel-small。



The following lists specific examples of virtual providers:

- `virtual/kernel`: Provides the name of the kernel recipe to use when building a kernel image.
- `virtual/bootloader`: Provides the name of the bootloader to use when building an image.
- `virtual/libgbm`: Provides `gbm.pc`.
- `virtual/egl`: Provides `egl.pc` and possibly `wayland-egl.pc`.
- `virtual/libgl`: Provides `gl.pc` (i.e. libGL).
- `virtual/libgles1`: Provides `glesv1_cm.pc` (i.e. libGLESv1_CM).
- `virtual/libgles2`: Provides `glesv2.pc` (i.e. libGLESv2).







# 参考资料

1、

https://blog.csdn.net/yanghanxing110/article/details/77737471

2、4 种用于构建嵌入式 Linux 系统的工具

https://zhuanlan.zhihu.com/p/39134627

3、

这篇文章非常好。

https://blog.csdn.net/qq_28992301/article/details/52872209

4、

https://blog.csdn.net/fulinus/category_10445379.html

5、

https://confluence.amlogic.com/pages/viewpage.action?pageId=168513950

6、

https://blog.csdn.net/u013921164/article/details/112952438

7、Yocto官方文档学习及项目实践

https://www.zhihu.com/column/c_1216023762614960128

8、中文文档

https://github.com/guevaraya/Yocto_doc

9、Yocto中开发内核的两种方法

这篇不错

https://blog.csdn.net/qq_27149449/article/details/119188694

10、

https://blog.csdn.net/faihung/article/details/82712213

11、Yocto添加drive recipe

https://blog.csdn.net/qq_34031123/article/details/104500620

12、yocto基本概念

这篇文档对概念介绍非常好。

https://blog.csdn.net/qq_35018427/article/details/104955295

13、

https://confluence.amlogic.com/pages/viewpage.action?pageId=168513950