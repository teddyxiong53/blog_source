---
title: avs之namespace层次关系
date: 2019-04-15 10:29:28
tags:
	 - avs

---





make doc，得到一个html目录。看看里面的内容。

从index.html开始看。

我觉得业务关系最核心的是：3A。

acl、adsl、afml。

通信、指令排序、焦点管理。

看Class标签。



avsCommon这个namespace下面内容比较多。

分析一下。

```
avsCommon
	sdkInterfaces
		audio
			一个总的接口：里面包含了3个子接口。闹钟、电话、通知。
		bluetooth
			1、蓝牙设备接口。就是用来打开、关闭、连接这些函数。
				对应的实现类是：BlueZBluetoothDevice
			2、蓝牙在主控接口。
				scan函数。
				对应的实现是：BlueZHostController。
			3、设备管理接口。
				就是对蓝牙设备和蓝牙主控进行封装。
		storage
			只有一个misc。其他的哪些放在哪里去了？
			这个是存储键值对的，存放了token。
			其他的storage interface放在capabilityAgents各自的目录下了。
			
		一大堆的XXXInterface类。
		
```



 参考资料

1、

