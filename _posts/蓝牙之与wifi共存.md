---
title: 蓝牙之与wifi共存
date: 2020-06-22 10:33:49
tags:
	- 蓝牙

---

1

看rk3308的启动时，有这样的打印：

```
Jan  1 08:00:13 rockchip user.info kernel: [   13.795964] rtk_btcoex: Open BTCOEX
Jan  1 08:00:13 rockchip user.info kernel: [   13.796031] rtk_btcoex: create_udpsocket: connect_port: 30001
Jan  1 08:00:13 rockchip user.info kernel: [   13.796100] rtk_btcoex: send msg INVITE_REQ with len:11
Jan  1 08:00:13 rockchip user.info kernel: [   13.798746] rtk_btcoex: BTCOEX hci_rev 0xaa89
Jan  1 08:00:13 rockchip user.info kernel: [   13.798800] rtk_btcoex: BTCOEX lmp_subver 0x7e1b
```

rtk_btcoex这个是什么意思？

搜索了一下，发现coex是coexist的缩写。表示共存。

这个表示wifi和蓝牙的共存功能。

需要这个功能，是因为单芯片的wifi蓝牙，二者共用了天线。

这就需要wifi和蓝牙通过一定的机制来合理共用天线。

共存机制的原理，是一个比较简单的机制：WiFi监听BT的工作状态，根据BT的工作状态来切换自己使用射频天线的时隙。



参考资料

1、Android平台上的WiFi BT共存机制

https://www.cnblogs.com/hunaiquan/p/5416105.html