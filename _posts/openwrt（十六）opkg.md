---
title: openwrt（十六）opkg
date: 2018-04-14 09:58:38
tags:
	- openwrt

---



opkg是openwrt的包管理工具。

跟Ubuntu的apt-get，alpine的apk类似。

都是需要指定一个软件仓库。

我现在都是指定在这里。速度还可以。

第一行的跟后面的不太一样。

```
src/gz reboot_core https://downloads.openwrt.org/releases/17.01.4/targets/brcm2708/bcm2710/packages/
src/gz reboot_base https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/base
src/gz reboot_luci https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/luci
src/gz reboot_packages https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/packages
src/gz reboot_routing https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/routing
src/gz reboot_telephony https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/telephony
```

我们就到https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/base

这个地址去看，下面都是ipk文件。



