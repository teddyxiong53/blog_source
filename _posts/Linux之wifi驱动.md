---
title: Linux之wifi驱动
date: 2020-06-13 17:57:49
tags:
	- Linux

---

--

# 一个实际的场景

有一个usb的wifi网卡。想要在Linux下使用，默认用不了。

这个时候应该怎么做？

1、先把usb插到windows电脑。windows一般是可以正常驱动的。

从设备管理器里，查看usb无线网卡的详细信息，查看硬件id。是一个类似0x3070这样的一个数字。

2、到下面这个网址，输入第一步查询的硬件id进行查询。这样就可以看内核是否已经支持这个设备。

http://linuxwireless.sipsolutions.net/en/users/Devices/USB/

3、然后在内核源代码里grep 上面查询到的id。看属于哪个驱动模块。

4、选择模块，重新编译内核。

5、把对应的wifi的firmware放入到/lib/firmware目录下。



# 博通模组

CPU 与 WiFi 通过SDIO接口连接，用于传输数据，而要考虑功耗的事情，就需要通过
**WL_HOST_WAKE : WLAN to wake-up HOST**来实现的.

其中 WL_REG_ON 主要用于上电，休眠的时候，请保持GPIO上电，否则会丢失WiFi内部的状态，导致WiFi唤醒失败；
WL_HOST_WAKE 主要用于WiFi设备有数据的时候，唤醒CPU，进入中断.

其中引脚的电平要看CPU如何配置的，如果配置的是高电平有效，那么默认情况下是低电平，当WiFi有数据过来的时候就拉高，直到主控这边把数据拿完再拉低，如果主控一直没有来拿数据就一直是高电平．

通过WL_HOST_WAKE中断实现当有网络数据的时候，才唤醒CPU，平时CPU处于Standby状态下, 达到低功耗的第一步.



# 参考资料

1、Linux环境下使用WIFI模块：WIFI驱动移植

https://blog.csdn.net/yunlong654/article/details/88635398

2、[物联网篇 ] 15 -博通AP6255模块中WL_HOST_WAKE功能

这个的参考资料比较有用。

https://blog.csdn.net/z2066411585/article/details/103964407

3、[RK3399] SDIO 接口 Wifi 驱动流程分析 (AP6354)

https://blog.csdn.net/Stephen_yu/article/details/84789507

4、WIFI / BT 驱动之—设备树配置

这个说了博通模组的引脚含义。

https://blog.csdn.net/xiaoma_2018/article/details/85159551