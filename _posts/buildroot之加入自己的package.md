---
title: buildroot之加入自己的package
date: 2019-05-17 15:37:11
tags:
	- Linux
---

1

在package目录下，新建一个demo_app目录。

下面新建：

```
Config.in  demo_app.mk
```

这2个文件。

修改package/Config.in文件，把demo_app加入进去。

```
menu "Target packages" #就加在最上面的这个menu下面。
	source "package/demo_app/Config.in"
```

在demo_app/Config.in里写入：

```
config BR2_PACKAGE_DEMO_APP
bool"demo app"
help
  demo app to show
```

然后写demo_app.mk文件

```
################################################################################
#
# demo app
#
################################################################################
DEMO_APP_VERSION = master
DEMO_APP_SITE_METHOD = git
DEMO_APP_SITE = https://github.com/teddyxiong53/buildroot_demo_app
DEMO_APP_SOURCE = demo_app-$(DEMO_APP_VERSION).tar.gz
DEMO_APP_ALWAYS_BUILD = YES
DEMO_APP_INSTALL_STAGING = YES
DEMO_APP_CFLAGS = 
DEMO_APP_LDFLAGS = 
OUT_BIN = demo_app
DEMO_APP_MAKE_FLAGS += \
		CROSS_COMPILE="$(CCACHE) $(TARGET_CROSS)" \
		CC=$(TARGET_CC)      \
		OUT_BIN=$(OUT_BIN)  \
		AR=$(TARGET_AR)      \
		STRIP=$(TARGET_STRIP) \
		CFLAGS=$(DEMO_APP_CFLAGS) \
		LDFLAGS=$(DEMO_APP_LDFLAGS) \
		STAGING_DIR=$(STAGING_DIR)  \
		TARGET_DIR=$(TARGET_DIR) 

define DEMO_APP_BUILD_CMDS
	$(MAKE) clean  -C $(@D) 
	$(MAKE) $(DEMO_APP_MAKE_FLAGS)  -C $(@D)
endef

define DEMO_APP_INSTALL_TARGET_CMDS
	$(INSTALL) -m 0755 -D $(@D)/$(OUT_BIN)  $(TARGET_DIR)/usr/bin
endef

$(eval $(generic-package))
```

make menuconfig，把demo_app选上。

然后make savedefconfig。保存。

看到对应的配置文件里有了这一项了。

```
BR2_PACKAGE_DEMO_APP=y
```



我在我的github上新建对应的repo。把代码生成上去。

demo_app.c和Makefile 这2个文件。



我的demo_app的Makefile里出了错。

重新提交。再make。不行。总是试图解压压缩包。我已经手动把压缩包删除了。

所以还需要到build目录下，把对应的demo_app目录删掉。这样才可以。

```
buildroot在编译之前会根据.config 文件来检查output/build/package 的6个文件，做相应的步骤：
.stamp_configured,  此文件表示已经配置过
    .stamp_downloaded, 此文件表示源码已经下载过，没有此文件会重新下载
.stamp_patched, 此文件表示已经打过补丁
.stamp_extracted  此文件表示已经压过
    .stamp_builted 此文件表示源码已经编译过  
.stamp_target_installed  此文件表示软件已经安装过
```

make一下，重新生成文件系统。

我还是在qemu vexrepss下测试。

现在可以运行了：

```
# demo_app 
hello buildroot package
```



buildroot怎么编译一个最小系统。

make  allnopackageconfig 

这个就可以。 



分析一下make demo_app的执行过。

打印是这样：

```
hlxiong@hlxiong-VirtualBox:~/work2/buildroot/buildroot$ make demo_app
WARNING: no hash file for demo_app-master.tar.gz
>>> demo_app master Extracting
gzip -d -c /home/hlxiong/work2/buildroot/buildroot/dl/demo_app-master.tar.gz | tar --strip-components=1 -C /home/hlxiong/work2/buildroot/buildroot/output/build/demo_app-master   -xf -
>>> demo_app master Patching
>>> demo_app master Configuring
>>> demo_app master Building
/usr/bin/make -j5 clean  -C /home/hlxiong/work2/buildroot/buildroot/output/build/demo_app-master 
rm -rf *.o demo_app *.d
/usr/bin/make -j5 CROSS_COMPILE=" /home/hlxiong/work2/buildroot/buildroot/output/host/bin/arm-buildroot-linux-gnueabihf-" CC=/home/hlxiong/work2/buildroot/buildroot/output/host/bin/arm-buildroot-linux-gnueabihf-gcc OUT_BIN=demo_app AR=/home/hlxiong/work2/buildroot/buildroot/output/host/bin/arm-buildroot-linux-gnueabihf-ar STRIP=/home/hlxiong/work2/buildroot/buildroot/output/host/bin/arm-buildroot-linux-gnueabihf-strip CFLAGS= LDFLAGS= STAGING_DIR=/home/hlxiong/work2/buildroot/buildroot/output/host/arm-buildroot-linux-gnueabihf/sysroot TARGET_DIR=/home/hlxiong/work2/buildroot/buildroot/output/target   -C /home/hlxiong/work2/buildroot/buildroot/output/build/demo_app-master
/home/hlxiong/work2/buildroot/buildroot/output/host/bin/arm-buildroot-linux-gnueabihf-gcc  -c -o demo_app.o demo_app.c
/home/hlxiong/work2/buildroot/buildroot/output/host/bin/arm-buildroot-linux-gnueabihf-gcc  -g -o demo_app demo_app.o
>>> demo_app master Installing to staging directory
>>> demo_app master Fixing libtool files
>>> demo_app master Installing to target
/usr/bin/install -m 0755 -D /home/hlxiong/work2/buildroot/buildroot/output/build/demo_app-master/demo_app  /home/hlxiong/work2/buildroot/buildroot/output/target/usr/bin
```

如果O目录不是output，那么就NEED_WRAPPER为y。rk3308的就是这么做的。

```
ifeq ($(O),$(CURDIR)/output)
CONFIG_DIR := $(CURDIR)
NEED_WRAPPER =
else
CONFIG_DIR := $(O)
NEED_WRAPPER = y
endif
```

如果NEED_WRAPPER为y，则执行生成Makefile的命令。

```
.PHONY: outputmakefile
outputmakefile:
ifeq ($(NEED_WRAPPER),y)
	$(Q)$(TOPDIR)/support/scripts/mkmakefile $(TOPDIR) $(O)
endif
```



# 经验

```
BELLE_SIP_VERSION = 1.6.x
BELLE_SIP_SITE = $(TOPDIR)/../external/belle-sip/belle-sip-1.6.x
BELLE_SIP_SITE_METHOD = local
BELLE_SIP_AUTOGEN = YES

# 对于只有autogen.sh的，需要加上这个
define BELLE_SIP_RUN_AUTOGEN
    cd $(@D) && PATH=$(BR_PATH) ./autogen.sh
endef

# 对于只有autogen.sh的，需要加上这个。
BELLE_SIP_PRE_CONFIGURE_HOOKS += BELLE_SIP_RUN_AUTOGEN

$(eval $(autotools-package))
```

添加某些操作前后的执行脚本。是通过hooks来做的。



参考资料

1、Buildroot构建指南--快速上手与实用技巧

https://blog.csdn.net/zhou_chenz/article/details/52335634

2、buildroot重新编译package

https://blog.csdn.net/qq_31811537/article/details/81069993

3、Buildroot工具

https://blog.csdn.net/zhou_chenz/article/category/6019071