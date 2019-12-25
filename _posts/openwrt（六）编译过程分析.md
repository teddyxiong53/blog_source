---
title: openwrt（六）编译过程分析
date: 2018-04-11 20:12:20
tags:
	- openwrt

---



openwrt肯定是改了kernel的，因为它的初始化进程被改成了procd，而不是默认的init，环境变量里也没有看到指定，我认为这个是在编译kernel之前，把改动合并进去的，到底是不是呢？需要把编译过程理一遍。

先看根目录的Makefile。

入口处是：

```
world:

ifndef ($(OPENWRT_BUILD),1)
#第一个逻辑
else
#第二个逻辑
endif
```

默认目标就是world。我们make的时候，也没有带OPENWRT_BUILD=1这个定义。

所以是进入到第一个逻辑。

我们继续看，第一个逻辑做了什么。

```
ifneq ($(OPENWRT_BUILD),1)
  _SINGLE=export MAKEFLAGS=$(space);

  override OPENWRT_BUILD=1 #把这个条件设置了。你下次make的时候，就会进入到第二个逻辑的。
  export OPENWRT_BUILD
  GREP_OPTIONS=
  export GREP_OPTIONS
  include $(TOPDIR)/include/debug.mk
  include $(TOPDIR)/include/depends.mk
  include $(TOPDIR)/include/toplevel.mk
```

这3个mk文件里，最重要的是toplevel.mk。

重点看这段。`%::`解释world目标的规则。

```
%::
	@+$(PREP_MK) $(NO_TRACE_MAKE) -r -s prereq
	@( \
		cp .config tmp/.config; \
		./scripts/config/conf --defconfig=tmp/.config -w tmp/.config Config.in > /dev/null 2>&1; \
		if ./scripts/kconfig.pl '>' .config tmp/.config | grep -q CONFIG; then \
			printf "$(_R)WARNING: your configuration is out of sync. Please run make menuconfig, oldconfig or defconfig!$(_N)\n" >&2; \
		fi \
	)
	@+$(ULIMIT_FIX) $(SUBMAKE) -r $@ $(if $(WARN_PARALLEL_ERROR), || { \
		printf "$(_R)Build failed - please re-run with -j1 to see the real error message$(_N)\n" >&2; \
		false; \
	} )
```

我们执行make V=s，简化后的规则是这样的：

```
prereq:: prepare-tmpinfo .config
	@make -r -s tmp/.prereq-build
	@make V=ss -r -s prereq
%::
	@make V=s -r -s prereq
	@make -w -r world
```

可以看到最后还是执行了prereq和world目录，都会进入到第二个逻辑的。

所以我们继续回到顶层Makefile看第二个逻辑。

它是包含了剩下的所有内容，所以第二个逻辑就是主逻辑。

首先是包含了4个Makefile。

```
  include rules.mk
  include $(INCLUDE_DIR)/depends.mk
  include $(INCLUDE_DIR)/subdir.mk
  include target/Makefile
  include package/Makefile
  include tools/Makefile
  include toolchain/Makefile
```



# 编译kernel

对应的Makefile是target/linux/bcm2708/Makefile。



# 怎样进行patch的？

在配置完openwrt后，首次编译会从网上下载各种源代码压缩包。

然后解压后，给这些源代码打上patch。

如果你要修改源代码，直接在源代码目录下修改就好了。

但是这样有个问题，就是你修改代码，在make clean后，就都没有了。



```
tools目录
这个目录下，是一下patch和Makefile。
每个Makefile里都有一句 $(eval $(call HostBuild))，表示编译这个工具是为了在主机上使用的。

toolchain - 包含一些命令去获取kernel headers, C library, bin-utils, compiler, debugger

target - 各平台在这个目录里定义了firmware和kernel的编译过程。

package - 包含针对各个软件包的Makefile。openwrt定义了一套Makefile模板，各软件参照这个模板定义了自己的信息，如软件包的版本、下载地址、编译方式、安装地址等。

include - openwrt的Makefile都存放在这里。

scripts - 一些perl脚本，用于软件包管理。

dl - 软件包下载后都放到这个目录里

build_dir - 软件包都解压到build_dir/里，然后在此编译

staging_dir - 最终安装目录。tools, toolchain被安装到这里，rootfs也会放到这里。

bin - 编译完成之后，firmware和各ipk会放到此目录下。

firmware由kernel和rootfs两个部分组成，要对两个部分先分别处理，然后再合并成一个.bin文件。

```



# 参考资料

1、openwrt: Makefile 框架分析

https://www.cnblogs.com/sammei/p/3968916.html

2、OpenWrt patch方法

https://blog.csdn.net/wwx0715/article/details/25160361