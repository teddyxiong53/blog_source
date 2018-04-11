---
title: openwrt（四）rt5350
date: 2018-04-11 15:03:13
tags:
	- openwrt

---



在搜索openwrt相关资料的时候，发现了rt5350这个东西。就以这个点进行一下深入了解。

# 什么是rt5350

rt5350是Ralink公司的一颗芯片。

一个WiFi SoC。简称WiSoC。集成了WiFi功能是soc芯片。

196个引脚，尺寸是12mm x 12mm。

是mips架构的。主频360MHz。mips架构已经是行将就木的了。

5个100M的端口。

支持usb2.0的host和client。

芯片手册在这里：https://static.sparkfun.com/datasheets/Wireless/WiFi/RT5350.pdf

使用了这款芯片的路由器有92款。

我看这些路由器，都是flash为2MB、4MB、8MB、16MB这几种。2M的真的是太狠了。

ram有4M、8M、16M、32M、64M。

我看这个是flash和ram都用得最少的，不知道是不是rtos的。

https://wikidevi.com/wiki/D-Link_DIR-600_rev_D1

2M Flash和8M的RAM。是2012年的产品。

d-link叫友讯，是台湾的。



# 参考资料

1、RT5350和OPENWRT智能家居开发入门教程

https://wenku.baidu.com/view/a4fd668d1eb91a37f0115ca5.html

2、Ralink RT5350

https://wikidevi.com/wiki/Ralink_RT5350