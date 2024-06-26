---
title: 蓝牙之mtu
date: 2019-03-11 09:54:11
tags:
	- 蓝牙

---

--

蓝牙的MTU（Maximum Transmission Unit）是指在蓝牙通信中每次数据传输的最大字节数。MTU的大小对于蓝牙通信的性能和效率具有重要影响，因为它决定了一次数据传输的大小，从而影响了数据传输的速率和稳定性。

在蓝牙通信中，MTU的大小通常由蓝牙协议栈或操作系统决定，并且可能因设备和配置而有所不同。

通常情况下，

==蓝牙传统模式（BR/EDR）下的MTU大小为672字节，==

==而蓝牙低功耗模式（BLE）下的MTU大小通常在20到512字节之间，==

具体取决于设备和协议栈的支持情况。

MTU的大小对于蓝牙通信有以下影响：
1. **数据传输效率**：较大的MTU可以减少通信开销，提高数据传输效率。
2. **延迟**：较大的MTU通常会降低传输数据的延迟，因为每次传输的数据量更大。
3. **内存消耗**：较大的MTU可能需要更多的内存来缓存数据，特别是在接收端。
4. **稳定性**：过大的MTU可能会增加数据传输的丢包率，特别是在信号弱或干扰严重的环境中。

因此，在进行蓝牙开发时，需要根据具体的应用场景和要求来合理设置MTU大小，以确保通信性能和稳定性。



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



蓝牙mtu和其他网络的mtu情况对比

```
以太网：1500

IEEE 802.3/802.2:　1492

X.25: 576

BLE: 23 => 这就是为什么WIFI 可以用于传输视频，传统蓝牙(BT)可以传输音频，而低功耗蓝牙（BTLE 或者BLE）只能够传输控制数据的原因了。
```



# 参考资料

1、一分钟读懂低功耗蓝牙(BLE)MTU交换数据包

https://zhuanlan.zhihu.com/p/28141658

2、Maximizing BLE Throughput Part 2: Use Larger ATT MTU

https://punchthrough.com/pt-blog-post/maximizing-ble-throughput-part-2-use-larger-att-mtu/

3、Logical Link Control and Adaptation Layer Protocol (L2CAP)

http://dev.ti.com/tirex/content/simplelink_cc2640r2_sdk_1_35_00_33/docs/ble5stack/ble_user_guide/html/ble-stack/l2cap.html

4、

https://www.bbsmax.com/A/RnJWrvoBzq/

5、一分钟读懂低功耗蓝牙(BLE)MTU交换数据包

https://zhuanlan.zhihu.com/p/28141658