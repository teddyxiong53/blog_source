---
title: yodaos之jsruntime在buildroot-qemu里运行
date: 2022-08-21 20:32:08
tags:
	- yodaos

---

--

对我比较有价值的，就是jsruntime。

鉴于官方提供的仓库没法直接使用。

我决定在qemu里弄一个测试环境。这样测试起来也比较方便。

就用qemu x86_64的。

就在package下面弄一个rokid的目录。

跟buildroot同一级目录，弄一个buildroot-yodart目录。

看jsruntime依赖了这些东西：

```
DEPENDS:=+libstdcpp +android-system-core +shadow-node \
	   +opus +speech +vol_ctrl +wpa_ctrl +ota_unpack \
	   +lumenlight +libffmpeg-audio-dec +librplayer +input-event \
	   +aliyunloglite +flora +httpsession +httpdns +property
```

一个个看

```
android-system-core
	对应这个目录。
	$(ROKID_DIR)/3rd/android_lib/system/core
	依赖了+property +android-kernel-headers
	android-kernel-headers
	PKG_SOURCE_DIR:=$(TOPDIR)/../3rd/android_lib/external/android-kernel-headers
	这个下面文件特别多。
	肯定不能直接放我当前的仓库。不然仓库就会变得很大。
	看看github上有没有现成的。
	通过github来取这个目录的。
	看这个仓库的提交历史，有这个：
	android kernel headers, import for use linux/ashmem.h
	就为了这一个头文件？
	谁使用了这个机制？
	我先不用这个。
	在rootfs里搜索ashmem_ioctl，好像没有谁使用了。
	先就不用这个。
	我看我们buildroot也有使用ashmem.h的。但是只是手动把文件放到目录而已。
	这样就够了。
```

先加property的。

这些package基本上都是基于cmake来编译的。

我就模仿buildroot/avs的mk文件和Config.in文件来改。

```
照着openwrt的Makefile里的内容来写。
需要安装到staging目录。
```



新增一个defconfig文件。

在我们的configs目录下。

```
直接先export BR2_EXTERNAL=../buildroot-yodart/
这样就不用每个make命令都带上这个变量。
make list-defconfigs   
```

可以看到。

```
External configs in "yodart buildroot":
  qemu_x86_64_yodart_defconfig        - Build for qemu_x86_64_yodart
```

直接make property-rebuild一下看看。

buildroot版本是2020.02.1



然后加shadownode的。

这个代码实在是太多了。

通过git的方式来获取吧。

直接从github官方仓库下载。

shadownode相比于iotjs，把deps下面的都已经放进了代码，而不是靠git submodule下载。这样方便了许多。



这个在openwrt和buildroot之间移植package，可以让我加深对二者的理解。

很多变量名字都是一样的。

buildroot使用的自己编译的工具链，对应openwrt的这个`TOOLCHAIN_DIR`变量的目录在哪里呢？





参考资料

