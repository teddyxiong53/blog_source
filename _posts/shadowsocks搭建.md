---
title: shadowsocks搭建
date: 2017-06-29 22:12:30
tags:

	- 翻墙

---

都说现在shadowsocks是很好的翻墙方式。那么必须学习一下。

shadowsocks的优点：

* 耗电很低。
* 支持开机自启动，断网没有影响。
* 可以使用自己的服务器。
* 支持区分国内外流量。
* 无需root

翻墙的感觉会达到无缝的感觉。

搭建ss需要一个vps。vps是Virtual Private Server的缩写。就相当于你买了一台服务器，放在国外，你可以随时通过你自己的这台服务器访问墙外的世界。

有三家vps商家可以选择：

DigitalOcean。30块一个月。有点贵。

搬瓦工BandWagon。11元一个月。可以考虑。可以支付宝支付。就选择这个了。

看看选择哪种主机呢？

就选择中国直连特惠主机，只有洛杉矶节点。

内存512M、硬盘10G、流量1000GB每月。

```
Basic VPS - Self-managed - SPECIAL 10G KVM PROMO V3 - LOS ANGELES - CHINA DIRECT ROUTE
SSD: 10 GB RAID-10
RAM: 512 MB
CPU: 1x Intel Xeon
Transfer: 1000 GB/mo
Link speed: 1 Gigabit
```

搬瓦工各节点测试IP：

Los Angeles：   104.194.78.3

Florida：       74.121.150.3

Phoenix：       198.35.46.2（可在控制面板里切换到这个机房）

我只能ping同洛杉矶那个。



买好账号后，打开

[https://bwh1.net/clientarea.php?action=products](https://bwh1.net/clientarea.php?action=products)

这个网址。登陆。



由于搬瓦工VPS后台控制面板集成了一键安装Shadowsocks服务，所以特别适合第一次尝试搭建Shadowsocks服务器的新手，很简单便捷。

安装好centos之后，用secureCRT登陆到这个系统上。

安装一些软件。





