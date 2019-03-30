---
title: 蓝牙之Android BLE
date: 2018-12-17 20:41:08
tags:
	- 蓝牙

---



这个题目放了很久，一直没有写内容。现在看看。

蓝牙通信的4个主要任务：

1、设置蓝牙。

2、查找设备。

3、连接设备。

4、传输数据。

创建蓝牙连接需要的api有：

```
BluetoothAdapter
	表示本地蓝牙设备。
BluetoothDevice
	表示远端设备。
BluetoothSocket
BluetoothServerSocket
BluetoothClass
	表示蓝牙设备的一般特性和功能。
	只读属性。
BluetoothProfile
	
BluetoothHeadset
	蓝牙耳机支持。
BluetoothA2dp
	音频传输。
BluetoothHealth
	表示健康设备。
BluetoothHealthCallback
BluetoothHealthAppConfiguration
```



权限

```
android.permission.BLUETOOTH
android.permission.BLUETOOTH_ADMIN
```



参考资料

1、Android 蓝牙BLE开发详解

https://blog.csdn.net/kong_gu_you_lan/article/details/81009800

2、android.bluetooth

https://developer.android.com/reference/android/bluetooth/package-summary