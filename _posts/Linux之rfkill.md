---
title: Linux之rfkill
date: 2018-10-23 21:46:14
tags:
	- Linux

---

1

很多计算机系统包含无线电传输，例如wifi、蓝牙、sim卡这些。

这些无线电设备消耗不少的能源，所以有必要在不使用的时候关闭掉。

怎样进行关闭呢？

Linux内核提供了rfkill这个内核子系统。

它提供了一个接口，在这个接口里，可以查询、激活或者关闭无线电传输。

关闭有两种：一种是软锁定，一种是硬锁定。

软锁定是软件可以重新激活。硬锁定是软件无法激活。

rfkill接口位于/dev/rfkill。其中包含了系统中所有无线电传输的当前状态。

每个设备都在sysfs里注册了当前rfkill状态。

每当设备的状态发生变化，都会反映到sysfs下的uevent节点。





rf代表的是Radio Frequency。射频。

对应的设备节点：

```
# ls /dev/rfkill -lh
crw-rw-r--    1 root     root       10,  63 Jan 20 03:50 /dev/rfkill
```

是一个misc device。



#常用命令

##列出设备

```
# rfkill list
0: bt_default: Bluetooth
        Soft blocked: no
        Hard blocked: no
1: phy0: Wireless LAN
        Soft blocked: no
        Hard blocked: no
2: brcmfmac-wifi: Wireless LAN
        Soft blocked: no
        Hard blocked: no
```

## 开关设备



```
# rfkill block 0
[  369.549507] [BT_RFKILL]: bt shut off power
# 
# rfkill unblock 0
[  374.920819] [BT_RFKILL]: rfkill_rk_set_power: set bt wake_host pin output high!
[  374.983559] [BT_RFKILL]: rfkill_rk_set_power: set bt wake_host pin input!
[  374.983646] [BT_RFKILL]: ENABLE UART_RTS
[  375.084530] [BT_RFKILL]: DISABLE UART_RTS
[  375.084661] [BT_RFKILL]: bt turn on power
```

也可以开关某一类设备：

```
rkfill block wifi
```

还可以关闭所有设备：

```
rfkill block all
```



在buildroot里的位置是，system tools -- util linux。

是busybox里的，代码在miscutils/rfkill.c里。这个是独立的一个可执行文件，不是busybox的链接。

看看rfkill代码逻辑：

```
1、检查参数，可以有0、1、2个参数。
2、rf_fd = device_open("/dev/rfkill", mode);
	打开这个设备文件。
3、full_read(rf_fd, &event, sizeof(event))
	读取内容。event的类型是：rfkill_event
4、config_open2(rf_sysfs, fopen_for_read);
	打开sysfs下的uevent节点。/sys/class/rfkill/rfkill%u/uevent
	
```



```
/oem # rfkill                               
ID TYPE      DEVICE          SOFT      HARD 
 0 bluetooth bt_default unblocked unblocked 
 1 wlan      phy0       unblocked unblocked 
 2 wlan      phy1       unblocked unblocked 
 3 bluetooth hci0       unblocked unblocked 
/oem #                                      
/oem # ls /sys/class/rfkill/                
rfkill0  rfkill1  rfkill2  rfkill3          
```



```
The rfkill subsystem has two parameters, rfkill.default_state and
rfkill.master_switch_mode, which are documented in kernel-parameters.txt.
```

rfkill在内核里的代码是kernel/net/rfkill。

这个目录下文件有这些：

```
├── core.c
├── input.c
├── Kconfig
├── Makefile
├── modules.builtin
├── modules.order
├── rfkill-bt.c
├── rfkill-gpio.c
├── rfkill.h
├── rfkill-regulator.c
└── rfkill-wlan.c
```

include/uapi/linux/rfkill.h

```
enum rfkill_type {
	RFKILL_TYPE_ALL = 0,
	RFKILL_TYPE_WLAN,
	RFKILL_TYPE_BLUETOOTH,
	RFKILL_TYPE_UWB,
	RFKILL_TYPE_WIMAX,
	RFKILL_TYPE_WWAN,
	RFKILL_TYPE_GPS,
	RFKILL_TYPE_FM,
	RFKILL_TYPE_NFC,
	NUM_RFKILL_TYPES,
};
```

本质上，是通过一些gpio控制无线模块的电源。

```
struct rfkill_rk_platform_data {
    char                    *name;
    enum rfkill_type        type;
    bool                    power_toggle;
    struct pinctrl          *pinctrl;
    struct rfkill_rk_gpio   poweron_gpio;
    struct rfkill_rk_gpio   reset_gpio;
    struct rfkill_rk_gpio   wake_gpio;      // Host wake or sleep BT
    struct rfkill_rk_irq    wake_host_irq;  // BT wakeup host
    struct rfkill_rk_gpio   rts_gpio;
    struct clk              *ext_clk;
};
```



```
	struct delayed_work	poll_work;
	struct work_struct	uevent_work;
	struct work_struct	sync_work;
```



下面这个命令，是如何被内核处理的呢？

```
echo 0 > /sys/class/rfkill/rfkill0/state
```



# 参考资料

1、在 Linux 下使用 rfkill 软开关蓝牙及无线功能 

https://linux.cn/article-5957-1.html

2、在 Linux 下使用 rfkill 软开关蓝牙及无线功能

https://www.linuxidc.com/Linux/2015-08/121119.htm

3、

https://www.whatled.com/post-1335.html

4、Linux内Documentation下的rfkill.txt

5、Documentation/ABI/stable/sysfs-class-rfkill