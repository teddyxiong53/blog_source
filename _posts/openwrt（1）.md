---
title: openwrt（1）
date: 2020-03-24 09:42:02
tags:
	- openwrt

---

1

自己编译烧录树莓派3b的。

这个用tar来解压会报错。只有11M左右。

```
bin/targets/brcm2708/bcm2710/openwrt-brcm2708-bcm2710-rpi-3-ext4-factory.img.gz
```

不用解压，直接用rufus进行烧录到sd卡就好了。

默认打开了串口。所以不用调整任何参数。

默认有hdmi输出和支持usb的键盘。所以如果有键盘，可以不用串口。



