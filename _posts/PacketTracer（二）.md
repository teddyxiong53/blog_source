---
title: PacketTracer（二）
date: 2018-04-12 12:14:26
tags:
	- PacketTracer
typora-root-url: ..\
---



# vlan

对应的pkt文件放在https://github.com/teddyxiong53/packet_tracer/03_vlan.pkt

![](/images/PacketTracer（二）-图1.png)

1、创建vlan。

思科ios里，有两种方法来创建vlan。

一种是在全局配置模式下。

```
switch(config)#vlan 10
```

一种是在vlan database下。

```
switch(vlan)#vlan 20
```

实际操作：

```
Switch>enable
Switch#config
Configuring from terminal, memory, or network [terminal]? 
Enter configuration commands, one per line.  End with CNTL/Z.
Switch(config)#vlan 10
Switch(config-vlan)#?
VLAN configuration commands:
  exit  Apply changes, bump revision number, and exit mode
  name  Ascii name of the VLAN
  no    Negate a command or set its defaults
Switch(config-vlan)#
Switch(config-vlan)#name Math
Switch(config-vlan)#exit
Switch(config)#
Switch(config)#exit
Switch#  //继续退出配置模式。
%SYS-5-CONFIG_I: Configured from console by console

Switch#vlan ?
  database  Configure VLAN database
Switch#vlan database //可以看到，推荐是在全局配置模式下做的。我们现在只是演示。
% Warning: It is recommended to configure VLAN from config mode,
  as VLAN database mode is being deprecated. Please consult user
  documentation for configuring VTP/VLAN in config mode.

Switch(vlan)#
Switch(vlan)#vlan 20 name Chinese //继续添加2个vlan，
VLAN 20 added:
    Name: Chinese
Switch(vlan)#vlan 30 name Other
VLAN 30 added:
    Name: Other
Switch(vlan)#
```

2、接下来，要做的事情，就是把端口划分为vlan。（交换机的端口都是很多的，一般是24个lan口）。

当前我在交换机上是接了7台pc。分别占用了交换机的FastEthernet 0/1到0/7 。

```
Switch(config)#interface fastEthernet 0/1
Switch(config-if)#switchport mode access 
Switch(config-if)#switchport access vlan 10
```

单个lan口的划分，就是上面这3条命令。

这样无疑是比较麻烦的，能不能批量设置？能。

```
Switch(config-if)#interface range fastEthernet 0/2 - 4
Switch(config-if-range)#switchport mode access 
Switch(config-if-range)#switchport access vlan 10
```

3、从vlan里删除某个lan。

```
Switch(config)#interface fa0/8
Switch(config-if)#no switchport access vlan 40
```

正式配置。我不用自动连线，自动连线，端口我不能控制，我选择双绞线的。

pc0到pc6，都是按顺序占用交换机的端口，ip地址也是从192.168.0.1到7 。

pc0和pc1划到vlan 10

pc3和pc4划到vlan 20

pc2、pc5、pc6划到vlan30 。

当前3个vlan多在前面建好了。

```
Switch#show vlan brief

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Fa0/2, Fa0/3, Fa0/4, Fa0/5
                                                Fa0/6, Fa0/7, Fa0/8, Fa0/9
                                                Fa0/10, Fa0/11, Fa0/12, Fa0/13
                                                Fa0/14, Fa0/15, Fa0/16, Fa0/17
                                                Fa0/18, Fa0/19, Fa0/20, Fa0/21
                                                Fa0/22, Fa0/23, Fa0/24, Gig1/1
                                                Gig1/2
10   Math                             active    Fa0/1
20   Chinese                          active    
30   Other                            active    
```

```
Switch(config)#interface range fastEthernet 0/1 - 2
Switch(config-if-range)#switchport mode access
  vlan  Set VLAN when interface is in access mode
Switch(config-if-range)#switchport access vlan 10
```

```
Switch(config-if-range)#interface range fastEthernet 0/4 - 5
Switch(config-if-range)#switchport mode access
Switch(config-if-range)#switchport access vlan 20
```

```
Switch(config-if-range)#interface fastEthernet 0/3
Switch(config-if)#
```

配置好之后，在同一个vlan里的才能ping通。



# wlan

一个无线路由器，连接4个pc。pc需要把有线网卡移除，再添加无线网卡。

有一台保留有线网卡。

路由器是Linksys WRT300N。

我发现有线反而连接不上去。静态ip和dhcp都不行。

反而无线的没有任何问题。

Linksys的ip地址是192.168.0.1，分配的ip地址是从100开始的。

可以通过http://192.168.0.1，name和密码都是admin。登陆到管理界面。

![](/images/PacketTracer（二）-图2.png)

# 配置静态路由

静态路由不能自适应，是需要管理员手动配置的。

简单，适合在简单网络里使用。

这个我在02_pc_route_server里就已经实现了。



# 配置动态路由

动态路由是指路由器能够自动建立自己的路由表。并且能够根据实际情况的变化进行调整。

这样就减轻了管理员的负担。

常用的动态路由协议包括：

1、rip。

2、ospf。

3、is-is。

4、bgp。

我们现在就以rip为例。网络结构是这样的。

![](/images/PacketTracer（二）-图3.png)

配置router0的。

```
Router(config)#router ? //我们查看一下，就是支持这4种动态路由协议。
  bgp    Border Gateway Protocol (BGP)
  eigrp  Enhanced Interior Gateway Routing Protocol (EIGRP)
  ospf   Open Shortest Path First (OSPF)
  rip    Routing Information Protocol (RIP)
Router(config)#router rip
Router(config-router)#network 172.16.3.0
Router(config-router)#end
```

配置router1的。

```
Router(config)#router rip
  A.B.C.D  Network number
Router(config-router)#network 172.16.1.0
Router(config-router)#end
Router#
%SYS-5-CONFIG_I: Configured from console by console
```

现在pc0 ping一下pc1。不通。

为什么？

我看rip那里，总是被自动改成172.16.0.0，我就把所有网段都改成192.168的。

还是 不行。我又发现1841的路由器，没有串口（路由器直接是用串口连接的）。

我换成generic的路由器，把router0和router1用串口连接起来。

还是不行。

配置之后，看rip。都是没有的。

show ip route

```
C    192.168.1.0/24 is directly connected, FastEthernet0/0
C    192.168.2.0/24 is directly connected, Serial2/0
```

按道理应该有一条：

```
R 192.168.3.0 via 192.168.2.2 
```

算了不管了。我重在理解概念。



# nat

nat最初的目的是把私有的ip地址映射成公网上合法的地址，用这种方式来减少对公网ip的需求。

什么时候需要使用nat？

1、需要连接到internet，但是你的电脑没有公网ip。

2、需要合并2个具有相同网络结构的内网。

nat一般应用在边界路由器上。正是有nat技术，我们ipv4还能勉强支撑。

nat也分为三种 ：

1、静态nat。

2、动态nat。

3、pat。

![](/images/PacketTracer（二）-nat.png)

pc0：192.168.0.4

pc1:192.168.0.2

server0:192.168.0.3

配置route0的静态路由：

```
网络：0.0.0.0
掩码：0.0.0.0
下一跳：131.107.0.254
```

配置router1的静态路由：

```
网络：0.0.0.0
掩码：0.0.0.0
下一跳：202.99.160.2
网络：131.107.0.0
掩码：255.255.255.0
下一跳：131.107.0.1
```

然后配置静态nat。

规划如下。

```
机器           内部ip地址       映射公网ip地址
pc0           192.168.0.4      131.107.0.4
pc1           192.168.0.2      131.107.0.2
server0       192.168.0.3      131.107.0.3
```

在 router0上进行设置。

```
Router(config)#interface fastEthernet 0/0
Router(config-if)#ip nat inside  #一个inside
Router(config-if)#exit
Router(config)#interface fastEthernet 0/1
Router(config-if)#ip nat outside //一个outside。
Router(config-if)#exit
Router(config)#exit
Router#debug ip nat   //打开调试。
IP NAT debugging is on
Router#
Router#config
Configuring from terminal, memory, or network [terminal]? 
Enter configuration commands, one per line.  End with CNTL/Z.
Router(config)#
Router(config)#ip nat ?
  inside   Inside address translation
  outside  Outside address translation
  pool     Define pool of addresses
Router(config)#ip nat inside ?
  source  Source address translation
Router(config)#ip nat inside source static  192.168.0.2      131.107.0.2
Router(config)#ip nat inside source static  192.168.0.3      131.107.0.3
Router(config)#ip nat inside source static  192.168.0.4     131.107.0.4
```

现在从pc0可以ping通server2。

现在看看动态nat的。

如果你有3个外网ip，但是内网有5台机器，使用动态nat，只能同时有3台计算机访问Internet。

所以这种其实也不是真实使用的情况。

现实中，一般是采用pat的方式。

pat的方式，就是采用端口号来区分内部机器，这样，只要有一台机器有公网ip，其余机器都可以同时上网。



# 参考资料

1、packet tracer5.0全攻略

https://wenku.baidu.com/view/25b3bdd2c1c708a1284a44de.html

2、构建简易网络与网络设备的简单配置（Cisco Packet Tracer）第三弹：动态路由协议配置

https://blog.csdn.net/u013009839/article/details/46651367

3、 网络(三) 之 网络地址转换NAT(使用Cisco Packet Tracer模拟)

https://blog.csdn.net/m0_37681914/article/details/72860274