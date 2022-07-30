---
title: yocto（1）
date: 2019-05-17 13:40:11
tags:
	- Linux
---

--

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



conf文件定义了各种管理build过程的变量。

这些文件分为几个部分：

1、机器配置。

2、分发配置。

3、编译器调整。

4、通用公共配置。

5、用户配置。

主配置文件是bitbake.conf这个文件。



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

## 编译运行

之前编译出错，把代码完全删掉重新同步编译成功了。

烧录可以运行。

可以得出这些信息：

```
1、使用的是toybox。而不是busybox，但是busybox也编译进去了。
2、使用的是systemd init系统。

```



```
meson_do_compile() {
    ninja ${PARALLEL_MAKE}
}
```

是靠这些来配置systemd的。在mesona1-av400.conf里。

```
DISTRO_FEATURES_BACKFILL_CONSIDERED = "sysvinit"
DEFAULT_DISTRO_FEATURES += " systemd"
DISTRO_FEATURES_append = " systemd"
DISTRO_FEATURES_remove = " sysvinit"
```



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



# 各种Features

[DISTRO_FEATURES](https://docs.yoctoproject.org/ref-manual/variables.html#term-DISTRO_FEATURES) 

[MACHINE_FEATURES](https://docs.yoctoproject.org/ref-manual/variables.html#term-MACHINE_FEATURES) 

[**IMAGE_FEATURES**](https://docs.yoctoproject.org/ref-manual/variables.html#term-IMAGE_FEATURES) 

[EXTRA_**IMAGE_FEATURES**](https://docs.yoctoproject.org/ref-manual/variables.html#term-EXTRA_IMAGE_FEATURES)



## IMAGE_FEATURES

在一个image里包含的feature。

最好是写在image的bb文件里，

你可以写在conf文件里，但是不推荐这么做。

如果要在image的bb文件外面对image feature进行修改。

使用EXTRA_IMAGE_FEATURES这个变量来进行操作。



用IMAGE_FEATURES和

https://docs.yoctoproject.org/dev-manual/common-tasks.html#customizing-images-using-custom-image-features-and-extra-image-features

poky/meta/conf/bitbake.conf里定义了PN等变量的。值得看一下。





# PACKAGECONFIG

这个是configure的选项配置。

我现在需要去掉gstreamer的libgles的配置。

应该怎么做呢？



在recipe的PACKAGECONFIG变量的基本架构如下:

```
PACKAGECONFIG[f1] = "--with-f1,--without-f1,build-deps-f1,rt-deps-f1"
```

在一个recipe中, 如果f1属性使能, 则--with-f1, build-deps-f1就会应用于这个recipe,

而如果f1属性被禁止, --without-f1 和 rt-deps-f1则会被应用.



使能recipe的某个属性

如果要增加使能recipe的某个属性的话, 有以下两种方法

方法一: 在recipe的附件文件即.bbappend文件中添加该依赖属性

```
PACKAGECONFIG_append = " f1"
```

方法二: 在bsp包的配置文件conf/local.conf中增加recipe的依赖属性

```
PACKAGECONFIG_append_pn-[recipename] = " f1"
```



应用实例

接下来, 以qtbase增加sql-sqlite为例, 对PACKAGECONFIG进行介绍.

在qtbase的recipe文件qtbase_git.bb中, sql-sqlite的属性配置为

```
PACKAGECONFIG[sql-sqlite] = "-sql-sqlite -system-sqlite,-no-sql-sqlite,sqlite3"
```

当sql-sqlite属性使能后, sqlite3会应用于qtbase中.

有一下两种方法, 使能qtbase的sql-sqlite属性.

方法一: 在qtbase_git.bbappend文件中增加sql-sqlite属性

```
PACKAGECONFIG_append = " sql-sqlite"
```

方法二: 在conf/local.conf文件中增加sql-sqlite属性

```
PACKAGECONFIG_append_pn-qtbase = " sql-sqlite"
```



用法说明：
PACKAGECONFIG[foo] = "--enable-foo,--disable-foo,foo_depends,foo_runtime_depends"

有四个参数，

--enable-foo：表示如果有foo的那么使能它

--disable-foo:表示没有foo的情况下就不是能它

foo_depends： 表示如果有foo的情况下编译时的依赖。

foo_runtime_depends:表示如果有foo的情况下，运行时的依赖

上面的例子是pango对基于x11或direcrfb的情况

如果是基于x11的`（${@base_contains('DISTRO_FEATURES', 'x11', 'x11', '', d)}），那么configure时，--with-x, 编译依赖${X11DEPENDS}`

`如果是基于direcrfb(${@base_contains('DISTRO_FEATURES', 'directfb', 'directfb', '', d)})的，那么运行confiure时，--without-x，编译依赖direcrfb`



这个是gstreamer-plugin-base的，在bbappend里增加opus配置。传递给meson程序来进行configure的。

```
DEPENDS += " libopus"
RDEPENDS_${PN} += " libopus"

PACKAGECONFIG_append = " opus"
PACKAGECONFIG[opus]  = "-Dopus=enabled,-Dopus=disabled,libopus"
```



参考资料

https://wiki.phytec.com/pages/viewpage.action?pageId=151257902

https://blog.csdn.net/xiaofeng_yan/article/details/7018349



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





某个开源组件下载失败或者速度较慢

​     可以把下载好的同版本组件放到DL_DIR指定目录下，然后复制一个*.done文件并改为对应名字即可

# 官网示例教程

```
git clone https://github.com/YoeDistro/poky
git checkout -t origin/kirkstone -b my-kirkstone
```

```
$ cd poky
$ source oe-init-build-env
```

然后

```
bitbake core-image-minimal
```

并发下载速度确实非常快。

编译完成后，

```
runqemu qemux86-64
```

# 添加打印调试

https://stackoverflow.com/questions/62337145/echo-statements-in-yocto-recipe-not-printing-to-terminal

inherit logging，然后使用这些函数进行打印

```
Functions are : bbplain, bbnote, bbwarn, bberror, bbfatal, bbdebug
```

必须要加在函数里

```
do_configure() {
    bbwarn "xxxxxxxxxxxxxxxxxxxxxx"
    bbwarn "--------${TOOLCHAIN_OPTIONS}--------------"
    ${S}/configure ${EXTRA_OECONF}
}
```

# 添加一个package

https://blog.csdn.net/sy373466062/article/details/50381067

https://blog.csdn.net/sy373466062/category_9264954.html

https://github.com/tonyho/helloYocto



```
内核放在了哪里？ 这个是放在了如下位置，我们可以用下面命令来确定：
bitbake -e linux-imx  | grep ^S=
```

LIC_FILES_CHKSUM这个随便找一个文件求md5值就行。

LIC_FILES_CHKSUM：这个是checksum，如果是基于版本管理的source，那么不需要，例如git与svn

```
LIC_FILES_CHKSUM = "file://helloYocto.c;md5=2dac018fa193620dc085aa1402e0b346"
S = "${WORKDIR}"
do_compile () {
    make
}
```

还有两个方法，这2个方法重载了bitbake中默认方法：

1. do_compile
2. do_install

这两个方法，对应了Package中的compile与install task。



Yocto中可以配置一个Distrbution的License，然后所有的软件包，都需要符合这个license才可以被shipped到image中，如果我们需要使用违反此license的软件包，那么就需要额外配置。



Toolchian中静态库的添加
没有静态库，是无法静态编译应用程序的，因此，为了方便，还需要在SDK中添加静态库，例如libc。

这个特性在只需要开启即可，在local.conf中添加一行：

SDKIMAGE_FEATURES_append = "staticdev-pkgs"



现在下载kernel代码特别慢。

在这个文件里看到

Z:\work\test\yocto-test\poky\meta\recipes-kernel\linux\linux-yocto_5.15.bb

```
SRC_URI = "git://git.yoctoproject.org/linux-yocto.git;name=machine;branch=${KBRANCH}; \
           git://git.yoctoproject.org/yocto-kernel-cache;type=kmeta;name=meta;branch=yocto-5.15;destsuffix=${KMETA}"
```

我先手动clone到本地。

```

```





FEATURE_PACKAGES

指定编译到image里的package

packagegroup-core-x11



IMAGE_FEATURES_REPLACES



MACHINE_HWCODECS



# core-image-minimal分析

https://blog.csdn.net/groundhappy/article/details/52859237

先不去考虑local.conf里面的一些配置内容，比如MACHINE等等，同时也不深入分析代码的构建那一部分，我们只分析通过Documentation可以查询到的。

只从bb文件以及配置的角度来查看。



指定了了需要安装到这个image里面的包，使用的时候需要很小心避免顺序的问题。

当core-image-minimal-initramfs使用的时候，

不要使用这个变量，

而是是要使用PACKAGE_INTALL来替代，

这样可以使initial内存磁盘菜谱使用一些固定的包。

而不受到IMAGE_INSTALL的影响。

```
CORE_IMAGE_BASE_INSTALL = '\
    packagegroup-core-boot \
    packagegroup-base-extended \
    \
    ${CORE_IMAGE_EXTRA_INSTALL} \
    '

CORE_IMAGE_EXTRA_INSTALL ?= ""

IMAGE_INSTALL ?= "${CORE_IMAGE_BASE_INSTALL}"
```

packagegroup-core-boot这个对应Z:\work\test\yocto-test\poky\meta\recipes-core\packagegroups\packagegroup-core-boot.bb



FEATURE_PACKAGES

这些FEATURE都是可以指定添加到image里面去的。

具体变量通过 IMAGE_FEATURES来配置

```
FEATURE_PACKAGES_hwcodecs = "${MACHINE_HWCODECS}"
说明有N种特性这可以添加到这个image里面。
```

例如，sato的就表示要把这些打包打image里。

```
IMAGE_FEATURES += "splash package-management x11-base x11-sato ssh-server-dropbear hwcodecs"

LICENSE = "MIT"

inherit core-image
```

# 文件下载过程

https://blog.csdn.net/groundhappy/article/details/55046166

bitbake通过几步来获取源代码或者文件。主要按顺序处理两个不同的步骤。

1主要是先从某个地方（缓存或者其他地方）获取源码，

2然后将源码解压到特定的位置或者指定的位置

```
处理第1部分的代码类似如下

src_uri = (d.getVar('SRC_URI', True) or "").split()
fetcher = bb.fetch2.Fetch(src_uri, d)
fetcher.download()
```

从BB文件的SRC_URI变量获取具体的下载地址

使用SRC_URI变量 产生一个 下载器，调用fetcher实现下载

```
处理第2部分的代码类似如下
 rootdir = l.getVar('WORKDIR', True)
 fetcher.unpack(rootdir)
```

通常下载好的文件会指定解压到WORKDIR目录中

SRCURI和WORKDIR变量不是硬编码到fetcher里面的。因为fetcher的方式可能是多种多样的。

比如OE的共享状态代码（sstate 主要是指已经编译过的）使用fetch模块获取sstate文件

当download()方法调用的时候。bitbake尝试使用下面的搜索顺序来解决URL

1 pre-mirror sites 首先使用预镜像地址来取得源码。这些位置定义在PREMIRRORS变量中

2 如果pre-mirror sites下载失败 那么再使用 SRC_URI地址来下载

3 如果下载还是失败。尝试使用镜像来下载。MIRRORS 



bitbake是支持cross-url的。可以镜像一个git仓库到一个http服务器上作为一个压缩包。

bitbake维护了一系列从网络下载的文件的缓存，所有非本地的文件都被放置在了download directory。这个目录通过DL_DIR指定

同时文件的完整性是很有必要的。

对于非本地的文档下载fetcher代码可以通过验证sha-256和MD5checksum来确定文档被准确下载了。

可以通过SRC_URI变量来指定合适的值。

比如

SRC_URI[md5sum] = "value"
SRC_URI[sha256sum] = "value"
**也可以在SRC_URL的尾部指定校验值**

SRC_URI = "http://example.com/foobar.tar.bz2;md5sum=4a8e0f237e961fd7785d19d07fdb994d"

```
如果存在多个下载URL，可以通过上面直接在末尾指定md5sum的方式，也可以命名这个url，然后指定名字的md5。如下
SRC_URI = "http://example.com/foobar.tar.bz2;name=foo"
SRC_URI[foo.md5sum] = 4a8e0f237e961fd7785d19d07fdb994d
```

一旦下载校验完毕。bitbake就会使用这个.done标记放在DL_DIR里面。

bitbake用这个标记来识别，避免后续重新下载或者计算checksum

## 本地文件获取器(file://)

本模块处理以file://开头的URLs.文件名指定的URL可以是一个相对或者绝对路径。

如果文件名是相对的。那么FILESPATH变量和系统PATH变量都会用来查找这个文件。

（如果FILESPATH和PATH没有找到，那么FILESDIR被用来查找这个合适的相对文件，由于FILESDIR将被遗弃了，所以不要使用）

如果这个文件不能找到。那么假定在变量DL_DIR指定的目录中。

如果你指定的是一个目录。那么整个目录都将被被解压缩。

以下是两个例子

```
SRC_URI = "file://relativefile.patch"
SRC_URI = "file:///Users/ich/very_important_software"
```



# sstate共享状态

sstate是shared state的意思。用来支持部分构建的。

*Supports Partial Builds:* You can build and rebuild individual packages as needed. Yocto Project accomplishes this through its [Shared State Cache](https://docs.yoctoproject.org/overview-manual/concepts.html#shared-state-cache) (sstate) scheme. Being able to build and debug components individually eases project development.



从根本上说，从头构建是有吸引力的，

因为它意味着所有部件都是全新构建的，不存在可能导致问题的过时数据。

当开发人员遇到问题时，他们通常会默认从头开始构建，

这样他们从一开始就有一个已知的状态。



从零开始构建镜像对这个过程来说既是一个优点，也是一个缺点。

如前一段所述，从头开始构建可以确保一切都是最新的，并且从已知的状态开始。

然而，从头开始建设也需要更长的时间，因为它通常意味着重建不一定需要重建的东西。



Yocto Project实现了**支持增量构建**的共享状态代码。

共享状态代码的实现回答了以下问题，

这些问题是开放式增量构建支持系统中的基本障碍：

1、系统的哪些部分发生了变化，哪些部分没有发生变化？

2、如何删除和替换已更改的软件？

3、不需要从头开始重建的预构建组件在可用时如何使用？



对于第一个问题，构建系统通过创建任务输入的校验和（或签名）来检测给定任务的“inputs”中的更改。

如果校验和发生变化，系统假设输入已更改，需要重新运行任务。

对于第二个问题，共享状态（sstate）代码跟踪哪些任务向构建过程添加了哪些输出。

这意味着可以删除、升级或以其他方式操作给定任务的输出。

第三个问题的部分解决方案解决了第二个问题，假设构建系统可以从远程位置获取sstate对象，并在认为它们是有效的情况下安装它们。



在确定需要构建系统的哪些部分时，

**BitBake是以task为单位，而不是以recipe为单位。**

您可能会想知道为什么使用每个任务比每个配方优先级更高。



为了帮助解释，考虑启用IPK打包后端，然后切换到DEB。

在这种情况下，[do_install](http://www.yoctoproject.org/docs/3.1/ref-manual/ref-manual.html#ref-tasks-install) 和[do_package](http://www.yoctoproject.org/docs/3.1/ref-manual/ref-manual.html#ref-tasks-package) 任务输出仍然有效。

但是，使用按配方的方法，构建将不包括`.deb`文件。

因此，您必须使整个构建无效并重新运行它。

重新运行所有内容并不是最好的解决方案。

而且，在这种情况下，核心是必须“taught”很多关于具体任务的知识。

这种方法不能很好地扩展，并且不允许用户在不接触打包的登台核心的情况下轻松地在层中添加新任务或作为外部配方。



参考资料

https://blog.csdn.net/Neutionwei/article/details/111059587

# 添加一个driver 

https://blog.csdn.net/yangzhiwen56/article/details/50592845

新建目录mkdir recipes-kernel/chardriver

新建文件chardriver_0.1.bb，内容如下：

```
DESCRIPTION = "Chardriver kernel module out of the kernel tree"
LICENSE = "CLOSED"

PROVIDES = "virtual/kernel-module-chardriver"
RPROVIDES_${PN} = "virtual/kernel-module-driver"
RPROVIDES_${PN}-dev = "virtual/kernel-module-driver"

#PR = "r0"

inherit module

SRC_URI = "file://chardriver.c \
                file://Makefile \
"

S = "${WORKDIR}"
```

写driver的Makefile

```
obj-m := chardriver.o

SRC := $(shell pwd)

all:
        $(MAKE) -C $(KERNEL_SRC) M=$(SRC)

modules_install:
        $(MAKE) -C $(KERNEL_SRC) M=$(SRC) modules_install

clean:
        rm -f *.o *~ core .depend .*.cmd *.ko *.mod.c
        rm -f Module.markers Module.symvers modules.order
        rm -rf .tmp_versions Modules.symvers
```

编译bitbake chardriver

编译过程文件在tmp/work/imx6ulevk-poky-linux-gnueabi/chardriver/0.1-r0/

现在驱动编译是OK了，但查看镜像却没有我们的驱动，也是因为我们没把驱动加入系统

vi ../sources/meta-elmo/conf/layer.conf

```
MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS += "chardev"    #添加此2行代码，此行表示将驱动编译进系统，下面那行表示系统运行里加载驱动
KERNEL_MODULE_AUTOLOAD += "chardev"
```

# RREPLACES

# RPROVIDES

A list of package name aliases that a package also provides.

本package提供的一些alias。

例如dropbear是这样：

```
RPROVIDES_${PN} = "ssh sshd"
```

dropbear提供了ssh和sshd的别名。

而这个表示跟openssh会冲突。

```
RCONFLICTS_${PN} = "openssh-sshd openssh"
```



# native是指什么

native表示在服务器上使用的内容，跟板端相对。



# BBCLASSEXTEND

一般是这么用的

```
BBCLASSEXTEND = "native nativesdk"
```

我觉得跟buildroot的

```
$(eval $(host-generic-package))
```

作用类似。

表示编译一个host的版本。

# CVE_PRODUCT

```
CVE_PRODUCT = "dropbear_ssh"
```

就是在CVE上检查漏洞用哪个名字来查找。

# INITSCRIPT_NAME

这个表示安装到/etc/init.d下面的脚本的名字。

```
INITSCRIPT_NAME = "dropbear"
INITSCRIPT_PARAMS = "defaults 10"
```

# Feature Backfilling

有时候需要对MACHINE_FEATURES和DISTRO_FEATURES这2个变量进行extend。

用来控制前面被enable的功能，或者无法被disable的功能。

对于这种情况，我们需要添加一个额外的feature item

但是我们不想强制那些已经有变量值在conf文件里的开发者添加新的feature。

所以，yocto提供了一个机制，自动backfill这些被添加的feature

你可以在bitbake.conf里找到DISTRO_FEATURES_BACKFILL和MACHINE_FEATURES_BACKFILL这2个变量。

他们的值是这样的：

```
DISTRO_FEATURES_BACKFILL = "pulseaudio sysvinit gobject-introspection-data ldconfig"
MACHINE_FEATURES_BACKFILL = "rtc qemu-usermode"
```

因为上面这些feature默认就被backfill了。

如果你想要添加新的feature被backfilled，就需要使用这2个变量：

```
DISTRO_FEATURES_BACKFILL_CONSIDERED
MACHINE_FEATURES_BACKFILL_CONSIDERED
```



# DISTRO_FEATURES

一个feature的有还是没有，会影响相关的多个软件。

影响的是这些软件的configure的选项。

例如，你支持X11这个feature。

那么相关的软件的`--enable-x11`这样的选项都会被打开。

另外常用的feature是bluetooth和nfs。

feature并不对应一个软件package。而是跟多个package产生关系。

有些distro feature同时也是machine feature。对应的就是combined feature

支持的features列表如下：

```
alsa
api-documentation
	是否编译时产生对应的文档。
bluetooth 支持蓝牙功能
cramfs
directfb
ext2
ipsec
ipv6
keyboard
ldconfig
nfs
opengl
pci
ptest
	表示package test，是否编译package下面的test内容。
systemd
usbgadaget
usbhost
usrmerge
	合并/usr目录。
wayland
wifi
x11
```

现在实际使用中发现问题。

我在amlogic-sbr-yocto.bb这个image的bb里修改DISTRO_FEATURES。

对于我单独编译某一个package时，没有起作用。

所以bb里改的，都是局部的。

要全局的改动。还是要在local.conf里做。

但是build/local.conf的改动，怎么进行保存呢？因为build目录是生成的临时目录。

知道了。mesona5-av400.conf，conf文件都是全局的。在这个里面加也是可以的。

之前的改动也是在这里。

# COMBINED_FEATURES

bluetooth就是一个典型例子。



# MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS

essential表示必要。

对应一个list，

包含的是一组推荐的，机器相关的package，安装到image里去。

build过程不依赖这些package。

会影响基于packagegroup-core-boot 的image。

一般来说，这个变量是用来处理必要的内核模块。

而且这个模块是会被编译进kernel image，而不是单独成一个ko文件。

这样的情况下，不会产生一个package。



参考资料

https://blog.csdn.net/qq_27149449/article/details/119188694



# OVERRIDES

```
OVERRIDES .= ":av400:onepass"
```

这个怎么理解？

https://docs.yoctoproject.org/ref-manual/variables.html?highlight=machineoverrides#term-OVERRIDES

OVERRIDES代表的是build时的state。

例如，一个an-override的字符串，出现在OVERRIDES的值里。

则下面的语句的影响是：FOO会被overridden覆盖掉。

```
FOO:an-override = "overridden"
```

这个是bitbake的条件语句语法的一部分。

https://docs.yoctoproject.org/bitbake/2.0/bitbake-user-manual/bitbake-user-manual-metadata.html#conditional-syntax-overrides

bitbake使用OVERRIDES来控制哪些变量被覆盖。

在bitbake解析了recipe和conf文件后。



你可以使用OVERRIDES来选择一个指定的版本。

OVERRIDES只能使用小写字母、数字和中划线。

注意，不能使用冒号。

下面是一个例子

```
OVERRIDES = "architecture:os:machine"
TEST = "default"
TEST:os = "osspecific"
TEST:nooverride = "othercondvalue"
```

`OVERRIDES` 变量列出了三个替代（条件）：“`architecture`”，“`os`”和“`machine`”。



```
DEPENDS = "glibc ncurses"
OVERRIDES = "machine:local"
DEPENDS:append:machine = "libmad"
```

上面语句的最终效果是：

```
DEPENDS值变成了"glibc ncurses libmad"
```



https://blog.csdn.net/weixin_44410537/article/details/108004470

https://www.cnblogs.com/chegxy/p/15731481.html#tid-zSnFS3

在bitbake中，一个变量可能有多个版本。

为了能够将变量切换到某个版本。

我们可以将版本的名字添加到OVERRIDES变量中。

通常情况下，我们用`:`来追加一个版本名称到变量名后。

一次表示不同版本的变量。

```
VAR = "var"
VAR:a = "vara"
VAR:b = "varb"
```

如果你使用VAR这个变量，你会发现它的值始终是var，

那么怎么使用其他版本的VAR呢？

这个就需要用到OVERRIDES机制了。

bitbake在解析完所有内容之后，会查看OVERRIDES变量。

（这个变量是由多个字符串组成）

然后bitbake会将有多个版本的变量替换为OVERRIDS变量里指定的版本。

例如，我们现在选择a版本。

```
OVERRIDES = "a"
```

基于这个代码搭建bitbake环境。

https://github.com/teddyxiong53/bbTutorial

然后在meta-tutorial目录下新建third目录和third_1.0.bb文件。

写入下面的内容：

```
DESCRIPTION = "Prints Hello World"
PN = 'printhello'
PV = '1'

OVERRIDES = "a:b"
VAR1 = "var"
VAR1_a = "vara"
VAR1_a_append = "a"
VAR2 = "var"
VAR2_b = "varb"
VAR2_append_b = "b"
VAR3 = "var"
VAR3_a_append = "a"
VAR4 = "var"
VAR4_append_b = "b"
VAR5 = "var"
VAR5_a = "vara"
VAR5_a_append = "a"
VAR5_a_append = "a"

python do_build() {
    bb.plain("********************");
    bb.plain("*                  *");
    bb.plain("*  Hello, World!   *");
    bb.plain("*                  *");
    bb.plain("********************");
    bb.plain("OVERRIDES: " + d.getVar("OVERRIDES", True));
    bb.plain("VAR1: " + d.getVar("VAR1", True));
    bb.plain("VAR2: " + d.getVar("VAR2", True));
    bb.plain("VAR3: " + d.getVar("VAR3", True));
    bb.plain("VAR4: " + d.getVar("VAR4", True));
    bb.plain("VAR5: " + d.getVar("VAR5", True));
}
```

运行结果是这样：

```
********************
*                  *
*  Hello, World!   *
*                  *
********************
OVERRIDES: task-build:a:b
VAR1: vara
VAR2: varbb
VAR3: a
VAR4: varb
VAR5: vara
```



当前的overrides展开是这样

```
OVERRIDES="linux:aarch64:pn-defaultpkgname:aarch64:armv8a:mesona5-av400:client:poky:dunfell:class-target:libc-glibc:forcevariable:a5:smarthome_kernel64:av400:onepass"
```



```
LIBCOVERRIDE=":libc-glibc"
DISTROOVERRIDES="poky:dunfell"
MACHINEOVERRIDES="aarch64:armv8a:mesona5-av400:client"
```

```
TOPDIR="/mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/build-av400"
SSTATE_DIR="/mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/build-av400/../sstate-cache"
```

这些为什么不导出？

```
# Make sure MACHINE isn't exported
# (breaks binutils at least)
MACHINE[unexport] = "1"
```

```
BUILD_SYS="x86_64-linux"
TARGET_SYS="aarch64-poky-linux"
export prefix="/usr"
```

## 实际使用

我发现OVERRIDES机制并不符合我的预期。

```
PACKAGES =+ "\
    ${PN}-wifi-power \
    ${PN}-usb-monitor \
"
PACKAGES_av400 =+ ""
```

PACKAGES_av400相当于 PACKAGES变量整个都清空了。



# MACHINEOVERRIDES

一个list，用冒号分割，



# 自己加DISTRO_FEATURE

看amlogic的代码，有这样的：

```
DISTRO_FEATURES_append = " aml-dtv "
```

按我的理解，DISTRO_FEATURES就是官方的那10几个。这个aml-dtv是怎么可以被当成DISTRO_FEATURES的？

搜索一下。

在这里：

```
./recipes-core/images/packagegroup-amlogic-baserootfs.bb:    ${@bb.utils.contains('DISTRO_FEATURES', 'aml-dtv', 'aml-dtvdemod', '', d)} \
```

这样DISTRO_FEATURES实际上退化成跟package一一对应了。

也有非一一对应的。

```
    ${@bb.utils.contains('DISTRO_FEATURES', 'optee', 'optee-userspace', '', d)} \
    ${@bb.utils.contains('DISTRO_FEATURES', 'optee', 'tee-supplicant', '', d)} \
    ${@bb.utils.contains('DISTRO_FEATURES', 'optee', 'optee-video-firmware', '', d)} \
```



./aml-comp/prebuilt/hosttools/aml-image-packer/a5/aml_upgrade_package.conf



# image features

https://docs.yoctoproject.org/ref-manual/features.html#ref-features-image

```
allow-empty-password
	允许dropbear和openssh使用空密码进行登陆。
dbg-pkgs
	安装调试工具。
debug-tweaks
dev-pkgs
doc-pkgs
empty-root-password
overlayfs-etc
package-management
post-install-logging
ptest-pkgs
read-only-rootfs
splash 开机画面
staticdev-pkgs

tools-debug
	安装strace、gdb等工具。
tools-sdk
x11
x11-base
x11-sato
```

# 只读rootfs

添加`read-only-rootfs`到IMAGE_FEATURES。

```
可以这样
IMAGE_FEATURES += "read-only-rootfs"
也可以这样
EXTRA_IMAGE_FEATURES = "read-only-rootfs"
```

# IMAGE_INSTALL

通过这个变量来指定要安装到image里的软件。

是通过image.bbclass来做的。

一下辅助的bbclass，例如core-image，会把IMAGE_FEATURES转换成IMAGE_INSTALL。

需要注意的是：

当使用core-image-minimal-initramfs的时候，

不要使用IMAGE_INSTALL来指定要安装的包。

而要使用PACKAGE_INSTALL变量。





## PACKAGE_INSTALL

PACKAGE_INSTALL和IMAGE_INSTALL关系？



注意与`FILES`差异，`FILES`是指明软件包内部哪些文件需要参与打包，

而`IMAGE_INSTALL`是指明哪个软件包需要参与打包。



这个文档不错。对于一些概念解释比较清楚。

https://www.icode9.com/content-4-1287459.html

# 创建initramfs

步骤如下：

1、创建一个initramfs 配方，参考core-image-minimal-initramfs.bb。

2、确定是否要把initramfs打包到kernel镜像里。把INITRAMFS_IMAGE_BUNDLE变量设置为1 。

这个是推荐的，可以避免循环依赖。

3、通过PACKAGE_INSTALL变量控制initramfs里的内容。

initramfs默认安装了这些

```
PACKAGE_INSTALL = "${INITRAMFS_SCRIPTS} ${VIRTUAL-RUNTIME_base-utils} udev base-passwd ${ROOTFS_BOOTSTRAP_INSTALL}"
```



INITRAMFS_SCRIPTS

包含的脚本在这个目录下

Z:\work\a113x2\yocto-code\code\poky\meta\recipes-core\initrdscripts\initramfs-framework_1.0.bb



amlogic的PACKAGE_INSTALL

```
PACKAGE_INSTALL += "base-files netbase ${VIRTUAL-RUNTIME_base-utils} ${VIRTUAL-RUNTIME_dev_manager} base-passwd ${ROOTFS_BOOTSTRAP_INSTALL} initramfs-meson-boot e2fsprogs "
```



# IMAGE_ROOTFS_SIZE

定义image的大小，单位是KB。

yocto计算的逻辑是这样的：

```
if (image-du * overhead) < rootfs-size:
    internal-rootfs-size = rootfs-size + xspace
else:
    internal-rootfs-size = (image-du * overhead) + xspace
where:
    image-du = Returned value of the du command on the image.
    overhead = IMAGE_OVERHEAD_FACTOR
    rootfs-size = IMAGE_ROOTFS_SIZE
    internal-rootfs-size = Initial root filesystem size before any modifications.
    xspace = IMAGE_ROOTFS_EXTRA_SPACE
```



# variable flags

我是看这个

```
create_version_file[vardepsexclude] += "DATETIME"
```

vardepsexclude表示什么含义？

在bitbake的手册里搜索，找到是属于variable flags这个章节。

variable flags又表示什么含义呢？

用来控制一个task的概念和依赖。

简称为varflags。

bitbake预定义了一组varflags。给recipe和class用。

```
dirs
	指定在task执行之前应该创建的目录。
cleandirs
	task执行前应该创建的空目录。
noexec
	标记task为空，且不执行，一般做为占位符使用。
nostamp
	告诉bitbake不要给这个task创建时间戳文件，这样就每次都会执行。
	do_aml_pack[nostamp] = "1"
fakeroot
	让一个task在fakeroot的环境里执行。
umask
	在这个umask下执行这个task。
deptask
	控制task的编译时依赖。
rdeptask
	控制task的运行时依赖。
depends
	控制inter-task依赖。
rdepends
	控制inter-task运行时依赖。
postfuncs
	在task之后执行的函数。
prefuncs
	在task之前执行的函数。
vardeps
	
```

## vardepsexclude

字面含义是变量依赖排除。

表示：从变量的依赖里排除掉。

具体怎么理解？这里有说明。

https://blog.csdn.net/Neutionwei/article/details/111059587

共享状态代码使用校验和（任务输入的唯一签名）来确定任务是否需要再次运行。

因为任务输入的更改会触发重新运行，

因此流程需要检测给定任务的所有输入。

对于shell任务，这是相当容易的，

因为构建过程为每个任务生成一个“run”shell脚本，并且可以创建一个校验和，

可以很好地了解任务的数据何时更改。

使问题复杂化的是，有些东西不应该包括在校验和中。

首先，有一个给定任务的实际特定构建路径—[WORKDIR](http://www.yoctoproject.org/docs/3.1/ref-manual/ref-manual.html#var-WORKDIR)。

工作目录是否更改并不重要，

因为它不应影响目标包的输出。

此外，**构建过程的目标是使本机包或跨包可重定位。**

注意：本机包和交叉包都在构建主机上运行。

但是，跨包为目标体系结构生成输出。

因此校验和需要排除`WORKDIR`。

排除工作目录的简单方法是将`WORKDIR`设置为某个固定值，并为“run”脚本创建校验和。

另一个问题来自“run”脚本，

这些脚本包含可能被调用或可能未被调用的函数。

增量构建解决方案包含用于计算shell函数之间依赖关系的代码。

这段代码用于将“run”脚本缩减到最小值集，从而缓解了这个问题，并使“run”脚本更具可读性。

到目前为止，shell脚本的解决方案已经存在。

Python任务呢？

即使这些任务比较困难，也可以采用同样的方法。

这个过程需要弄清楚Python函数访问的变量以及它调用的函数。

同样，增量构建解决方案包含的代码首先确定变量和函数的依赖关系，

然后为用作任务输入的数据创建校验和。

**像`WORKDIR` 的例子一样，存在依赖关系应该被忽略的情况。对于这些情况，可以使用如下行指示生成过程忽略依赖项：**

```html
PACKAGE_ARCHS[vardepsexclude] = "MACHINE"     
```



此示例确保[PACKAGE_ARCHS](http://www.yoctoproject.org/docs/3.1/ref-manual/ref-manual.html#var-PACKAGE_ARCHS) 变量不依赖于[MACHINE](http://www.yoctoproject.org/docs/3.1/ref-manual/ref-manual.html#var-MACHINE)的值，即使它引用了[MACHINE](http://www.yoctoproject.org/docs/3.1/ref-manual/ref-manual.html#var-MACHINE)的值。

同样，在某些情况下，您需要添加BitBake无法找到的依赖项。您可以使用以下行来完成此操作：

```html
PACKAGE_ARCHS[vardeps] = "MACHINE"
```

作为一个例子，考虑一个内嵌Python的例子，

BitBake无法找出依赖关系。

在调试模式下运行（即使用`-DDD`）时，

BitBake会在发现无法确定依赖关系的内容时生成输出。



到目前为止，仅讨论对任务的直接投入。

基于直接输入的信息在代码中称为“basehash”。

但是，任务的间接输入问题仍然存在——已经构建并存在于[Build Directory](http://www.yoctoproject.org/docs/3.1/ref-manual/ref-manual.html#build-directory)中的项目。

特定任务的校验和（或签名）需要添加特定任务所依赖的所有任务的哈希值。

选择要添加的依赖项是一个策略决策。

然而，其效果是生成一个主校验和，它结合了basehash和任务依赖项的散列。



在代码级别上，存在多种方法可以影响basehash和依赖任务哈希。

在BitBake配置文件中，可以为BitBake提供一些额外的信息，以帮助它构造basehash。

下面的语句有效地生成了一个全局变量依赖排除列表（即变量从未包含在任何校验和中）：

```
BB_HASHBASE_WHITELIST ?= "TMPDIR FILE PATH PWD BB_TASKHASH BBPATH DL_DIR \
     SSTATE_DIR THISDIR FILESEXTRAPATHS FILE_DIRNAME HOME LOGNAME SHELL TERM \
     USER FILESPATH STAGING_DIR_HOST STAGING_DIR_TARGET COREBASE PRSERV_HOST \
     PRSERV_DUMPDIR PRSERV_DUMPFILE PRSERV_LOCKDOWN PARALLEL_MAKE \
     CCACHE_DIR EXTERNAL_TOOLCHAIN CCACHE CCACHE_DISABLE LICENSE_PATH SDKPKGSUFFIX"
```



前面的例子排除了[WORKDIR](http://www.yoctoproject.org/docs/3.1/ref-manual/ref-manual.html#var-WORKDIR) ，

因为该变量实际上是作为[TMPDIR](http://www.yoctoproject.org/docs/3.1/ref-manual/ref-manual.html#var-TMPDIR)中的路径构造的，[TMPDIR](http://www.yoctoproject.org/docs/3.1/ref-manual/ref-manual.html#var-TMPDIR)位于白名单中。



决定通过依赖链包含哪些依赖任务哈希的规则更为复杂，

通常使用Python函数来完成。

`meta/lib/oe/sstatesig.py`显示了两个示例，

并说明了如何在需要时将自己的策略插入到系统中。

这个文件定义了[OE-Core](http://www.yoctoproject.org/docs/3.1/ref-manual/ref-manual.html#oe-core)使用的两个基本签名生成器：“OEBasic”和“OEBasicHash”。

默认情况下，BitBake中启用了一个虚拟的“noop”签名处理程序。

这意味着行为与以前的版本没有变化。

默认情况下，OE-Core通过中的此设置使用“OEBasicHash”签名处理程序`bitbake.conf`文件：

```html
BB_SIGNATURE_HANDLER ?= "OEBasicHash" 
```









https://forums.openpli.org/topic/41447-how-to-get-rid-of-taskhash-mismatch/

# native概念

在tmp/work/x86_64-linux目录下，有很多xx-native的包。例如：

```
acl-native           
aml-hosttools-native 
aml-img-packer-native
android-tools-native 
```

native应该就相当于buildroot里的host概念。

tmp/work下面这4个目录的用途：

```
aarch64-poky-linux
	所有aarch64都可以用的包编译放在这下面。
all-poky-linux
	这个是对于x86、aarch这些都是可以用的。都是一些文本文件类的。
mesona5_av400-poky-linux
	这个是av400特有的一些包。
x86_64-linux
	这个是x86的包，就是一些xx-native的包。
```

# 编译kernel和uboot

```
KERNEL_DEVICETREE = "a5_a113x2_av400_1g.dtb "
UBOOT_MACHINE = "a5_av400"
```

指定的这2个变量，是怎么传递使用的？

KERNEL_DEVICETREE这个是官方定义的。

是dtb文件，而不是dts文件。

要使用这个变量，需要inherit kernel-devicetree这个bbclass。

另外，是怎么指定使用自己的kernel仓库的？

应该是mesona5-av400.conf里这一行指定的：

```
include conf/machine/include/mesona5_k5.4_64b.inc
```

在meta-meson里，是这个bb文件。怎么指定到这个文件的？

Z:\work\a113x2\yocto-code\code\meta-meson\recipes-kernel\linux\linux-meson_5.4.bb

在Z:\work\a113x2\yocto-code\code\meta-meson\conf\machine\include\amlogic_common.inc里，指定了：

```
PREFERRED_PROVIDER_virtual/kernel ?= "linux-meson"
```



```
AML_GIT_ROOT ?= "git.myamlogic.com"
AML_GIT_PROTOCOL ?= "git"
AML_GIT_ROOT_YOCTO_SUFFIX ?= "/yocto"
AML_GIT_ROOT_PR ?= "git.myamlogic.com"
AML_GIT_ROOT_WV ?= "git.myamlogic.com"
AML_GIT_ROOT_PROTOCOL ?= "git"
```



```
AML_RDK_PREBUILT_SITE ?= "http://10.18.11.6/shanghai/image/linux-distro/Public/YOCTO/prebuilt/"
```

最终是这里确定的kernel版本。

```
PREFERRED_VERSION_u-boot = "v2019.%"
PREFERRED_VERSION_linux-meson = "5.4.%"
OVERRIDES .= ":a5:smarthome_kernel64"
```



```
PROVIDES = "virtual/bootloader"
```



# DISTROOVERRIDES

冒号分割的list。

默认是包含DISTRO变量的内容。

而DISTRO表示的是发行版的short name。

例如poky这个名字。

而long name，是对应DISTRO_NAME这个变量。

如果DISTRO变量没有被赋值，那么使用的是meta/conf/distro/defaultsetup.conf这个里面的值。

```
IMAGE_LINGUAS ?= "en-us en-gb"

DISTRO_FEATURES_DEFAULT ?= "acl alsa argp bluetooth ext2 ipv4 ipv6 largefile pcmcia usbgadget usbhost wifi xattr nfs zeroconf pci 3g nfc x11 vfat"
DISTRO_FEATURES ?= "${DISTRO_FEATURES_DEFAULT}"
IMAGE_FEATURES ?= ""
```

# TCMODE

TC是toolchain的缩写。



# EXTRA_IMAGEDEPENDS

一组recipe，不会install到rootfs里的。

用来构建image，但是不需要install 到rootfs的一些package。

典型就是bootloader。

```
EXTRA_IMAGEDEPENDS += "u-boot"
```

在这里使用的：

```
./meta/classes/image.bbclass:143:        for dep in (d.getVar('EXTRA_IMAGEDEPENDS') or "").split():
```



# TARGET_PREFIX

这个哪里定义的？怎么传递的？

https://docs.yoctoproject.org/ref-manual/variables.html?highlight=target_prefix#term-TARGET_PREFIX

**TARGET_PREFIX的值根据情况变化：**

1、对于target的，值是TARGET_SYS

2、对于native的，是BUILD_PREFIX

3、对于nativesdk的，是SDK_PREFIX

## TARGET_SYS

你不需要自己设置TARGET_SYS的值。

yocto会自动基于 [TARGET_ARCH](https://docs.yoctoproject.org/ref-manual/variables.html?highlight=target_prefix#term-TARGET_ARCH), [TARGET_VENDOR](https://docs.yoctoproject.org/ref-manual/variables.html?highlight=target_prefix#term-TARGET_VENDOR), and [TARGET_OS](https://docs.yoctoproject.org/ref-manual/variables.html?highlight=target_prefix#term-TARGET_OS) variables. 来设置。

Consider these two examples:

- Given a native recipe on a 32-bit, x86 machine running Linux, the value is “i686-linux”.
- Given a recipe being built for a little-endian, MIPS target running Linux, the value might be “mipsel-linux”.

TARGET_ARCH在哪里被设置的？

在bitbake.conf里来定义，来自于TUNE_ARCH，

而TUNE_ARCH是这里：

```
./conf/machine/include/arm/arch-armv8a.inc:90:TUNE_ARCH = "${@bb.utils.contains('TUNE_FEATURES', 'aarch64', '${TUNE_ARCH_64}', '${TUNE_ARCH_32}' ,d)}"
```



# deploy

这个bbclass的作用是通过sstate来加速deploy的步骤。

# require、include、inherit的区别

BitBake 有两种指令引用文件：

- `include filename`，这是一种可选引用，如果 filename 找不到，不会有 error 产生；
- `require filename`，如果 filename 没找到，会产生 error。

值得一提的是，include 和 require 都是在 BBPATH 中指定的目录查找 filename。



参考资料

这篇文档翻译比较好，写得清晰。

https://blog.csdn.net/Archer1991/article/details/62423014
https://www.cnblogs.com/zxc2man/p/14545663.html



# bluez5.inc文件分析

```
SUMMARY
	这个信息是给rpm、opkg这些包管理器看的。不超过72个字符。
	如果没有写DESCRIPTION，同时会把SUMMARY当成DESCRIPTION用。
DESCRIPTION
	还是给包管理器看的。
HOMEPAGE
	这个是更详细的信息。
SECTION
	这个也是给包管理器看的分类信息。
LICENSE
	使用的license。详细规则见后面。
LIC_FILES_CHKSUM
	专门关注协议文档的变化，因为协议变更是很严重的。
	所有配方文件必须定义此变量（除非LICENSE设置为“CLOSED”）。
	
DEPENDS
	build时的依赖。
	依赖的内容是其他的配方文件名字。
	bitbake会保证本配置执行时，依赖的东西都已经被build，而且已经被安装到sysroot下面。
	DEPENDS 使得配方“a”的do_configure任务取决于配方“b”的do_populate_sysroot任务。 	  这意味着当配方“a”正在配置自身时，配方“b”放入sysroot的任何内容都必须可用。
PROVIDES
	提供本配方的别名。
	默认情况下，PROVIDES里加入了PN。也就是别名跟本名是一致的。
	例如liav，你可以给它起别名为libpostproc。
	那么这么写：
	PROVIDES += "libpostproc"
	你就可以在其他的地方使用libpostproc来指代libav了。
	
RPROVIDES
	运行时依赖的包提供别名。
RCONFLICTS
	冲突包。
	一般这样：RCONFLICTS _ $ {PN} =“foo（> = 1.2）”
PACKAGECONFIG
	这个是用打开或者关闭软件的某些feature。
	基本格式是：
	PACKAGECONFIG ?? =“f1 f2 f3 ...”
    PACKAGECONFIG [f1] =“--with-f1， - without-f1，build-deps-f1，rt-deps-f1”
    PACKAGECONFIG [f2] =“--with-f2， - without-f2，build-deps-f2，rt-deps-f2”
    PACKAGECONFIG [f3] =“--with-f3， - without-f3，build-deps-f3，rt-deps-f3”
EXTRA_OECONF
	指定configure的参数。
S
	源代码解压后，在build目录下的位置。
	此位置在工作目录（WORKDIR）中，且不是静态的。
	$ {WORKDIR} / $ {PN} - $ {PV}
D
	目标目录。do_install任务在build目录中安装组件的位置。
ALLOW_EMPTY
	如果输出包为空，仍然应该生成包。 默认情况下，BitBake不产生空包。
PACKAGES
	配方创建的包的列表。
SYSTEMD_SERVICE
	如果配方继承了systemd类，那么此变量为配方生成包的指定了systemd的服务名称
	
RDEPENDS
	RDEPENDS使得配方“a”的do_build任务取决于配方“b”的do_package_write_ipk任务。
	这意味着当构建配方“a”时，“b”的包文件必须可用。
	更重要的是，以包管理器理解的方式，包“a”将被标记为依赖于包“b。
INITSCRIPT_PACKAGES
	包含初始化的软件包列表。 
	如果有多个包，则应该使用带有附加的包名称的形式的变量名。
	只有配方继承update-rc.d.bbclass，此变量才可使用。
	该变量是可选的且默认为值为PN。
INITSCRIPT_NAME
	安装到$ {sysconfdir} /init.d的初始化脚本名。
	只有配方继承update-rc.d.bbclass，此变量才可使用。 此变量是必需的。
EXCLUDE_FROM_WORLD
	排除在bitbake world命令之外。
```

bitbake里的配置

```
SECTION = "base"
PRIORITY = "optional"
SUMMARY ?= "${PN} version ${PV}-${PR}"
DESCRIPTION ?= "${SUMMARY}."

LICENSE ??= "INVALID"
MAINTAINER = "OE-Core Developers <openembedded-core@lists.openembedded.org>"
HOMEPAGE = ""

T = "${WORKDIR}/temp"
D = "${WORKDIR}/image"
S = "${WORKDIR}/${BP}"
B = "${S}"

OLDEST_KERNEL = "3.2.0"

export MAKE = "make"
EXTRA_OEMAKE = ""
EXTRA_OECONF = ""
export LC_ALL = "en_US.UTF-8"
export TZ = 'UTC'

DISTRO ??= "nodistro"
DISTRO_NAME ??= "OpenEmbedded"

BB_NUMBER_THREADS ?= "${@oe.utils.cpu_count()}"

MACHINE_FEATURES ?= ""
DISTRO_FEATURES ?= ""


```



# LICENSE规则

配方的源文件LICENSE列表。LICENSE需遵循以下规则：
　　（1）不要在单个LICENSE名称中使用空格。
　　（2）当LICENSE可选择多个时，使用 | 分隔LICENSE。
　　（3）当存在涵盖源文件的不同部分的多个LICENSE时，使用 ＆ 分隔LICENSE。
　　（4）您可以在LICENSE名称之间使用空格。
　　（5）对于标准LICENSE，请使用meta / files / common-licenses /中的LICENSE，或者在meta / conf / licenses.conf中定义的具有SPDXLICENSEMAP标志的LICENSE。
下面是一些例子：

 LICENSE =“LGPLv2.1 | GPLv3”
 LICENSE =“MPL-1＆LGPLv2.1”
 LICENSE =“GPLv2 +”

第一个示例来自Qt的配方，源文件可以选择LGPLv2.1或GPLv3许可。第二个示例来自Cairo，其中两个 LICENSE涵盖源代码的不同部分。最后一个示例来自sysstat，它提供了一个单一的 LICENSE。
您还可以针对每个包指定 LICENSE以处理输出组件具有不同的LICENSE情况。例如，如果某个软件的代码根据GPLv2许可，但是文档却根据GNU 1.2自由文档许可，其LICENSE可以被规定如下：

```
LICENSE =“GFDL-1.2＆GPLv2”
LICENSE _ $ {PN} =“GPLv2”
LICENSE _ $ {PN} -doc =“GFDL-1.2”
```

amlogic的meta-meson，LICENSE统一这样指向同一个文件了。

```
LIC_FILES_CHKSUM = "file://${COREBASE}/../meta-meson/license/COPYING.GPL;md5=751419260aa954499f7abaabaa882bbe"
```



# amlogic uboot的bb文件

这样来指定代码目录。

```
S = "${WORKDIR}/uboot-repo"
SRCREV_FORMAT = "bl2_bl30_src_ao_bl31_bl31-1.3_bl32-3.8_bl33_fip"
PR = "r1"
PV = "v2019.01+git${SRCPV}"
```



# 强制一个package每次都重新编译

在对应的bb文件里写上：

```
do_compile[nostamp] = "1"
```

如果还想要每次都重新执行configure，则写上：

```
do_configure[nostamp] = "1"
```



https://stackoverflow.com/questions/46688182/how-to-force-package-to-be-recompiled-on-yocto



# do_image_complete执行时机



https://www.icode9.com/content-4-1287459.html



# avs-sdk的编译

下面语句的含义是：使用git仓库的最新版本的代码。

```
SRCREV = "${AUTOREV}"
```



# INSANE_SKIP

跳过对so文件的检查。

```
INSANE_SKIP_${PN} = "dev-elf dev-so textrel"
INSANE_SKIP_${PN}-dev = "dev-elf dev-so"
```



构建配方时，OpenEmbedded 构建系统会对输出执行各种 QA 检查，以确保检测和报告常见问题。

虽然忽略 QA 消息甚至禁用 QA 检查很诱人，但最好尝试解决任何报告的 QA 问题。



https://blog.csdn.net/happybeginner/article/details/122339305

https://blog.csdn.net/qq_15269787/article/details/119829987

这个里面的demo写得不错。

https://blog.csdn.net/BGK112358/article/details/83827172

这篇讲了常见问题的解决。

https://blog.csdn.net/punmpkin/article/details/103135537

# 工具链toolchain的生成

downloads目录下只有这2个压缩包：

```
gcc-9.3.0.tar.xz
gcc-linaro-7.3.1-2018.05-x86_64_aarch64-elf.tar.xz
```



# `tmp/work-shared`目录

为了提高效率，yocto用这个目录来存放某些recipe，这些recipe的特点是跟其他的recipe共用了work目录。

在实际使用中，这个只给gcc使用

```
gcc-cross
libgcc
gcc-runtime
```



# do_build和do_compile关系

listtasks看到的帮助信息里写的：

```
do_build                       Default task for a recipe - depends on all other normal tasks required to 'build' a recipe

do_compile                     Compiles the source in the compilation directory
```







这个phytec对外可见的confluence，挺好的

https://wiki.phytec.com/pages/viewpage.action?pageId=69501955

这家公司的官网

http://www.phytec.cn/

查看kernel使用的哪个版本

```
bitbake virtual/kernel -e | grep "PREFERRED_PROVIDER_virtual/kernel"
```

查看bootloader使用的版本

```
bitbake virtual/bootloader -e | grep "PREFERRED_PROVIDER_virtual/bootloader"
```



# yocto调试工具

## 从失败的任务中查看日志

可以在`${WORKDIR}/temp/log.do_taskname`文件中找到任务的日志。

## 使用`devshell`

在调试某些命令甚至只是编辑包时，

`devshell`可能是一个有用的工具。

当调用`devshell`时，将为指定的目标运行到`do_patch`之前和包括`do_patch`在内的所有任务。

然后，打开一个新终端，并将放置在源目录`${S}`中。

在新的终端中，仍然定义了所有与构建相关的`OpenEmbedded`环境变量，

因此可以使用`configure`和`make`等命令。

这些命令执行起来就像`OpenEmbedded`构建系统正在执行它们一样。

因此，在调试构建或准备与`OpenEmbedded`构建系统一起使用的软件时，这种方法非常有用。

```
bitbake android-tools-adbd -c devshell
```

在这个环境中，可以运行`configure`或`compile`命令，就好像它们是由`OpenEmbedded`构建系统本身运行的一样。如前所述，工作目录也会自动更改为源目录。

值得记住的是，在使用devshell时，需要使用完整的编译器名称，比如arm-poky-linux-gnuea -gcc，而不是仅仅使用gcc。这同样适用于其他应用程序，如binutils、libtool等。BitBake设置了环境变量，比如CC来帮助应用程序，比如make来找到正确的工具。

```
which make
/mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/build-av400/tmp/hosttools/make
```

使用devshell带来了哪些便利呢？

大家一般在什么情况下使用devshell呢？

感觉也没有特别有用。可能就是在频繁编译的时候，可以少敲一些字符吧。



我现在就碰到一个情况，感觉需要借助devshell。

alsa-lib的编译，为什么没有看到c文件？



参考资料

https://blog.csdn.net/weixin_44410537/article/details/90734459

# cflags等编译选项的传递和修改

在bb文件里

```
TARGET_CFLAGS_append = "xx"
```



# u-boot的编译分析

怎么定位到这个代码目录的？

```
NOTE: u-boot: compiling from external source tree /mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/aml-comp/uboot
```

是需要inherit externalsrc

Z:\work\a113x2\yocto-code\code\meta-meson\conf\machine\include\amlogic_externalsrc.inc

```
./conf/machine/include/amlogic_common.inc:2:include conf/machine/include/amlogic_externalsrc.inc
```

这个文件包含了amlogic_common.inc

Z:\work\a113x2\yocto-code\code\meta-meson\conf\machine\include\mesona5_k5.4_64b.inc

还定义了

```
PREFERRED_VERSION_u-boot = "v2019.%"
PREFERRED_VERSION_linux-meson = "5.4.%"
OVERRIDES .= ":a5:smarthome_kernel64"
```

`OVERRIDES .= ":a5`这个就表示有些带后缀的，使用带_a5后缀的版本。



```
EXTERNALSRC_pn-linux-meson = "${@'${MESON_ROOT_PATH}/aml-comp/kernel/aml-5.4' if (os.path.isdir('${MESON_ROOT_PATH}/aml-comp/kernel/aml-5.4')) else ''}"
```



```
+ export
 CROSS_COMPILE=aarch64-elf-
+ unset SOURCE_DATE_EPOCH
+ UBOOT_TYPE=a5_av400
+ LDFLAGS= ./mk a5_av400
```

编译出来的文件在这里：

```
hanliang.xiong@walle01-sz:~/work/a113x2/yocto-code/code/aml-comp/uboot/build$ ls -lh
total 11M
-rw-r--r-- 1 hanliang.xiong szsoftware 2.0M Jun 21 11:08 a5_av400-u-boot.aml.zip
-rw-r--r-- 1 hanliang.xiong szsoftware 3.1M Jun 21 11:08 u-boot.bin.sd.bin.signed
-rw-r--r-- 1 hanliang.xiong szsoftware 3.1M Jun 21 11:08 u-boot.bin.signed
-rw-r--r-- 1 hanliang.xiong szsoftware 3.1M Jun 21 11:08 u-boot.bin.usb.signed
```

uboot的o文件就生成在这个目录下

```
aml-comp/uboot/bl33/v2019/build
```

因为build目录整个都是在gitignore里。所以编译对git没有影响。

但是这个目录有起什么作用呢？

```
/mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/build-av400/tmp/work/mesona5_av400-poky-linux/u-boot/v2019.01+git999-r1/u-boot-v2019.01+git999/
```

没有uboot的代码编译o文件。都是一些yocto需要的文件。

这样install了

```
install /mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/aml-comp/uboot/fip/u-boot.bin.signed /mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/build-av400/tmp/work/mesona5_av400-poky-linux/u-boot/v2019.01+git999-r1/deploy-u-boot/u-boot-mesona5-av400-v2019.01+git999-r1.bin.signed
```

对应的代码是u-boot-meson.inc里的do_deploy

```
do_deploy () {
    install -d ${DEPLOYDIR}
    install ${S}/fip/${UBOOT_BINARY} ${DEPLOYDIR}/${UBOOT_IMAGE}
```



https://wiki.koansoftware.com/index.php/Building_Software_from_an_External_Source



# devtool

https://docs.yoctoproject.org/ref-manual/devtool-reference.html

现在已经做了一段时间的yocto。觉得有必要把devtool研究一下了。

devtool是一个命令行工具。

提供了一些功能，帮助你build、test和打包软件。

这个命令是跟随bitbake一起提供的。

```
常用的命令是：

add                      添加recipes

modify                  提取源码

upgrade               更新recipes

search                   搜索package
```



```
devtool modify busybox
```

这个命令会把busybox的代码拷贝到workspace目录下面。

这个时候在构建项目，则使用的是workspace目录下的源码，如下所示：

参考资料



https://blog.csdn.net/jiangwei0512/article/details/120407354



https://blog.csdn.net/qq_34160841/article/details/107287365

# PREFERRED_VERSION

```
PREFERRED_VERSION_u-boot = "v2019.%"
PREFERRED_VERSION_linux-meson = "5.4.%"
```



# STAGING相关变量

STAGING_DIR_NATIVE，对于uboot，这个目录是在：

```
/mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/build-av400/tmp/work/mesona5_av400-poky-linux/u-boot/v2019.01+git999-r1/recipe-sysroot-native
```

重点是recipe-sysroot-native

staging相关的变量有：

```
STAGING_BASE_LIBDIR_NATIVE
STAGING_BASELIBDIR
STAGING_BINDIR
STAGING_BINDIR_CROSS
STAGING_BINDIR_NATIVE
STAGING_DATADIR
STAGING_DATADIR_NATIVE
STAGING_DIR
STAGING_DIR_HOST
STAGING_DIR_NATIVE
STAGING_DIR_TARGET
STAGING_ETCDIR_NATIVE
STAGING_EXECPREFIXDIR
STAGING_INCDIR
STAGING_INCDIR_NATIVE
STAGING_KERNEL_BUILDDIR
STAGING_KERNEL_DIR
STAGING_LIBDIR
STAGING_LIBDIR_NATIVE
```

比较关键的是STAGING_DIR_TARGET这个。

对于aml-halaudio，是这样：

```
bitbake -e aml-halaudio  |grep STAGING_DIR_TARGET

STAGING_DIR_TARGET="/mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/build-av400/tmp/work/aarch64-poky-linux/aml-halaudio/git-r0/recipe-sysroot"
```

用file命令查看这个目录下的东西，是x64的。

不是应该是aarch64的吗？

对于yocto，

host和target是一回事。

native才是不一样的。

```
 bitbake -e aml-utils |grep  ^STAGING_DIR
STAGING_DIR="/mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/build-av400/tmp/sysroots"
STAGING_DIR_HOST="/mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/build-av400/tmp/work/aarch64-poky-linux/aml-utils/999-r0/recipe-sysroot"
STAGING_DIR_NATIVE="/mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/build-av400/tmp/work/aarch64-poky-linux/aml-utils/999-r0/recipe-sysroot-native"
STAGING_DIR_TARGET="/mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/build-av400/tmp/work/aarch64-poky-linux/aml-utils/999-r0/recipe-sysroot"
```



# task顺序研究

以linux-yocto为例。

查看log。有20个。顺序如下。

```
do_fetch (8359): log.do_fetch.8359
do_unpack (8441): log.do_unpack.8441
do_patch (5650): log.do_patch.5650
do_copy_defconfig (27693): log.do_copy_defconfig.27693
do_configure (27788): log.do_configure.27788
do_compile (31731): log.do_compile.31731
do_shared_workdir (20614): log.do_shared_workdir.20614
do_compile_kernelmodules (16664): log.do_compile_kernelmodules.16664
do_uboot_mkimage (3088): log.do_uboot_mkimage.3088
do_strip (9837): log.do_strip.9837
do_sizecheck (10052): log.do_sizecheck.10052
do_install (10208): log.do_install.10208
do_package (7880): log.do_package.7880
do_packagedata (10268): log.do_packagedata.10268
do_populate_sysroot (25948): log.do_populate_sysroot.25948
do_bundle_initramfs (26152): log.do_bundle_initramfs.26152
do_deploy (26174): log.do_deploy.26174
do_package_write_rpm (460): log.do_package_write_rpm.460
do_populate_lic (10276): log.do_populate_lic.10276
do_package_qa (21158): log.do_package_qa.21158
```

涉及的脚本

```

从上面可以获得共有20个任务，他们的执行脚本具体在下面四个目录下面的文件中：
poky/meta/classes/base.bbclass
poky/meta/classes/kernel.bbclass
 
poky/meta/classes/kernel-yocto.bbclass
 
fsl-release-bsp/sources/meta-fsl-bsp-release/imx/meta-bsp/recipes-kernel/linux/linux-imx_4.1.15.bb
```

这些任务的顺序主要是由poky/meta/class目录下面的*.bbclass文件创建的，还有部分由bsp目录下面创建的。

先看base.bbclass，搜索addtask

```
addtask fetch
addtask unpack after do_fetch
addtask configure after do_patch
addtask compile after do_configure
addtask install after do_compile
addtask build after do_populate_sysroot

addtask cleansstate after do_clean
addtask cleanall after do_cleansstate
```

再看kernel.bbclass，搜索addtask

```
addtask symlink_kernsrc before do_configure after do_unpack

addtask bundle_initramfs after do_install before do_deploy

addtask compile_kernelmodules after do_compile before do_strip

addtask shared_workdir after do_compile before do_compile_kernelmodules
addtask shared_workdir_setscene

addtask savedefconfig after do_configure

addtask kernel_link_images after do_compile before do_strip

addtask sizecheck before do_install after do_strip

addtask deploy after do_populate_sysroot do_packagedata
```



参考资料

https://blog.csdn.net/kunkliu/article/details/122562290

# 查看环境变量

```
bitbake -e | grep -w DISTRO_FEATURES
	查看DISTRO_FEATURES变量值
bitbake -e busybox | grep ^S=
	S="/mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/build-av400/tmp/work/aarch64-poky-linux/busybox/1.31.1-r0/busybox-1.31.1"
	
bitbake -e | grep -w MACHINEOVERRIDES
	MACHINEOVERRIDES="aarch64:armv8a:mesona5-av400:client"
	
bitbake -e u-boot | grep ^WORKDIR=
	WORKDIR="/mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/build-av400/tmp/work/mesona5_av400-poky-linux/u-boot/v2019.01+git999-r1"
```

查看overrides

```
OVERRIDES="linux:aarch64:pn-defaultpkgname:aarch64:armv8a:mesona5-av400:client:poky:dunfell:class-target:libc-glibc:forcevariable:a5:smarthome_kernel64:av400:onepass"
```



# ERROR: Unable to connect to bitbake server, or start one 

解决办法是：

```
rm -rf ./bitbake.lock
```



https://blog.csdn.net/hhs_1996/article/details/121316806



# Yocto do_install build issue : "installed-vs-shipped"

解决办法：

对应模块bb 或者 bbappend文件写入

> INSANE_SKIP_${PN} += "installed-vs-shipped"



# KERNEL_MODULE_AUTOLOAD



# VOLATILE_BINDS

这个是给readonly rootfs加类似mount --bind来实现可写的。

例如这样：

```
VOLATILE_BINDS:append = "\
    /data/etc/ssh /etc/ssh\n\
"
```

看这个文件。

Z:\work\a113x2\yocto-code\code\poky\meta\classes\rootfs-postcommands.bbclass

参考资料

https://stackoverflow.com/questions/34067897/bitbake-not-installing-my-file-in-the-rootfs-image

https://stackoverflow.com/questions/71210980/check-volatile-binds-content-in-bbclass-file



# 各种dir的具体位置

例如这个：

```
FILES_${PN} += "${libdir}/alsa-lib/lib*.so ${datadir}/alsa"
FILES_${PN}-dev += "${libdir}/alsa-lib/*.la"
```

libdir和datadir在哪里，又谁定义的？

```
Variable name	Definition	        Typical value
-------------  --------------------    --------------------
prefix	        /usr                    /usr
base_prefix	(empty)	                (empty)
exec_prefix	${base_prefix}	        (empty)
base_bindir	${base_prefix}/bin	/bin
base_sbindir	${base_prefix}/sbin	/sbin
base_libdir	${base_prefix}/lib	/lib
datadir        ${prefix}/share	        /usr/share
sysconfdir	/etc	                /etc
localstatedir	/var	                /var
infodir        ${datadir}/info	        /usr/share/info
mandir         ${datadir}/man	        /usr/share/man
docdir         ${datadir}/doc	        /usr/share/doc
servicedir	/srv	                /srv
bindir         ${exec_prefix}/bin	/usr/bin
sbindir        ${exec_prefix}/sbin	/usr/sbin
libexecdir	${exec_prefix}/libexec	/usr/libexec
libdir         ${exec_prefix}/lib	/usr/lib
includedir	${exec_prefix}/include	/usr/include
palmtopdir	${libdir}/opie	        /usr/lib/opie
palmqtdir	${palmtopdir}	        /usr/lib/opie
```



下面的命令，相当于在本package的image目录下，创建了对应的目录。

```
install -d ${D}${libdir}
install -d ${D}${includedir}
install -d ${D}${bindir}
```





https://wiki.koansoftware.com/index.php/Directories_and_installation_variables

http://www.embeddedlinux.org.cn/OEManual/index.html



# 出错解决

这篇文章思路值得学习。

https://blog.csdn.net/happybeginner/article/details/122339305



# 调整使用本地的代码包

主要是为了解决某些包默认下载非常慢的问题。



https://blog.csdn.net/Gary_F/article/details/91378450



# 使能staticdev静态库

没有静态库，是无法静态编译应用程序的，因此，为了方便，还需要在SDK中添加静态库，例如libc。

这个特性在只需要开启即可，在local.conf中添加一行：

SDKIMAGE_FEATURES_append = "staticdev-pkgs"



参考资料

https://blog.csdn.net/lyn631579741/article/details/108183021

# 安装到rootfs里

是靠FILES_${FN}来做的。

要修改或移除，则：

```
do_install_append(){
     rm -r ${D}/sxe
     rm -r ${D}/${datadir}/sxm
}
```



还有就是在镜像对应的bb文件里，例如amlogic-sbr-yocto.bb里，

给IMAGE_INSTALL添加内容。

https://stackoverflow.com/questions/58336239/how-to-install-files-in-yocto

https://blog.csdn.net/lyn631579741/article/details/108183021

# 配置包管理器server

就用Python来启动一个简单的server。



以rpm方式的为例说明。

服务器上，就在tmp/deploy/rpm目录下启动http server

```
python -m SimpleHTTPServer
```

板端有个smart命令可以进行软件包的管理。

查看软件状态。

```
smart status
```

配置服务器信息

```
smart channel --add all type=rpm-md baseurl=http://192.168.2.100:8000/all
smart channel --add  cortexa9hf_vfp_neon  type=rpm-md baseurl=http://192.168.2.100:8000/cortexa9hf_vfp_neon 
smart channel --add cortexa9hf_vfp_neon_mx6qdl type=rpm-md baseurl=http://192.168.2.100:8000/cortexa9hf_vfp_neon_mx6qdl
smart channel --add imx6qsabresd type=rpm-md baseurl=http://192.168.2.100:8000/imx6qsabresd
```

然后就可以适应smart upate命令进行软件包的更新了。

还可以安装

```
smart install bash-completion
```

服务器如果新编译了程序，需要刷新一下index，

```
bitbake package-index
```



## ipk的情况

服务器上还是一样，启动server。

板端配置是这样：

修改/etc/opkg/opkg.conf

```
src/gz all http://192.168.10.8/all
src/gz cortexa9hf-vfp-neon http://192.168.10.8/cortexa9hf-vfp-neon
src/gz dart http://192.168.10.8/dart
dest root /
lists_dir ext /var/lib/opkg
```



./poky/meta/recipes-devtools/opkg/opkg_0.4.2.bb

https://blog.csdn.net/lyn631579741/article/details/108183021

https://jumpnowtek.com/yocto/Using-your-build-workstation-as-a-remote-package-repository.html

这篇文章讲得很详细了。

https://wiki.phytec.com/pages/viewpage.action?pageId=128713168

# 运行商业license软件的加入

只需要在local.conf里加上：

```
LICENSE_FLAGS_WHITELIST="commercial"
```

也可以只允许某些商业license的软件加入。

```
LICENSE_FLAGS_WHITELIST="commercial_libav libxpm"
```

# IMAGE_FSTYPES

这个是指生成rootfs的文件格式。

```
IMAGE_FSTYPES = "ext3 tar.bz2"
```

这个表示的含义是，以ext3和tar.bz2这2种格式。

# selinux-image和core-image对比

```
IMAGECLASS ?= " ${@bb.utils.contains('DISTRO_FEATURES', 'selinux', 'selinux-image', 'core-image', d)} "
```

从上面语句，可以看出，selinux-image和core-image是两种并列的情况。

Z:\work\a113x2\yocto-code\code\poky\meta\classes\core-image.bbclass

./meta-selinux/classes/selinux-image.bbclass



# += .= append区别

你可以使用_append方式来给一个已经存在的变量追加值，跟+=不一样的是这种方式不会在原值和
  你要追加的值中间加上空格。



# BBCLASSEXTEND

允许你扩展一个recipe，用来build对应软件的变种。

```
BBCLASSEXTEND =+ "native nativesdk"
BBCLASSEXTEND =+ "multilib:multilib_name"
```

**相当于对xxx这个recipe产生了2个新的recipe，名字为xxx-native.bb和xxx-nativesdk.bb。**

BitBake支持两个功能，便于从单个配方文件创建该配方文件的多个化身，其中所有化身都是可构建的。

这些功能通过[`BBCLASSEXTEND`](https://www.yoctoproject.org/docs/1.6/bitbake-user-manual/bitbake-user-manual.html#var-BBCLASSEXTEND) 和 [`BBVERSIONS`](https://www.yoctoproject.org/docs/1.6/bitbake-user-manual/bitbake-user-manual.html#var-BBVERSIONS) 变量启用 。



Bitbake可以使用相同的配方为目标或本机构建主机构建配方.

这可以通过`BBCLASSEXTEND = "native"`配方来实现.

**这将使您能够使用-native来引用本机构建主机的配方构建.**



但有时候你想要构建该配方的方式有所不同,

具体取决于你是为目标还是主机构建,

这是在使用_class-target或_class-native的时候.

因此,在您的示例中,该`DEPENDS_append_class-target = " grub-efi-native"`行

意味着在为目标构建此配方时,DEPENDS也将包括`grub-efi-native`.



https://blog.csdn.net/fulinus/article/details/121904179

https://stackoverflow.com/questions/61425186/bbclassextend-native-nativesdk



# bootlin 300页ppt总结

https://bootlin.com/doc/training/yocto/yocto-slides.pdf

全局变量：在conf文件里的是全局的。

局部变量：在bb、bbclass、bbappend文件里的是局部的。

所有变量的最后覆盖是在build/conf/local.conf里。在这个文件里，要避免使用+=和.=这种操作。

变量的解析顺序难以预测。

```
bitbake world --runall=fetch
```

查看recipe的依赖有哪些

```
bitbake -g -u taskexp core-image-minimal
```



SDK的意义，很多人只需要开发应用，不需要生成image。

所以他们只需要基于sdk来做。就可以得到ipk文件用来发布。

```
bitbake -c populate_sdk core-image-minimal
```



```
TOOLCHAIN_OPTIONS = " --sysroot=${STAGING_DIR_TARGET}"
```

```
export MAKE = "make"
EXTRA_OEMAKE = ""
EXTRA_OECONF = ""
export LC_ALL = "en_US.UTF-8"
export TZ = 'UTC'
```



```
export BUILD_CC="gcc "
```

```
export CC="aarch64-poky-linux-gcc  -march=armv8-a+crc -fstack-protector-strong  -D_FORTIFY_SOURCE=2 -Wformat -Wformat-security -Werror=format-security --sysroot=/mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/build-av400/tmp/work/aarch64-poky-linux/defaultpkgname/1.0-r0/recipe-sysroot"
```

```
DATE := "${@time.strftime('%Y%m%d',time.gmtime())}"
TIME := "${@time.strftime('%H%M%S',time.gmtime())}"
DATETIME = "${DATE}${TIME}"
```



# COREBASE

对应的是这个目录

```
COREBASE="/mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/poky"
```



# No space left on device or exceeds fs.inotify.max_user_watches

bitbake的时候，出现了这个问题，需要执行下面的命令：

```
sudo sysctl -w fs.inotify.max_user_watches="99999999"
```



# ASSUME_PROVIDED

https://lynxbee.com/speed-up-yocto-build-time-using-assume-provided/

从这篇文章看，这个是可以加快构建速度的。

具体指代了什么行为？

就是告诉bitbake，你本地已经安装了哪些native的软件了。不要yocto自己去编译这些了。

例如

```
ASSUME_PROVIDED = "\
    git-native \
    u-boot-mkimage \
    "
```

# toolchain

当前的toolchain是怎么指定的？都是编译出来的吗？如果要使用现成的二进制，怎么做？

```
hanliang.xiong@walle01-sz:/mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/build-av400/tmp/sysroots-components/x86_64$ find -name "*aarch64"
这里放的是strip这些工具。
./binutils-cross-aarch64
这里放的是gcc、g++这些工具。
./gcc-cross-aarch64/usr/lib/aarch64-poky-linux/gcc/aarch64-poky-linux/9.3.0/plugin/include/config/aarch64

```

![img](../images/random_name/84cefaac40d0fbab93c8f1a773add19f.png)

工具链是在这里指定的。

poky\meta\recipes-devtools\gcc

参考资料

https://blog.csdn.net/Neutionwei/article/details/111059573

# image-info.txt内容

```
./buildhistory/images/mesona5_av400/glibc/amlogic-sbr-yocto/image-info.txt
./buildhistory/images/mesona5_av400/glibc/vendor-image/image-info.txt
./buildhistory/images/mesona5_av400/glibc/recovery-image/image-info.txt
./buildhistory/images/mesona5_av400/glibc/core-image-minimal/image-info.txt
```

amlogic-sbr-yocto/image-info.txt

```
DISTRO = poky
DISTRO_VERSION = 3.1.11
USER_CLASSES = buildstats
IMAGE_CLASSES = license_image
IMAGE_FEATURES = debug-tweaks tools-debug
IMAGE_LINGUAS = 
IMAGE_INSTALL = packagegroup-core-boot packagegroup-base-extended packagegroup-amlogic-sbr-baserootfs gdb aml-bluez-alsa
BAD_RECOMMENDATIONS = 
NO_RECOMMENDATIONS = 
PACKAGE_EXCLUDE = 
ROOTFS_POSTPROCESS_COMMAND = write_package_manifest; license_create_manifest;   ssh_allow_empty_password;  ssh_allow_root_login;  postinst_enable_logging;  rootfs_update_timestamp ;   write_image_test_data ;  set_systemd_default_target; systemd_create_users; empty_var_volatile; version_hook;  sort_passwd; rootfs_reproducible;
IMAGE_POSTPROCESS_COMMAND =  buildhistory_get_imageinfo ;
IMAGESIZE = 209552
```



# buildhistory-web

看看怎么搭建web页面来进行查看。



```
SDK_NAME="poky-glibc-x86_64-defaultpkgname-aarch64-mesona5-av400"
```

```
INHERIT=" buildhistory externalsrc poky-sanity uninative reproducible_build package_ipk buildstats debian devshell sstate license remove-libtool blacklist sanity"
```

# toaster

这个是启动网页来对yocto工程进行管理。

在build目录下，执行：

```
source toaster start
```

如果提示确实python库，按照提示进行安装就好。

然后访问地址：http://ip:8000 

如果要指定port，使用：

```
source toaster start webport=8400
```

同时指定ip地址：

```
source toaster start webport=0.0.0.0:8400
```



启动会需要一些时间。

但是进入界面，不能导入现有的工程。

好像也没有什么大的用途。



https://docs.yoctoproject.org/toaster-manual/setup-and-use.html



https://www.cnblogs.com/liushuhe1990/articles/13096512.html

# bb文件展开后的效果

可以以这个为例看看。

```
PV = 1.2.1.2
PR = r0
PKG = libasound2
RPROVIDES = alsa-lib (=1.2.1.2) libasound
RDEPENDS = alsa-conf alsa-ucm-conf glibc (>= 2.31+git0+4f0a61f753)
RRECOMMENDS = 
RREPLACES = libasound
RCONFLICTS = libasound
PKGSIZE = 1001666
FILES = /usr/bin/* /usr/sbin/* /usr/libexec/* /usr/lib/lib*.so.* /etc /com /var /bin/* /sbin/* /lib/*.so.* /lib/udev /usr/lib/udev /lib/udev /usr/lib/udev /usr/share/alsa-lib /usr/lib/alsa-lib/* /usr/share/pixmaps /usr/share/applications /usr/share/idl /usr/share/omf /usr/share/sounds /usr/lib/bonobo/servers
FILELIST = /usr/lib/libasound.so.2 /usr/lib/libasound.so.2.0.0

```

原始文件是这里

Z:\work\a113x2\yocto-code\code\poky\meta\recipes-multimedia\alsa\alsa-lib_1.2.1.2.bb



# do_populate_lic



# 写一个动态库





https://blog.csdn.net/punmpkin/article/details/103178462

# 一个库

Z:\work\a113x2\yocto-code\code\meta-meson\recipes-devtools\android-tools\liblog_git.bb

里面的写法：

```
SRC_URI_append = " ${@get_patch_list_with_path('${AML_PATCH_PATH}/vendor/amlogic/aml_commonlib')}"

S = "${WORKDIR}/git/liblog"

#do_package_qa[noexec] = "1"

do_compile(){
    ${MAKE} -C ${S}
}
```



# image.bbclass

```
IMAGE_FEATURES ?= ""
IMAGE_FEATURES[type] = "list"
IMAGE_FEATURES[validitems] += "debug-tweaks read-only-rootfs stateless-rootfs empty-root-password allow-empty-password allow-root-login post-install-logging"


EXCLUDE_FROM_WORLD = "1"

USE_DEVFS ?= "1"
USE_DEPMOD ?= "1"

do_fetch[noexec] = "1"
do_unpack[noexec] = "1"
do_patch[noexec] = "1"
do_configure[noexec] = "1"
do_compile[noexec] = "1"
do_install[noexec] = "1"
deltask do_populate_lic
deltask do_populate_sysroot
do_package[noexec] = "1"
deltask do_package_qa
do_packagedata[noexec] = "1"
deltask do_package_write_ipk
deltask do_package_write_deb
deltask do_package_write_rpm
```

# yocto阶段分析

源码获取，来源有：

1、release的，就是官方的release链接。

2、本地目录。

3、git、svn方式的。

通常一个组件包下载完毕后，在存放目录下会生成一个包名加".done"的文件表示该包下载完成，

默认情况下该变量指定的目录为`build/downloads/`，如果多用户在一台编译机器上使用，可以指定一个公共目录，避免重复下载，比如`DL_DIR ?= "/opt/downloads"`，同时修改`chmod 777 /opt/downloads`即可。



一个技巧就是某个开源组件一直下载失败，那就从其他地方下载同版本组件拷贝到存放目录下，并复制一个`*.done`文件改为对应名字即可。



默认情况，构建系统会将`file://`指定带".diff"或".patch"的补丁文件应用到${S}目录，如果不想使用这个补丁，可以显示指定不应用。

 这种强制更改`FILESPATH`变量默认值的方法是不正确的，正确做法是采用`FILESEXTRAPATHS`变量来扩展搜索目录，比如下面做法：

```
FILESEXTRAPATHS_prepend := " ${THISDIR}/../../sources/XXX:${THISDIR}/../../sources/YYY:" #同时扩展2个路径
FILESEXTRAPATHS_append := " ${THISDIR}/../EEE:" #尾部的分号必须存在
```

额外说明一下，在.bbappend文件中只能使用`FILESEXTRAPATHS`变量。

**THISDIR**

 bb或bbappend文件所在目录，位于配方（recipe）文件中。

**TMPDIR**

默认情况下该变量指定的目录为`build/tmp/`。



 假设bb文件中指定源码来源于git，则在 do_fetch 期间，源码将被被克隆到 `${WORKDIR}/git`目录中。由于此路径与S的默认值不同，所以必须专门设置，才能定位到源：

```
 SRC_URI = "git://path/to/repo.git"
 S = "${WORKDIR}/git"
```



这个阶段主要包含四个任务，分别为`do_prepare_recipe_sysroot`、`do_configure`、`do_compile`和`do_install`。

 是不是很好奇，突然跑出一个奇怪任务`do_prepare_recipe_sysroot`？虽然这个任务没有出现在上图中，但它却非常重要。



**do_prepare_recipe_sysroot任务**

 网上大多资料都简要带过这个任务，未能讲明白这个任务是做什么的，但想要了解yocto的配方文件共享机制就必须弄明白这个任务是做什么的！



 `do_prepare_recipe_sysroot`与`do_populate_sysroot`是`staging.bbclass`类中关键任务，用于共享配方之间成果物！

抛出一个问题思考一下，

如果一个配方B需要使用配方A的成果物怎么办（比如头文件、动态/静态链接库、配置文件）？

yocto为了解决这种问题，提供了一套配方成果物共享机制，该机制分为两阶段：

 第一阶段在A配方构建时完成。

A配方在构建时，需要在`do_install` 任务中将**需要共享的文件安装至`${D}`目录**，

后续执行的`do_populate_sysroot`任务将自动拷贝`${D}`目录下部分子目录到`${SYSROOT_DESTDIR}`，

**而`${SYSROOT_DESTDIR}`目录最终会放置到共享区（默认为`build/tmp/sysroots-components`）暂存，**

**其他配方构建时就可以从共享区拷贝。**



那么，`${D}`目录下哪些子目录会被自动拷贝？

自动拷贝的目录由三个变量指定，

分别为

`SYSROOT_DIRS`（目标设备需要保存的子目录）、

`SYSROOT_DIRS_BLACKLIST`（目标设备不需要保存的子目录）、

`SYSROOT_DIRS_NATIVE`（本机设备需要保存的目录），



以`SYSROOT_DIRS`变量为例，其默认值为：

```
SYSROOT_DIRS = " \
         ${includedir} \
         ${libdir} \
         ${base_libdir} \
         ${nonarch_base_libdir} \
         ${datadir} \
     "
```



第二阶段在B配方构建时完成。

B配方中添加`DEPENDS += "A"`，便可使用A配方的成果物了。

bitbake执行构建任务时会保证B配方的`do_prepare_recipe_sysroot`任务执行前，

A配方的成果物已位于`build/tmp/sysroots-components`中。



 `do_prepare_recipe_sysroot`任务会在`${WORKDIR}`目录中创建两个`sysroot`目录并填充（所有依赖拷贝到其中），

这两个目录名分别为`"recipe-sysroot"`和`"recipe-sysroot-native"`（本机），

其中`"recipe-sysroot"`给目标设备使用，

A配方生成的成果物就在里面，

另一个`"recipe-sysroot-native"`是给本机设备使用的。

例如tmp/work/aarch64-poky-linux/liblog/999-r0/recipe-sysroot-native



这里只介绍了构建依赖`DEPENDS`，但还有一种运行时依赖`RDEPENDS`，一般情况运行依赖会由构建系统自动添加，详情请参阅[RDEPENDS](https://www.yoctoproject.org/docs/2.7/ref-manual/ref-manual.html#var-RDEPENDS)。



**do_configure任务**

 此任务用于完成编译源码前的配置，

配置可以来自配方本身，也可以来自继承的类，

一般情况我们都会使用[autotools](https://docs.yoctoproject.org/ref-manual/classes.html#ref-classes-autotools)(配方中使用inherit autotools)、

[`cmake`](https://www.yoctoproject.org/docs/2.7/ref-manual/ref-manual.html#ref-classes-cmake)类(配方中使用inherit cmake)

或默认的make（不需要额外配置）。

该任务运行时将当前工作目录设置为`${B}`（一般与`${S}`相同），

该任务有个默认行为，

即如果找到一个`makefile` (`makefile`, `makefile`，或`GNUmakefile`)并且`CLEANBROKEN`没有设置为“1”，

则运行`oe_runmake clean`。



**do_compile任务**

 编译源代码。该任务运行时将当前工作目录设置为`${B}`（一般与`${S}`相同），该任务有个默认行为，即如果找到一个`makefile` (`makefile`, `makefile`，或`GNUmakefile`)，则运行`oe_runmake`，若未找到此类文件将不执行任何操作。

 如果在执行`oe_runmake`时需要传入额外编译选项或链接库，则可以使用在配方中以下变量：

```
CFLAGS += "-I${WORKDIR}/recipe-sysroot/usr/include/xxx  -DBMCW=ON" #gcc的编译选项，增加额外头文件检索路径，定义BMCW宏
CXXFLAGS = " -fPIC" #g++的编译选项，告诉编译器产生位置无关代码
LDFLAGS += "-L${WORKDIR}/recipe-sysroot/usr/lib -yyy" #编译器链接选项
```



还记得上面提过的依赖吗？这个任务就是把其他配方所需依赖安装到`${D}`目录，然后`do_populate_sysroot`任务才能去`${D}`目中拷贝。假设A模块执行`do_install`的一个简单示例：

```
do_install() {
    oe_runmake DESTDIR=${D}${libdir} install #执行Makefile中安装任务（安装.so），传入安装目录
    install -m 0644 -d ${D}${includedir}/api #创建头文件目录
    install -m 0644 ${S}/api_common.h  ${D}${includedir}/api #安装头文件
    install -m 0644 ${S}/api_xxx.h  ${D}${includedir}/api #安装头文件
}
```

 之后B模块在配方中添加如下：

```
DEPENDS += " A"
CFLAGS += " -I${WORKDIR}/recipe-sysroot/usr/include/api"
```

 这样B模块就可以使用A模块编译的动态库。

该大阶段涉及但未解释的变量有以下：

**B**

 包构建的编译目录，一般情况`${B}`与`${S}`相同，即为`${WORKDIR}/${BPN}-${PV}`。

**D**

 包构建成果物的安装目录，也称为目标目录。默认情况这个目录为`${WORKDIR}/image`。



**FILES**

 用于指定包（模块）安装在`${D}`目录中哪些成果物要打包，

该变量位于配方文件中（如有需要可在此文件中修改）。

简单来说就是在`do_install`任务中安装在`${D}`目录下的文件不会都打包，以`rsa`模块为例该变量的默认值为：

```
FILES_rsa="/usr/bin/* /usr/sbin/* /usr/libexec/* /usr/lib/lib*.so.*             /etc /com /var             /bin/* /sbin/*             /lib/*.so.*             /lib/udev /usr/lib/udev             /lib/udev /usr/lib/udev             /usr/share/hikrsa /usr/lib/hikrsa/*             /usr/share/pixmaps /usr/share/applications             /usr/share/idl /usr/share/omf /usr/share/sounds             /usr/lib/bonobo/servers"
```

 也就是说，**只要成果物安装在上面这些目录下的都会参与打包，**

当然如果不放心或需要额外增加文件，可以在配方文件中显性指定：

```
FILES_${PN} += " \
        ${sbindir}/rsaverify \
" #${sbindir}默认为/usr/sbin/
```



**do_rootfs任务**

 该任务将创建目标设备的根文件系统（将需要打包至目标设备的程序、库、文件等都放置到根文件系统中），这个根文件系统最终打包到image中。

do_rootfs任务会通过`ROOTFS_POSTPROCESS_COMMAND`来优化文件大小

（如`mklibs`过程优化了库的大小，同时`prelink`优化了共享库的动态链接以减少可执行文件的启动时间），

`ROOTFS_POSTPROCESS_COMMAND`如下：

```
ROOTFS_POSTPROCESS_COMMAND() {
write_package_manifest; license_create_manifest;   ssh_allow_empty_password;  ssh_allow_root_login;  postinst_enable_logging;
  rootfs_update_timestamp ;   write_image_test_data ;  set_systemd_default_target; systemd_create_users; empty_var_volatile;
remove_etc_version ;  set_user_group; sort_passwd; rootfs_reproducible;
}
```

创建的文件系统所在位置由`IMAGE_ROOTFS`变量指定，查看示例：

```
~/work/bmc$ bitbake -e obmc-phosphor-image | grep ^IMAGE_ROOTFS
IMAGE_ROOTFS="~/work/bmc/build/tmp/work/4u_x201-openbmc-linux-gnueabi/obmc-phosphor-image/1.0-r0/rootfs"
```

 如果我们修改了某个程序，但又不想重新烧写整个固件，那就去这个目录下找到程序，再通过`TFTP`方式（或`NFS`直接挂载）下载到目标是设备调试即可。



**do_image任务**

 `do_image` 任务会通过 `IMAGE_PREPROCESS_COMMAND` 对image进行预处理，主要是优化image大小，`IMAGE_PREPROCESS_COMMAND` 如下：

```
IMAGE_PREPROCESS_COMMAND() {
 mklibs_optimize_image;  prelink_setup; prelink_image;  reproducible_final_image_task;
}
```



构建系统`do_image`根据需要动态生成支持的 `do_image_*` 任务，生成的任务类型取决于[IMAGE_FSTYPES](https://docs.yoctoproject.org/ref-manual/variables.html#term-IMAGE_FSTYPES)变量。`do_image_*` 任务将所有内容转换为一个`image`文件或一组`image`文件，并且可以压缩根文件系统`image`大小，以减小最终烧写到目标设备的`image`整体大小。用于根文件系统的格式取决于 [IMAGE_FSTYPES](https://docs.yoctoproject.org/ref-manual/variables.html#term-IMAGE_FSTYPES)变量，压缩取决于格式是否支持压缩。



**总结**：image生成生成阶段就是创建目标设备的根文件系统，并将需要打包至目标设备的程序、库、文件等都放置到根文件系统中，然后对文件和整个文件系统进行优化压缩，最终生成image。





```
bitbake -e amlogic-sbr-yocto |grep IMAGE_ROOTFS

IMAGE_ROOTFS="/mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code/build-av400/tmp/work/mesona5_av400-poky-linux/amlogic-sbr-yocto/1.0-r0/rootfs"
```



这个相当于根文件系统目录。

这个专栏，5篇文章质量很高。

https://blog.csdn.net/zz2633105/category_11576131.html

# 添加一个package到image里

有两种方法将软件包添加到映像打包。

**第一种**

 在顶层目录下搜索固件名对应的bb文件，在其中添加 IMAGE_INSTALL += “xxx” ,其中xxx为软件包名字，即bb文件名称。

 在obmc-phosphor-image.bb文件中添加IMAGE_INSTALL += "xxx"即可，但这种方式添加的软件包将应用到所有项目中，这往往不是我们想要的，因此推荐第二种方式。



第二种

 在对应机型的layer.conf 文件中添加，例如meta-byosoft/meta-4u-x201/conf/layer.conf 文件添加如下：

IMAGE_INSTALL_append += "hellomake"
IMAGE_INSTALL_append += "hellocmake"
IMAGE_INSTALL_append += "helloauto"
IMAGE_INSTALL_append += "scripts"

 然后删除build/conf目录，再次执行以下命令：



# PACKAGES

这个变量具体指什么？

指recipe创建的packages。

默认有这些：

```
xx-src
xx-dbg
xx-staticdev
xx-dev
xx-doc
xx-locale
xx
```

do_package 这个task会遍历PACKAGES变量里的值。

同时使用FILES变量的值来把文件放到对应的package里。

可以自己加

```
PACKAGES =+ "${PN}-tools"
FILES_${PN}-tools = "${bindir}/*"
```

怎么查看所有的packages呢？

好像没有办法从环境变量里查看出来。

在某个具体的bb文件里，例如在aml-halaudio里。

```
do_print_info() {
    echo -------${PACKAGES}--------
}
```

这个打印出来是：

```
aml-halaudio-src aml-halaudio-dbg aml-halaudio-staticdev aml-halaudio-dev aml-halaudio-doc aml-halaudio-locale aml-halaudio
```



https://stackoverflow.com/questions/46878640/is-there-a-way-to-check-the-exact-list-of-packages-that-will-be-installed-in-the



# bb文件里增加环境变量

当前aml_halaudio的编译依赖了环境变量，所以需要在bb文件里产生环境变量。

具体怎么操作呢？

也就是export就可以。

```
export ENV_VARIABLE
```



https://blog.csdn.net/aaaLG/article/details/107939692



# WORKDIR

是这样定义的：

```
The WORKDIR directory is defined as follows:

${TMPDIR}/work/${MULTIMACH_TARGET_SYS}/${PN}/${EXTENDPE}${PV}-${PR}
```

展开例子是这样：

```
poky/build/tmp/work/qemux86-poky-linux/foo/1.3.0-r0
```



```
S=${WORKDIR}/git
```

这样写法表示什么？

表示是外部的git仓库目录。

workdir的作用是什么？

对应recipe的工作目录吧。



参考资料

https://stackoverflow.com/questions/28827764/workdir-in-a-yocto-recipe

# 添加external git仓库

```
Depending on the type of build (eg, 'inherit module' for out of tree Linux kernel modules) you may or may not need to set EXTERNALSRC_BUILD.

 inherit externalsrc
 EXTERNALSRC = "/some/path"
 EXTERNALSRC_BUILD = "/some/path"
```

你可以指定build的目录。

一个完整例子

```
#
# Recipe example with externalsrc
#
# (C)2019 Marco Cavallini - KOAN - <https://koansoftware.com>
#

LICENSE = "CLOSED"
LIC_FILES_CHKSUM = ""

inherit externalsrc

EXTERNALSRC = "/home/koan/yocto-qemuarm-sumo/ninvaders-0.1.1"
EXTERNALSRC_BUILD = "${EXTERNALSRC}"

DEPENDS = "ncurses"

EXTRA_OEMAKE = "-e"


do_install() {
	install -d ${D}${bindir}
	install -m 0755 nInvaders ${D}${bindir}
}

FILES_${PN} = "${bindir}/*"

```

EXTERNALSRC_BUILD 这个被设置后，才设置的B变量。

所以不能把B变量赋值给它。



https://wiki.koansoftware.com/index.php/Building_Software_from_an_External_Source

# TARGET_CFLAGS

TARGET_CFLAGS怎么传递给Makefile的CFLAGS的？

bitbake会帮你转过去的。暂不深究。

# oe_runmake

```
oe_runmake_call() {
	bbnote ${MAKE} ${EXTRA_OEMAKE} "$@"
	${MAKE} ${EXTRA_OEMAKE} "$@"
}

oe_runmake() {
	oe_runmake_call "$@" || die "oe_runmake failed"
}
```

这个很简单。



# sysroot-destdir

安装头文件就是安装到这里。

例如alsa-lib的。

```
./sysroot-destdir/usr/include/sys/asoundlib.h
```

aml-halaudio里依赖alsa-lib，表现是aml-halaudio的recipe-sysroot下面把alsa-lib的头文件都拷贝过来了

```
aarch64-poky-linux/aml-halaudio/git-r0/recipe-sysroot/usr/include
```



# DISTRO_FEATURES_BACKFILL_CONSIDERED 

1. Initialization Manager的选择

   yocto默认使用SysVinit作为启动器，然而yocto也支持systemd启动方式。若选择systemd则需要如下内容：

   设置如下变量启用systemd：

​     DISTRO_FEATURES_append = “ systemd”

​     VIRTUAL-RUNTIME_init_manager = “systemd”

   此时系统启动的时候默认采用systemd方式启动，但是sysvinit脚本也安装到image中只不过在rescure/minimal中使用sysvinit方式启动

   **删除SysVinit脚本：**

​     **DISTRO_FEATURES_BACKFILL_CONSIDERED = “sysvinit”**

参考资料

https://blog.csdn.net/faihung/article/details/82713816

# HOST_ARCH

这个跟TARGET_ARCH是一样的，都是aarch64 。

总的来说，在yocto里，host和target，都是target。

而native才是编译机器。native和build又基本都是指编译机器。

这名字就奇怪了。

BUILD_ARCH才是x86的。

MACHINE_ARCH是mesona5_av400

在bitbake.conf里定义的。

```
BUILD_ARCH := "${@os.uname()[4]}"
BUILD_OS := "${@os.uname()[0].lower()}"
BUILD_SYS = "${BUILD_ARCH}${BUILD_VENDOR}-${BUILD_OS}"

HOST_ARCH = "${TARGET_ARCH}"
HOST_OS = "${TARGET_OS}"
HOST_VENDOR = "${TARGET_VENDOR}"
HOST_SYS = "${HOST_ARCH}${HOST_VENDOR}-${HOST_OS}"

T = "${WORKDIR}/temp"
D = "${WORKDIR}/image"
S = "${WORKDIR}/${BP}"
B = "${S}"

STAGING_DIR = "${TMPDIR}/sysroots"  这个目录是空的。
COMPONENTS_DIR = "${STAGING_DIR}-components"

export MAKE = "make"
EXTRA_OEMAKE = ""
EXTRA_OECONF = ""
export LC_ALL = "en_US.UTF-8"
export TZ = 'UTC'


```



# openbmc文章

openbmc是yocto比较常见的使用场景。通过这个来找yocto的文章。

https://blog.csdn.net/qq_34160841/article/details/119977679



# bitbake里使用if else

https://stackoverflow.com/questions/52492036/if-else-statement-using-external-variable-in-a-bitbake-file

只能在匿名python函数里。



# core-image.bbclass分析

CORE_IMAGE_BASE_INSTALL

```
packagegroup-core-boot
packagegroup-base-extended

IMAGE_INSTALL ?= "${CORE_IMAGE_BASE_INSTALL}"
```

继承了image.bbclass。这个就有700行左右。





```
IMGCLASSES += "rootfs-postcommands"
```

这个是作用是什么？

```
IMAGE_FEATURES[validitems] += "debug-tweaks read-only-rootfs stateless-rootfs empty-root-password allow-empty-password allow-root-login post-install-logging"
```



```
# Images are generally built explicitly, do not need to be part of world.
EXCLUDE_FROM_WORLD = "1"
```

```
def rootfs_command_variables(d):
    return ['ROOTFS_POSTPROCESS_COMMAND','ROOTFS_PREPROCESS_COMMAND','ROOTFS_POSTINSTALL_COMMAND','ROOTFS_POSTUNINSTALL_COMMAND','OPKG_PREPROCESS_COMMANDS','OPKG_POSTPROCESS_COMMANDS','IMAGE_POSTPROCESS_COMMAND',
            'IMAGE_PREPROCESS_COMMAND','RPM_PREPROCESS_COMMANDS','RPM_POSTPROCESS_COMMANDS','DEB_PREPROCESS_COMMANDS','DEB_POSTPROCESS_COMMANDS']
```



```
addtask do_image_complete after do_image before do_build
```



```
    packagegroup-core-boot \
    packagegroup-base-extended \
```

packagegroup-core-boot定义在：

meta-openembedded\meta-oe\recipes-core\packagegroups\packagegroup-boot.bb

poky\meta\recipes-core\packagegroups\packagegroup-core-boot.bb



```
# Make sure we build the kernel
DEPENDS = "virtual/kernel"
```



# VIRTUAL-RUNTIME



# base-files

poky\meta\recipes-core\base-files\base-files_3.0.14.bb

# RRECOMMENDS和RDEPENDS

https://stackoverflow.com/questions/14238825/anyone-tell-me-the-difference-for-rrecommends-and-rdepends

我觉得RDEPENDS应该是对于opkg包管理进行安装的时候有用。

当前我是直接使用整包烧录的，所以RDEPENDS没有正确指定还没有关系。

RDEPENDS is a hard, runtime dependency.

RRECOMMENDS is a soft, runtime dependency. 

大多数的package的RDEPENDS是自动推导出来的。

所以一般的bb文件里，不用写RDEPENDS变量。



# poky\meta\conf\documentation.conf

这个文件可以当帮助文档看。



# elinux文档

https://elinux.org/images/9/9a/Buildroot-vs-Yocto-Differences-for-Your-Daily-Job-Luca-Ceresoli-AIM-Sportline.pdf

这个很好，对buildroot和yocto进行了全面的对比，很有启发。

recipe hash

每个task都会生成hash。

hash值涉及的内容：

1、所有的recipe变量和task的code内容。

2、SRC_URI包含的文件的内容。

只要这些内容有变化，hash就会变化，系统就可以根据需要执行task。

结果存储在sstate里。

要强制执行task，可以加-f参数。



bitbake -c savedefconfig



# overlay实现

```
Buildroot: System configuration menu:
    • Root filesystem overlay directories
    • Post-build and post-image scripts
Yocto
	• ROOTFS_POSTPROCESS_COMMAND and IMAGE_POSTPROCESS_COMMAND
```

ROOTFS_POSTPROCESS_COMMAND

```
./poky/meta/classes/rootfsdebugfiles.bbclass:31:ROOTFS_POSTPROCESS_COMMAND += "rootfs_debug_files ;"
```

poky\meta\classes\rootfsdebugfiles.bbclass

这个是一个可以参考的例子。

我们扩展的有一个。

```
./recipes-core/images/amlogic-sbr-yocto.bb:88:ROOTFS_POSTPROCESS_COMMAND += "version_hook; "
```

这个的作用是产生./tmp/work/mesona5_av400-poky-linux/amlogic-sbr-yocto/1.0-r0/rootfs/version.txt

这个确实就相当于修改rootfs的内容了。

我可以在这里来对rootfs进行修改。

有两种方法：

1、从目录进行拷贝。

2、直接脚本进行文件的生成和修改。

先看看当前buildroot里的overlay的文件有哪些。

说实话，也不是非要不可的。

主要是开机脚本。

还有一些工具脚本和文件。

怎么放合适？

工具类的，我可以单独弄一个recipe，直接来进行文件的拷贝。

文件覆盖的，这个就得考虑顺序问题。

要理顺开机脚本的，就要先把systemd研究一下。

例如，开机时是怎么挂载的？

当前编译出来的/init，是一个脚本，分析一下内容。

这个init是从哪个recipe来的？

这样搜索，看了init不会直接的文件，估计是通过脚本修改出来的。

```
find -name "init" -type f | xargs grep "Cannot find root hash in initramfs" 
./build-av400/tmp/work/mesona5_av400-poky-linux/amlogic-sbr-yocto/1.0-r0/rootfs/init:        echo "Cannot find root hash in initramfs"
./build-av400/tmp/work/mesona5_av400-poky-linux/core-image-minimal/1.0-r0/rootfs/init:        echo "Cannot find root hash in initramfs"
```

是这个

```
./recipes-core/initrdscripts/files/init-meson.sh:239:        echo "Cannot find root hash in initramfs"
```

meta-meson\recipes-core\initrdscripts\initramfs-meson-boot_1.0.bb

```
do_install() {
        install -m 0755 ${WORKDIR}/init-meson.sh ${D}/init
        install -d ${D}/dev
        mknod -m 622 ${D}/dev/console c 5 1
}
```

init-meson.sh逻辑分析

```
early_setup
	创建sys、proc等目录并挂载。
	udev生成dev文件。
从/proc/cmdline里读取参数，来决定rootfs的分区和类型。
mount_and_boot
	这个就是主要函数了。
	等待root设备就绪。
	dm_verity_setup system
	dm_verity_setup vendor
	boot_root
		最后切换到switch_root，这个就转到systemd了。
```

```
setup dm-verity for system partition(/dev/system) mount to /rootfs
Cannot find root hash in initramfs
setup dm-verity for vendor partition(/dev/vendor) mount to none
Cannot find root hash in initramfs
dm-verity is disabled
```



最后转到systemd，是靠

```
lrwxrwxrwx 1 root root 22 2018-03-09 12:34 /sbin/init -> ../lib/systemd/systemd
```



```
mesona5-av400 login: root (automatic login)
```



有个神奇的现象，为什么我没有配网，默认可以联网？

```
sh-5.0# wpa_cli status                     
Selected interface 'wlan0'                 
bssid=28:80:88:1d:4b:c1                    
freq=5240                                  
ssid=libo-rax80-5g                         
id=0                                       
mode=station                               
pairwise_cipher=NONE                       
group_cipher=NONE                          
key_mgmt=NONE                              
wpa_state=COMPLETED                        
ip_address=192.168.1.68                    
address=08:e9:f6:a8:f0:0c                  
uuid=341796ab-6b3a-5796-868a-a8f5cb5aaf92  
```

就是因为这个热点是没有密码的。所以下面的配置可以保证可以联网。

```
sh-5.0# cat /etc/wpa_supplicant.conf     
ctrl_interface=/var/run/wpa_supplicant   
ctrl_interface_group=0                   
update_config=1                          
                                         
network={                                
        key_mgmt=NONE                    
}                                        
```



# 修改编译线程数

有时候编译的时候占用资源太多。可以这样限制：

```
PARALLEL_MAKE="-j 2" bitbake 
```

# 在imx上学习yocto

如果我们想删除的包没有显示在 IMAGE_INSTALL 和 IMAGE_IMAGE_FEATURES 的定义里，通常是被封装到了包组里面，这时，可以用 PACKAGE_EXCLUDE 变量设置：

```
PACKAGE_EXCLUDE = "package_name package_name package_name ..."
```

这些列出的包都不会被安装到目标镜像中。这里可能会出现一个问题，如果其他一些包依赖于这里列出的包（即在 RDEPENDS 变量中列出），构建时会报错，必须接触相应的依赖关系。



自定义包组

包组（packagegroup）就是按特定需求把几个包组合成一个变量，

以 packagegroup- 为前缀，

在类似 `meta*/recipes*/packagegroups/packagegroup*.bb`的文件中定义。

以 poky/meta/recipes-core/packagegroups/packagegroup-base.bb 文件为例，

文件内通过 PACKAGES 变量列出了要产生的包组，

然后再用 RDEPENDS 和 RRECOMMENDS 项设置每个包组所包含的软件包。





下面是一个简单的例子，我们自定义一个名为 packagegroup-custom.bb 的 recipe 文件：

```bash
DESCRIPTION = "My Custom Package Groups"

inherit packagegroup

PACKAGES = "\
    ${PN}-apps \
    ${PN}-tools \
    "

RDEPENDS_${PN}-apps = "\
    dropbear \
    portmap \
    psplash"

RDEPENDS_${PN}-tools = "\
    oprofile \
    oprofileui-server \
    lttng-tools"

RRECOMMENDS_${PN}-tools = "\
    kernel-module-oprofile"
```

`${PN}` 是替代文件名（packagegroup-custom）的变量，

所以，这里是定义了两个包组：

packagegroup-custom-apps 和 packagegroup-custom-tools ，

**然后用 `RDEPENDS_${PN}-*` 设置了每个包组依赖的软件包。**

如果只想定义一般包组，

可以不用 PACKAGES 变量，`${PN}` 即是包组的名称，用 `RDEPENDS_${PN}` 设置包组依赖的软件包。





参考资料

这篇文章对于镜像的裁剪有独到之处。

https://shaocheng.li/posts/2020/12/12/

# Yocto 应用开发

Yocto 的应用开发有两种方式，一种是在 yocto 项目内新建 recipe ，另一种是导出 SDK ，然后使用 SDK 独立开发应用软件，第二种更方便一点。

## 安装 SDK

执行如下命令，生成扩展 SDK 安装脚本：

```bash
~/imx-yocto-bsp-5.4.47/imx6ullevk-fb$ bitbake imx-image-multimedia -c populate_sdk
```

生成的脚本位于 tmp/deploy/sdk 目录下，执行这个脚本即可安装：

```bash
~/imx-yocto-bsp-5.4.47/imx6ullevk-fb$ cd tmp/deploy/sdk/
~/imx-yocto-bsp-5.4.47/imx6ullevk-fb/tmp/deploy/sdk$ ./fsl-imx-fb-glibc-x86_64-imx-image-multimedia-cortexa7t2hf-neon-imx6ull14x14evk-toolchain-5.4-zeus.sh
```

默认安装在 /opt 目录下。也可以把这个脚本复制到其他主机中执行。

我自己测试验证一遍。

```
bitbake amlogic-sbr-yocto -v -c populate_sdk
```

执行需要的时间很长，我之前做了一次，有一些错误。

现在再做一次看看。

现在生成比第一次快很多。也没有看到打印错误。

执行这个脚本：

```
 ./poky-glibc-x86_64-amlogic-sbr-yocto-aarch64-mesona5-av400-toolchain-3.1.11.sh -d /mnt/fileroot/hanliang.xiong/work/test/yocto-sdk2
```

有打印下面的错误：

```
Extracting SDK............tar: ./sysroots/aarch64-poky-linux/dev/console: Cannot mknod: Operation not permitted
...................................tar: Exiting with failure status due to previous errors
```

现在不管这错误，直接去看sdk是否正常。

首先修改environment-setup-aarch64-poky-linux 里的目录位置。

看连接的so的位置是这样的：

```
/mnt/fileroot/hanliang.xiong/work/test/yocto-sdk2/sysroots/x86_64-pokysdk-linux/usr/bin/aarch64-poky-linux/aarch64-poky-linux-gcc: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), dynamically linked, interpreter /usr/local/oe-sdk-hardcoded-buildpath/sysroots/x86_64-pokysdk-linux/lib/ld-linux-x86-64.so.2, BuildID[sha1]=dbbc07e0b294a97367096035feff9c2791c871a1, for GNU/Linux 3.2.0, stripped
```

运行source environment-setup-aarch64-poky-linux 的前提是，LD_LIBRARY_PATH是空的。

```
if [ ! -z "$LD_LIBRARY_PATH" ]; then
    echo "Your environment is misconfigured, you probably need to 'unset LD_LIBRARY_PATH'"
    echo "but please check why this was set in the first place and that it's safe to unset."
    echo "The SDK will not operate correctly in most cases when LD_LIBRARY_PATH is set."
    echo "For more references see:"
    echo "  http://tldp.org/HOWTO/Program-Library-HOWTO/shared-libraries.html#AEN80"
    echo "  http://xahlee.info/UnixResource_dir/_/ldpath.html"
    return 1
fi
```

现在怎么让aarch64-poky-linux-gcc可以使用呢？

找到方法了。

很简单，就是安装到默认目录就一切正常了。默认是到/opt/poky/3.1.11，不需要管理员权限的。





怎样完全重新生成sdk？

https://stackoverflow.com/questions/53377944/how-to-clean-populate-sdk-in-yocto

说是可以把tmp/deploy/sdk目录删掉。

然后用-f再populate_sdk一次。





# d.getVar

BB_DEFAULT_TASK ?= "build"

d.getVar('INHIBIT_DEFAULT_DEPS', False)

后面的False参数，表示不要进行展开。

相当于shell里的`${XX}`

https://stackoverflow.com/questions/37041117/bitbake-d-getvarx-true-what-does-true-mean



```
THISDIR = "${@os.path.dirname(d.getVar('FILE'))}"
```

# class-target和class-native

看base.bbclass里有这个

```
BASEDEPENDS = ""
BASEDEPENDS_class-target = "${@base_dep_prepend(d)}"
BASEDEPENDS_class-nativesdk = "${@base_dep_prepend(d)}"
```

class-target和class-nativesdk后缀的具体产生了什么影响？

bitbake可以用同一个recipe文件来build target或者native的包。

类似于buildroot里的：

```
$(eval $(generic-package))
$(eval $(host-generic-package))
```

bitbake默认是编译给target，要让recipe同时给native编译，需要加上：

```
BBCLASSEXTEND = "native"
```

有时候给target和native编译需要的内容有所区别。

所有就要class-target和class-nativesdk后缀来进行override。





参考资料

https://stackoverflow.com/questions/49665642/difference-between-class-target-and-class-native-in-yocto-recipe

#  任务校验和和setscene

BitBake使用校验和（或签名）以及setcene来确定是否需要运行任务。 





```
export PACKAGE_INSTALL ?= "${IMAGE_INSTALL} ${ROOTFS_BOOTSTRAP_INSTALL} ${FEATURE_INSTALL}"
```



# COMPONENTS_DIR

这个目录是sysroot内容的位置。

`do_prepare_recipe_sysroot`这个task会通过软链接或者拷贝的方式，把各个recipe里的DEPENDS指定的包弄到本目录下。

这个目录是通过sstate来处理的。

recipe里不要直接使用这个目录。拷贝行为都是自动的。



# recipe-sysroot

每个菜谱在其工作目录中都有两个sysroot，一个用于目标文件(recipe-sysroot)，一个用于构建主机的本地文件(recipesysroot-native).



recipe不能直接填充sysroot目录

应该在${D}目录中的do_install任务期间将文件安装到标准位置

https://www.cnblogs.com/liushuhe1990/articles/12466137.html



https://stackoverflow.com/questions/53331063/how-to-simplify-recipe-sysroot-native



# 编译64位kernel和32位应用的组合

当前默认编译出来的是全部64位的。

我们在buildroot上都是用的64bit kernel + 32bit app的组合。

看看yocto上如何实现。

看aml-setenv.sh脚本里有这样的语句：

```
    if [ -n "$(echo $TARGET_MACHINE | grep -- lib32)" ]; then
      NEED_A6432_SUPPORT=y
    fi

    if [ "${NEED_A6432_SUPPORT+set}" = "set" ] && [ $(grep '^MULTTILIBS' conf/local.conf | grep -c 'multilib:lib32[^-]') -eq 0 ]; then
      cat >> conf/local.conf <<EOF
#Added for A6432 support
require conf/multilib.conf
MULTTILIBS = "multilib:lib32"
DEFAULTTUNE_virtclass-multilib-lib32 = "armv7athf-neon"
EOF
    fi
```

具体能不能工作，还存在疑问。

# 同时编译target和native版本

以acl为例，看看这个是怎么同时编译了target和native 这2个版本的。

就是靠bb文件的最后一行加上这个：

```
BBCLASSEXTEND = "native nativesdk"
```

acl是还有加这个package。

```
PACKAGES =+ "lib${BPN}"
FILES_lib${BPN} = "${libdir}/lib*${SOLIBS}"
```

那就是得到libacl的package？

给这个package分配的文件是自己的/usr/lib/lib*so的文件。



```
./recipes-devtools/avb/avb_2.0.bb:20:BBCLASSEXTEND = "native"
```



# TUNE_FEATURES

这个是很基础的feature，决定了芯片的特点。



# IMAGE_BOOT_FILES

安装到boot分区的文件。



搜索wks.in后缀的文件

./code/poky/meta-yocto-bsp/wic/genericx86.wks.in



参考资料

https://stackoverflow.com/questions/56914301/how-to-deploy-files-to-boot-partition-with-yocto

# WIC

参考资料

Yocto中WIC控制以及WKS文件

https://blog.csdn.net/qq_38131812/article/details/124270885

# WARN_QA

最近项目需要在 Yocto 里面回退一个软件包到比较旧的版本，而新版本的软件包已经生成了 cache ，这样在编译的时候就会遇到如下错误：

QA Issue: Package version for package went backwards which would break package feeds
1
主要原因是：

如果启用了构建历史记录，

那么当一个包在相同的名称下被构建出来时，

Yocto 的 ERROR_QA 或者 WARN_QA 就会报告它的版本比以前构建的包的版本要低。

如果你将旧版本包放置到镜像中，并使用该镜像升级目标系统上的包，

则旧版本包可能导致目标系统无法正确升级到该包的“新”版本。



解决我们这个问题的方法就是在配置文件里面去掉 ERROR_QA 里面的 version-going-backwards 报告项：

```
ERROR_QA_remove = "version-going-backwards"
```

# systemd跟sysvinit共存

实际上是可以共存的。systemd本来就提供了对sysvinit的兼容。

但是我尽量不用吧。

# dropbear的bb文件分析

这个是一个基础的包。

各种特性比较全，

例如跟openssh是冲突的。可以这样来指定：

```
RCONFLICTS_${PN} = "openssh-sshd openssh"
```

对外提供命令别名：

```
RPROVIDES_${PN} = "ssh sshd"
```

传递给dropbear的make参数是：

```
EXTRA_OEMAKE = 'MULTI=1 SCPPROGRESS=1 PROGRAMS="${SBINCOMMANDS} ${BINCOMMANDS}"'
```

PROGRAMS指定了要编译出来的二进制文件有哪些。





## INITSCRIPT_PARAMS

`update-rc.d.bbclass`这个文件控制了3个变量：

```
INITSCRIPT_PACKAGES
INITSCRIPT_NAME  
INITSCRIPT_PARAMS
```

```
INITSCRIPT_PARAMS = "start 99 5 2 . stop 20 0 1 6 ."
```

这个表示的含义是：

这个开机脚本的runlevel是99 ，在initlevel 2和initlevel 5里会调用start。

在initlevel 0/1/6会调用stop。

INITSCRIPT_PARAMS的内容会被传递给update-rc.d命令。

```
update-rc.d - install and remove System-V style init script links
```

```
SYNOPSIS
       update-rc.d [-f] name remove

       update-rc.d name defaults

       update-rc.d name defaults-disabled

       update-rc.d name disable|enable [ S|2|3|4|5 ]
```

```
update-rc.d  updates  the  System V style init script links /etc/rcrun-
       level.d/NNname whose target  is  the  script  /etc/init.d/name. 
```

# virtual/crypt



```
hanliang.xiong@walle01-sz:~/work/a113x2/yocto-code/code/poky$ grep -nwr "virtual\/crypt" . |grep "PROVIDES" 
./meta/recipes-core/musl/musl_git.bb:22:PROVIDES += "virtual/libc virtual/libiconv virtual/libintl virtual/crypt"
./meta/recipes-core/libxcrypt/libxcrypt.inc:16:PROVIDES = "virtual/crypt"
```



As an example of adding an extra provider, suppose a recipe named foo_1.0.bb contained the following:

```
PROVIDES += "virtual/bar_1.0"
```

The recipe now provides both "foo_1.0" and "virtual/bar_1.0". 

The "virtual/" namespace is often used to denote cases where multiple providers are expected with the user choosing between them.

 Kernels and toolchain components are common cases of this in OpenEmbedded.



参考资料

https://stackoverflow.com/questions/37815066/where-do-the-virtual-terms-come-from

# musl.bb

## INHIBIT_DEFAULT_DEPS

禁用默认的依赖。一般用来禁止对标准C库的依赖。



在复杂的情况下，musl还是不推荐的。

Using systemd with musl is not recommended



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

14、rockchip yocto开发

https://wiki.t-firefly.com/zh_CN/AIO-3399J/yocto_develop.html

15、openeuler的教程

https://docs.openeuler.org/zh/docs/22.03_LTS/docs/Embedded/%E5%BF%AB%E9%80%9F%E6%9E%84%E5%BB%BA%E6%8C%87%E5%AF%BC.html

16、对bitbake相关脚本进行分析

https://www.cnblogs.com/shortnil/p/9500296.html

17、

https://www.nxp.com/docs/en/supporting-information/EUF-SDS-T0106.pdf

18、

https://zhuanlan.zhihu.com/p/82217693

19、这个培训PPT有300页。

https://bootlin.com/doc/training/yocto/yocto-slides.pdf

20、这里有文档翻译。

https://blog.csdn.net/neutionwei/category_8031220.html

21、

这个网站文档格式不错。

https://developer.toradex.com/linux-bsp/how-to/build-yocto/build-a-reference-image-with-yocto-projectopenembedded/

http://trac.gateworks.com/wiki/Yocto/packages