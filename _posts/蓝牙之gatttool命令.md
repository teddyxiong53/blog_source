---
title: 蓝牙之gatttool命令
date: 2021-02-27 14:10:30
tags:
- 蓝牙
---

--

hcitool是wield对设备连接进行管理。

gatttool则是对ble进行各种细致操作。

gatttool用法分为两种：

1、直接带参数执行。

2、交互模式。

gatttool查看帮助信息

```
gatttool -help-gatt
	查看gatt相关的选项。
	有这些：
		--primary 发现primary服务。
		--characteristics 发现特征。
		--char-read 特征值读操作。
		--char-write 
		--char-desc 特征值描述符发现。
		--listen 监听通知。
		-I 交互模式
```

```
gatttool --help-params	
	查看参数相关的选项。
	-s 开始handle，默认从0x0001开始。
	-e 结束handle，默认为0xffff
	-u，指定uuid
```

```
gatttool --help-char-read-write  
	特征值读写相关参数。
	-a 通过特征值handle来读写
	-n 写特征值。
```



gatttool的参数主要有：

```
-i 指定蓝牙的hci接口，一般是hci0。机器上只有一个蓝牙设备则不需要指定。
-b：在连接多个ble设备的前提下，指定其中一个蓝牙设备的地之后。
-t：指定自己的地址类型，是public还是private。默认public。
-m：设备mtu的大小。
-l：指定安全级别。默认是low。
-I：进入交互模式。
```

长选项有：

```
--primary 寻找ble可用的服务。
	举例：gatttool -b 
```



gatttool这个工具已经过时了。很快会被bluetoothctl命令替换。



参考资料

1、

