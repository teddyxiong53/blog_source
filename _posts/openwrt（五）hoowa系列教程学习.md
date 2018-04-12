---
title: openwrt（五）hoowa系列教程学习
date: 2018-04-11 15:58:09
tags:
	- openwrt

---



hoowa写了一系列的教程，感觉不错，学习一下。

# 芯片架构

在arm广泛应用之前，路由器芯片的架构主要就是mips。

龙芯采用的就是mips架构，但是开始没有取得授权，直到2009年才跟mips达成和解。

mips架构曾经有过辉煌的历史，曾经跟x86、powerpc三足鼎立。还有用mips做服务器的。

mips架构也是通用的，针对电脑的。

但是没有竞争过Intel。

于是mips转战嵌入式市场。因为开放架构，所以有大量的公司基于mips架构做路由器芯片。

我们现在用的路由器，90%都是mips芯片。而且都是32位的。在这个领域，mips的性价比的最高的，比低端arm要好 。

路由器的soc，业内也喜欢叫做RoC。Router on a Chip。

集成了内存控制、gpio、switch芯片、wifi芯片、加密芯片、SATA接口、pcie接口、usb接口。

功耗在1到3W。主频在400M到800M。

但是现在随着arm横扫一切，在路由器领域，也有arm的身影了。博通推出的 bcm470x系列芯片，就是arm架构的，小米路由器第一代就是用这种芯片的。

# 芯片厂家

1、Atheros公司。

mips架构发明人约翰·轩尼诗的公司。是路由芯片的顶级公司。是WiFi标准的制定者之一。

目前国内的智能路由只有极路由1代使用了这个芯片。Atheros也是目前openwrt支持最全面的的芯片。

这家公司在国内的问题就是配套产业链不够完善。而且跟tp-link有协议，不能卖给其他厂家。

该公司在2011年被高通收购。

2、博通。

博通的大部分芯片还是mips架构，现在在向arm转。

3、Ralink公司。

雷凌科技，台湾的。在国内出货量最大的。性价比最高。2011年被联发科收购。

对openwrt支持不够。驱动代码不开源。

# 传统路由器是怎么做的？

芯片厂家提供的SDK已经很完善了，连web界面都是完善的。设备厂家只剩下拼价格和外观。

# 智能路由器怎么做？

大部分的智能路由器都是基于openwrt。



# 搭建硬件环境

选择板子的原则：

1、支持openwrt系统，要完善。

2、有8M的flash。

3、有64M的ram。

4、不能是旧货。

5、在国内可以买到。

hoowa选择了一款Atheros的板子。

spi flash的分区是这样的。

```
[ 0.690000] 5 tp-link partitions found on MTD device spi0.0
[ 0.700000] Creating 5 MTD partitions on "spi0.0":
[ 0.700000] 0x000000000000-0x000000020000 : "u-boot"
[ 0.710000] 0x000000020000-0x00000012a290 : "kernel"
[ 0.730000] 0x00000012a290-0x0000007f0000 : "rootfs"
[ 0.760000] 0x000000300000-0x0000007f0000 : "rootfs_data"
[ 0.760000] 0x0000007f0000-0x000000800000 : "art"
[ 0.770000] 0x000000020000-0x0000007f0000 : "firmware"
```

有一个data区，art区，firmware区。

大小如下：

```
u-boot：128K。
kernel：1M。
rootfs：6.7M。
rootfs_data：4.9M。
art：64K。无线的硬件参数。
firmware：7.9M。包含了除u-boot和art之外的内容。
```





br-lan：虚拟设备，用于LAN口设备桥接的，目前路由器普遍将有线LAN口(一般四个)和WIFI无线接口桥接在一起作为统一的LAN。

wlan0：实设备，当启动了wifi功能以后将产生此设备。
pppoe-wan：虚拟设备，在PPPOE拨号成功以后产生。

```
root@LEDE:~# brctl show
bridge name     bridge id               STP enabled     interfaces
br-lan          7fff.b827eb004eca       no              eth0
```

读取日志，用logread命令。

# 配置wan口参数

我当前的wan口是连接到另外一个路由器上的的。所以openwrt就不需要拨号了。

wan口可以配置的为：

1、dhcp。

2、静态ip。

3、pppoe。

4、pptp。

5、3g。

前面3种是最常用的。

我当前用的是静态ip的。

# 防火墙相关

openwrt下的防火墙的默认行为已经可以满足路由器的需求了，一般情况下不需要修改。

相关知识做一个了解即可。

## 内置防火墙

openwrt的nat、dmz、Firewall rules都是用/etc/config/firewall这个配置文件来管理的。

这个配置文件是/etc/init.d/firewall启动的时候，被解析生成iptables来产生作用。

相当于是对iptables的一个封装。



感觉这个教程后续没有太多的东西了。



# 参考资料

1、跟hoowa学做智能路由

https://blog.csdn.net/gaopeiliang/article/details/40158569