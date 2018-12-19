---
title: 蓝牙之uuid
date: 2018-12-13 17:18:35
tags:
	- 蓝牙
typora-root-url:../
---



每个设备可以包含多个service，每个service对应一个uuid。

概念的层次关系：

```
profile：规范
	service：服务
		characteristic：特征值
```

service和characteristic都需要用uuid来进行标识。

![](/images/蓝牙概念层次.png)

耳机不适合用ble，因为ble适合在数据量非常小的。而耳机的数据量很大。



主机和从机的通信都是通过characteristic来实现。



蓝牙规范执行了两种uuid：

1、基本的uuid。

2、16bit的uuid。（是uuid的简略写法）



有一个共用的基本uuid

```
0x0000xxxx-0000-1000-8000-00805F9B34FB
```

上面这个xxxx，就是16bit的uuid。

例如心率测量就是：2A37，那么完整的就是：

```
0x00002A37-0000-1000-8000-00805F9B34FB
```

对应蓝牙的属性，16bit足够用了。

基本uuid不能用于任何基本定制的属性、服务和特性。

对于定制的uuid，必须使用完整的128位的uuid。



字符串长度是36。32个是数字，4个是“-”。

8-4-4-4-12 。



蓝牙4.0是以参数来进行数据传输的。

就是说，服务端定义好一个参数，客户端可以对这个参数进行读、写、通知操作。

这个参数，在蓝牙里有个术语，叫特征值。

对特征值进行分类，一组特征值就是一个服务。

每个特征值有属性：

```
长度
权限
值
描述
```



蓝牙4.0引入了2个核心协议ATT和GATT。

主要是为了ble的，但是传统蓝牙也可以用。



在开发中我们需要获取设备的UUID字段，可以询问硬件工程师，也可以通过蓝牙测试工具查看service UUID 和

characteristic UUID。



# 定义uuid

可以自定义uuid。有什么约束吗？

按格式来就行了。

service的uuid。可以理解为tcp协议栈里的端口号。

例如80默认是提供http服务的，但是你只要客户端和服务端约定好，用其他的端口号也完全没有问题。



# 常用的uuid

我们只看16bit的。

```
var uuids = {
    "0001": "SDP",
    "0003": "RFCOMM",
    "0005": "TCS-BIN",
    "0007": "ATT",
    "0008": "OBEX",
    "000f": "BNEP",
    "0010": "UPNP",
    "0011": "HIDP",
    "0012": "Hardcopy Control Channel",
    "0014": "Hardcopy Data Channel",
    "0016": "Hardcopy Notification",
后面省略了，太多了。
```



# uuid换算

128位的和16位、32位的可以有公式进行换算。



# 参考资料

1、对Android蓝牙UUID的理解

http://dxjia.cn/2016/01/29/android-bluetooth-uuid/

2、蓝牙UUID编码

https://blog.csdn.net/qq_37389133/article/details/79412836

3、蓝牙概念

http://www.cnblogs.com/hshy/p/8268025.html

4、通用属性配置文件（GATT）及其服务，特性与属性介绍

http://blog.chinaunix.net/uid-21411227-id-5750680.html

5、各种通用蓝牙UUID列表

https://blog.csdn.net/qq_15003505/article/details/75315049

6、

https://blog.csdn.net/andry05/article/details/81118383

7、蓝牙UUID及其128位换算

https://blog.csdn.net/zhangjs0322/article/details/39048509

8、【BLE-CC2640】CC2640之使用自定义128bit的UUID

http://www.voidcn.com/article/p-vuyeyimy-eo.html

