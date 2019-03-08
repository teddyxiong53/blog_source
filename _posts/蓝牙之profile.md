---
title: 蓝牙之profile
date: 2018-11-27 16:08:35
tags:
	- 蓝牙

---



蓝牙有4种基本的profile，分别是：

1、GAP。Generic Access Profile。这种profile保证不同的的蓝牙产品之间可以发现和连接对方。

2、SDAP。Service Discovery Application Profile。可以找到其他蓝牙设备提供的服务。

3、SPP。Serial Port Profile。模拟串口协议。

4、GOEP。Generic Object Exchange Profile。通用对象交换协议。

有9种应用层协议。

1、无线电话。

2、对讲。

3、耳机。

4、拨号。

5、传真。

6、使用PPP协议建立局域网。

7、设备之间对象传输。

8、FTP协议。

9、同步。



蓝牙当前一共有22种profile。



为什么有这么多的profile？

因为存在不同的工作组，他们各自为战，只关注自己的特定问题。

可以看做是康威定律在起作用。

蓝牙协议的开发是，很多公司开发，最后由标准组织来认定。

随着时间的推移，很多不合时宜的profile会被淘汰掉。



profile和协议的关系是什么？

一个profile具体说明了一个或者多个协议怎样实现功能。

例如GAP这个profile，主要是说明如何发现设备和建立连接。

主要使用了HCI协议。



参考资料

1、树莓派之蓝牙编程

https://blog.csdn.net/qq_25005909/article/details/77512903

2、Linux下Bluez的编程实现

这篇文章非常全面。

https://www.cnblogs.com/chenbin7/archive/2012/10/16/2726510.html

3、对于蓝牙Profile的理解

这个思考确实有见地。

https://www.jianshu.com/p/f96a871c9ebc