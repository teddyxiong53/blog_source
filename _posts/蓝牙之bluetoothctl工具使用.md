---
title: 蓝牙之bluetoothctl工具使用
date: 2018-12-14 16:59:35
tags:
	- 蓝牙

---

--

这个工具是交互性的。

基本操作逻辑是：

```
进入主菜单
$ bluetoothctl
主菜单的前面是[bluetooth]标记的
[bluetooth] help
可以看到advertiser、scan、gatt这3个单词的颜色不一样，表示这3个是子菜单。
进入gatt子菜单
[bluetooth] menu gatt
退出gatt子菜单
[bluetooth] back
```

操作的对象有：

本机的控制器

远端的蓝牙设备

# 本机控制器操作

## list

列出本机所有的控制器的简单信息。

举例：

```
[bluetooth]# list
Controller 00:1A:7D:DA:71:13 thinkpad [default] 
```

## show [ctrl]

查看指定控制器的详细信息。

举例：

```
[bluetooth]# show
Controller 00:1A:7D:DA:71:13 (public)
        Name: thinkpad
        Alias: thinkpad
        Class: 0x000c010c
        Powered: yes
        Discoverable: yes
        DiscoverableTimeout: 0x00000000
        Pairable: yes
        UUID: Headset AG                (00001112-0000-1000-8000-00805f9b34fb)
        UUID: Generic Attribute Profile (00001801-0000-1000-8000-00805f9b34fb)
        UUID: A/V Remote Control        (0000110e-0000-1000-8000-00805f9b34fb)
        UUID: Generic Access Profile    (00001800-0000-1000-8000-00805f9b34fb)
        UUID: PnP Information           (00001200-0000-1000-8000-00805f9b34fb)
        UUID: A/V Remote Control Target (0000110c-0000-1000-8000-00805f9b34fb)
        UUID: Audio Sink                (0000110b-0000-1000-8000-00805f9b34fb)
        UUID: Audio Source              (0000110a-0000-1000-8000-00805f9b34fb)
        Modalias: usb:v1D6Bp0246d0536
        Discovering: no
Advertising Features:
        ActiveInstances: 0x00
        SupportedInstances: 0x05
        SupportedIncludes: tx-power
        SupportedIncludes: appearance
        SupportedIncludes: local-name
```

## select [ctrl]

选择哪个控制器来使用。

不管。

## power on/off

控制器开关。

## pairable on/off

配对开关

## discoverable on/off

可发现性开关

## discoverable-timetout [value]

查询或设置可发现性超时时间。

默认是0s。

## agent 

可以跟on、off或找一个capability值。

## scan on/off

扫描开关。

## info [dev]





## devices

查看本机可以访问的设备。

```
[bluetooth]# devices 
Device 18:F0:E4:E9:B6:56 Mi Note 3
Device 08:D4:6A:78:68:D7 G7 ThinQ
Device B4:0B:44:F4:16:8D Teddy
```

## paired-devices

查看配对过的设备。

```
[bluetooth]# paired-devices 
Device 08:D4:6A:78:68:D7 G7 ThinQ
Device B4:0B:44:F4:16:8D Teddy
```



扫描、配对、连接手机

```
scan on
```

然后会得到一个列表。

就可以关闭扫描了。

```
scan off
```

可以从扫描的打印中看到我的手机的信息。

```
[NEW] Device 7F:1E:B8:A6:1F:87 HONOR V30 PRO
```

连接

```
[bluetooth]# connect 7F:1E:B8:A6:1F:87
Attempting to connect to 7F:1E:B8:A6:1F:87
[CHG] Device 7F:1E:B8:A6:1F:87 Connected: yes
Connection successful
```

接着自动打印了手机蓝牙的信息，内容较多。就不放这里了。

看了一下，都是ble的服务。

最后面是这样的内容，0000aaa0-0000-1000-8000-aabbccddeeff 这个是我在nrf connect这个app里gatt server增加的内容。

```
[CHG] Device 7F:1E:B8:A6:1F:87 UUIDs: 0000046a-0000-1000-8000-00805f9b34fb
[CHG] Device 7F:1E:B8:A6:1F:87 UUIDs: 00001800-0000-1000-8000-00805f9b34fb
[CHG] Device 7F:1E:B8:A6:1F:87 UUIDs: 00001801-0000-1000-8000-00805f9b34fb
[CHG] Device 7F:1E:B8:A6:1F:87 UUIDs: 00001803-0000-1000-8000-00805f9b34fb
[CHG] Device 7F:1E:B8:A6:1F:87 UUIDs: 0000180d-0000-1000-8000-00805f9b34fb
[CHG] Device 7F:1E:B8:A6:1F:87 UUIDs: 0000181c-0000-1000-8000-00805f9b34fb
[CHG] Device 7F:1E:B8:A6:1F:87 UUIDs: 0000aaa0-0000-1000-8000-aabbccddeeff
[CHG] Device 7F:1E:B8:A6:1F:87 UUIDs: 0000fe35-0000-1000-8000-00805f9b34fb
[CHG] Device 7F:1E:B8:A6:1F:87 UUIDs: 11c8b310-80e4-4276-afc0-f81590b2177f
[CHG] Device 7F:1E:B8:A6:1F:87 ServicesResolved: yes
```

现在看手机上nrf connect软件里，已经可以看到跟电脑的连接了。

所以，上面这个连接，实际上连接的ble。从蓝牙地址也可以看出来。ble这个是随机的。

普通蓝牙地址，不是上面这个。

手机上显示是connected / not boned。

手机既是client，也是server。

作为client，可以看到2个服务。

```
Generic Access
	uuid是0x1800
	里面有2个特征值。
	device id，uuid是0x2a00，可读，读取得到是thinkpad。
	Appearance：uuid是0x2a01，可读，读取得到268
```

连接后，提示符编程了设备名字。

```
[HONOR V30 PRO]# 
```

进入到menu gatt。

查看属性

```
[HONOR V30 PRO]# list-attributes 
```

这个看到的就是前面连接时打印的哪些特征值。

属性操作的，以00002a00-0000-1000-8000-00805f9b34fb 这个device name为例。

需要先select，才能操作。

```
select-attribute <attribute/UUID> 
```

那么就这样：

```
select-attribute 00002a00-0000-1000-8000-00805f9b34fb
```

这样提示符变成了这样

```
[HONOR V30 PRO:/service0028/char0029]# 
```



参考资料

1、



