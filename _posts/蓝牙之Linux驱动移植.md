---
title: 蓝牙之Linux驱动移植
date: 2018-11-28 10:04:28
tags:
	- 蓝牙
typora-root-url: ..\
---

1

内核里的蓝牙代码在net/bluetooth目录下。目录下47个文件。

同一层目录下还有：wireless、Ethernet、netlink。



入口文件是af_Bluetooth.c。

```
subsys_initcall(bt_init);
	debugfs_create_dir//注册debugfs
	bt_sysfs_init// /sys/class/bluetooth
	sock_register(&bt_sock_family_ops);//注册蓝牙类型的socket，这样就可以创建蓝牙的socket了。
	hci_sock_init//接下来就是蓝牙从底层的hci到上层依次进行初始化。
	l2cap_init
	sco_init
	mgmt_init
```

sys目录下的情况是这样：

```
# ls
address    name       rfkill3    type
device     power      subsystem  uevent
# pwd
/sys/class/bluetooth/hci0
# cat name 
RTK_BT_4.1
# cat type 
BR/EDR
```

```
# ls -lh
-r--r--r--    1 root     root        4.0K Mar 17 17:29 claim
lrwxrwxrwx    1 root     root           0 Mar 17 17:29 device -> ../../hci0
-r--r--r--    1 root     root        4.0K Mar 17 17:29 hard
-r--r--r--    1 root     root        4.0K Mar 17 17:29 index
-r--r--r--    1 root     root        4.0K Mar 17 17:29 name
-r--r--r--    1 root     root        4.0K Mar 17 17:29 persistent
drwxr-xr-x    2 root     root           0 Mar 17 17:29 power
-rw-r--r--    1 root     root        4.0K Mar 17 17:29 soft
-rw-r--r--    1 root     root        4.0K Mar 17 17:29 state
lrwxrwxrwx    1 root     root           0 Mar 17 17:29 subsystem -> ../../../../../../../class/rfkill
-r--r--r--    1 root     root        4.0K Mar 17 17:29 type
-rw-r--r--    1 root     root        4.0K Jan  1  1970 uevent
# pwd
/sys/class/bluetooth/hci0/rfkill3
# cat claim 
0
# cat hard 
0
# cat index 
3
# cat name 
hci0
# cat persistent 
0
# cat soft 
0
# cat state 
1
# cat type 
bluetooth
```





参考资料

1、Linux下的USB蓝牙适配器驱动

https://www.linuxidc.com/Linux/2010-08/28127.htm

2、linux 蓝牙驱动移植

http://www.voidcn.com/article/p-bdlwsxna-ry.html