---
title: arm之corelink
date: 2018-03-06 14:12:11
tags:
	- arm

---



总是看到PL010 UART这种描述，PL010到底是什么呢？

我们在arm的官网上看到这样的信息：

```
ARM PrimeCell UART (PL010) overview
```

我看网站的大纲视图上有CoreLink控制器和外设，描述的就是这些信息。下面梳理出来。



CoreLink系统IP和设计工具为设计人员提供了基于AMBA规格构建SoC的组件和方法。

我觉得可以理解为ARM体系下的外设标准设计。

外设对应的标准编号为：

```
PL01X   uart
PL022   同步串口
PL03X   rtc
PL050   ps2鼠标键盘
PL060   gpio
PL13X   smart card interface
PL16X   dc-dc转换
PL18X   mmc接口
PL220   外部总线
PL341   DDR2

```

