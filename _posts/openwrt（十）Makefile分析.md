---
title: openwrt（十）Makefile分析
date: 2018-04-12 22:18:04
tags:	
	- openwrt

---



openwrt的Makefile真的是非常复杂。我暂时不打算花太多时间去深入阅读。

我慢慢积累吧。

```
到这个目录下编译kernel。
/home/teddy/work/openwrt/openwrt-master/build_dir/target-arm_arm1176jzf-s+vfp_musl_eabi/linux-brcm2708_bcm2708/linux-4.9.87
到这个目录下生成镜像。
/home/teddy/work/openwrt/openwrt-master/target/linux/brcm2708/image
在package目录下各个子目录里make。
/home/teddy/work/openwrt/openwrt-master/package/libs/libubox

/home/teddy/work/openwrt/openwrt-master/package/system/opkg

/home/teddy/work/openwrt/openwrt-master/package/libs/toolchain
```

