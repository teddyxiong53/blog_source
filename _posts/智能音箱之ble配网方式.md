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



蓝牙ble配网，需要板端运行一个gatt-server。就是运行一个服务端，这个就是本质。ap配置，是一个基于wifi的服务端。

这个是在bluez的tools/gatt-server.c的基础上修改。所以本质是在板子上启动一个gatt服务器。

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

发现问题了。

是需要先手动执行bluetoothd。

```
# 板端依次执行：
hciconfig hci0 up
# 注意这个的位置，是没有在环境变量里的，所以要带上完整路径。
/usr/libexec/bluetooth/bluetoothd &
# 启动配置程序，则个有对应的package。自己编译出来。
ble_wificonfig
```

现在就可以看到了。

可以用配网程序连接上，并且把wifi信息发送过来。

我觉得需要通过dbus调试来分析过程。

```
export DBUS_SESSION_BUS_ADDRESS="unix:path=/var/run/dbus/system_bus_socket"
dbus-monitor
```

这样就可以观察dbus上的消息了。

如果没有上面那个环境变量设置，dbus-monitor会报错：

```
Failed to open connection to session bus: Using X11 for dbus-daemon autolaunch was disabled at compile time, set your DBUS_SESSION_BUS_ADDRESS instead
```

