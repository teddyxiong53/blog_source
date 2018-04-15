---
title: openwrt（十四）netifd
date: 2018-04-13 23:02:19
tags:
	- openwrt

---



# 什么是netifd

netifd是openwrt里进行网络配置的守护进程。

基本上所有的网络接口设置和内核的netlink事件都可以由netifd来完成。

在启动netifd之前，用户要把配置写入到/etc/config/network里。

# netifd基本框架

我们配置一个网络接口，一般都要完成3种工作：

1、mac地址、mtu、速率协商。这些属于二层属性（OSI模型）。这些都是直接操作实际网络设备的。

2、ip地址、路由。这些三层属性。

3、特定的接入方式。例如静态ip、dhcp、pppoe。

所以层次关系是这样的：

```
---------------------------------
协议处理层：dhcp PPPoE
---------------------------------
接口层：lan wan（三层）
---------------------------------
device层：br-lan  eth0（二层）
---------------------------------
```

作为路由器的使用者，我们只关心配置interface层的哪个接口（lan口，wan口）。以及配置成怎样的上网方式。

使用netifd配置网络，也是以interface为中心。

1、创建一个interface。

2、指明依赖的device。

3、绑定上网方式。





# 参考资料

1、OpenWrt netifd学习笔记

https://blog.csdn.net/jasonchen_gbd/article/details/74990247