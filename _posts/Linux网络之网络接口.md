---
title: Linux网络之网络接口
date: 2018-04-10 17:50:39
tags:
	- Linux网络

---



linux里网络接口分为两类：

1、物理接口。

包括eth0、radio0、wlan0这些。代表了实际存在的一个硬件。当对应的驱动被加载，就会出现对应的设备。

2、虚拟接口。

lo、eth0:1、eth0.1、vlan2、br0、pppoe-dsl、gre0、sit0、tun0、imq0、teql0。

这些都是虚拟网卡。虚拟网卡是为了给系统管理员最大的灵活度来对系统进行配置。

一个虚拟网卡往往是跟一个物理网卡绑定的。

虚拟网卡的分类：

1、别名。

```
eth4:5, eth4:6
这种名字是一种过时的用法，用来管理一个有多个地址的网卡。但是这个现在还是被支持的。
对应的文档在Documentation/networking/alias.txt里。
我们大概看看这个文档。
我们要给eth0插件一个别名。
ifconfig eth0:0 192.168.1.2 ...
route都是指向物理网卡的。所以这个对route没有影响。
要删除的话，就职这样：
ifconfig eth0:0 down
如果eth0被关闭了，eth0:0也会被关闭。
```

2、vlan。

```
vlan的名字是这样的：eth4.0, eth4.1 
把一个二层网络分割开来。
需要网卡支持802.1q协议。支持最多4096个vlan。12个bit。
```

3、堆叠的vlan。

```
这个是802.1ad支持的。配置方法是这样的：
ip link add link eth0 eth0.1000 type vlan proto 802.1ad id 100
ip link add link eth0.1000 eth0.1000.1000 type vlan proto 802.1q id 1000
```

4、网桥。

```
名字是这样的：br0, br-lan
用来连接多个物理网卡的。

```

5、隧道。tunnel interface。

```
名字是：pppeo-dsl、pppoa-dsl、tun0、vpn1

```

6、特殊用途。

```
名字是：imq0, teql3

```

上面有很多点，我还不清楚的，我单独写文章描述各个点的。



# 参考资料

1、Linux Network Interfaces

https://wiki.openwrt.org/doc/networking/network.interfaces