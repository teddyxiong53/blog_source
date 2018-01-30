---
title: Linux之cloud-lab（二）buildroot分析
date: 2018-01-30 10:48:12
tags:
	- Linux
	- buildroot

---



buildroot目录下的东西多，要先理顺了，才方便后面的调试。

# 目录梳理

```
teddy@teddy-ubuntu:~/work/txkj/cloud-lab/labs/linux-lab/buildroot$ tree -L 1
.
├── arch：下面放着config.arm这种配置文件。配置项目都比较简单。
├── board：下面子目录很多。我们用的在qemu/vexpress目录下。下面就放了一个readme.txt。我看其他的可能放了patch或者配置文件之类。
├── boot：放了各种不同的bootloader，我用的是uboot目录下的。里面放着一些patch。
├── CHANGES
├── Config.in
├── Config.in.legacy
├── configs：全是文件。我们用的是qemu_arm_vexpress_defconfig。内容不多，只有20行左右。
├── COPYING
├── DEVELOPERS
├── dl：下载的一些源代码包。包括gcc、uclibc等的源代码。全是压缩包。
├── docs：帮助文档。
├── fs：各种文件系统子目录。不过下面都是放在几个配置文件而已。
├── linux：几个配置文件。
├── Makefile
├── Makefile.legacy
├── package：各种补丁。下面有一堆的mk文件，比较重要。
├── README
├── support：好像是一些工具。
├── system：放在device_table.txt等文件。
├── toolchain：全是配置文件。
└── utils：工具。
```

# make help内容

1、清理。

```
clean 删除在build过程中生成的文件。
distclean 删除非源代码文件之外的其他文件。包括.config文件。
```

2、build类。

```
all 
toolchain：
sdk
```

3、配置类。

```
menuconfig。
nconfig、xconfig、gconfig都没有从顶层往下传。不管。
defconfig
其他还有一堆没有什么用的。
```

4、package相关。

假如包名是xxx。

```
xxx build和install xxx以及它的依赖。
xxx-source  只是下载对应的源代码
xxx-extract 提取源代码
xxx-patch 打补丁
xxx-depends build对应的依赖
xxx-configure 
xxx-build
xxx-show-depends

```

5、busybox

```
make busybox-menuconfig
```

6、uclibc。

```
uclibc-menuconfig
```

7、文档。









# 顶层Makefile梳理

大概1000行。

1、buildroot的版本是2018.02-git

2、需要的make的最低版本是3.8.1

3、禁止了并行编译。

4、包含了support/misc/utils.mk文件。

5、包括了package/Makefile.in。

```
1、pkg-download.mk。提供了一个DOWNLOAD函数，给外面调用来下载。
2、pkg-generic.mk。
```

packages-file-list.txt 是比较重要的文件。

我以lzip这个包为切入点，看看处理过程。

我在顶层Makefile里加error。打印出package有这些：

```
host-lzip toolchain-buildroot toolchain bash busybox host-e2fsprogs ifupdown-scripts initscripts linux-headers ncurses host-patchelf readline skeleton-init-common skeleton-init-sysv skeleton uclibc host-util-linux host-fakeroot host-makedevs host-e2fsprogs host-fakeroot host-makedevs
```



HOST_DIR：放交叉编译工具链的。

STAGING_DIR：放目标rootfs的位置。

做出来的文件系统，把include头文件都放进去了。



现在感觉看起来很难看下去。用调试的方法来做。

在顶层Makefile的最后，加上这个：

```
xhl:
	make -C $(TOP_DIR)/buildroot $(xhl_target)
```

因为直接在buildroot下编译，很多顶层的变量没有传递下来，执行不对。

现在我就可以在linux-lab这个目录下，执行：

```
make xhl xhl_target=lzip-depends
```

现在来进行各种buildroot下的编译，默认很多东西没有传递上来的。

在这里配置的lzip的下载地址。

```
./package/lzip/lzip.mk:8:LZIP_SITE = http://download.savannah.gnu.org/releases/lzip
```

我在电脑的浏览器上打开这个地址，下面很多包的列表，所以只靠这个地址没法完成下载，还要看版本号。

在buildroot的顶层Makefile里这样包含进去的。

```
include $(sort $(wildcard package/*/*.mk))
```

lzip.mak的完整内容：

```
LZIP_VERSION = 1.19
LZIP_SITE = http://download.savannah.gnu.org/releases/lzip
LZIP_LICENSE = GPL-2.0+
LZIP_LICENSE_FILES = COPYING

define LZIP_CONFIGURE_CMDS
	(cd $(@D); $(TARGET_MAKE_ENV) ./configure --prefix=/usr \
		$(TARGET_CONFIGURE_OPTS) )
endef

define HOST_LZIP_CONFIGURE_CMDS
	(cd $(@D); $(HOST_MAKE_ENV) ./configure --prefix=$(HOST_DIR) \
		$(HOST_CONFIGURE_OPTS) )
endef

define LZIP_BUILD_CMDS
	$(TARGET_MAKE_ENV) $(MAKE) -C $(@D)
endef

define HOST_LZIP_BUILD_CMDS
	$(HOST_MAKE_ENV) $(MAKE) -C $(@D)
endef

define LZIP_INSTALL_TARGET_CMDS
	$(TARGET_MAKE_ENV) $(MAKE) -C $(@D) DESTDIR=$(TARGET_DIR) install
endef

define HOST_LZIP_INSTALL_CMDS
	$(HOST_MAKE_ENV) $(MAKE) -C $(@D) install
endef

# It's not autotools-based
$(eval $(generic-package))
$(eval $(host-generic-package))

```

现在看package目录下的mk文件，

pkg-generic.mk就是最后提供了generic-package和host-generic-package这2个东西给外面用了。

pkg-cmake.mk提供2个接口：cmake-package和host-cmake-package。

这部分涉及的东西确实太多太杂了。我暂时不打算深入下去了。

