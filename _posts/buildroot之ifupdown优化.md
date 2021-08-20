---
title: buildroot之ifupdown优化
date: 2021-08-18 11:39:33
tags:
	- buildroot

---

--

当前ifupdown导致系统启动时，会卡住一段时间。严重拖慢了系统的开机速度。所以需要解决一下这个问题。

是busybox间接引入进来的。

先把busybox在buildroot里的配置和编译过程梳理一下。

kconfig-package的编译过程是怎样的？

make busybox-rebuild，调用的过程是怎样的？

./buildroot/package/ifupdown-scripts/network/if-pre-up.d/wait_iface

对应的配置项是

BR2_PACKAGE_IFUPDOWN_SCRIPTS=y

是默认选中的。

```
default y if BR2_ROOTFS_SKELETON_DEFAULT
```

```
BR2_ROOTFS_SKELETON_DEFAULT=y
```

我在自己的配置文件里，强行把这个去掉看看。

