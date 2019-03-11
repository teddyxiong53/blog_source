---
title: 蓝牙之mtu
date: 2019-03-11 09:54:11
tags:
	- 蓝牙

---





MTU是不可协商的。双方在获知对方的mtu后，用较小值做MTU进行通信。

ble的mtu是23个字节。

ble的完整包的构成是这样：

```
引导 | 访问地址 |  LL头 | Data       |  CRC |
1字节   4字节      2字节  0到255字节    3字节
```

Data这个部分的长度，跟蓝牙的版本有关系。

在4.0和4.1上面，Data的值是27字节。

在4.2上面，增加了新的特性。

对Data部分进一步分解，分为2部分：

```
L2CAP Header |   ATT Data
4字节               0到251字节
```

L2CAP头部固定为4字节。里面包含了分片和重组信息。靠这个头部信息支持，上层的包最大可以到64KB。

这4个字节，又分为2部分：

2个自己的长度。

2个字节的Channel id。



iPhone6和iPhone6s的ATT_MTU是185字节。



给gatt的，是20字节。

因为23字节里，一个字节的ATT操作码。2个字节的ATT handle。





参考资料

1、一分钟读懂低功耗蓝牙(BLE)MTU交换数据包

https://zhuanlan.zhihu.com/p/28141658

2、Maximizing BLE Throughput Part 2: Use Larger ATT MTU

https://punchthrough.com/pt-blog-post/maximizing-ble-throughput-part-2-use-larger-att-mtu/

3、Logical Link Control and Adaptation Layer Protocol (L2CAP)

http://dev.ti.com/tirex/content/simplelink_cc2640r2_sdk_1_35_00_33/docs/ble5stack/ble_user_guide/html/ble-stack/l2cap.html

4、

https://www.bbsmax.com/A/RnJWrvoBzq/