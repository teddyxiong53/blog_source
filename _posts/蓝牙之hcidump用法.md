---
title: 蓝牙之hcidump用法
date: 2020-05-14 15:05:35
tags:
	- 蓝牙

---

--

这个类似于tcpdump。

hcidump，就是命令行上抓取蓝牙数据包的工具。

直接运行hcidump，就可以。不用带参数。

默认是这样：

```
/ # hcidump
HCI sniffer - Bluetooth packet analyzer ver 5.50
device: hci0 snap_len: 1500 filter: 0xffffffffffffffff
```

默认使用hci0设备。抓包长度1500字节。

-w选项：抓到的内容写入到文件，而不是输入到控制台。

-t选项：显示时间戳。

-a选项：用ASCII码显示抓到数据。

-x选项：用16进制显示抓到的数据。

-X选项：同时用ASCII码和16进制显示抓到的数据。就用这个。

所以，最实用的一条命令是：

```
hcidump -X -t -w 1.txt
```

得到的1.txt文件，不能直接打开看，本质上是一个pcap文件，用wireshark打开看就可以。



一个小实验

1、执行：hcidump -X -t -w 1.txt

2、执行：sdptool browse。这个是扫描周围的蓝牙设备。

3、把1.txt拷贝到电脑上，用wireshark打开看看。





