---
title: Android系统之分区规范
date: 2017-06-24 23:14:06
tags:

	- 安卓

---

在刷机中，总是看到很多的分区，那么在安卓的规范了，需要有哪些分区？这些分区又分别起到什么作用呢？本文就此进行梳理。

鉴于我的手机没有root，很多操作不方便。我就基于网上的文章进行总结。

用adb shell对安卓手机进行访问。

`ls -la /dev/block/platform/hi_mci.0/by-name`，下面是对命令的输入结果进行梳理后的情况。

```
boot --> /dev/block/mmcblk0p20 分区数够多的，都到20了。boot分区在20号分区上。boot分区放的是kernel。
cache --> /dev/block/mmcblk0p22。
cust --> /dev/block/mmcblk0p28
data --> p29
dsp --> p17
fastboot2 --> p5
hifi --> p18
hisitest0 --> p24
hisitest1 --> p25
hisitest2 --> p26
log --> p3
logo --> p12
mcuimage --> p1
misc --> p7
modemimage --> p16
modemlog --> p19
modemnvbkup --> p8
modemnvm1 -->p14
modemnvm2 --> p15
nvme --> p9
oeminfo--> p10
recovery --> p21
round --> p4
secureboot --> p6
system --> p27
teeos --> p2
userdata --> p23
vrcb --> p11
```



参考资料

1、Android Fastboot 与 Recovery 和刷机

https://www.jianshu.com/p/d960a6f517d8

2、分区布局

https://source.android.com/devices/bootloader/system-as-root