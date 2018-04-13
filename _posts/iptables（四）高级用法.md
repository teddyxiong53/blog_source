---
title: iptables（四）高级用法
date: 2018-04-13 14:03:11
tags:
	- iptables
typora-root-url: ..\
---



# snat和dnat

snat、dnat、masquerade都是nat。

snat是指，往外发送数据的时候，把数据包里的src ip替换为指定ip，这样接收方就认为是指定ip发来的东西。

masquerade是指，用发送数据段网卡的ip来替换数据包src ip，从这个定义看，masquerade就是snat的特例。

在ip地址不固定的情况下，例如拨号网络或者dhcp分配ip，就要用masquerade。

dnat是指，数据包发送出去的时候，把dst ip修改为指定ip，你以为你访问的是A，实际上你访问的是B。

dnat是在prerouting的时候工作，snat是在postrouting的时候工作。

##应用举例

现在我们有一个公网ip：10.144.235.10 。

但是我们局域网里有3台电脑，希望通过snat的方式来联网。

应该怎么做？

网络拓扑如下：

![](/images/iptables（四）-snat实例.png)

要求：

1、访问10.144.235.10的8088端口，可以转发到pc1的80端口。



现在我们在路由器上添加下面这些规则：

```
iptables -t nat -A POSTROUTING -s 192.168.80.0/24 -j SNAT --to-source 10.144.235.10
```

如果eth0的ip不固定。可以这样。

```
iptables -t nat -A POSTROUTING -s 192.168.80.0/24 -o eth0 -j MASQUERADE
```

然后转发pc1的80端口到路由器的8088端口。

```
iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 8088 -j DNAT --to-destination 192.168.80.10:80
```



# redirect和dnat的区别

环境：wan（eth0），lan（eth1）

```
iptalbes -t nat -A PREROUTING -i eth1 -p tcp --dport 80 -j REDIRECT --to 3128
```

```
iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 80 -j DNAT --to 172.16.11.1:3128
```

```
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 3389 -j DNAT --to 172.16.11.250
```

结论：

redirect是dnat的一个特例。dnat更加强大。

# masquerade和snat的区别



# -j和-g的区别

-j表示jump，类似函数调用，会返回。

-g相当于goto，一去不复返。



# raw表的用途

raw表工作在最前线，可以提前drop数据，降低系统的负载。



# 什么是专表专用，专链专用？

filter：专门用于过滤数据。

nat：专门用于地址转换。

mangle：用于修改数据包的内容。

raw：预处理数据。

# 一个公网ip的最大连接数

由内核里的nf_conntrack_max这个变量来决定。



# 参考资料

1、《iptables高级使用研讨v1.0.0》

2、 iptables的DNAT和SNAT

https://blog.csdn.net/wylfengyujiancheng/article/details/50238999