---
title: Linux之rfkill
date: 2018-10-23 21:46:14
tags:
	- Linux

---



rfkill

用来使能和去使能无线设备的。

可以用来管理系统里的蓝牙和wifi。



rf代表的是Radio Frequency。射频。

对应的设备节点：

```
# ls /dev/rfkill -lh
crw-rw-r--    1 root     root       10,  63 Jan 20 03:50 /dev/rfkill
```



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



# 参考资料

1、在 Linux 下使用 rfkill 软开关蓝牙及无线功能 

https://linux.cn/article-5957-1.html