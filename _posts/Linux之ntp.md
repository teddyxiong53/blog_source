---
title: Linux之ntp
date: 2018-07-23 09:38:53
tags:
	- Linux

---



为了避免Linux长时间运行后，时间不同步。所以需要ntp服务来进行时间同步。

# ntp和sntp关系

NTP（Network Time Protocol）和 SNTP（Simple Network Time Protocol）是两种用于网络时间同步的协议，它们之间有一定的关系。

NTP 是一种用于分布式网络环境中的时间同步协议。它通过在计算机之间传输时间信息，使得网络中的所有计算机都能够以高精度和一致性的方式保持时间同步。NTP 在网络中建立一个时间服务器和时间客户端的体系结构，时间服务器负责提供准确的时间信息，而时间客户端通过与时间服务器通信来同步本地时间。

**SNTP 是 NTP 的一个简化版本，它更加轻量级且易于实现。**SNTP 的目标是提供一种简单的时间同步解决方案，适用于资源受限的设备或特定应用场景。相对于 NTP，SNTP 省略了一些复杂的功能和算法，仅提供基本的时间同步功能。

**NTP 和 SNTP 的关系可以理解为 SNTP 是 NTP 的子集。**SNTP 基本上采用了 NTP 的核心机制和数据包格式，但在协议功能和精度方面进行了简化。SNTP 可以作为 NTP 的替代方案，特别适用于一些对时间同步要求不高、资源受限或需要简单实现的场景。

总结起来，NTP 是一种功能丰富的网络时间同步协议，而 SNTP 是 NTP 的简化版本，适用于对时间同步要求不高的场景。

# 参考资料

1、Linux的NTP配置总结

https://blog.csdn.net/xuleisdjn/article/details/78459835