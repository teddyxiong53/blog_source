---
title: vpn（一）基本概念
date: 2018-04-20 09:54:37
tags:
	- vpn

---



# 定义

vpn，虚拟专用网络。Virtual Private Network。

用来在公网上搭建专用网络，进行加密通信，一般是在 企业里使用。

vpn可以通过服务器、硬件、软件等多种方式进行实现。

# 使用场景

最常见的就是公司员工在外面出差，想要访问公司的内网，就需要通过vpn来访问。

传统的做法是租用DDN（数字数据网）专线或帧中继。这样很贵。

# 工作原理

一个通俗的比喻就是马路上的公交专线。

由于公共ip的短缺，我们在组建局域网的时候，通常使用保留地址作为内部ip。

这些保留地址是无法在Internet上被路由的。

所以正常情况下，我们无法直接通过Internet访问到局域网里的主机。

但是有时候，我们有这样的需求，这就要用到vpn技术。

一般vpn网关采用双网卡的结构，外网卡使用公共ip接入到internet。

# vpn和ssr的区别

1、vpn走的是专用通道，它是用来给企业传输加密数据的，所以vpn的流量特征很明显。所以现在pptp类型的vpn基本都被封死了。l2tp的也被干扰很严重。

2、ssr的流量特征不明显。检测没有那么容易。



# 分类标准

## 按vpn协议分

vpn的隧道协议主要有3种，pptp、l2tp、ipsec。

pptp和l2tp工作的二层。所以也叫二层隧道协议。

ipsec工作在三层，所以也叫三层隧道协议。

## 按vpn的应用分

1、Access VPN。

2、Intranet VPN。

3、Extranet VPN。

## 按所用的设备类型分

1、路由器式vpn。

2、交换机式vpn。

3、防火墙式vpn。这种最常见。

## 按实现原理分

1、重叠vpn。

2、对等vpn。

# 实现方式

1、vpn服务器。在大型局域网里。

2、软件vpn。

3、硬件vpn。

4、集成vpn 。

# 常用vpn技术

1、MPLS VPN。基于MPLS技术的VPN。

2、SSL VPN。基于https的vpn技术。

3、ipsec VPN。



# 分析一下pptp

pptp是点到点隧道协议。

使用一个tcp连接对隧道进行维护。

使用通用路由封装（GRE）技术，把数据封装成PPP数据，通过隧道传送。

可以对PPP帧里的 数据进行压缩或者加密。





# 参考资料

1、百度百科

https://baike.baidu.com/item/虚拟专用网络/8747869?fr=aladdin&fromid=382304&fromtitle=VPN

2、vpn搭建以及pptp原理

http://blog.51cto.com/runningyongboy/1719715

3、vpn工作原理

https://wenku.baidu.com/view/6698d3e714791711cd79177e.html?from=search