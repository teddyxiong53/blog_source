---
title: btstack（3）其他例子分析
date: 2018-12-20 14:21:35
tags:
	- 蓝牙
---



# gap_inqury

扫描附近的蓝牙热点。

很简单。

```
pi@raspberrypi:~/work/bt/btstack-master/port/raspi$ sudo ./gap_inquiry 
Packet Log: /tmp/hci_dump.pklg
Hardware UART without flowcontrol, 921600 baud, H5, BT_REG_EN at GPIOO 128
Phase 1: Download firmware
Phase 2: Main app
BTstack up and running at B8:27:EB:AA:E4:60
Starting inquiry scan..
Device found: 64:A2:F9:1F:12:2B with COD: 0x5a020c, pageScan 1, clock offset 0x25f0, rssi -75 dBm, name 'OnePlus 6'
Device found: F4:4E:FD:4F:64:EB with COD: 0x240404, pageScan 1, clock offset 0x7d71, rssi -63 dBm, name 'smart_si_FD4F64EB'
Device found: 08:EB:ED:34:82:B2 with COD: 0x240404, pageScan 1, clock offset 0x1b51, rssi -85 dBm, name 'SoundBox Pro'
Device found: 48:2C:A0:3E:28:5E with COD: 0x5a020c, pageScan 1, clock offset 0x696c, rssi -91 dBm, name '小米手机'
Device found: AC:C1:EE:1D:C0:CD with COD: 0x5a020c, pageScan 1, clock offset 0x7750, rssi -86 dBm, name '红米手机'
Device found: 08:EB:ED:9E:57:47 with COD: 0x240404, pageScan 1, clock offset 0x7566, rssi -83 dBm, name 'SoundBox Pro'
Device found: B4:0B:44:F4:16:8D with COD: 0x5a020c, pageScan 1, clock offset 0x707d, rssi -42 dBm, name 'xhl_bt'
Device found: EC:51:BC:A8:02:8E with COD: 0x5a020c, pageScan 1, clock offset 0x13fa, rssi -89 dBm, name 'OPPO R11s'
Device found: 18:F0:E4:E9:B6:56 with COD: 0x5a020c, pageScan 1, clock offset 0x5e5f, rssi -85 dBm, name '小米手机'
Device found: 34:D7:12:92:1A:B0 with COD: 0x5a020c, pageScan 1, clock offset 0x04a3, rssi -86 dBm, name '坚果 Pro 2'
```

# gap_le_advertisements

这个就是把收到的ble广告打印出来。



# gap_link_keys

把存储的key打印出来。我这个当前没有key 。

```
pi@raspberrypi:~/work/bt/btstack-master/port/raspi$ sudo ./gap_link_keys 
Packet Log: /tmp/hci_dump.pklg
Hardware UART without flowcontrol, 921600 baud, H5, BT_REG_EN at GPIOO 128
Phase 1: Download firmware
Phase 2: Main app
BTstack up and running at B8:27:EB:AA:E4:60
Stored link keys: 
.
```

# gatt_battery_service

搜索附近的提供电池查询服务的设备。

# gatt_browser

演示client的写法。

# le_streamer

这个需要手机上安装lightblue。或者另外用电脑跑le_streamer_client来配合做实验。

