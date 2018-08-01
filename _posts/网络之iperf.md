---
title: 网络之iperf
date: 2018-07-31 09:28:29
tags:
	- 网络

---



用iperf2的，iperf3和iperf2不兼容。

配置。

```
./configure --host=arm  CXX=arm-linux-gnueabihf-g++ CC=arm-linux-gnueabihf-gcc --prefix=/home/hlxiong/tools/install/iperf2_32
```

然后make和make install就好了。



常用命令：

服务端：

```
iperf -s -i 1
```

客户端：

```
iperf -c 192.168.0.100 -i 1 -t 30
```



#参考资料

