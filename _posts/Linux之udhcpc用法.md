---
title: Linux之udhcpc用法
date: 2022-04-06 16:03:11
tags:
	- Linux

---

--

```
udhcpc -q -n -s /usr/share/udhcpc/default.script -i wlan0 2> /dev/null | grep "adding dns*" | awk '{print $3}'
```

上面这个命令是拿到dns server的ip地址。

default.script这个脚本，会监听dns事件。



udhcpc和dhcpcd比较

我觉得区别可能是：

udhcpc侧重于一次性执行的命令。

而dhcpcd则侧重于作为一个daemon后台一直运行。

二者可以同时使用。



整个udhcpc的框架是可执行文件udhcpc、脚本文件/usr/share/udhcpc/default.script、DNS配置文件/etc/resolv.conf。

入口是udhcpc，然后udhcpc调用shell脚本default.script中的deconfig/leasefail/bound/renew/nak等选项，resolv.conf存放DNS配置文件。



udhcpc遵循DHCP协议和DHCP服务器进行交互，通过状态机来解析从DHCP服务器获取的packet。



参考资料

1、

https://www.cnblogs.com/arnoldlu/p/13567937.html