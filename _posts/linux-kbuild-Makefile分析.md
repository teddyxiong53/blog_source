---
title: linux kbuild Makefile分析
date: 2016-11-03 20:50:12
tags:
	- linux
	- Makefile
---

kbuild系统是从内核2.6版本开始引入的。
# 1. linux内核的Makefile分类
1. kernel Makefile
这个也叫Top Makefile，专门指内核代码根目录的Makefile。这个Makefile不需要改动。

2. kbuild Makefile
kbuild系统利用kbuild Makefile来编译内核或者模块。当kernel Makefile被解析完成后，kbuild系统会读取相关的kbuild Makefile进行编译，kbuild Makefile有特定的语法来指定哪些内容编译到内核镜像，哪些内容编译成模块，内核及驱动开发人员需要编写各自的kbuild Makefile。

3. ARCH Makefile
位于arch/$(ARCH)/Makefile。只有平台开发人员需要关心这个。

下面我们要讨论的就是kbuild Makefile。
# 2. kbuild Makefile
1. 名字
kbuild Makefile的文件名不一定要是Makefile，但是当然推荐用Makefile这个名字。你也可以用Kbuild这个文件名。当Kbuild和Makefile两个文件同时存在时，则Kbuild系统使用Kbuild这个文件。
2. 目标定义
Kbuild文件要定义的2个内容是obj-?和xxx-objs。xxx-objs内容可以没有，在当前目录就一个源文件的时候。
obj-?的“?”的可能取值是y和m。y表示编译进内核，m表示编译成ko模块。
例如：
`obj-y=$(target).o
如果没有指定xxx-objs，则编译这个目标对象的源文件是$(target).c或者$(target).s。
如果指定了xxx-objs，则源文件由xxx-objs的内容来指定。`
3. 嵌套编译
如果当前目录下还有子目录，那么怎么来把子目录也包含进来呢？
这么写就行了。
obj-? = $(subdir)/
# 3.看几个例子
我们以driver/net目录下的Makefile为例，看一看。
```
obj-$(CONFIG_MII) += mii.o
obj-$(CONFIG_MDIO) += mdio.o
obj-$(CONFIG_PHYLIB) += phy/
```
在经过menuconfig之后，`CONFIG_MII`的取值就是y或者m或者n这3个值中的一个。
`obj-n`是被忽略的。
从上面举例的这3行，phy这个是个子目录，我们再进去看看Makefile。

```
libphy-objs			:= phy.o phy_device.o mdio_bus.o
obj-$(CONFIG_PHYLIB)		+= libphy.o
obj-$(CONFIG_MARVELL_PHY)	+= marvell.o
```







