---
title: 智能音箱之ble配网方式
date: 2020-03-20 14:12:11
tags:
	- 智能音箱
---

1

以rk3308的ble配网作为分析对象。

参考文档《RK3308_RTL8723DS_WIFI_BT_说明文档_V1.20》《Rockchip Linux WIFI BT 开发指南 V4.0 20181126》

蓝牙使用bluez + bluez-alsa来实现A2DP sink、HFP、ble蓝牙配网这3个功能。

需要去掉内核默认的HCI UART driver。因为wifi驱动自己另外写了。

蓝牙使用rk3308的ttys4串口来进行控制。



蓝牙ble配网，需要板端运行一个gatt-server。这个是在bluez的tools/gatt-server.c的基础上修改。

增加了给手机端连接的service及对应的characteristic。



操作过程：

板端：

```
1、打开蓝牙，可以用hciconfig hci0 up
2、执行gatt-service程序。
```

手机端：

```
1、安装rk提供的wifi introducer apk。打开扫描。

```



目前是扫描不到。

