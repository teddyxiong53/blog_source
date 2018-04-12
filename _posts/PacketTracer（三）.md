---
title: PacketTracer（三）
date: 2018-04-12 15:58:49
tags:
	- PacketTracer
typora-root-url: ..\
---



# vpn

除了用来科学上网，vpn在企业的主要用途是用来让总部和分公司的私有ip地址可以直接访问。

![](/images/PacketTracer（三）-vpn.png)

配置模拟Internet的路由器。

```
Router(config)#interface FastEthernet0/0
Router(config-if)#ip address 100.0.0.1 255.255.255.0
Router(config-if)#no shutdown //打开网卡

Router(config)#interface fastEthernet 0/1
Router(config-if)#ip address 200.0.0.1 255.255.255.0
Router(config-if)#no shutdown 
```

配置总公司的路由器。

```
Router(config)#crypto isakmp policy 1
Router(config-isakmp)#
Router(config-isakmp)#hash md5 
Router(config-isakmp)#authentication pre-share 
Router(config-isakmp)#exit
Router(config)#crypto isakmp key example address 200.1.1.2 //设置远端对等体的共享秘钥为example这个单词。

```





# 参考资料

1、

https://wenku.baidu.com/view/830d7480bceb19e8b8f6bae4.html