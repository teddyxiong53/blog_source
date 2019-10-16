---
title: python之ipaddress模块
date: 2019-10-08 16:10:22
tags:		
	- python

---

1

罗列出一个网段里所有的ip地址

```
net = ipaddress.ip_network("192.168.56.0/24")
for ip in net:
	print(ip)
	
注意，必须是192.168.56.0，注意最后这个0 。如果写成其他数字，则错误。
因为结尾0为0，才代表网络。
但是这个可以通过另外一个参数来解决。
就是strict=False，这样就可以任意写一个ip地址。
```



ping一个255个地址的网络，耗时500s左右。大概8分钟。非常久。

我用20个线程来做。

用10个线程来做，时间就缩短到50s左右，的确是提高了10倍。

用50个线程，只需要13秒左右。

用75个线程，10秒左右。

200个线程，需要9秒。

100个线程。也是9秒左右。

所以75个线程差不多了。



现在扫描所有ip都可以了。

接下来就是进行http请求machine_name。



```
IPv4地址示例（CIDR表示法）：192.168.100.10/24
CIDR表示法可以是从 /8位 到 /30位的任何值，偶尔有 /32位（/31无效），但通常使用/24
IPv6地址示例：2001:db8:abcd:100::1/64
ipaddress模块是按照CIDR表示法设计的，由于其简洁易用，受到人们的推荐。
ipaddress模块还包含了一些方法，用于在必要的情况下还原子网掩码。
“主机”和“接口”之间的主要区别在于主机或ip_address对象不包含CIDR表示法，而ip_interface对象包含CIDR表示法：
处理不需要或不使用CIDR表示法的IP数据包时，ip_address对象最为有用。
当使用节点和接口标识来连接到必须包含网络/子网标识的IP网络时，ip_interface对象最管用。
ip_network对象包含网络中的所有地址，并且对于网络标识非常有用。
常用方法：
ipaddress.ip_address("192.168.0.10")
工厂方法，创建IPv4Address对象。特点是不带掩码。
参数可以是二进制的，也可以是十六进制的。
只有十六进制和字符串方式的有实用价值。

ipaddress.ip_interface("192.168.0.0/24")
工厂方法，创建IPv4Interface对象。
特点是带掩码。
```



参考资料

1、Python"ipaddress" 模块之概述

https://blog.csdn.net/j2iayu7y/article/details/80213273