---
title: 蓝牙之hciconfig
date: 2018-11-27 16:36:35
tags:
	- 蓝牙

---



bluez协议栈在安装完成后，会提供2个工具。

hcitool和gattool。

使用工具的前提是以root方式运行。

首先是查看当前有的蓝牙设备。

hciconfig，类似ifconfig。只是操作对象不是网卡，而是蓝牙设备而已。



```
root@raspberrypi:~# hciconfig 
hci0:   Type: BR/EDR  Bus: UART
        BD Address: B8:27:EB:AA:E4:60  ACL MTU: 1021:8  SCO MTU: 64:1
        UP RUNNING PSCAN 
        RX bytes:42850 acl:96 sco:0 events:805 errors:0
        TX bytes:8222 acl:96 sco:0 commands:208 errors:0
```

打开和关闭。

```
hciconfig hci0 down
hciconfig hci0 up
```

打开蓝牙设备后，就可以使用hcitool工具集对蓝牙进行控制。

工具集分为2部分，一个传统蓝牙的，一个是ble的。



# 代码分析

hciconfig.c

```
ctl = socket(AF_BLUETOOTH, SOCK_RAW, BTPROTO_HCI)//打开一个蓝牙的socket。
//如果没有带参数，那么就调用print_dev_list(ctl, 0);打印修改信息。

//通过ioctl进行查询。这宏在内核里定义的。
ioctl(ctl, HCIGETDEVLIST, (void *) dl)
//然后循环
ioctl(ctl, HCIGETDEVINFO, (void *) &di) 
```

蓝牙驱动是怎么实现HCIGETDEVLIST这些的呢？

在kernel/net/bluetooth/hci_sock.c里有：

```
	switch (cmd) {
	case HCIGETDEVLIST:
		return hci_get_dev_list(argp);
```

肯定是有地方调用了hci_register_dev这个来注册蓝牙设备。

蓝牙的驱动就是在./drivers/bluetooth目录下。



看当前rk3308的，蓝牙相关的内核宏是怎样配置的。

```
CONFIG_BT_BREDR=y
CONFIG_BT_RFCOMM=y
CONFIG_BT_RFCOMM_TTY=y
# CONFIG_BT_BNEP is not set
CONFIG_BT_HIDP=y
CONFIG_BT_HS=y
CONFIG_BT_LE=y
# CONFIG_BT_SELFTEST is not
CONFIG_BT_DEBUGFS=y
# CONFIG_BT_HCIBTSDIO is no
# CONFIG_BT_HCIUART is not 
# CONFIG_BT_HCIVHCI is not 
# CONFIG_BT_MRVL is not set

```

/sys/kernel/debug/bluetooth 内核调试文件系统。

目前看drivers/bluetooth这个目录下，rk3308的没有编译。

因为它是用rtl8723ds，这个是蓝牙wifi一体的。单独的驱动。

kernel/drivers/net/wireless/rockchip_wlan

但是这个目录下搜索不到hci_register_dev的调用。

./external/rkwifibt/realtek/bluetooth_uart_driver/rtk_coex.c

这里注册了。

```
hlxiong@hlxiong-VirtualBox:~/work2/rk3308_no_modify/external/rkwifibt/realtek/bluetooth_uart_driver$ grep -nwr "hci_register_dev" .
./hci_ldisc.c:607:      if (hci_register_dev(hdev) < 0) {
```



```
rtk_hciattach -n -s 115200 /dev/ttyS4 rtk_h5
```

