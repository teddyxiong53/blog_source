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

# yocto发展历史

Yocto Project 是一个开源的、跨平台的嵌入式 Linux 构建系统，它提供了一整套工具和方法来创建自定义的嵌入式 Linux 发行版。以下是 Yocto Project 的发展历史：

1. **2009年**: Yocto Project 的前身是 OpenEmbedded 构建系统，由开源社区形成，并由 Linux 基金会提供支持。OpenEmbedded 是一个构建和集成嵌入式 Linux 发行版的框架，致力于为嵌入式设备提供灵活性和可定制性。

2. **2010年**: Linux 基金会宣布成立 Yocto Project，旨在为嵌入式 Linux 提供一个共同的基础设施和工具链。Yocto Project 的目标是提供一个开发者友好的、可扩展的构建系统，以便开发者可以定制和构建适合他们的特定嵌入式设备的 Linux 发行版。

3. **2011年**: Yocto Project 发布了第一个稳定版本 1.0，其中包含了核心构建系统 BitBake 和 OpenEmbedded-Core 组件。

4. **2012年**: Yocto Project 发布了版本 1.2，引入了更多的工具和功能，包括 Hob 图形界面工具和 Toaster 前端。

5. **2014年**: Yocto Project 发布了版本 1.6，其中引入了新的图形界面工具 Hob 2.0，以及新的构建系统扩展功能。

6. **2015年**: Yocto Project 发布了版本 2.0，引入了新的构建系统层次结构和改进的软件包管理工具。此版本还提供了更好的 Docker 集成和嵌入式虚拟化支持。

7. **2016年**: Yocto Project 发布了版本 2.1，引入了更多的构建系统改进和功能增强，包括新的 BSP 工具和构建配置工具。

8. **2017年**: Yocto Project 发布了版本 2.4，其中包含了许多性能改进、新的软件包和工具，以及对容器化和 IoT 设备的增强支持。

9. **2019年**: Yocto Project 发布了版本 3.0，带来了许多重要的变化，包括对 Python 3 的支持、改进的构建系统性能、新的层管理工具等。

10. **2020年**: Yocto Project 发布了版本 3.2，其中包含了对 Rust 语言的支持、增强的 SDK 功能、更好的多架构支持等。

Yocto Project 持续不断地发展和改进，通过每年的新版本发布，为嵌入式开发者提供更好的构建工具和功能。它已经成为了嵌入式 Linux

 构建的主要解决方案之一，广泛应用于各种嵌入式系统和设备。

# yocto跟buildroot比较

Yocto Project和Buildroot都是用于构建嵌入式Linux系统的流行工具。它们有一些共同点，但也有一些区别。以下是Yocto Project和Buildroot之间的比较：

1. **灵活性和可定制性**：Yocto Project被设计为高度可定制和灵活的构建系统。它使用分层的元数据和概念，允许用户根据需要自定义各个组件和功能。Buildroot则更加简单和直接，提供了一个简单的配置文件，以选择和构建所需的软件包。它的定制性较低，更适合简单的嵌入式系统需求。

2. **学习曲线**：Yocto Project的学习曲线相对较陡峭，它有更复杂的架构和概念，需要一些时间和精力来理解和使用。相比之下，Buildroot更容易上手，学习和使用起来相对简单，适合初学者和对定制需求较少的项目。

3. **社区支持和生态系统**：Yocto Project拥有广泛的社区支持和活跃的开发者社区，它由Linux基金会支持，并且有许多官方和第三方的层和组件可用。Buildroot社区也相当活跃，但相对规模较小，可用的软件包和层的数量较少。

4. **目标设备和架构支持**：Yocto Project在目标设备和架构的支持方面非常强大，它支持广泛的硬件平台，并具有强大的跨体系结构的构建能力。Buildroot也提供了一些目标设备和架构的支持，但相对较少。

5. **工具和生态系统集成**：Yocto Project提供了广泛的工具集成，包括BitBake构建引擎、OpenEmbedded Core、Crosstool-NG等。它还支持与其他工具和框架的集成，如Docker、Systemd等。Buildroot则专注于提供简单而完整的构建环境，没有像BitBake那样复杂的构建引擎。

总的来说，Yocto Project适用于需要更高度定制和灵活性的复杂嵌入式系统项目，它的学习曲线较陡峭，但提供了更强大的功能和更广阔的生态系统。而Buildroot则适用于简单的嵌入式系统需求，学习曲线较平缓，更易于上手和使用。选择哪个工具取决于项目的需求、团队的技术水平和对定制程度的要求。

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

### bb和bbclass文件关系

在 Yocto Project 构建系统中，`bb` 和 `bbclass` 文件是两种不同类型的文件，

它们在配方（recipe）的定义和构建过程中发挥不同的作用。

1. **.bb 文件**：这是 BitBake 配方文件的扩展名，==通常用于定义如何构建一个软件包或镜像==。 `.bb` 文件包含有关软件包的元数据，包括软件包的名称、版本、来源、依赖关系、安装目标等。这些文件通常被放置在 Yocto Project 的层目录结构中的 `recipes` 子目录中。 `.bb` 文件定义了构建软件包所需的任务和依赖关系。它们是 BitBake 构建系统的核心。

2. **.bbclass 文件**：这些文件包含 BitBake 类的定义，==它们提供了一组通用的功能或方法==，可以在多个 `.bb` 文件中共享和重用。 `.bbclass` 文件定义了一组变量、函数和任务，以简化或通用化配方的构建过程。它们通常包含在 BitBake 层目录结构中的 `classes` 子目录中。开发人员可以将 `.bbclass` 文件包含到自己的 `.bb` 文件中，以获得这些通用功能。这有助于避免在不同 `.bb` 文件中重复定义相同的功能，从而提高代码的可维护性。

关系和作用：

- `.bb` 文件是特定软件包或镜像的配方文件，定义了如何构建该软件包。它包含有关软件包的元数据以及构建任务和依赖关系。

- `.bbclass` 文件定义通用的功能和方法，可以在多个 `.bb` 文件中共享。这些类允许开发人员重用常见功能，如自动配置、构建和安装任务，从而减少重复的代码。

- `.bb` ==文件可以包含一个或多个 `.bbclass` 文件，以继承和使用其中定义的功能。==这允许 `.bb` 文件继承 `.bbclass` 文件中的功能，同时可以在 `.bb` 文件中进行定制和配置。

总之，`.bb` 文件是软件包或镜像的具体构建定义，而 `.bbclass` 文件是用于提供通用构建功能和任务的类定义。它们共同构成了 Yocto Project 构建系统中的配方和通用构建功能的基础。

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

# 常用命令

Yocto Project 是一个强大的嵌入式 Linux 构建系统，它有很多命令和工具，用于构建和管理嵌入式 Linux 发行版。以下是一些常用的 Yocto 命令：

1. **初始化构建环境：**

   - `source oe-init-build-env`：进入构建目录并设置构建环境。
   
2. **构建软件包和映像：**

   - `bitbake <recipe>`：构建指定的软件包或映像。
   
3. **清理构建目录：**

   - `bitbake -c clean <recipe>`：清理指定软件包的构建文件。
   - `bitbake -c cleansstate <recipe>`：清理指定软件包的 sstate 缓存。
   - `bitbake -c cleanall <recipe>`：清理指定软件包的构建文件和 sstate 缓存。

4. **构建整个发行版：**

   - `bitbake <image>`：构建整个 Linux 发行版映像。
   
5. **查看可用的软件包和映像：**

   - `bitbake-layers show-recipes`：显示可用的软件包和配方。
   - `bitbake-layers show-recipes -i`：显示已安装的软件包和配方。

6. **查看构建日志：**

   - `less <log_file>`：查看构建日志文件。
   
7. **查看软件包信息：**

   - `bitbake -e <recipe>`：显示指定软件包的环境变量和配置。
   
8. **清理整个构建目录：**

   - `bitbake -c cleanall <recipe>`：清理整个构建目录，包括构建文件和 sstate 缓存。

9. **更新 sstate 缓存：**

   - `bitbake -c sstate_update <recipe>`：更新 sstate 缓存，以便在多个构建中共享构建结果。

10. **运行软件包测试：**

    - `bitbake -c test <recipe>`：运行软件包的测试。

11. **导出构建结果：**

    - `bitbake -c populate_sdk <recipe>`：导出 SDK（Software Development Kit）以供开发人员使用。

这些命令是 Yocto Project 中的一些常用工具，用于构建、管理和定制嵌入式 Linux 发行版。根据您的项目需求，还有其他 Yocto 命令和工具可供使用。

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

```
IMAGE_FEATURES ?= ""
IMAGE_FEATURES[type] = "list"
IMAGE_FEATURES[validitems] += "debug-tweaks read-only-rootfs read-only-rootfs-delayed-postinsts stateless-rootfs empty-root-password allow-empty-password allow-root-login post-install-logging overlayfs-etc"

```

这是 Yocto Project 中 image 配置的一部分，其中定义了一些特性（features）以控制生成的 Linux 发行版镜像的行为和属性。以下是其中一些特性的简要解释：

1. **debug-tweaks**: 启用调试相关的调整和功能，以便在开发过程中更轻松地进行故障排除。

2. **read-only-rootfs**: 根文件系统（rootfs）以只读模式挂载，以提高系统的稳定性和安全性。

3. **read-only-rootfs-delayed-postinsts**: 延迟执行 `postinst` 脚本，直到 root 文件系统从只读模式切换到可写模式。

4. **stateless-rootfs**: 使根文件系统变得无状态，通常用于创建可恢复的嵌入式系统。

5. **empty-root-password**: 禁用 root 用户的密码，通常用于安全性考虑。

6. **allow-empty-password**: 允许空密码。

7. **allow-root-login**: 允许 root 用户登录。

8. **post-install-logging**: 启用 `postinst` 脚本的日志记录。

9. **overlayfs-etc**: 使用 OverlayFS 来管理 `/etc` 目录的变更，以便支持动态修改配置文件。

这些特性可以根据项目的需求进行调整，以生成定制的嵌入式 Linux 发行版。选择哪些特性要启用取决于系统的安全性、性能、需求以及具体应用场景。



在一个image里包含的feature。

最好是写在image的bb文件里，

==你可以写在conf文件里，但是不推荐这么做。==

==如果要在image的bb文件外面对image feature进行修改。==

==使用EXTRA_IMAGE_FEATURES这个变量来进行操作。==

```
meta/conf/bitbake.conf文件里：
IMAGE_FEATURES += "${EXTRA_IMAGE_FEATURES}"
```



用IMAGE_FEATURES和

https://docs.yoctoproject.org/dev-manual/common-tasks.html#customizing-images-using-custom-image-features-and-extra-image-features

poky/meta/conf/bitbake.conf里定义了PN等变量的。值得看一下。



`IMAGE_FEATURES` 是 Yocto Project 中的一个变量，

==用于定义将包含在生成的镜像中的特性或功能。==

这些特性可以包括额外的软件包、配置选项、文件系统设置等。

通过设置 `IMAGE_FEATURES`，您可以定制生成的镜像以满足特定的需求或配置。

以下是一些常见的 `IMAGE_FEATURES` 的示例和解释：

1. **"debug-tweaks"**：==启用额外的调试功能，如 gdbserver 支持和日志级别设置。==

2. **"ssh-server-openssh"**：在镜像中包含 OpenSSH 服务器，以便通过 SSH 连接到目标设备。

3. **"package-management"**：启用包管理功能，如 opkg 或 apt，以便在目标设备上安装和管理软件包。

4. **"tar"**：包含 tar 命令行工具，以便在目标设备上进行文件操作。

5. **"audio"**：启用音频支持，包括 ALSA 驱动和相关工具。

6. **"usb-gadget"**：启用 USB Gadget 支持，允许目标设备模拟 USB 设备。

7. **"x11"**：启用 X Window System（X11）支持，以便在目标设备上运行图形用户界面应用程序。

您可以根据项目需求自定义 `IMAGE_FEATURES` 变量，以在生成的镜像中包含特定的功能或软件包。这允许您创建适用于不同目标设备或应用程序需求的镜像配置。配置 `IMAGE_FEATURES` 变量通常是在 Yocto Project 的配方文件（如 `.bb` 文件）中执行的。

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

==如果要增加使能recipe的某个属性的话, 有以下两种方法==

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

==有四个参数，==

==--enable-foo：表示如果有foo的那么使能它==

==--disable-foo:表示没有foo的情况下就不是能它==

==foo_depends： 表示如果有foo的情况下编译时的依赖。==

==foo_runtime_depends:表示如果有foo的情况下，运行时的依赖==

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



# 



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

## MACHINE_FEATURES和DISTRO_FEATURES 分别有哪些特性，如何划分？

简单点，一个描述硬件，一个描述软件。

MACHINE_FEATURES 和 DISTRO_FEATURES 是 Yocto 构建系统中用于控制特定功能和配置选项的变量。它们的作用如下：

**MACHINE_FEATURES：**
==MACHINE_FEATURES 用于描述目标设备或机器的特定功能和属性，以便在构建过程中进行相关配置。==不同的目标设备可能需要不同的配置选项，因此 MACHINE_FEATURES 允许你在构建针对不同设备的软件镜像时进行适当的设置。以下是一些常见的 MACHINE_FEATURES：

- `kernel26`：表示目标设备使用 Linux 内核 2.6。
- `usbhost`：表示目标设备支持 USB 主机模式。
- `wifi`：表示目标设备支持无线网络。
- `touchscreen`：表示目标设备配备了触摸屏。

要启用或禁用这些特性，你可以在 `local.conf` 或 `.conf` 文件中设置 `MACHINE_FEATURES` 变量。

**DISTRO_FEATURES：**
==DISTRO_FEATURES 用于描述目标 Linux 发行版或发行配置中的功能和属性。==这些特性通常用于指定软件包集合、系统服务和默认配置选项，以确保生成的 Linux 发行版与目标环境的需求相匹配。以下是一些常见的 DISTRO_FEATURES：

- `systemd`：表示使用 systemd 作为 init 系统。
- `x11`：表示支持 X Window 系统（图形用户界面）。
- `opengl`：表示支持 OpenGL 图形库。
- `pam`：表示支持 Pluggable Authentication Modules（PAM）。

要启用或禁用这些特性，你可以在 `local.conf` 或 `.conf` 文件中设置 `DISTRO_FEATURES` 变量。

划分 MACHINE_FEATURES 和 DISTRO_FEATURES 的关键在于，前者主要用于描述硬件特性和属性，而后者主要用于描述软件特性和配置选项。这有助于确保构建系统生成的软件镜像与目标硬件和目标 Linux 发行版的需求相匹配。

# IMAGE_FEATURES和DISTRO_FEATURES关系

`IMAGE_FEATURES` 和 `DISTRO_FEATURES` 是 Yocto Project 构建系统中的两个关键变量，

它们之间存在一定的关系，但也有不同的作用。



1. **DISTRO_FEATURES**：`DISTRO_FEATURES` 是用于==描述发行版特性的变量。==它定义了整个发行版或分发中的全局特性，==这些特性会影响所有镜像和软件包。==例如，`DISTRO_FEATURES` 可以包括 "systemd"、"x11"、"pam" 等，用于标识发行版所支持的系统特性。

2. **IMAGE_FEATURES**：`IMAGE_FEATURES` 是==用于描述生成的镜像特性的变量==。它允许您在生成的镜像中包括与特定镜像相关的特性。==这些特性通常是与硬件平台或用途相关的==，因此可以在不同的镜像中定义不同的 `IMAGE_FEATURES`，以满足特定需求。例如，一个针对嵌入式系统的镜像可能包括 "debug-tweaks"、"package-management" 和 "ssh-server-openssh"，而一个用于 IoT 设备的镜像可能只包括 "package-management" 和 "ssh-server-dropbear"。

关系和区别：

- `DISTRO_FEATURES` 定义了整个发行版的特性，影响所有镜像和软件包，而 `IMAGE_FEATURES` 定义了特定镜像的特性。

- ==`DISTRO_FEATURES` 在全局范围内设置，通常在发行版层或 BSP 层配置文件中定义。`IMAGE_FEATURES` 在特定镜像的 BitBake 配方文件中定义。==

- `DISTRO_FEATURES` 通常包括基本系统特性，如 init 系统、包管理器等。`IMAGE_FEATURES` 包括特定于镜像的特性，如调试支持、网络服务等。

- `DISTRO_FEATURES` 是发行版开发者定义的，而 `IMAGE_FEATURES` 是系统集成者或设备制造商定义的，以满足特定硬件和应用程序需求。

总之，`DISTRO_FEATURES` 和 `IMAGE_FEATURES` 都是用于配置 Yocto Project 构建的关键变量，==但它们的作用范围和目的不同。==

`DISTRO_FEATURES` 定义全局发行版特性，而 `IMAGE_FEATURES` 允许为不同镜像定义特定特性，以满足目标设备的需求。

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



`MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS` 是一个 Yocto Project 构建系统中的机器配置变量，

==用于定义适用于特定目标机器（`MACHINE`）的附加软件包建议（`RRECOMMENDS`）列表。==

这个变量允许您为特定机器添加额外的建议性软件包，以满足特定目标机器的需求。

在 Yocto 构建系统中，`RRECOMMENDS` 变量用于指定一个软件包所建议安装的其他软件包。这些建议性软件包通常与目标软件包相关，以提供额外的功能或增强性能。

`MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS` 的作用是为特定的目标机器定义附加的建议性软件包。这在以下情况下非常有用：

1. **硬件相关功能**：某些机器可能具有特定的硬件功能，需要额外的软件包来充分利用这些功能。通过 `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS`，您可以为这些机器添加相关的建议性软件包。

2. **性能优化**：某些机器可能需要特定的性能优化或配置，这可以通过添加建议性软件包来实现。

3. **自定义需求**：如果特定机器有自定义需求或限制，您可以通过 `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS` 为其添加相应的建议性软件包。

下面是一个示例，演示了如何在 `MACHINE` 配置文件中使用 `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS`：

```bitbake
MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS = "package1 package2"
```

在上述示例中，`MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS` 定义了一个空格分隔的软件包列表，这些软件包将会成为特定机器的建议性软件包。

总之，`MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS` 是 Yocto 构建系统中的一个机器配置变量，用于为特定目标机器指定额外的建议性软件包。这可以帮助您根据机器的需求自定义构建，以满足特定硬件或性能要求。



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



注意与`FILES`差异，`FILES`是指明软件包内部哪些文件需要参与打包，

而`IMAGE_INSTALL`是指明哪个软件包需要参与打包。



这个文档不错。对于一些概念解释比较清楚。

https://www.icode9.com/content-4-1287459.html





`PACKAGE_INSTALL` 和 `IMAGE_INSTALL` 是 Yocto Project 构建系统中用于管理软件包安装的变量，它们之间存在一些关系，但也有一些重要的区别。

1. **PACKAGE_INSTALL**：
   - `PACKAGE_INSTALL` 是一个 BitBake 类的变量，==通常在配方（recipe）文件中使用。==
   - 该变量用于指定要将哪些软件包包含在构建过程中的软件包列表中。这些软件包通常是目标设备上的软件包。
   - `PACKAGE_INSTALL` 变量定义了配方所依赖的软件包，这些软件包将被安装到目标设备上。
   - 该变量用于构建目标设备上的软件包集合，而不是生成镜像文件。

2. **IMAGE_INSTALL**：
   - `IMAGE_INSTALL` 是一个 BitBake 类的变量，==通常在镜像配方文件中使用。==
   - 该变量用于指定将包含在生成的镜像文件中的软件包列表。这些软件包通常是用于构建目标设备的根文件系统（rootfs）。
   - `IMAGE_INSTALL` 变量定义了生成的镜像文件中包含的软件包，这些软件包将成为生成的镜像的一部分。
   - 该变量用于定义生成的镜像文件的内容，以及要在镜像中包含的软件包。

关系和区别：

- `PACKAGE_INSTALL` 和 `IMAGE_INSTALL` ==都用于管理软件包，但它们分别用于不同的上下文。==`PACKAGE_INSTALL` 用于构建目标设备上的软件包集合，而 `IMAGE_INSTALL` 用于定义生成的镜像文件的内容。

- `PACKAGE_INSTALL` 可以在配方文件中指定，以确定配方的构建过程中需要的软件包，而 `IMAGE_INSTALL` 通常在镜像配方文件中指定，以确定生成的镜像文件的内容。

- `PACKAGE_INSTALL` 用于处理软件包的依赖关系和构建过程，而 `IMAGE_INSTALL` 用于定义生成的镜像的内容，包括软件包、配置文件和其他文件。

总之，`PACKAGE_INSTALL` 和 `IMAGE_INSTALL` 是 Yocto Project 构建系统中用于管理软件包的变量，它们用于不同的上下文和目的。`PACKAGE_INSTALL` 用于构建目标设备上的软件包集合，而 `IMAGE_INSTALL` 用于定义生成的镜像文件的内容。它们在构建过程中具有不同的作用和用途。

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

`IMAGE_ROOTFS_SIZE` 是 Yocto Project 构建系统中的一个变量，

用于指定生成的镜像文件系统（rootfs）的大小。

通过设置 `IMAGE_ROOTFS_SIZE` 变量，您可以控制生成的镜像文件系统的大小，以确保它满足特定的存储要求。

`IMAGE_ROOTFS_SIZE` 的值通常以字节为单位，

==并可以采用常见的存储单位，如 KB、MB 或 GB。==

例如，您可以设置 `IMAGE_ROOTFS_SIZE` 为 `1024M` 表示 1GB 的镜像文件系统大小。

以下是一个示例 `IMAGE_ROOTFS_SIZE` 变量的设置：

```shell
IMAGE_ROOTFS_SIZE = "512M"
```

在这个示例中，`IMAGE_ROOTFS_SIZE` 被设置为 512MB。

# IMAGE_ROOTFS_EXTRA_SPACE

`IMAGE_ROOTFS_EXTRA_SPACE` 是 Yocto Project 构建系统中的一个变量，

==用于指定生成的镜像文件系统（rootfs）的额外空间大小。==

通过设置 `IMAGE_ROOTFS_EXTRA_SPACE` 变量，您可以为镜像文件系统预留额外的可用空间，以确保在实际使用中有足够的空间来安装和运行应用程序或进行其他操作。

`IMAGE_ROOTFS_EXTRA_SPACE` 的值通常以字节为单位，也可以使用常见的存储单位，如 KB、MB 或 GB。例如，您可以设置 `IMAGE_ROOTFS_EXTRA_SPACE` 为 `256M` 表示预留 256MB 的额外空间。

以下是一个示例 `IMAGE_ROOTFS_EXTRA_SPACE` 变量的设置：

```shell
IMAGE_ROOTFS_EXTRA_SPACE = "256M"
```

在这个示例中，`IMAGE_ROOTFS_EXTRA_SPACE` 被设置为 256MB。

# IMAGE_PREPROCESS_COMMAND

`IMAGE_PREPROCESS_COMMAND` 是 Yocto Project 构建系统中的一个变量，

==用于指定在生成镜像之前执行的自定义命令或脚本。==

这些命令用于在构建过程中预处理镜像，允许您执行一些自定义操作以满足特定需求。

`IMAGE_PREPROCESS_COMMAND` 的值是一个 shell 命令或脚本的字符串。这些命令将在生成镜像之前执行。这些自定义操作可以包括以下内容：

- 拷贝、移动或删除文件或目录。
- 修改配置文件。
- 执行任何其他必要的自定义设置。

通过设置 `IMAGE_PREPROCESS_COMMAND`，您可以在构建镜像之前执行任何必要的自定义操作，以满足特定的需求。这对于在镜像生成过程中自动执行一些任务非常有用。

以下是一个示例 `IMAGE_PREPROCESS_COMMAND` 变量的设置：

```shell
IMAGE_PREPROCESS_COMMAND = "my_custom_script.sh"
```

在这个示例中，`my_custom_script.sh` 是一个自定义脚本，将在生成镜像之前执行。这个脚本可以包括您希望在镜像生成之前执行的所有自定义操作。

# IMAGE_CLASSES

`IMAGE_CLASSES` 是 Yocto Project 构建系统中的一个变量，

==用于指定在生成镜像时要应用的 BitBake 类。==

BitBake 类是一组功能和任务的集合，它们可以用于自定义镜像的构建过程。通过设置 `IMAGE_CLASSES` 变量，您可以选择应用哪些类来构建生成的镜像，以满足特定需求或要求。

`IMAGE_CLASSES` 的值是一个以空格分隔的 BitBake 类的列表。这些类通常包含在 Yocto Project 构建系统中，或者您也可以自定义自己的类。

以下是一些常见的 `IMAGE_CLASSES` 类的示例：

- `image`：==这是默认的镜像类，用于构建标准的 Linux 镜像==。

- `live`：用于构建 Live CD 或 Live USB 镜像，允许从可启动的媒体引导并运行 Linux。

- `tar`：用于构建 tarball 格式的镜像，通常用于离线分发。

- `wic`：用于使用 Yocto Image Creator (Wic) 构建镜像，支持更高级的自定义。

- `ext4`：用于创建 ext4 文件系统格式的镜像。

- `ubi`：用于创建 UBI（Unsorted Block Images）格式的镜像，通常用于嵌入式系统。

您可以通过设置 `IMAGE_CLASSES` 变量来组合这些类，以满足特定的镜像需求。例如，如果您需要构建一个 Live CD 镜像，您可以设置：

```shell
IMAGE_CLASSES = "image live"
```

通过选择不同的类组合，您可以定制生成的镜像以满足不同目标设备或应用程序的需求。这提供了 Yocto Project 构建系统中的灵活性和可定制性。

# DM_VERITY_IMAGE

`DM_VERITY_IMAGE` 是 Yocto Project 构建系统中的一个变量，

用于指定是否启用 Device Mapper Verity 验证（DM-Verity）功能。

DM-Verity 是一个用于校验 Linux 文件系统完整性的技术，通常用于嵌入式系统中，以确保文件系统没有被损坏或篡改。



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

看这个解释就懂了：

```
PKG_CONFIG_PATH[vardepsexclude] = "datadir WORKDIR"

在 Yocto Project 中，`PKG_CONFIG_PATH` 是一个 BitBake 变量，用于定义用于查找 pkg-config 包配置文件的路径。`PKG_CONFIG_PATH` 变量允许您明确指定 pkg-config 工具用于查找依赖库的路径。

`PKG_CONFIG_PATH[vardepsexclude]` 是 `PKG_CONFIG_PATH` 变量的一个设置，用于控制哪些 BitBake 变量不会自动引发 `PKG_CONFIG_PATH` 的重新解析。在这种情况下，通过设置 `PKG_CONFIG_PATH[vardepsexclude] = "datadir WORKDIR"`，您告诉 BitBake 不要重新解析 `PKG_CONFIG_PATH` 变量，即使 `datadir` 和 `WORKDIR` 这两个变量的值发生变化。

这是有用的，因为 `PKG_CONFIG_PATH` 通常包括了一系列路径，它们在构建时应该是稳定的，不随其他变量的变化而变化。通过设置 `PKG_CONFIG_PATH[vardepsexclude]`，您可以避免不必要的重新解析，提高构建系统的效率。

通常情况下，`vardepsexclude` 是一个用于排除特定 BitBake 变量的列表，以防止它们触发 `PKG_CONFIG_PATH` 的重新解析。这有助于确保 `PKG_CONFIG_PATH` 只在必要时被重新解析，从而避免不必要的构建延迟。
```





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



在 Yocto 构建系统中，`TCMODE`（Target Configuration Mode）是一个变量，用于指定目标体系结构的构建配置模式。

它定义了构建系统在为目标体系结构构建软件包时的行为。

`TCMODE` 变量有以下几个可能的值：

1. `nativesdk`：在本地主机（native）上构建 SDK 时使用。这允许构建 SDK，以便在开发目标体系结构的应用程序时使用。

2. `cross`：用于目标体系结构的交叉编译。这是构建目标体系结构软件包的标准模式。

3. `crosssdk`：在构建 SDK 时使用的目标体系结构模式。这允许构建目标体系结构的 SDK，以便在开发目标体系结构的应用程序时使用。

不同的 `TCMODE` 值会影响构建系统的行为，以确保适当的软件包和工具被构建，以满足不同的构建需求。在创建构建配置或在构建系统配置文件中指定 `TCMODE` 值是很常见的，以便控制目标体系结构的构建行为。

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



`INSANE_SKIP` 是 Yocto Project 构建系统中用于==控制静态检查（sanity check）过程的一个变量==。

这个变量允许您指定哪些检查应该被跳过，以满足特定的构建需求。

静态检查是构建过程中的一项重要步骤，

==用于检查生成的软件包和镜像是否符合标准和预期的要求。==

然而，在某些情况下，由于特殊需求或其他原因，您可能希望跳过特定的检查步骤。

`INSANE_SKIP` 的值是一个以逗号分隔的检查列表，每个检查都有一个特定的名称。

您可以将这些检查的名称添加到 `INSANE_SKIP` 变量中，以告诉 Yocto Project 构建系统跳过这些检查。以下是一些示例：

```shell
INSANE_SKIP = "ldflags ldflagslibs"
```

==在这个示例中，`INSANE_SKIP` 变量设置为跳过 "ldflags" 和 "ldflagslibs" 这两个检查步骤。==

常见的 `INSANE_SKIP` 检查包括：

- `ldflags`：用于检查链接标志（ldflags）是否正确设置。
- `ldflagslibs`：用于检查链接标志中的库是否正确。
- `dev-so`：用于检查共享库是否包含正确的符号（symbol）。
- `pkgconfig`：用于检查 pkg-config 文件是否正确。

通过使用 `INSANE_SKIP` 变量，您可以在特定情况下灵活地跳过某些检查，以满足特定的构建需求。请注意，应谨慎使用 `INSANE_SKIP`，以确保不会导致潜在的问题或安全风险。跳过某些检查可能会导致生成的软件包或镜像不符合预期的标准。



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

Yocto Project Devtool 是一个工具，用于简化嵌入式 Linux 软件开发和构建工作流程。

它可以帮助开发人员添加、修改、调试和测试软件包，

==而无需手动编写 BitBake 配方（recipes）。==

以下是一些基本的 `devtool` 命令和用法：

1. **安装软件包到工程中**:
   
   ```bash
   devtool add <recipe-name>
   ```
用于将一个软件包添加到当前 Yocto Project 工程中。`<recipe-name>` 是软件包的名称，Devtool 将自动生成一个 BitBake 配方。
   
   以我的argcv加入为例：
   
   ```
   devtool add argcv  https://github.com/teddyxiong53/argcv --srcbranch main
   ```
   
   需要指定分支为main，因为现在github默认是main分支，为不指定的时候，默认是找master分支。会出错。
   
   默认是在这个目录下：
   
   ```
   build-av400/workspace$ tree
   .
   ├── appends
   │   └── argcv_git.bbappend
   ├── conf
   │   └── layer.conf
   ├── README
   ├── recipes
   │   └── argcv
   │       └── argcv_git.bb
   └── sources
       ├── argcv
       │   ├── argcv.c
       │   ├── argcv.h
       │   ├── LICENSE
       │   ├── Makefile
       │   ├── README.md
       │   └── test.c
       └── devtoolsrcq0mulksg
   ```
   
   
   
2. **修改已存在的软件包**:
   
   ```bash
   devtool modify <recipe-name>
   ```
用于修改已存在的软件包的 BitBake 配方。==它会将配方复制到 `workspace/sources/<recipe-name>` 中，然后您可以进行修改。==
   
3. **生成软件包的 patches**:
   
   ```bash
   devtool extract <recipe-name>
   ```
用于从已存在的软件包生成 patches，以便进行修改或调试。
   
4. **重新构建软件包**:
   
   ```bash
   devtool build <recipe-name>
   ```
用于重新构建软件包，包括修改后的软件包。这将使用 BitBake 构建过程重新构建软件包。
   
5. **测试软件包**:
   
   ```bash
   devtool test <recipe-name>
   ```
用于测试软件包，包括运行自动化测试套件或手动测试。
   
6. **将软件包从工程中移除**:
   ```bash
   devtool remove <recipe-name>
   ```
   用于从当前工程中移除软件包，同时删除相关的 BitBake 配方。

7. **查看工程中的软件包**:
   ```bash
   devtool list
   ```
   用于列出工程中的所有软件包。

8. **查看软件包信息**:
   ```bash
   devtool info <recipe-name>
   ```
   用于查看特定软件包的信息，包括 BitBake 配方的位置。

9. **生成软件包的 README 文件**:
   ```bash
   devtool finish <recipe-name>
   ```
   用于生成软件包的 README 文件，以提供软件包的使用和集成信息。

以上是一些常用的 `devtool` 命令和用法，它们可以帮助简化 Yocto Project 软件包开发和构建过程。使用 `devtool` 可以加速软件包开发，减少手动配置和编写 BitBake 配方的工作。您可以在 Yocto Project 文档中找到更多有关 `devtool` 的信息和详细用法。

## devtool的帮助信息

```
NOTE: Starting bitbake server...
usage: devtool [--basepath BASEPATH] [--bbpath BBPATH] [-d] [-q] [--color COLOR] [-h] <subcommand> ...

OpenEmbedded development tool

options:
  --basepath BASEPATH   Base directory of SDK / build directory
  --bbpath BBPATH       Explicitly specify the BBPATH, rather than getting it from the metadata
  -d, --debug           Enable debug output
  -q, --quiet           Print only errors
  --color COLOR         Colorize output (where COLOR is auto, always, never)
  -h, --help            show this help message and exit

subcommands:
  Beginning work on a recipe:
    add                   Add a new recipe
    modify                Modify the source for an existing recipe
    upgrade               Upgrade an existing recipe
  Getting information:
    status                Show workspace status
    search                Search available recipes
    latest-version        Report the latest version of an existing recipe
    check-upgrade-status  Report upgradability for multiple (or all) recipes
  Working on a recipe in the workspace:
    build                 Build a recipe
    rename                Rename a recipe file in the workspace
    edit-recipe           Edit a recipe file
    find-recipe           Find a recipe file
    configure-help        Get help on configure script options
    update-recipe         Apply changes from external source tree to recipe
    reset                 Remove a recipe from your workspace
    finish                Finish working on a recipe in your workspace
  Testing changes on target:
    deploy-target         Deploy recipe output files to live target machine
    undeploy-target       Undeploy recipe output files in live target machine
    build-image           Build image including workspace recipe packages
  Advanced:
    create-workspace      Set up workspace in an alternative location
    export                Export workspace into a tar archive
    menuconfig            Alter build-time configuration for a recipe
    extract               Extract the source for an existing recipe
    sync                  Synchronize the source tree for an existing recipe
    import                Import exported tar archive into workspace
Use devtool <subcommand> --help to get help on a specific command
```



## devtool系列文章

https://zhuanlan.zhihu.com/p/363402893







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

`PREFERRED_VERSION` 是 Yocto Project 和 OpenEmbedded 构建系统中的一个特殊变量，

用于指定软件包的首选版本。

这个变量通常用于指定项目所需软件包的特定版本或版本范围。下面是关于 `PREFERRED_VERSION` 的一些关键信息：

1. **目的**：`PREFERRED_VERSION` 的主要目的是允许开发人员控制构建所使用的软件包版本。这对于确保构建的稳定性和可重现性非常重要。

2. **语法**：`PREFERRED_VERSION` 的语法是一个表达式，可以使用通配符来匹配多个版本。通常，它的形式是 `"package-name = "version""`，其中 `"package-name"` 是软件包名称，而 `"version"` 是首选的版本或版本范围。

3. **示例**：以下是一些 `PREFERRED_VERSION` 的示例：

   - `PREFERRED_VERSION_u-boot = "v2019.%"`：表示首选 `u-boot` 软件包的版本是 `v2019`，后面的 `%` 通配符表示匹配 `v2019` 后的任何版本。

   - `PREFERRED_VERSION_linux-meson = "5.4.%"`：表示首选 `linux-meson` 软件包的版本是 `5.4`，后面的 `%` 通配符表示匹配 `5.4` 后的任何版本。

4. **作用范围**：==`PREFERRED_VERSION` 的作用范围通常是软件包的配置文件（`.bb` 文件）。每个软件包可以具有自己的 `PREFERRED_VERSION` 设置。==

5. **版本解析**：`PREFERRED_VERSION` 会在可用版本中查找与给定版本或版本范围匹配的软件包。如果找到多个匹配项，构建系统将尝试选择最匹配的版本，以满足构建要求。

6. **通配符**：通配符如 `%` 用于匹配任何字符串。这可以在首选版本中用于选择特定版本号之后的所有版本。

总之，`PREFERRED_VERSION` 是一个在 Yocto 构建系统中用于管理软件包版本的重要工具，允许开发人员更好地控制构建过程中使用的软件包版本，以确保构建的稳定性和一致性。

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

# 允许商业license软件的加入

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

你可以使用_append方式来给一个已经存在的变量追加值，

跟+=不一样的是这种方式不会在原值和你要追加的值中间加上空格。



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

表示编译一个host的版本。native相当于host版本。nativesdk相当于target版本。



1. **"native" 类别**：这表示配方将被处理为本地主机（开发主机）上的本地构建。这通常用于构建主机本身使用的工具或程序。如果您在配方中指定了 `do_configure`、`do_compile` 等任务，它们将在本地主机上运行。
2. **"nativesdk" 类别**：这表示配方将被处理为 SDK（Software Development Kit）构建，用于交叉编译工具链和库以供目标设备使用。如果您需要为目标设备构建开发工具、库或 SDK，则可以使用这个类别。



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



`DISTRO_FEATURES_BACKFILL_CONSIDERED` 是 Yocto Project 构建系统中的一个特殊变量，

用于配置哪些 `DISTRO_FEATURES` 特性需要进行“回填”（backfill）以适应特定的发行版（Distribution）。

这个变量通常在发行版配置文件（`conf/distro/*.conf`）中设置。

在 Yocto 构建系统中，`DISTRO_FEATURES` 是一个用于指定构建中启用的特性的变量。

它允许您启用或禁用各种功能，以满足特定发行版的需求。

==有时候，特定的发行版可能需要启用额外的 `DISTRO_FEATURES` 特性来支持其功能，但同时又需要保持兼容性。==



通常，`DISTRO_FEATURES_BACKFILL_CONSIDERED` 可以包含一个特性列表，指定哪些特性需要被考虑进行“回填”，以满足特定发行版的需求。这有助于确保构建的兼容性，并满足特定发行版的要求。

以下是一个示例，展示如何在发行版配置文件中设置 `DISTRO_FEATURES_BACKFILL_CONSIDERED`：

```bitbake
DISTRO_FEATURES_BACKFILL_CONSIDERED = "wifi"
```

==在上述示例中，`wifi` 特性被列为需要考虑进行“回填”，以确保发行版支持 WiFi 功能。==

这有助于确保构建中正确启用了所需的功能。

总之，`DISTRO_FEATURES_BACKFILL_CONSIDERED` 是 Yocto Project 构建系统中的一个变量，用于指定哪些 `DISTRO_FEATURES` 特性需要进行“回填”，以满足特定发行版的需求。这有助于确保构建的兼容性，并确保所需功能正确启用。

## 为什么不直接append到DISTRO_FEATURES里呢？

在 Yocto Project 中，`DISTRO_FEATURES` 是一个用于指定构建中启用的特性的变量。

通常，`DISTRO_FEATURES` 是在分布版的配置文件中设置的，以便明确定义在特定分布版中应启用的特性。

在实际应用中，分布版的特性通常是固定的，以确保在构建中启用了必要的功能。

而 `DISTRO_FEATURES_BACKFILL_CONSIDERED` 的目的是允许在特定情况下对特性进行“回填”。这在以下情况下可能会有用：

1. 特定的发行版需要在构建中启用额外的特性，以满足其要求。在这种情况下，`DISTRO_FEATURES_BACKFILL_CONSIDERED` 可以包含需要的特性，以确保它们在构建中启用。

2. 某些特性的启用可能受到其他因素的影响，例如硬件或构建目标。为了确保兼容性，`DISTRO_FEATURES_BACKFILL_CONSIDERED` 可以用于自动启用或回填特性，以适应不同的情况。

总之，`DISTRO_FEATURES` 通常用于明确定义发行版的特性，而 `DISTRO_FEATURES_BACKFILL_CONSIDERED` 用于确保在特定情况下进行特性的回填或调整。这种分离的方法有助于保持构建系统的清晰性，确保特性的启用是可管理的。如果您知道在所有情况下都需要某些特性，您可以将它们添加到 `DISTRO_FEATURES` 中，但在特殊情况下使用 `DISTRO_FEATURES_BACKFILL_CONSIDERED` 以进行调整。



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

# DEPENDS

`DEPENDS` 是 Yocto Project 中 BitBake 配方文件中的一个关键变量，

==用于指定当前配方（recipe）所依赖的其他配方。==

这些依赖关系告诉 BitBake 构建系统在构建当前软件包或镜像时需要使用哪些其他软件包或组件。



例如，假设您有一个名为 `myapp` 的软件包，它依赖于 `libfoo` 和 `libbar` 这两个库。您可以在 `myapp` 配方文件中设置 `DEPENDS` 变量如下：

```shell
DEPENDS = "libfoo libbar"
```

==这将告诉 BitBake 构建系统，在构建 `myapp` 之前，需要首先构建 `libfoo` 和 `libbar` 这两个依赖项。==

通过适当设置 `DEPENDS` 变量，您可以构建复杂的依赖关系树，确保软件包的所有依赖项都满足。这有助于确保生成的镜像或软件包具有所需的功能和组件。

除了显式列出 `DEPENDS`，BitBake 还会自动检测一些隐式依赖项，例如编译时依赖关系。 BitBake 会分析配方文件中的构建任务，以确定所需的依赖项。但在某些情况下，显式列出依赖关系是更明确和可控的方法。

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

# ERROR: No recipes available for

编译出现了这个错误。

```
ERROR: No recipes available for:
  /mnt/fileroot/hanliang.xiong/work/a113x2/yocto-code/code2/meta-meson/recipes-support/cryptsetup/cryptsetup_2.3.2.bbappend
```

我觉得直接的原因是，cryptsetup的bb文件，没有2.3.2的。

之前为什么没有碰到这个问题？

难道是没有使能？

之前有2.3.2的文件。现在只有2.3.7的，把2.3.2的文件放进来就好了。

# 重要的bbclass文件分析

## base.bbclass

## core-image.bbclass

## image.bbclass

## image_type.bbclass

# onepass

"onepass" 是 Yocto Project 和 BitBake 构建系统中的一个特殊标志，

用于指示 BitBake 在单次构建过程中尽量完成尽可能多的任务。

==在默认情况下，BitBake 可能会执行多次构建，以确保所有依赖关系都满足，==

==而 "onepass" 标志允许在单个构建中尽量完成更多任务，从而提高构建效率。==

"onepass" 标志的使用可以加快构建速度，

特别是对于大型项目，

因为它减少了构建过程中重复任务的执行次数。

当启用 "onepass" 时，BitBake 会尝试尽可能多地执行任务，同时确保不违反构建规则或引发不一致性。

您可以在 BitBake 命令中使用 "onepass" 标志，如下所示：

```bash
bitbake -c <task> -f -D onepass <recipe>
```

其中：
- `<task>` 是要执行的任务名称，例如 "do_compile"。
- `<recipe>` 是要构建的配方文件的名称。

通过使用 "onepass" 标志，您可以控制 BitBake 在单个构建过程中尽量完成尽可能多的任务，从而提高构建效率，特别是在多核系统上。请注意，"onepass" 标志的效果可能会因项目配置和任务依赖关系而有所不同。



# IMAGE_LINGUAS

`IMAGE_LINGUAS` 是 Yocto Project 构建系统中的一个变量，

==用于指定在生成的镜像中包含的语言支持。==

通过设置 `IMAGE_LINGUAS` 变量，您可以自定义镜像以包括特定的语言本地化支持。

`IMAGE_LINGUAS` 变量包含一个以空格分隔的语言列表。

每个语言代表一个本地化设置，可以包括翻译、字体和其他相关本地化资源。

这些语言设置将被包含在生成的镜像中，以支持多语言用户界面和应用程序。

以下是一个示例 `IMAGE_LINGUAS` 变量的设置：

```shell
IMAGE_LINGUAS = "en_US de_DE fr_FR"
```

在这个示例中，`IMAGE_LINGUAS` 包含三种语言设置：英语（"en_US"）、德语（"de_DE"）和法语（"fr_FR"）。这表示生成的镜像将包括这三种语言的本地化支持。

通过设置 `IMAGE_LINGUAS` 变量，您可以定制生成的镜像以满足多语言支持的需求。这对于国际化和本地化的嵌入式系统非常有用，因为它允许您在一个镜像中包括多种语言的支持。请注意，为了实现这一点，您还需要确保相关的翻译和本地化资源可用。



# PACKAGE_ARCH = "${MACHINE_ARCH}"

在 Yocto Project 构建系统中，`PACKAGE_ARCH` 是一个变量，用于指定软件包的体系结构（architecture）。`MACHINE_ARCH` 通常是一个定义了目标设备架构的变量，而 `PACKAGE_ARCH` 可以设置为与目标设备架构相关的值，以确保构建的软件包与目标设备的架构匹配。

==通常情况下，`PACKAGE_ARCH` 变量被设置为`${MACHINE_ARCH}`，以确保软件包的架构与目标设备的架构一致==。这是因为 Yocto Project 构建系统支持交叉编译，可以构建适用于多种不同架构的软件包。因此，将 `PACKAGE_ARCH` 设置为 `${MACHINE_ARCH}` 是一种常见的做法，以确保生成的软件包与目标设备的架构兼容。

例如，如果目标设备的架构是 ARM，那么在配方文件中通常会设置：

```shell
PACKAGE_ARCH = "${MACHINE_ARCH}"
```

这样，构建的软件包将会被编译为适用于 ARM 架构的二进制文件。

通过设置 `PACKAGE_ARCH` 为 `${MACHINE_ARCH}`，可以确保生成的软件包与目标设备的硬件架构一致，从而避免架构不匹配的问题，这对于嵌入式系统的开发和部署非常重要。

# EXTRA_OEMAKE

`EXTRA_OEMAKE` 是 Yocto Project 构建系统中的一个变量，

用于向 BitBake 配方（recipe）中的 ==Makefile 命令添加额外的选项或参数。==

通过设置 `EXTRA_OEMAKE` 变量，==您可以自定义 Makefile 命令的行为，==向构建过程中传递额外的选项或参数。

通常，`EXTRA_OEMAKE` 变量的值是一个字符串，其中包含了要传递给 Makefile 命令的额外选项。这些选项可以包括编译标志、链接标志、目标文件、定义的宏等，具体取决于 Makefile 的用途和构建需求。

例如，如果您需要在构建过程中向 Makefile 命令传递额外的编译标志 `-O2` 和 `-Wall`，您可以设置 `EXTRA_OEMAKE` 变量如下：

```shell
EXTRA_OEMAKE = "CFLAGS='-O2 -Wall'"
```

这将使 Yocto Project 构建系统在运行 Makefile 命令时将 `-O2` 和 `-Wall` 编译标志传递给编译器。

# EXTRA_OECONF

`EXTRA_OECONF` 是 Yocto Project 中用于配置软件包构建的变量之一。

它通常用于向配置脚本传递额外的参数或选项，以自定义构建过程。

在 Yocto Project 中，软件包的构建过程通常由 Autotools、CMake、Makefile 或其他构建系统的配置脚本控制。

`EXTRA_OECONF` 可以用来==向这些配置脚本传递额外的参数。==以下是一些示例用法：

1. **向 Autotools 脚本传递参数：**

   ```bitbake
   EXTRA_OECONF = "--disable-feature --enable-something"
   ```

   在这个示例中，`EXTRA_OECONF` 用于向 Autotools 脚本传递 `--disable-feature` 和 `--enable-something` 选项。

2. **设置预处理宏：**

   ```bitbake
   EXTRA_OECONF = "--define=PREPROCESS_MACRO=value"
   ```

   您可以使用 `EXTRA_OECONF` 来设置预处理宏，以影响软件包的编译过程。

3. **添加库路径和包含路径：**

   ```bitbake
   EXTRA_OECONF = "--with-lib-dir=${STAGING_LIBDIR} --with-inc-dir=${STAGING_INCDIR}"
   ```

   这个示例中，`EXTRA_OECONF` 用于指定库路径和包含路径，以确保构建过程中能够找到所需的库和头文件。

4. **自定义选项：**

   ```bitbake
   EXTRA_OECONF = "--custom-option=value"
   ```

   您可以根据需要添加自定义选项，以适应软件包的特定需求。

`EXTRA_OECONF` 变量允许您对软件包构建过程进行细粒度的控制，以满足特定需求和配置。您可以根据软件包的要求自定义 `EXTRA_OECONF` 变量，以实现所需的构建设置。这有助于确保生成的软件包在目标设备上正确配置和运行。

# EXTRA_OEMESON

`EXTRA_OEMESON` 是 Yocto Project 中用于 Meson 构建系统的变量，用于配置软件包的构建过程。Meson 是一种现代的构建系统，它在 Yocto 中广泛用于构建许多软件包。

`EXTRA_OEMESON` 变量用于向 Meson 构建系统传递额外的参数或选项，以自定义构建过程。以下是一些示例用法：

1. **向 Meson 脚本传递参数：**

   ```bitbake
   EXTRA_OEMESON = "-Dcustom_option=value -Danother_option=enabled"
   ```

   在这个示例中，`EXTRA_OEMESON` 用于向 Meson 脚本传递 `-Dcustom_option=value` 和 `-Danother_option=enabled` 选项。

2. **设置构建类型：**

   ```bitbake
   EXTRA_OEMESON = "--buildtype=release"
   ```

   您可以使用 `EXTRA_OEMESON` 来设置构建类型，如 "debug"、"release" 等。

3. **自定义选项：**

   ```bitbake
   EXTRA_OEMESON = "--custom-option=foo --another-option=bar"
   ```

   您可以根据软件包的要求添加自定义选项，以满足特定的构建配置。

`EXTRA_OEMESON` 变量允许您对 Meson 构建过程进行细粒度的控制，以满足软件包的特定需求和配置。它允许您根据软件包的要求自定义 Meson 构建设置，以确保生成的软件包在目标设备上正确配置和运行。 Meson 构建系统通常用于现代软件包，并提供了许多自定义选项，以适应各种构建需求。

# kirkstone的冒号用途

在 Yocto Project 中，冒号 `:` 通常用于==分隔不同的 BitBake 类别和类别特定的变量==。它的主要用途包括：

1. **指定 BitBake 类别**：冒号用于指定特定的 BitBake 类别，例如 `do_build`, `do_install`, `do_configure` 等。这有助于定义针对不同构建任务的操作。

   例如，您可以在 BitBake 配方中使用以下方式指定一个任务：

   ```bitbake
   do_build:mytask() {
       # 这是一个自定义构建任务
   }
   ```

   这将定义一个名为 `mytask` 的自定义构建任务。

2. **指定 BitBake 类别特定的变量**：冒号还用于指定特定 BitBake 类别的变量。这意味着您可以为不同构建任务指定不同的变量值。

   例如，您可以设置一个特定于构建任务的变量：

   ```bitbake
   FILES_${PN}:mytask += "${datadir}/myfiles"
   ```

   这将在构建任务 `mytask` 中添加特定文件到软件包。

3. **继承类别和操作**：冒号还可用于继承 BitBake 类别和操作。通过继承，您可以重用和扩展现有的 BitBake 类别和任务。

   例如，您可以继承 `do_configure` 操作，然后在其基础上添加自定义操作：

   ```bitbake
   do_configure:mytask() {
       # 在配置之前执行一些自定义操作
       inherit do_configure
   }
   ```

4. **指定 BitBake 类别的变体**：冒号也用于指定 BitBake 类别的变体。这允许您为不同的构建目标定义不同的操作。

   例如，您可以定义一个 `do_build` 操作的变体，以根据目标选择不同的构建选项：

   ```bitbake
   do_build:myvariant() {
       # 根据目标选择不同的构建选项
   }
   ```

总之，冒号 `:` 在 Yocto Project 中用于定义和区分不同的 BitBake 类别、操作和变量，以实现更灵活和精确的控制和定制软件包的构建过程。

# RPROVIDES:${PN}-dev = "alsa-dev"

在 Yocto Project 的 BitBake 配方中，`RPROVIDES` 变量用于指定软件包提供的功能或库。

在您的示例中，==`${PN}-dev` 是软件包名称的占位符，通常用于表示开发文件和头文件包。==

具体来说，`RPROVIDES:${PN}-dev = "alsa-dev"` 表示 `${PN}-dev` 软件包提供了 "alsa-dev" 功能或库。

==这意味着其他软件包可以依赖于 `${PN}-dev` 软件包来获取 "alsa-dev" 功能或库，==

通常是开发时所需的头文件和开发库文件。

这种关系的定义有助于确保开发软件包正确地提供所需的开发文件，并使其他软件包能够正确地依赖于这些开发文件以进行开发和编译。

这对于 Yocto Project 构建和管理软件包之间的依赖关系非常重要。



# SRC_URI[sha256sum]

`SRC_URI` 是在 Yocto Project 的 BitBake 配方中用于指定软件包源代码下载地址的变量。

`SRC_URI[sha256sum]` 是用于指定下载文件的 SHA-256 校验和的部分。

SHA-256 校验和是一种用于验证下载文件完整性的加密哈希值。

在 BitBake 配方中，您可以为下载的软件包文件指定 SHA-256 校验和，以确保文件在下载后没有被篡改或损坏。

具体来说，`SRC_URI` 变量可以包含一个或多个下载 URL，

==每个 URL 可以配备一个或多个哈希值（例如 SHA-256）。==

`SRC_URI[sha256sum]` 是用于指定 SHA-256 校验和的部分。示例：

```bitbake
SRC_URI = "https://example.com/software.tar.gz \
           file://local-copy.tar.gz;md5=1234567890abcdef1234567890abcdefab \
           file://another-local-copy.tar.gz;sha256=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdefab"
```

在上述示例中：

- ==第一个 URL 使用默认的 SHA-256 校验和。BitBake 将自动计算文件的 SHA-256 值，并与配方中指定的哈希值进行比较，以确保下载的文件完整。==

- 第二个 URL 是本地文件的示例，使用 `md5` 指定了 MD5 校验和，而不是 SHA-256。

- 第三个 URL 也是本地文件的示例，使用 `sha256` 指定了 SHA-256 校验和。

通过使用 `SRC_URI` 中的哈希值，您可以确保 Yocto Project 在构建过程中使用正确的、完整的源代码文件。

如果哈希值不匹配，BitBake 将引发错误，以防止使用损坏或被篡改的文件。这有助于确保软件包的可靠性和安全性。

# PACKAGES_DYNAMIC

`PACKAGES_DYNAMIC` 是 Yocto Project BitBake 配方中的一个变量，

==用于指定动态生成软件包名称的规则。==

这允许根据 BitBake 变量或其他条件动态生成软件包名称，以适应不同的配置选项和需求。

通常，`PACKAGES_DYNAMIC` 的值是一个包含规则的列表，这些规则定义了如何生成软件包名称。

每个规则由两部分组成：一个变量名和一个 BitBake 函数。

当 BitBake 函数返回非空值时，相应的软件包将被生成。

以下是一个示例：

```bitbake
PACKAGES_DYNAMIC += "^mydynamicpackage$"
mydynamicpackage() {
    if [ "$SOMETHING" = "something" ]; then
        echo "my-dynamic-package-name"
    fi
}
```

在上述示例中，我们：

1. 将 `mydynamicpackage` 添加到 `PACKAGES_DYNAMIC` 变量中，以指定一个动态生成软件包名称的规则。

2. `mydynamicpackage()` 函数定义了如何生成软件包名称。在此示例中，如果某个条件（在这里是 `$SOMETHING` 的值等于 "something"）成立，那么该函数会返回软件包名称 "my-dynamic-package-name"。

通过使用 `PACKAGES_DYNAMIC`，您可以在 BitBake 配方中定义动态生成软件包名称的规则，以适应不同的配置和需求。这对于自定义构建非常有用，因为它允许您根据条件生成特定的软件包，以满足项目的需求。

# MLPREFIX

`MLPREFIX` 是 Yocto Project 中一个与多重软件包 (multilib) 构建相关的变量。

多重软件包构建是为了在相同的目标系统上支持多个不同架构或 ABI（应用程序二进制接口）的软件包。

这对于支持多种目标体系结构或操作系统变体非常有用。

`MLPREFIX` 变量的目的是允许您为不同的架构或 ABI 构建软件包时指定不同的前缀。

通常，软件包名称中包含了用于标识目标体系结构或 ABI 的前缀。

例如，对于 ARM 架构的软件包，可能会使用前缀 `arm-`，而对于 x86 架构的软件包，可能会使用前缀 `x86-`。

`MLPREFIX` 变量允许您定义不同架构或 ABI 的前缀，以便在多重软件包构建期间应用到软件包名称上。

这有助于确保不同版本的软件包彼此独立，不会相互干扰。

例如，您可以像这样在 Yocto Project 配方中使用 `MLPREFIX`：

```bitbake
MLPREFIX_x86-64 = "x86-64-"
MLPREFIX_arm = "arm-"
```

在上述示例中，我们定义了两个不同的架构（x86-64 和 ARM）的 `MLPREFIX`。然后，在构建多重软件包时，将自动应用适当的前缀到软件包名称上，以确保它们在同一系统上并行存在并且不会互相冲突。

`MLPREFIX` 变量是多重软件包构建的重要组成部分，使您能够管理并维护不同架构或 ABI 的软件包。

# autotools-brokensep

`autotools-brokensep` 是 Yocto Project 中的一个类（class），

用于处理基于 Autotools 构建系统的软件包的构建问题。

Autotools 是一套用于自动配置、构建和安装软件的工具，包括 Autoconf、Automake 和 Libtool。

==在某些情况下，使用 Autotools 构建的软件包可能会遇到一些问题，特别是在多重软件包构建环境中。==

`autotools-brokensep` 类==主要用于解决 Autotools 构建系统中的路径分隔符问题，==

特别是在多重软件包构建环境中。

路径分隔符问题通常涉及到构建软件包时，Autotools 使用了硬编码的路径分隔符（例如 `/`），

而在某些情况下，这会导致问题，特别是当构建软件包以不同架构或 ABI 时。

该类通过在构建过程中设置适当的环境变量来解决路径分隔符问题，以确保软件包能够在多重软件包构建环境中正确构建。这有助于避免路径分隔符问题引发的构建失败或错误。

在 Yocto Project 配方中，您可以通过继承 `autotools-brokensep` 类来应用这个类的功能。示例：

```bitbake
inherit autotools-brokensep
```

通过继承 `autotools-brokensep` 类，您可以确保您的 Autotools 构建系统在多重软件包构建环境中能够正确运行。这有助于提高构建系统的可移植性和兼容性。

# inherit allarch

`inherit allarch` 是 Yocto Project 配方中的一条指令，

用于指定某个软件包或类别的构建适用于所有目标架构，

==即不考虑目标架构的区别，使用相同的构建规则。==

当您在 Yocto Project 中编写软件包配方时，通常会针对不同的目标架构（如 x86、ARM、MIPS 等）编写不同的构建规则和设置。

这是因为不同的架构可能需要不同的编译选项、库路径、代码优化等。

然而，在某些情况下，某个软件包或类别的构建规则对于所有目标架构都是相同的，这时可以使用 `inherit allarch` 指令。



以下是示例：

```bitbake
inherit allarch
```

通过继承 `allarch` 类，您表明该软件包或类别的构建规则是与目标架构无关的。

这有助于减少重复工作，提高代码可维护性，并简化构建系统的设置。请确保只在确信构建规则与目标架构无关的情况下使用此指令。

# LICENSE_FLAGS = "commercial"

`LICENSE_FLAGS` 是 Yocto Project 配方中用于指定软件包许可证标志的变量。

`LICENSE_FLAGS` 可以用于设置软件包的许可证策略，以控制许可证的使用和合规性。

在您提供的示例中，`LICENSE_FLAGS` 被设置为 "commercial"，

这意味着软件包或软件包类别在构建过程中将使用商业许可证。

这通常用于指示软件包包含有限制性或商业性质的许可证，可能需要额外的许可证或授权，以便在商业环境中使用。

软件包可能受到专有软件的许可证限制，或者可能包含专有代码或算法。

在 Yocto Project 中，通过设置 `LICENSE_FLAGS`，可以在构建过程中强制执行许可证策略，确保软件包的使用与其许可证的要求一致。这有助于确保遵守许可证，特别是对于商业许可证的软件包。

请注意，`LICENSE_FLAGS` 变量的值可以包括其他许可证标志，以指定更多的许可证策略。例如，您可以将其设置为 "commercial gpl3"，以表示软件包使用商业许可证和 GNU General Public License 3.0 许可证。

在实际使用时，您需要确保软件包的许可证与您的项目需求和政策一致，以遵守相关法律和许可证规定。

# yocto怎样进行CVE漏洞检查？

在 Yocto Project 中，您可以使用 OpenEmbedded Security (OpenEmbedded Security) 组件进行 CVE（公开已知漏洞）漏洞检查。

OpenEmbedded Security 是 Yocto Project 中的一组工具和机制，

用于帮助开发者识别和管理软件包中的漏洞，并采取适当的措施来保护系统的安全性。

以下是进行 CVE 漏洞检查的一般步骤：

1. **确保 CVE 数据源可用：** 在 Yocto 构建系统中，您需要确保 CVE 数据源可用。通常，Yocto Project 使用 National Vulnerability Database（NVD）作为 CVE 数据源。确保 Yocto 配方中的 `CVE_CHECK_URI` 变量设置为正确的 NVD 数据源 URL。

   ```bitbake
   CVE_CHECK_URI = "https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-recent.json.gz"
   ```

2. **启用 CVE 检查：** 在 Yocto 配方中，确保 `CVE_CHECK` 变量设置为 "1"，以启用 CVE 漏洞检查。

   ```bitbake
   CVE_CHECK = "1"
   ```

3. **运行 BitBake：** 运行 BitBake 命令以构建软件包。在构建过程中，CVE 检查工具将分析软件包并与 CVE 数据源进行比较，以检查是否存在已知的漏洞。

   ```bash
   bitbake your-image
   ```

4. **查看 CVE 报告：** 检查构建日志以查看 CVE 报告。漏洞检查工具将生成 CVE 报告，其中列出了已知的漏洞及其影响的软件包。您可以在构建日志中搜索 "CVE" 来查看相关信息。

5. **采取措施：** 如果在 CVE 报告中发现了漏洞，需要采取适当的措施来解决问题。这可能包括更新软件包、应用补丁、修改配置或采取其他安全措施，以确保系统的安全性。

请注意，进行 CVE 漏洞检查是确保系统安全性的重要步骤，特别是在部署到生产环境中的系统。及时识别和处理已知漏洞是维护系统安全的关键。在构建系统的配置中，您可以调整 CVE 检查的详细程度和策略，以满足特定需求和政策。

## 给出cve日志的示例

以下是一个示例 CVE（公开已知漏洞）报告的简化版本，以便更好地理解其结构和内容。实际的 CVE 报告可能会更详细。

```plaintext
CVE ID: CVE-2022-12345
描述: 该漏洞允许攻击者执行远程代码，可能导致系统受到攻击。
影响的软件包: foobar 1.2.3
修复版本: 1.2.4
发布日期: 2022-01-15

CVE ID: CVE-2022-54321
描述: 该漏洞允许攻击者绕过身份验证，访问受限资源。
影响的软件包: bazqux 4.5.6
修复版本: 4.5.7
发布日期: 2022-03-20
```

上述示例包括了两个 CVE 报告，每个报告都包括以下信息：

1. **CVE ID:** 每个漏洞都有一个唯一的 CVE 标识符，通常以 "CVE-" 开头，后跟一系列数字。该标识符用于唯一标识漏洞。

2. **描述:** 描述了漏洞的性质，通常包括了漏洞可能被利用的方式以及可能导致的危害。

3. **影响的软件包:** 列出了受漏洞影响的软件包和它们的版本号。这有助于用户确定哪些软件包受到威胁。

4. **修复版本:** 指定了已修复漏洞的软件包版本。用户通常需要升级到此版本以解决漏洞。

5. **发布日期:** 报告中的 CVE 漏洞的发布日期，用于指示漏洞何时被公开。

实际的 CVE 报告可能会更详细，包括漏洞的 CVSS（Common Vulnerability Scoring System）评分、漏洞的详细说明、漏洞利用的条件等。CVE 报告通常由安全研究人员或组织发布，以帮助用户了解并解决系统中的潜在漏洞。在 Yocto Project 中，CVE 报告的信息用于执行漏洞检查并确保系统的安全性。



# SRCREV ?= "${AUTOREV}"

在 Yocto 项目中，`SRCREV` 变量用于指定要从 Git 代码仓库中检出的特定版本或提交的引用。

==通常，`SRCREV` 的默认值设置为 `${AUTOREV}`，这表示自动使用最新的代码提交（HEAD）进行构建。==

- `${AUTOREV}`：它表示使用 Git 代码仓库的最新提交来进行构建。这可以确保您总是使用最新的代码进行构建，适用于开发和测试目的。每次构建都会检查 Git 仓库的最新提交，因此构建可能会有不同的代码版本。

如果您想使用特定的 Git 引用、分支、标签或提交来进行构建，可以将 `SRCREV` 设置为相应的值。例如：

```bitbake
SRCREV = "master"  # 使用 master 分支的代码进行构建
```

或者，您可以将 `SRCREV` 设置为特定的 Git 提交的 SHA-1 值：

```bitbake
SRCREV = "abcdef1234567890"  # 使用特定的提交进行构建
```

这样，您可以控制构建过程使用的代码版本。请注意，如果要确保构建在不同时间具有相同的代码版本，可以使用特定的引用或提交，而不是 `${AUTOREV}`。

# inherit useradd

在 Yocto 项目中，`inherit useradd` 是一种 `recipe` 文件中的 `inherit` 指令，用于指定该软件包==在构建和部署过程中需要创建用户和组。==

这对于确保软件包在目标设备上以正确的权限和身份运行非常重要。

当您在 `recipe` 文件中包含 `inherit useradd` 时，Yocto 构建系统将自动处理用户和组的创建，以确保软件包在目标设备上运行时，用户和组的权限和身份得到正确配置。这有助于确保软件包的功能和安全性。

例如，==如果您有一个需要以特定用户身份运行的服务或应用程序==，您可以在 `recipe` 文件中包含 `inherit useradd`，以确保在构建和部署过程中创建所需的用户和组。这可以确保软件包在目标设备上以正确的权限和身份运行，从而提高了系统的安全性和稳定性。

# yocto里python函数定义前面加上fakeroot 作用是什么

在 Yocto 项目中，将 `fakeroot` 添加到 Python 函数定义前面的作用是在==该函数执行期间启用虚拟根权限（virtual root）。==

`fakeroot` 是一个工具，用于模拟超级用户权限，

以便在构建过程中记录对根文件系统的所有文件操作。

==这通常在构建过程中非常有用，因为它允许 Yocto 跟踪所有文件操作，并生成 `.fakeroot` 文件，其中包含记录的权限、所有者和组信息。==

通过使用 `fakeroot`，Yocto 能够跟踪和记录构建过程中的文件操作，以确保构建的软件包在最终映像中包含正确的文件权限、所有者和组信息。

这有助于确保构建的映像是正确的，并且不会包含意外的权限或所有者信息，从而提高系统的稳定性和安全性。

通常，Python 函数定义前面加上 `fakeroot` 的情况包括 `do_install` 函数，因为这个函数通常用于将文件复制到最终的映像目录中，而 `fakeroot` 可以确保正确地记录这些文件操作。

示例：

```python
fakeroot python do_install() {
    # Your installation code here
}
```

这样的函数定义将在执行期间启用虚拟根权限，以确保正确记录安装过程中的文件操作，从而生成正确的 `.fakeroot` 文件。

## 那对于普通的shell函数，怎么做类似的操作呢

对于普通的 shell 函数，要在执行期间启用虚拟根权限（fakeroot），可以使用 `fakeroot` 命令将整个函数包装起来。这将使整个 shell 函数在虚拟根环境中执行，以便跟踪和记录所有文件操作。

以下是示例，演示如何在普通 shell 函数中使用 `fakeroot`：

```bash
my_shell_function() {
    # Your shell function code here

    # Wrap the function with 'fakeroot'
    fakeroot <<EOF
        # Your shell function code here
    EOF

    # Rest of your shell function code
}
```

在上述示例中，`my_shell_function` 是您的普通 shell 函数。在函数中，使用 `fakeroot` 命令将函数包装在 `<<EOF` 和 `EOF` 之间，以便在此环境中启用虚拟根权限。

这将确保整个函数在虚拟根环境中执行，并跟踪和记录所有文件操作。请注意，在 `fakeroot` 块内部的所有操作将在虚拟根环境中执行，而在块之外的操作将在正常环境中执行。

通过这种方式，您可以在普通 shell 函数中模拟超级用户权限，以确保跟踪文件操作并生成正确的 `.fakeroot` 文件，从而增强 Yocto 项目的构建过程的可追溯性和控制性。

# addhandler 

`addhandler` 是 Yocto Project 中用于添加事件处理程序的一种方法。

事件处理程序是在 BitBake 构建系统中执行特定任务时触发的自定义脚本或函数，用于自定义任务的行为。

`addhandler` 通常用于 BitBake 类 (`bbclass`) 文件或 `.bb` 配方文件中，以添加自定义事件处理程序。

事件处理程序可以捕获构建过程中的特定事件，例如任务的启动、完成、失败等，并在事件发生时执行特定的操作。

例如，以下是一个使用 `addhandler` 的示例：

```python
addhandler my_custom_event_handler event_name

my_custom_event_handler() {
    # Your custom event handling code here
}
```

==在上述示例中，`addhandler` 用于将 `my_custom_event_handler` 函数绑定到名为 `event_name` 的事件。==

当 `event_name` 事件发生时，`my_custom_event_handler` 函数将被触发执行。

通过使用 `addhandler`，您可以在 Yocto 构建过程中的特定事件发生时执行自定义操作，以满足特定的需求或自定义构建过程。

这使得 Yocto 构建系统非常灵活，可以根据项目的需求进行自定义扩展和修改。

# bb.event有哪些事件，分别在什么时候发生

BitBake 的 `bb.event` 模块包含了许多事件，它们用于在不同的构建阶段触发自定义操作。

以下是一些常见的 `bb.event` 事件，以及它们在构建过程中的发生时机：

1. `bb.event.RecipeParsed`: 当 BitBake 解析配方文件时触发，通常用于检查和处理配方的元数据。

2. `bb.event.RecipePreFinalise`: 在 BitBake 预处理配方文件和任务之前触发，可以用于在构建任务之前执行一些操作。

3. `bb.event.RecipeTaskPreprocess`: 在任务预处理之前触发，可以用于在任务执行之前进行额外处理。

4. `bb.event.RecipeTaskPostprocess`: 在任务预处理之后触发，用于在任务执行后进行额外处理。

5. `bb.event.RecipeParsedPreprocess`: 在解析配方之前触发，可以用于在配方解析之前执行一些自定义操作。

6. `bb.event.RecipePrepend`: 在 BitBake 解析配方之后，执行`prepend` 指令时触发。

7. `bb.event.RecipeAppend`: 在 BitBake 解析配方之后，执行 `append` 指令时触发。

8. `bb.event.RecipeSched`: 在任务调度期间触发，可以用于自定义任务的调度行为。

9. `bb.event.RecipeTaskFailed`: 当任务执行失败时触发，可以用于处理构建中出现的错误。

10. `bb.event.RecipeTaskCompleted`: 当任务成功完成时触发，可以用于执行任务完成后的自定义操作。

这些事件提供了丰富的扩展和自定义选项，以满足特定项目需求。您可以在适当的事件中添加自定义处理程序以执行额外的操作，以定制和增强 Yocto 构建过程。根据项目的需求，您还可以自定义事件来处理特定的构建任务。

# yocto python代码里的d表示什么

==在 Yocto 构建系统中，`d` 是一个特殊的变量，代表当前任务或函数的数据上下文。==

这个上下文包含了与当前任务或函数执行==相关的所有元数据和变量信息。==

`d` 是 BitBake 构建系统中的一个常见的变量名，通常在 Python 函数中用于访问元数据和配置信息。

`d` 是 BitBake 中的一个全局变量，它在各种任务和函数中都是可用的，用于获取当前任务的元数据和配置信息，以及设置变量的值。具体来说，`d` 可以用于：

1. 访问配方文件中定义的变量，如 `PN`（包名）、`PV`（包版本）、`S`（源代码目录）等。
2. 获取构建目标的体系结构和 SDK 版本信息。
3. 设置自定义变量的值，以在构建任务中使用。

通过使用 `d`，您可以在 Yocto 构建系统中的 Python 函数中轻松地访问和操作构建任务的元数据和配置信息，以满足特定的需求。它是 BitBake 构建系统中非常重要的工具之一。

## 那在shell里怎么访问d

在 shell 脚本中，您可以访问 `d` 变量的值，但它通常需要通过特定的方式传递给 shell 脚本。`d` 变量代表了任务的元数据和配置信息，通常由 BitBake 构建系统中的 Python 函数访问和操作。如果您需要在 shell 脚本中使用 `d` 变量的信息，可以通过 BitBake 提供的环境变量将其传递给 shell。

==一种常见的方法是使用 `export` 命令将 `d` 变量的信息导出为环境变量，以便在 shell 中访问。==例如，您可以在 Python 函数中执行以下操作：

```python
import os

def my_python_function(d):
    # 获取需要传递给 shell 的信息
    some_info = d.getVar("SOME_VARIABLE")

    # 将信息导出为环境变量
    os.environ["MY_SHELL_VARIABLE"] = some_info
```

然后，在 shell 脚本中，您可以访问 `MY_SHELL_VARIABLE` 环境变量来获取 `d` 变量的信息。例如：

```bash
#!/bin/sh

# 在 shell 中访问通过环境变量传递的信息
echo "The value of MY_SHELL_VARIABLE is: $MY_SHELL_VARIABLE"
```

通过这种方式，您可以将 `d` 变量的信息传递到 shell 脚本中，并在 shell 中使用。请注意，`d` 变量中的信息需要在 Python 函数中进行处理和导出，然后才能在 shell 脚本中使用。

## 怎么在bitbake命令行访问d的值

在 BitBake 命令行中访问 `d` 变量的值并不直接支持，因为 `d` 是在 BitBake 执行构建任务时由 Python 函数设置和处理的，而 BitBake 命令行通常用于触发任务的构建，而不是直接访问 `d` 变量的值。

通常情况下，要获取 `d` 变量的值，您需要通过编写 Python 函数，然后使用 BitBake 执行该函数。以下是一个示例：

1. 创建一个自定义 Python 函数，该函数可以获取 `d` 变量的值并执行您的逻辑。例如，创建一个名为 `my_custom_function` 的函数：

```python
python my_custom_function() {
    some_value = d.getVar("SOME_VARIABLE")
    # 在这里执行您的自定义逻辑，使用 some_value
}
```

2. 使用 BitBake 执行该自定义函数。可以使用以下命令：

```bash
bitbake -c my_custom_function <recipe>
```

这将触发执行 `my_custom_function` 函数，您可以在其中访问 `d` 变量的值并执行自定义逻辑。

请注意，`<recipe>` 是要构建的配方名称，`my_custom_function` 是您创建的自定义函数名称。在函数中，您可以使用 `d.getVar("SOME_VARIABLE")` 来获取 `SOME_VARIABLE` 变量的值，然后执行您的逻辑。

总之，要在 BitBake 命令行中访问 `d` 变量的值，通常需要创建一个自定义的 Python 函数，然后使用 BitBake 命令触发该函数的执行。这种方法允许您在构建任务中获取和操作 `d` 变量的值。

# oe.data模块介绍

代码在：

layers\openembedded-core\meta\lib\oe\data.py

里面就2个函数：

```
def typed_value(key, d):
def export2json(d, json_file, expand=True, searchString="",replaceString=""):
```



`oe.data` 模块是 Yocto 构建系统中的一个关键模块，

==提供了访问和处理构建系统的元数据、变量和配置信息的功能。==

这个模块允许您在 BitBake 配方中访问构建系统的各种配置和数据，以便更好地定制和控制构建过程。以下是一些 `oe.data` 模块的重要功能和用途：

1. 访问配置变量：`oe.data` 模块允许您获取和设置 Yocto 构建系统中的配置变量。您可以使用该模块来查询各种配置选项，以便根据需要自定义构建。

2. 获取元数据信息：该模块提供了函数来获取配方中的元数据信息，如作者、许可证、依赖关系等。这有助于了解和管理构建中使用的配方的特性。

3. 处理层和类：`oe.data` 模块允许您查询构建系统中使用的层和类。这对于检查构建环境和选择特定功能或类别的代码非常有用。

4. 配方相关操作：该模块提供了一些函数，用于处理 BitBake 配方（.bb 文件）的信息，如解析配方文件、查找配方的路径等。

5. 获取任务信息：您可以使用 `oe.data` 模块来查询与任务相关的信息，如任务的依赖关系、任务的顺序和任务的状态。

6. 访问 BitBake 配方数据：该模块允许您获取 BitBake 配方的数据，包括配置变量的值、包含的文件和任务信息。

总之，`oe.data` 模块是 Yocto 构建系统的一个核心组成部分，用于访问和处理构建过程中的元数据和配置信息。它提供了丰富的功能，以帮助开发人员更好地管理和自定义构建过程，使其适应不同项目和需求的要求。这对于构建复杂的嵌入式 Linux 系统非常有帮助。

## 使用oe.data示例

下面是一些使用 `oe.data` 模块的示例代码片段，用于访问和处理 Yocto 构建系统的元数据和配置信息：

1. 获取构建目标的架构（MACHINE）：

```python
import oe.data

# 获取构建目标的架构
machine = oe.data.typed_value("MACHINE", d)
print("构建目标的架构是:", machine)
```

2. 查询当前构建使用的层列表：

```python
import oe.data

# 获取当前构建使用的层列表
layers = oe.data.typed_value("BBLAYERS", d)
print("当前构建使用的层列表:", layers)
```

3. 获取配方的作者信息：

```python
import oe.data

# 获取配方的作者信息
author = oe.data.getVar("AUTHOR", d)
print("作者信息:", author)
```

4. 查询任务的依赖关系：

```python
import oe.data

# 获取特定任务的依赖关系
task_dependencies = oe.data.getVarFlag("do_configure", "depends", d)
print("do_configure 任务的依赖关系:", task_dependencies)
```

这些示例演示了如何使用 `oe.data` 模块查询和获取构建系统中的元数据和配置信息。您可以根据自己的需求进一步扩展这些示例以满足特定任务的要求。这对于自定义 BitBake 配方以及处理构建任务的配置非常有帮助。

# FILESPATH 

在base.bbclass里：

```
FILESPATH = "${@base_set_filespath(["${FILE_DIRNAME}/${BP}", "${FILE_DIRNAME}/${BPN}", "${FILE_DIRNAME}/files"], d)}"
```



这行代码用于设置 `FILESPATH` 变量，==该变量指定了 BitBake 配方文件中的附件文件搜索路径。==让我解释一下这行代码的含义：

1. `${@base_set_filespath([...], d)}`：这部分代码调用 BitBake 内置函数 `base_set_filespath([...], d)`，其中 `...` 是一个包含文件路径的列表。这个函数的作用是设置 `FILESPATH` 变量，以包括列出的文件路径。

2. `FILE_DIRNAME`、`BP`、`BPN`：这些都是 BitBake 配方中可用的变量。`FILE_DIRNAME` 是当前配方文件的目录路径，`BP` 是包名，`BPN` 是包名（不包括版本号）。这些变量用于构建 `FILESPATH` 中的路径。

3. `${FILE_DIRNAME}/${BP}`、`${FILE_DIRNAME}/${BPN}`、`${FILE_DIRNAME}/files`：这些是文件路径的一部分，用于构建 `FILESPATH`。`${FILE_DIRNAME}/${BP}` 表示配方文件的目录路径加上包名，`${FILE_DIRNAME}/${BPN}` 表示配方文件的目录路径加上包名（不包括版本号），`${FILE_DIRNAME}/files` 表示配方文件的目录路径下的 "files" 子目录。

总的来说，这行代码的作用是将配方文件所在目录、包名和特定子目录的路径添加到 `FILESPATH` 变量中，以便 BitBake 可以在这些路径下搜索和访问与配方相关的文件。这对于配方中使用附件文件非常有用，例如补丁文件、配置文件等。这样，BitBake 将能够在这些路径中查找并使用这些文件。

# 除了addtask、addhandler，还有其他的add功能吗

BitBake 支持一系列的 `add` 功能，其中包括 `addtask` 和 `addhandler`，以及其他一些类似的功能，用于配置和扩展 BitBake 配方的行为。

以下是一些常见的 `add` 功能：

1. **addtask**: `addtask` 用于向 BitBake 配方中添加一个任务。任务是构建过程中执行的操作，例如编译、安装、打包等。您可以使用 `addtask` 来定义自定义任务或覆盖现有任务的行为。

2. **addhandler**: `addhandler` 用于向 BitBake 配方中添加事件处理程序。事件处理程序是在构建过程中特定事件发生时执行的函数。您可以使用 `addhandler` 来监听和响应事件，以执行自定义操作。

3. **addfeature**: `addfeature` 用于向 BitBake 配方中添加功能标记。功能标记用于控制和配置构建过程的各个方面。您可以使用 `addfeature` 来启用或禁用特定功能。

4. **addgroup**: `addgroup` 用于将一个或多个包组添加到 BitBake 配方中。包组是一组相关软件包，它们一起构建和安装。您可以使用 `addgroup` 来定义自定义包组。

5. **addtaskfunc**: `addtaskfunc` 用于定义一个任务函数，该函数将在任务执行时调用。这允许您编写自定义任务函数以执行特定的构建操作。

6. **addvar**: `addvar` 用于向 BitBake 配方中添加自定义变量。您可以使用 `addvar` 来定义和设置自定义变量，以在构建过程中使用。

7. **adddepends**: `adddepends` 用于添加任务依赖关系。这允许您定义任务之间的依赖关系，以确保它们按正确的顺序执行。

这些 `add` 功能使 BitBake 配方变得非常灵活，允许开发人员自定义构建过程并控制任务的执行顺序和行为。这些功能通常是通过 BitBake 配方中的 `do_<task>` 函数来定义和配置的。

# task有哪些属性可以配置

在 BitBake 配方中，可以配置任务（task）的多个属性，以控制其行为和执行方式。以下是一些常见的任务属性：

1. **dirs**：指定任务的工作目录，即任务在执行时的工作路径。

2. **depends**：定义任务的依赖关系，指定任务在执行之前需要满足的条件。

3. **file-checksums**：配置文件的校验和列表，用于验证下载的文件是否完整和正确。

4. **vardeps**：指定任务的变量依赖关系，表示任务在特定变量值发生变化时需要重新执行。

5. **network**：指示任务是否需要网络连接，通常用于表示任务是否需要从远程源下载文件。

6. **nostamp**：用于禁用任务的状态文件（stamp file），通常用于防止任务被 BitBake 标记为已完成。

7. **runearly**：表示任务应该尽早执行，通常用于执行需要在构建之前运行的任务。

8. **python**：指定任务使用 Python 脚本执行，用于自定义任务行为。

9. **fakeroot**：表示任务应该在伪装（fakeroot）环境中执行，通常用于模拟特权操作。

10. **parallel**：配置任务是否可以并行执行，以加速构建过程。

这些属性用于控制任务的执行方式和行为，以确保构建过程按照所需的顺序和规则进行。根据 BitBake 的版本和配置，可能还存在其他任务属性，具体取决于 BitBake 的功能和配置。

# SSTATETASKS 是什么

`SSTATETASKS` 是 BitBake 中用于定义构建状态任务（sstate tasks）的变量。

构建状态任务是为了==支持增量构建和缓存构建结果而执行的任务。==

它们通常执行构建过程的一部分，但不会对最终构建结果产生影响，因此可以被缓存并在后续构建中重用。

在 Yocto Project 和 OpenEmbedded 系统中，`SSTATETASKS` 变量用于列出哪些任务会被包括在构建状态中。这些任务的输出结果将被缓存，以便在下次构建相同软件包时可以加速构建过程。通常，`SSTATETASKS` 中包括了一系列任务名称，这些任务通常是编译、配置、安装和其他构建任务。

`SSTATETASKS` 变量的典型用法如下：

```python
SSTATETASKS += "do_configure do_compile do_install"
```

这表示在构建状态中包括了 `do_configure`、`do_compile` 和 `do_install` 这三个任务。在构建状态中执行这些任务会生成缓存文件，以加速未来的构建。

构建状态非常有用，因为它们可以节省构建时间，特别是在多次构建相同软件包时。它们还可以提高系统构建的效率，因为只有在需要时才执行任务，而不是每次都重新构建。

# BUILDCFG_FUNCS

`BUILDCFG_FUNCS` 是一个 BitBake 变量，用于定义包含在配置文件（`local.conf` 或 `bitbake.conf`）中的额外 BitBake 配方配置的函数。

这些函数可以用于根据配置文件中的值动态修改或扩展 BitBake 配方的配置。

通常，`BUILDCFG_FUNCS` 变量的值==是一个包含函数名称的列表。==

这些函数可以在配置文件中定义，以影响特定的 BitBake 配方或全局配置。当配置文件被加载时，这些函数将在 BitBake 配方的配置之前或之后执行，以实现自定义配置。

示例：

```python
BUILDCFG_FUNCS = "my_custom_config"
```

上面的示例将执行名为 `my_custom_config` 的函数，该函数可以在配置文件中定义。这个函数可以用于根据配置文件的值设置不同的配置选项、添加层或进行其他自定义操作。

`BUILDCFG_FUNCS` 变量允许您通过编写自定义函数来扩展和修改 BitBake 配方的配置，从而实现更灵活的构建系统配置。这对于需要根据不同的构建需求动态调整配置的情况非常有用。

# do_install[cleandirs] = "${D}"

在 BitBake 配方中，`do_install` 是一个任务，用于将软件包的构建结果安装到临时目录（`${D}`）。

==`${D}` 代表临时目录，通常是 `WORKDIR` 下的一个子目录，用于构建和安装软件包的临时文件和目录。==

`do_install[cleandirs]` 是一个 BitBake 变量，用于指定在执行 `do_install` 任务之前清理哪些目录。具体来说，`${D}` 是 `do_install` 任务默认会清理的目录。这是因为在 `do_install` 任务执行之前，通常会希望确保`${D}` 目录是干净的，以避免旧文件残留导致构建结果不正确。

如果您想在 `do_install` 任务之前执行其他清理操作或者清理其他目录，

==可以通过设置`do_install[cleandirs]` 来指定要清理的目录。==

例如，您可以将其他目录添加到 `do_install[cleandirs]` 中，以确保它们在 `do_install` 任务执行之前被清理。这可以用于定制构建过程，确保构建环境是干净的。

示例：

```python
do_install[cleandirs] = "${D} /path/to/other/directory"
```

上面的示例将清理 `${D}` 目录和 `/path/to/other/directory` 目录，以确保它们在 `do_install` 任务执行之前是空的。这可以帮助确保构建结果的准确性。

# do_populate_sysroot

`do_populate_sysroot` 是 BitBake 构建系统中的一个任务，

其主要作用是将构建好的软件包（通常是二进制文件、库和头文件）==部署到一个虚拟的系统根目录，==

这个根目录被称为 "sysroot"。

这个 sysroot 目录通常包括了软件包的运行时依赖项，以及开发人员需要在交叉编译环境中进行开发和构建的文件。

`do_populate_sysroot` 任务的主要作用包括：

1. **准备运行时环境**: 将构建好的二进制文件、库文件和数据文件移动到 sysroot 目录，以便软件包可以在目标设备上正确运行。这包括库文件的符号链接、共享库缓存等。

2. **提供开发支持**: 将头文件、开发工具和构建工具移动到 sysroot 目录，以便开发人员可以使用这些文件来交叉编译应用程序，为目标设备构建软件。

3. **处理运行时依赖关系**: 为了确保软件包能够正确运行，`do_populate_sysroot` 任务还会处理软件包的运行时依赖关系。这可能包括将依赖的库文件复制到 sysroot 目录，以便软件包能够在目标设备上正确链接。

总之，`do_populate_sysroot` 任务的目标是创建一个包含软件包的运行时和开发所需文件的虚拟根文件系统，以便构建和开发过程能够在交叉编译环境中进行。这对于嵌入式系统和嵌入式 Linux 分发版的构建非常重要。

## 这个sysroot在哪个目录下？是所有的包共用一个还是多个？

==`sysroot` 实际上是一个虚拟的目录，==

位于每个构建目标（target）的临时工作目录下。

每个目标（例如 ARM 架构、x86 架构等）都有一个单独的 `sysroot` 目录。

这个目录的位置由 BitBake 配方和 BitBake 变量来管理。

默认情况下，每个目标（target）都有自己的 `sysroot` 目录，这意味着不同目标之间的 `sysroot` 是相互独立的，不会共用相同的 `sysroot` 目录。

`sysroot` 目录的位置通常位于构建工作目录（`WORKDIR`）的子目录中，

其路径由 BitBake 变量 `STAGING_DIR_TARGET` 控制。

通常，`sysroot` 目录的路径类似于 `${WORKDIR}/temp/work/<target>/sysroot`，其中 `<target>` 是目标架构的名称，例如 `arm`, `x86`, `aarch64` 等。

这种设计使得可以为不同的目标架构分别构建并管理 `sysroot` 目录，以确保构建和开发环境的隔离性。

这对于交叉编译和嵌入式 Linux 开发非常有用，因为不同的目标可能需要不同的运行时依赖关系和开发工具。

# recrdeptask

`recrdeptask` 是 BitBake 构建系统中的一个任务属性，

用于指定一个==任务的递归依赖任务（Recursive Dependency Task）。==



在 BitBake 构建系统中，每个任务可以有一个或多个依赖任务，这些依赖任务会在执行主任务之前执行。

递归依赖任务是指在执行主任务之前，首先执行与主任务的依赖任务相关的任务。

==这些递归依赖任务通常用于确保在执行主任务之前，所有相关的任务都已经完成。==

例如，考虑一个主任务 `do_build`，它可能依赖于 `do_configure` 和 `do_compile` 任务。

在这种情况下，如果将 `do_compile` 标记为 `recrdeptask`，则 BitBake 将确保在执行 `do_build` 之前，首先执行 `do_configure`，然后执行 `do_compile`。

递归依赖任务属性的使用可以帮助==确保任务的执行顺序和依赖关系正确，以避免构建过程中出现问题。==

这对于复杂的构建流程和依赖关系管理非常有用。



# EXCLUDE_FROM_WORLD

`EXCLUDE_FROM_WORLD` 是一个 Yocto 构建系统中的 BitBake 变量，用于指示某个特定的软件包或组件是否应该被排除（exclude）出构建过程之外。这个变量通常用于控制构建系统不要为某些软件包执行编译和构建操作，因为这些软件包可能不是构建过程的一部分，或者是特殊情况下不需要构建的。

设置 `EXCLUDE_FROM_WORLD` 的值为 "1" 表示将该软件包排除出构建过程。这通常用于在特定配置下排除不需要构建的软件包，以提高构建效率或解决特定问题。

例如，某些软件包在某些目标平台上可能无法正常构建，或者它们不是构建系统的一部分，但由于某些原因它们仍然存在于元数据中。在这种情况下，可以使用 `EXCLUDE_FROM_WORLD` 变量将其排除出构建过程，以确保构建系统不会尝试构建它们。

这个变量通常在软件包的 `.bb` 文件中设置，以控制软件包是否排除出构建过程。例如：

```bitbake
EXCLUDE_FROM_WORLD = "1"
```

需要注意的是，`EXCLUDE_FROM_WORLD` 的值可以是 1 或 0，其中 1 表示排除，0 表示不排除。

# CLASSOVERRIDE 

`CLASSOVERRIDE` 是 Yocto 构建系统中的一个变量，用于指定覆盖（override）特定类（class）的行为。

在 Yocto 中，类是一种用于定义软件包或组件如何被构建和配置的方式。

不同的类可以为不同类型的软件包或构建目标提供不同的行为。

通过使用 `CLASSOVERRIDE` 变量，您可以为特定的软件包或组件指定一个不同的类，从而覆盖其默认行为。

在上述示例中，`CLASSOVERRIDE` 被设置为 "class-cross"，这意味着软件包或组件将使用 "class-cross" 类来定义其行为。这通常用于指定特定软件包的构建方式，以满足交叉编译的需求，例如为不同的目标体系结构生成二进制代码。"class-cross" 类通常包含了与交叉编译相关的设置和规则。

`CLASSOVERRIDE` 变量的值应该是一个已经存在的 BitBake 类的名称，以确保正确的类被应用。这使得您可以针对不同的软件包或组件采用不同的构建类，以满足其特定需求。

这个变量通常在软件包的 `.bb` 文件中设置，以控制软件包使用哪个类。如果不设置 `CLASSOVERRIDE`，则软件包将使用默认类来构建和配置。

# yocto的override机制，有哪些东西可以被override

Yocto 构建系统的 override 机制非常灵活，==允许您覆盖（override）几乎所有层面的配置和行为==。以下是一些常见的可以被 override 的内容：

1. **软件包的配置变量**: 您可以覆盖软件包的配置变量，以自定义构建选项、编译参数、安装路径等。这通常在 `.bb` 文件中使用 `OVERRIDES` 变量来实现，例如 `PN-override`。

2. **BitBake 类（Class）**: 您可以为软件包或组件指定不同的 BitBake 类，以覆盖其默认行为。这通常使用 `CLASSOVERRIDE` 变量来实现。

3. **任务的覆盖**: 您可以定义自定义任务，并覆盖默认的任务。这通常在 `.bbappend` 文件中实现，例如 `do_configure_prepend`。

4. **层的覆盖**: 您可以在层的 `.conf` 文件中覆盖全局配置变量，以影响整个构建。这通常使用 `LAYERDEPENDS` 变量和 `BBLAYERS` 变量来实现。

5. **BBFILES 变量**: 您可以通过修改 `BBFILES` 变量来指定构建的 BitBake 文件列表，从而添加或排除特定的 `.bb` 文件。

6. **BitBake 配置变量**: 您可以覆盖 BitBake 的全局配置变量，例如 `MACHINE`、`DISTRO`、`SDKMACHINE` 等，以影响整个构建。

7. **图像特征（Image Features）**: 您可以通过 `IMAGE_FEATURES` 变量覆盖图像生成过程中的特征选项，以创建不同的图像。

8. **软件包提供（Provides）、替代（Replaces）和冲突（Conflicts）**: 您可以通过 `RPROVIDES`, `RREPLACES`, 和 `RCONFLICTS` 变量来覆盖软件包的提供、替代和冲突关系。

9. **跨层的覆盖**: 不仅可以在软件包的同一层内进行覆盖，还可以跨多个层对软件包进行覆盖，以适应不同的项目需求。

总之，Yocto 提供了广泛的 override 机制，使您能够根据项目需求定制构建过程中的各种配置和行为。这种灵活性使得 Yocto 极具适应性，可以用于构建各种不同类型的嵌入式 Linux 系统。

# yocto libc-glibc 特性

在 Yocto 中，`libc-glibc` 是指使用 GNU C 库（glibc）作为标准 C 库的特性。

glibc 是 Linux 系统上最常见的标准 C 库，提供了许多用于编程的标准 C 函数和库，

因此它在 Yocto 构建系统中具有重要的地位。

以下是 `libc-glibc` 特性的一些关键特点和信息：

1. **默认标准 C 库**：在 Yocto 构建中，默认情况下使用 glibc 作为标准 C 库。这是因为 glibc 是 Linux 系统上最常用的标准 C 库，支持广泛的硬件架构和软件包，因此适用于大多数嵌入式 Linux 系统。

2. **兼容性**：glibc 与 POSIX 标准高度兼容，使得它适用于许多不同类型的应用程序。它提供了对多线程、国际化、字符编码转换等特性的支持。

3. **广泛的软件包支持**：glibc 可以与许多软件包和库一起使用，因此它允许构建各种不同类型的应用程序，从嵌入式系统到服务器应用程序。

4. **丰富的特性**：glibc 提供了丰富的功能，包括标准 C 库函数、网络支持、文件系统支持、多语言支持和其他功能。这些功能使得它适用于各种不同的用途。

5. **多架构支持**：glibc 可以针对多种硬件架构进行编译，包括 x86、ARM、MIPS、PowerPC 等。这使得它适用于多种不同类型的设备。

在 Yocto 中，您可以使用 `DISTRO_FEATURES` 变量来指定要使用的 libc 特性。如果希望使用 glibc，只需确保 `libc-glibc` 特性被包含在 `DISTRO_FEATURES` 中。如果您需要使用其他的标准 C 库，Yocto 也支持其他选项，

==例如 `libc-musl`（musl libc）和 `libc-uclibc`（uClibc-ng）。==

选择适合项目需求的 libc 特性非常重要，因为它将影响构建的软件包和系统功能。

# BB_RENAMED_VARIABLES[PNBLACKLIST] = "SKIP_RECIPE"

在 Yocto/OpenEmbedded 构建系统中，`BB_RENAMED_VARIABLES` 是一个变量，用于指定将某个变量重命名为另一个变量的映射关系。在这里，`BB_RENAMED_VARIABLES[PNBLACKLIST] = "SKIP_RECIPE"` 表示将变量 `PNBLACKLIST` 重命名为 `SKIP_RECIPE`。

通常情况下，变量 `PNBLACKLIST` 用于指定不要构建的特定软件包的名称。通过将其重命名为 `SKIP_RECIPE`，可以更容易地理解其作用，或者在构建配置中使用 `SKIP_RECIPE` 变量而不必担心 `PNBLACKLIST`。

这种变量重命名的方法可用于改进变量名称的可读性，或者根据项目的需求来进行自定义。在构建系统中，保持变量名称的清晰和一致性是很重要的，以便更容易理解和维护构建配置。

# BB_MULTI_PROVIDER_ALLOWED

`BB_MULTI_PROVIDER_ALLOWED` 是 Yocto 构建系统中的一个变量，

==用于控制是否允许多个提供相同功能的软件包同时存在于构建中。==

这在处理软件包提供者（providers）时非常有用。

在 Yocto 构建系统中，某个功能（例如库或工具）可以由多个不同的软件包提供，这些软件包通常在不同的层中或以不同的方式提供相同的功能。例如，多个软件包可能提供了相同的图形库或网络工具。

`BB_MULTI_PROVIDER_ALLOWED` 变量有以下两个值：

- `libressl`：当设置为此值时，允许多个提供者提供相同功能。这意味着，即使有多个软件包提供相同功能，构建系统也不会抛出错误。
- `openssl`：当设置为此值时，构建系统会检测到存在多个提供者提供相同功能时，并抛出错误，要求选择一个提供者或解决依赖关系。

这个变量通常在 `local.conf` 或 `distro` 配置文件中设置，以控制软件包提供者的行为。如果您希望允许多个提供者提供相同功能，可以将其设置为 `libressl`。如果您希望严格控制提供者，可以将其设置为 `openssl`。这有助于确保构建系统的稳定性和可维护性。

# yocto编译recipe文件时，怎样调试效率比较高，有什么技巧

提高 Yocto 构建效率并调试 recipe 文件的关键技巧包括：

1. 使用 `bitbake -c` 命令：可以使用 `bitbake` 命令的 `-c` 选项来执行特定任务，例如 `compile`、`clean`、`configure` 等。这有助于只重新构建需要的部分，而不是整个软件包。例如，`bitbake -c compile <recipe>` 可以只编译指定的软件包。

2. 并行构建：通过设置 `BB_NUMBER_THREADS` 变量，您可以控制并行构建任务的数量，以加速整个构建过程。通常，将其设置为您系统可用的 CPU 核心数是一个不错的选择。

3. 使用 sstate 缓存：Yocto 使用 sstate 缓存来存储先前构建的结果，以便在后续构建中重复使用。确保启用 sstate 缓存，以减少构建时间。

4. 使用局部源码镜像：设置 `BB_GENERATE_MIRROR_TARBALLS` 为 1，以便将构建过程中下载的源码和文件存储在局部镜像中，以便在以后的构建中重复使用，从而减少下载时间。

5. 使用预构建 SDK：构建 SDK 时，可以将其保存并在以后的构建中重复使用，而不必每次都重新构建。

6. 使用调试工具：Yocto 提供了一些调试工具，如 `devtool`，它可以帮助您修改和调试 recipe 文件。

7. 避免不必要的依赖项：确保 recipe 文件中的依赖项是必要的，避免不必要的依赖项会减少构建时间。

8. 使用专门的构建机器：如果可能的话，使用性能较高的计算机作为构建服务器，以提高构建速度。

9. 仔细分析构建日志：构建日志中包含了详细的信息，可以帮助您找到构建过程中的瓶颈和问题。

10. 避免不必要的 recipe 文件：如果您不需要某个软件包或组件，可以通过排除相关的 recipe 文件来减少构建时间。

11. 针对性地调试：如果您正在调试特定软件包或问题，可以只构建和调试相关的软件包，而不必构建整个系统。

综合使用这些技巧，您可以显著提高 Yocto 构建效率并更高效地调试 recipe 文件。

# yocto编译过程中CFLAGS的传递过程

Yocto 编译过程中的 `CFLAGS` 传递是通过 BitBake 构建系统和 recipe 文件中的变量进行管理的。以下是 `CFLAGS` 传递的主要流程和修改方法：

1. **设置 `CFLAGS` 变量：** 在 recipe 文件中，您可以设置 `CFLAGS` 变量来定义编译时的选项。例如：

   ```bitbake
   CFLAGS += "-O2 -pipe"
   ```

   这将为编译器传递 `-O2` 和 `-pipe` 选项。

2. **BitBake 层级传递：** BitBake 构建系统将会将 recipe 文件中设置的 `CFLAGS` 传递到 BitBake 层级。这包括 BitBake 中定义的全局变量，如 `TUNE_CCARGS` 和 `TUNE_PKGARCH`. ==BitBake 层级的 `CFLAGS` 设置可以在 `conf/local.conf` 中修改==，例如：

   ```bitbake
   TUNE_PKGARCH = "armv7a-vfp-neon"
   ```

   这会影响生成的 `CFLAGS`。

3. **MACHINE 层级传递：** `MACHINE` 层级的配置可以在 `conf/machine/` 目录中找到，它会进一步影响到 `CFLAGS` 的设置。不同的机器可以有不同的 `CFLAGS` 配置。

4. **DISTRO 层级传递：** `DISTRO` 层级的配置位于 `conf/distro/` 目录中，它可能会在某些情况下修改 `CFLAGS`。例如，某些 `DISTRO` 可能会为不同的目标平台定义不同的 `CFLAGS`。

5. **内部依赖：** 如果您的软件包依赖其他软件包，它可能会继承其他软件包的 `CFLAGS` 设置。这可以通过 `DEPENDS` 变量来管理。

如果您需要修改 `CFLAGS`，可以在 recipe 文件中进行修改，或者通过修改 `local.conf`、`machine` 配置文件或 `distro` 配置文件来影响 BitBake 层级、`MACHINE` 层级和 `DISTRO` 层级的设置。

需要注意的是，修改 `CFLAGS` 变量会影响整个软件包的编译选项，因此请小心确保修改是合适的，并不会引入不必要的问题。此外，如果您只需要修改特定软件包的编译选项，最好在该软件包的 recipe 文件中进行设置，以确保只影响该软件包。

# EXTRA_OECONF:append:class-target 

`EXTRA_OECONF:append:class-target` 是 Yocto 中用于配置软件包编译时的额外 `./configure` 参数的一种方式。这允许您在软件包的编译过程中添加自定义的配置参数。

下面是关于这个配置项的一些说明：

- `EXTRA_OECONF` 是一个 BitBake 变量，用于传递给软件包的 `configure` 脚本额外的参数。

- `:append` 表示将这些额外的参数追加到现有的 `EXTRA_OECONF` 参数之后。

- ==`class-target` 表示这些参数仅适用于 `class` 为 `target` 的软件包。不同的软件包类别（如 `class-native`、`class-nativesdk`、`class-cross` 等）可以具有不同的配置参数。==

这种方法的常见用途是针对目标设备的特定需求，为目标平台添加特定的编译选项。例如，您可能需要为 ARM 架构上的目标设备启用 NEON 指令集，可以使用以下方式配置：

```bitbake
EXTRA_OECONF:append:class-target = " --enable-neon"
```

这会将 `--enable-neon` 添加到目标软件包的 `configure` 脚本参数中，以启用 NEON 指令集支持。

请注意，具体的 `configure` 参数取决于软件包的构建系统和目标软件包的要求。要了解哪些参数适用于特定软件包，可以查看软件包的文档或查看 `configure` 脚本的帮助信息。

# INITSCRIPT_NAME = "dbus-1"

```
INITSCRIPT_NAME = "dbus-1"
INITSCRIPT_PARAMS = "start 02 5 3 2 . stop 20 0 1 6 ."
```



在 Yocto 中，`INITSCRIPT_NAME` 和 `INITSCRIPT_PARAMS` 是用于定义初始化脚本的变量，用于管理启动和停止服务。这些变量通常用于创建位于 `/etc/init.d` 目录下的初始化脚本（init script）。

- `INITSCRIPT_NAME` 定义了初始化脚本的名称。在这个示例中，初始化脚本的名称为 "dbus-1"。这将决定在 `/etc/init.d` 目录下创建的脚本文件的名称。

- `INITSCRIPT_PARAMS` 定义了初始化脚本的启动和停止参数。这些参数决定了服务在系统启动和关闭时的行为。具体来说，这里定义了启动级别（runlevel）以及启动和停止的顺序。==在示例中，启动参数是 "start 02 5 3 2 ."，表示在运行级别 2、3、5 启动服务，并且启动顺序为 02。停止参数是 "stop 20 0 1 6 .”，表示在运行级别 0、1、6 停止服务，并且停止顺序为 20。==

通过这两个变量的设置，Yocto 将生成相应的初始化脚本文件，以便在系统启动和关闭时自动启动和停止指定的服务。这有助于管理系统上运行的服务，以确保它们在适当的时间启动和停止。

# bitbake变量的属性

BitBake 变量具有不同的属性，这些属性指定了它们的特性和行为。以下是一些常见的 BitBake 变量属性：

1. **vardeps（Variable Dependencies）**: 这个属性定义了一个变量的依赖关系。==如果变量的某个依赖发生变化，它也会发生变化。==

2. **type**: 指定了变量的类型，例如 "string"、"boolean"、"choice" 等。这有助于确保变量包含适当类型的数据。

3. **default**: 定义了变量的默认值。如果没有为变量指定值，它将使用默认值。

4. **value**: 指定了变量的值。通常在配置文件中设置变量的值。

5. **expand**: 一个布尔属性，表示是否应该在使用变量值时进行扩展。如果设置为 "1"，则会在值中扩展其他变量。

6. **section**: 用于指定变量所属的配置文件部分。这有助于组织和查找相关的变量。

7. **description**: 提供关于变量用途和用法的说明。

8. **visibility**: 控制变量的可见性。它可以是 "global"（全局可见）或 "unbundled"（未捆绑）等。

9. **read-only**: 一个布尔属性，表示变量是否为只读。如果设置为 "1"，则无法在构建过程中修改该变量的值。

10. **require**: 声明变量需要的其他特定变量。这有助于确保所需的变量在使用前已经定义。

这些属性用于定义和控制 BitBake 变量的行为。在编写 Yocto Project 配置文件时，你可以使用这些属性来管理和配置各种变量，以满足你的构建需求。不同的变量可以具有不同的属性，具体的属性设置可能因变量的用途而异。这些属性的目的是确保变量被正确解释和使用。

# layers\openembedded-core\meta\conf\documentation.conf

这个应该就是包含了yocto所有变量的说明了。

值得看看。

# bb里根据变量值A为条件给多个其他变量来赋值，应该怎么做？

在 BitBake 配方文件中，您可以根据变量值 `A` 的条件来设置多个其他变量的值。您可以使用 Python 函数和 BitBake 的 `d` 对象来实现这一点。以下是一个示例，演示如何根据变量值 `A` 的条件来设置多个其他变量：

```python
A = "some_value"

python () {
    # 获取当前配置的 BitBake 数据层
    import bb.data
    data = bb.data.init()

    if A == "some_value":
        data.setVar("B", "value_for_A_some_value")
        data.setVar("C", "another_value_for_A_some_value")
    elif A == "another_value":
        data.setVar("B", "value_for_A_another_value")
        data.setVar("C", "another_value_for_A_another_value")
    else:
        data.setVar("B", "default_value_for_A")
        data.setVar("C", "default_value_for_A")
}
```

在上述示例中，我们首先设置变量 `A` 的值。然后，我们使用 Python 函数中的条件语句来检查 `A` 的值，根据不同的条件设置变量 `B` 和 `C` 的值。在设置这些变量的值时，我们使用 BitBake 的 `data` 对象，该对象允许我们动态地设置 BitBake 变量的值。

请注意，我们在条件语句中根据 `A` 的不同值设置了不同的变量 `B` 和 `C` 的值，但您可以根据您的具体需求来扩展和定制这个示例。此示例演示了如何使用 Python 函数和 BitBake 的 `data` 对象来实现根据变量值 `A` 的条件设置多个其他变量的值。

# UBI_VOLNAME

`UBI_VOLNAME` 是用于定义 UBI 卷（UBI Volume）的名称的 BitBake 变量。

UBI 卷是嵌入式系统中用于存储文件系统、数据或其他信息的逻辑存储单元。

`UBI_VOLNAME` 变量用于为一个 UBI 卷指定一个可识别的名称。

通常，`UBI_VOLNAME` 变量会与其他 UBI 相关的变量一起使用，以配置 UBI 卷的各个属性。在创建 UBI 卷的 BitBake 配方文件中，您可以使用类似下面的示例来设置 `UBI_VOLNAME` 变量：

```shell
UBI_VOLNAME = "rootfs"
```

这里将 UBI 卷命名为 "rootfs"。具体的配置可能会因您的项目和需求而有所不同，但 `UBI_VOLNAME` 是其中一个重要的配置项，因为它决定了如何在 UBI 文件系统中标识和访问特定的 UBI 卷。

请注意，`UBI_VOLNAME` 变量的值通常需要与设备树或内核的 UBI 配置相匹配，以便正确识别和挂载 UBI 卷。所以在设置 `UBI_VOLNAME` 时，请确保它与设备树和内核配置中的设置相匹配，以避免潜在的问题。

# R = "${IMAGE_ROOTFS}"

在 BitBake 配方中，`R` 是一个通常用于设置安装目标（Root）的变量。`"${IMAGE_ROOTFS}"` 表示将 `R` 变量设置为 `IMAGE_ROOTFS` 变量的值。 

`IMAGE_ROOTFS` 是 Yocto Project 构建系统中表示根文件系统路径的一个变量。它指向构建过程中生成的 Linux 根文件系统的位置。将 `R` 设置为 `IMAGE_ROOTFS` 通常用于告诉 BitBake 配方在构建完成后将根文件系统复制到某个目标位置。==这在创建镜像或在嵌入式设备上部署根文件系统时非常有用。==

例如，通过设置 `R` 为 `IMAGE_ROOTFS`，您可以轻松地在构建过程中访问和操作生成的根文件系统，如创建镜像文件或将其安装到目标设备的存储介质中。



# BB_HASHEXCLUDE_COMMON

`BB_HASHEXCLUDE_COMMON`是BitBake构建工具中的一个配置变量，

==用于定义哪些文件或目录不应影响任务输出的哈希值。==

通常用于构建 BitBake recipes 时，以排除一些不重要的文件或目录，从而提高构建性能和减少噪音。

==当BitBake构建一个任务时，它会计算任务的输出哈希值，以确定是否需要重新构建任务。==

`BB_HASHEXCLUDE_COMMON`可以让您定义哪些文件或目录应该被排除在哈希值计算之外，从而防止这些文件的更改触发不必要的重新构建。

这个变量通常在`.bbappend`文件中使用，允许您针对特定的 BitBake recipes 配置`BB_HASHEXCLUDE_COMMON`，以满足您的构建需求。示例用法如下：

```shell
# 排除一个目录下的所有文件
BB_HASHEXCLUDE_COMMON += "/path/to/excluded/directory/*"

# 排除特定文件
BB_HASHEXCLUDE_COMMON += "/path/to/excluded/file.txt"
```

通过配置`BB_HASHEXCLUDE_COMMON`，您可以更精确地控制哪些文件不应影响任务哈希值，从而提高构建效率。

# IMAGE_MANIFEST

`IMAGE_MANIFEST`是Yocto项目中用于生成镜像清单（manifest）的变量。

==清单是一个文本文件，列出了镜像中包含的所有文件、元数据和构建信息，==

==通常用于跟踪构建的内容和版本。==

镜像清单通常以一种易于阅读和共享的格式显示，以便开发人员、测试人员和部署人员了解构建的内容。

通过设置`IMAGE_MANIFEST`变量，您可以要求Yocto在构建过程中生成一个镜像清单文件，其中包含有关构建的详细信息。这个清单文件通常位于构建目录的子目录中，以供后续参考。示例用法如下：

```bitbake
IMAGE_MANIFEST = "1"
```

此示例会告诉Yocto生成一个镜像清单。清单文件通常存储在`${DEPLOY_DIR_IMAGE}`目录下，并以`.manifest`文件扩展名结尾。例如，如果您的镜像名称是`my-image`, 则清单文件可能是`my-image.manifest`。

通过查看清单文件，您可以了解构建中包含的软件包、文件、版本信息等，这对于调试、验证和部署都非常有用。这有助于确保构建的一致性和可追溯性。

# image_types_wic

`image_types_wic`是Yocto项目中用于定义支持的WIC（Yocto Image Creator）镜像类型的变量。WIC是Yocto的一个工具，用于创建各种类型的嵌入式镜像。镜像类型定义了镜像应该包括哪些文件和组件以及如何组织这些文件。

通过设置`image_types_wic`变量，您可以指定支持的WIC镜像类型，以便在构建过程中生成这些镜像。每个镜像类型都有一个关联的类，它定义了该类型镜像应该包含的文件和配置。

以下是一些常见的`image_types_wic`值和它们的用途：

1. `wic`：默认的WIC镜像类型，用于生成标准的Yocto镜像。

2. `wic.gz`：生成GZip压缩的WIC镜像。

3. `wic.bmap`：生成BMAP格式的WIC镜像，这允许快速写入到SD卡或其他嵌入式存储介质。

4. `wic.bmap.gz`：生成BMAP格式的GZip压缩WIC镜像。

在`local.conf`或`<machine>.conf`文件中，您可以使用`image_types_wic`变量来定义支持的WIC镜像类型，以满足您项目的需求。例如：

```bitbake
image_types_wic = "wic wic.gz wic.bmap wic.bmap.gz"
```

这将使Yocto构建系统生成这四种不同类型的WIC镜像，以便满足不同部署和存储需求。

# FEATURE_INSTALL

`FEATURE_INSTALL`是一个Yocto Project中的配置选项，用于定义哪些功能特性（features）在构建嵌入式Linux镜像时应该被包括。

功能特性是一种方法，允许您在构建时根据项目需求启用或禁用不同的功能。

这使得您可以轻松地自定义嵌入式系统的组件和行为。

通常，`FEATURE_INSTALL`设置在`local.conf`文件中。它是一个空格分隔的功能列表。以下是一些常见的功能特性，您可以根据项目需求包括或排除它们：

- `rtc`：启用实时时钟（RTC）支持。

- `wifi`：启用Wi-Fi功能。

- `bluetooth`：启用蓝牙功能。

- `usb`：启用USB功能。

- `ethernet`：启用以太网网络功能。

- `audio`：启用音频功能。

- `debug-tweaks`：启用用于调试的额外工具和选项。

- `dev-pkgs`：包括开发工具包（如编译器）。

- `tools-sdk`：包括一组开发工具。

- `x11`：启用X11图形系统支持。

通过在`FEATURE_INSTALL`中列出所需的功能特性，您可以自定义Yocto构建系统，以便生成满足项目需求的定制嵌入式Linux镜像。此外，还可以通过在`local.conf`中配置`PACKAGE_INSTALL`来控制要安装的软件包列表，以满足功能特性的需求。

在实际的Yocto项目中，根据项目需求选择启用或禁用不同的功能特性，以创建适合嵌入式设备的自定义Linux镜像。

# PSEUDO_PASSWD 

```
PSEUDO_PASSWD = "${IMAGE_ROOTFS}:${STAGING_DIR_NATIVE}"
```



`PSEUDO_PASSWD`是一个环境变量，用于配置 Yocto Project 的 Pseudo 工具的密码。Pseudo 是一个用于模拟 root 权限的工具，以便在构建根文件系统时不需要实际 root 权限。这对于构建根文件系统和软件包非常有用，因为它允许在构建过程中执行诸如文件权限更改等需要 root 权限的任务。

在这里，`${IMAGE_ROOTFS}` 和 `${STAGING_DIR_NATIVE}` 都是 Pseudo 工具的密码所需的路径。`${IMAGE_ROOTFS}` 表示根文件系统的路径，`${STAGING_DIR_NATIVE}` 表示本地构建工具链的路径。通过在这些路径上配置 Pseudo 工具的密码，可以让 Pseudo 工具在构建过程中执行必要的文件操作。

这样的配置可以确保在构建根文件系统和软件包时，Pseudo 工具能够模拟 root 权限并执行必要的文件操作，而无需实际 root 权限，从而增强了构建的安全性。

# oe.utils.features_backfill("DISTRO_FEATURES", d)

`oe.utils.features_backfill("DISTRO_FEATURES", d)` 是 Yocto/OpenEmbedded 中用于填补 `DISTRO_FEATURES` 变量的功能。`DISTRO_FEATURES` 是一个描述发行版所支持的特性和功能的变量。通过在 `DISTRO_FEATURES` 中指定特性，您可以为不同的目标构建不同的发行版。

==`features_backfill` 函数用于确保 `DISTRO_FEATURES` 变量包含所需的特性。它==会检查目标机器 (MACHINE) 是否支持指定的特性，并在需要时将这些特性添加到 `DISTRO_FEATURES` 中。

这个函数通常在 `local.conf` 文件或分层配置文件中使用，以根据目标机器或项目的需求来配置 `DISTRO_FEATURES` 变量，以便正确生成所需的发行版。通常，您不需要手动调用此函数，BitBake 会在构建过程中自动处理 `DISTRO_FEATURES` 变量的设置。

# Sstate summary

```
Sstate summary: Wanted 8 Found 4 Missed 4 Current 210 (50% match, 98% complete)
```

这个Sstate summary表明了在构建过程中使用了Sstate（Shared State Cache）来加速构建。

Sstate是一种缓存机制，它可以存储已经构建过的文件、中间结果和依赖关系，以便在以后的构建过程中重复使用，从而加快构建速度。

具体解释如下：

- `Wanted`：表示在当前构建过程中需要的Sstate条目的总数。
- `Found`：表示已经在Sstate缓存中找到的Sstate条目的总数，这些条目可以重复使用，从而加快构建速度。
- `Missed`：表示在Sstate缓存中未找到的Sstate条目的总数，需要重新构建。
- `Current`：表示在Sstate缓存中当前可用的Sstate条目的总数，这些条目可能被重用。

在这个示例中，有8个Sstate条目是构建过程中所需的，但只找到了4个，另外4个没有在Sstate缓存中找到，需要重新构建。当前Sstate缓存中有210个Sstate条目可供重用，其中50%匹配，98%完成，表示构建过程中的大部分内容可以从Sstate缓存中重复使用，从而提高构建效率。

Sstate是Yocto构建系统的一个重要特性，它有助于减少构建时间，特别是在重复构建相同软件包或相同配置时。

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