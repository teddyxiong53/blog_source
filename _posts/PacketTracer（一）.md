---
title: PacketTracer（一）
date: 2018-04-12 09:40:32
tags:
	- PacketTracer

---



很久之前玩过PacketTracer，但是没有玩透。现在需要用到网络知识，所以重新再学习一遍。

下面我就简称PT。

# 什么是PT？

1、是思科发布的一个辅助学习工具。

2、为思科的网络课程初学者去设计、配置、排除网络故障提供了网络模拟环境。

当前最新版本是7.0的。

我电脑上安装的是6.0的，不打算更新了。



# 设备梳理

因为我并不是初学，所以还是安装梳理思路的方式来做。

先把典型设备各选择一种来进行了解。

##路由器

1841，这个名字看着挺顺眼，就了解一下这个。

```
1、在2013年就停产了。价格是3000块左右。
2、是模块化接入路由器。
3、支持QoS，支持vpn。
4、速率是10M和100Mbps。
5、lan接口是2个。
6、ram是384M，flash是128M。
7、有一个usb接口。
8、功率最大50W。
9、适用于中小企业。
```

##交换机

就选2950T-24。

```
1、是快速以太网交换机。
2、背板带宽是8.8Gbps。
3、支持10M、100M、1000M。
4、也是停产了。
5、端口数量是24个，这就是后缀24的含义了。
```

## 集线器

这个没有名字，就叫generic。

## 无线设备

就选择LinkSys的WRT300N。

```
1、支持802.11b和802.11g。
2、一个wan口，4个lan口。
3、覆盖范围500m。
```

#找一套好的教程

我不打算花太多时间。所以找一套教程帮助自己快速学习。

http://jsjxy.shiep.edu.cn/network/files/Packet_Tracer_使用教程.pdf

这个简单，看起来还可以，只有32页。



# 第一个例子

给的第一个例子，就是配置vlan的。我喜欢，因为我现在就是要做一下vlan实验。

1、拖一个2950T的交换机到画布上。

点击进入到命令行界面。

我们先看看开机打印内容。

```
C2950 Boot Loader (C2950-HBOOT-M) Version 12.1(11r)EA1, RELEASE SOFTWARE (fc1) #思科自己的bootloader
Compiled Mon 22-Jul-02 18:57 by miwang//编译时间是2002年的了。
Cisco WS-C2950T-24 (RC32300) processor (revision C0) with 21039K bytes of memory.
2950T-24 starting...
Base ethernet MAC Address: 0090.0CA7.8148 //打印mac地址。
Xmodem file system is available.
Initializing Flash... //初始化flash
flashfs[0]: 1 files, 0 directories
flashfs[0]: 0 orphaned files, 0 orphaned directories
flashfs[0]: Total bytes: 64016384
flashfs[0]: Bytes used: 3058048
flashfs[0]: Bytes available: 60958336
flashfs[0]: flashfs fsck took 1 seconds.//文件系统检查画了1秒。
...done Initializing Flash.

Boot Sector Filesystem (bs:) installed, fsid: 3
Parameter Block Filesystem (pb:) installed, fsid: 4


Loading "flash:/c2950-i6q4l2-mz.121-22.EA4.bin"...
########################################################################## [OK]
              Restricted Rights Legend //版权声明

Use, duplication, or disclosure by the Government is
subject to restrictions as set forth in subparagraph
(c) of the Commercial Computer Software - Restricted
Rights clause at FAR sec. 52.227-19 and subparagraph
(c) (1) (ii) of the Rights in Technical Data and Computer
Software clause at DFARS sec. 252.227-7013.

           cisco Systems, Inc.
           170 West Tasman Drive
           San Jose, California 95134-1706



Cisco Internetwork Operating System Software
IOS (tm) C2950 Software (C2950-I6Q4L2-M), Version 12.1(22)EA4, RELEASE SOFTWARE(fc1)
Copyright (c) 1986-2005 by cisco Systems, Inc.
Compiled Wed 18-May-05 22:31 by jharirba

Cisco WS-C2950T-24 (RC32300) processor (revision C0) with 21039K bytes of memory.
Processor board ID FHK0610Z0WC
Running Standard Image
24 FastEthernet/IEEE 802.3 interface(s)
2 Gigabit Ethernet/IEEE 802.3 interface(s)

63488K bytes of flash-simulated non-volatile configuration memory.
Base ethernet MAC Address: 0090.0CA7.8148
Motherboard assembly number: 73-5781-09 //各种序列号
Power supply part number: 34-0965-01
Motherboard serial number: FOC061004SZ
Power supply serial number: DAB0609127D
Model revision number: C0
Motherboard revision number: A0
Model number: WS-C2950T-24
System serial number: FHK0610Z0WC

Cisco Internetwork Operating System Software //思科自己的iOS操作系统。
IOS (tm) C2950 Software (C2950-I6Q4L2-M), Version 12.1(22)EA4, RELEASE SOFTWARE(fc1)
Copyright (c) 1986-2005 by cisco Systems, Inc.
Compiled Wed 18-May-05 22:31 by jharirba

Press RETURN to get started! //这里就是login，askfirst。
Switch>
```

默认登陆进来是普通用户。

一共有3种模式：

```
1、普通用户，提示符是：Switch>
2、全局配置。提示符是：Switch(config)#
3、端口配置。提示符是：Switch(config-if)#
```

切换到root，是输入enable。我就理解为su就好了。

进入全局配置，是输入configure terminal。Switch(config)#

进入端口配置，是输入interface fa0/1。Switch(config-if)#

现在还是一台空的交换机，没有连接什么设备，也没有进行过配置。

```
Switch#show vlan

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Fa0/1, Fa0/2, Fa0/3, Fa0/4
                                                Fa0/5, Fa0/6, Fa0/7, Fa0/8
                                                Fa0/9, Fa0/10, Fa0/11, Fa0/12
                                                Fa0/13, Fa0/14, Fa0/15, Fa0/16
                                                Fa0/17, Fa0/18, Fa0/19, Fa0/20
                                                Fa0/21, Fa0/22, Fa0/23, Fa0/24
                                                Gig1/1, Gig1/2
1002 fddi-default                     act/unsup 
1003 token-ring-default               act/unsup 
1004 fddinet-default                  act/unsup 
1005 trnet-default                    act/unsup 

VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
1    enet  100001     1500  -      -      -        -    -        0      0
1002 fddi  101002     1500  -      -      -        -    -        0      0   
1003 tr    101003     1500  -      -      -        -    -        0      0   
1004 fdnet 101004     1500  -      -      -        ieee -        0      0   
1005 trnet 101005     1500  -      -      -        ibm  -        0      0   

Remote SPAN VLANs
------------------------------------------------------------------------------


Primary Secondary Type              Ports
------- --------- ----------------- ------------------------------------------
```

命令行这边，我不打算深入，我还看看图形的这边，这让我可以更加专注网络本身。

其实图形界面的是转成了命令行的，你点击图标的是，可以看到命令行的输出。



安装目录下，有教程的。

```
C:\Program Files (x86)\Cisco Packet Tracer 6.0\help\default
```

我还是看官方教程吧。



# 从头再来第一个例子

我发现现在对于PT不是那么熟悉。我还是自己来弄一个简单的例子。

最简单的网络结构。

pc直连到一个server。server提供网页访问。pc和server都只有一个以太网接口。

server：配置ip为192.168.0.1。

pc：配置ip为192.168.0.2 。

默认server就启动了web服务的。

所以pc上点开browser，输入：http://192.168.0.1/index.html

可以得到这样的界面：

```
Cisco Packet Tracer
Welcome to Cisco Packet Tracer. Opening doors to new opportunities. Mind Wide Open. Quick Links: 
A small page 
Copyrights 
Image page 
Image 
```

现在我要看看具体的包的传输过程。

我选择Add Simple PDU。从pc到server。

然后单步走。

可以看到这个就是一个ping的过程。

我们双击pc到server的这一条。出现详细信息窗口。

分为3个标签：

1、OSI Model。很形象地把分层的内容罗列出来。

2、Inbound PDU Detail。

3、Outbound PDU Detail。

可以看到，以太网帧有8个字节的前导。

我继续把pc上的各个东西都点击一遍。

##pc具有的功能

###command prompt

telnet失败了。我找了一下，在server上没有看到telnet服务的。

```
PC>telnet 192.168.0.1
Trying 192.168.0.1 ...
% Connection refused by remote host
PC>
```

### 防火墙



## sever具有的功能

1、可以添加一个无线模块上去。必须下电才能添加模块。

下电是找一个绿色的电源灯，点击一下就下电了。再点击一下就开机了。



# 第一个例子的改进

我们在pc和server之间，加上2个1841的路由器。

为了以后不再重复学习，我把前面的保存为01_pc_to_server.pkt。

新建一个02_pc_route_server.pkt文件。

上传到github上保存。

路由器默认接口都是没有打开的，需要手动打开。

1841都是2个以太网接口。

路由器支持的命令。

```
Router(config-if)#?
  arp                Set arp type (arpa, probe, snap) or timeout
  bandwidth          Set bandwidth informational parameter
  cdp                CDP interface subcommands
  crypto             Encryption/Decryption commands
  custom-queue-list  Assign a custom queue list to an interface
  delay              Specify interface throughput delay
  description        Interface specific description
  duplex             Configure duplex operation.
  exit               Exit from interface configuration mode
  fair-queue         Enable Fair Queuing on an Interface
  hold-queue         Set hold queue depth
  ip                 Interface Internet Protocol config commands
  ipv6               IPv6 interface subcommands
  mac-address        Manually set interface MAC address
  mtu                Set the interface Maximum Transmission Unit (MTU)
  no                 Negate a command or set its defaults
  pppoe              pppoe interface subcommands
  priority-group     Assign a priority group to an interface
  service-policy     Configure QoS Service Policy
  shutdown           Shutdown the selected interface
  speed              Configure speed operation.
  standby            HSRP interface configuration commands
  tx-ring-limit      Configure PA level transmit ring limit
  zone-member        Apply zone name
```

我现在首先要做的，就是让路由器给pc分配ip地址，用dhcp。

但是看图形界面没有dhcp相关的东西。

那就到命令行里去找一下。

命令查看帮助的方法，都是`xxx ?`这样。

我现在的拓扑结构是：

```
pc -->(0) route0(1) -->(0)route1(1) --> server
```

现在配置route0的网卡0为：192.168.0.1，同时为pc提供dhcp服务。

在路由器上这样操作。

```
Router#configure   #先进入到config
Router(config)#interface fastEthernet 0/0  #再进入到网卡0的接口配置。
Router(config-if)#
Router(config-if)#ip address 192.168.0.1 255.255.255.0 #配置网卡的地址。
Router(config-if)#exit #退出接口配置。
Router(config)#
Router(config)#ip dhcp pool pool01  #配置一个叫pool01的dhcp地址池。
Router(dhcp-config)#
Router(dhcp-config)#network 192.168.0.0 255.255.255.0
Router(dhcp-config)#
Router(dhcp-config)#default-router 192.168.0.1
Router(dhcp-config)#
```

现在可以在pc上设置为dhcp，看看能否获取到ip地址。

可以看到pc现在被分配了192.168.0.2的ip地址。说明设置正常。

现在要配置route0的网卡1的地址，我就给一个192.168.1.1的地址吧。

然后route1的网卡0根route0的网卡1是连接的，那就给route1的网卡2 ip地址为192.168.1.2 。

然后route1的网卡1的ip地址为192.168.2.1 。server的ip地址为192.168.2.2 。

这样配置后，从pc 192.168.0.2无法ping通192.168.2.2的server。

```

PC>ping 192.168.2.2

Pinging 192.168.2.2 with 32 bytes of data:

Reply from 192.168.0.1: Destination host unreachable.
Reply from 192.168.0.1: Destination host unreachable.
```

问题出在哪里呢？

route0可以ping通route1的。

```
Router#ping 192.168.1.2

Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 192.168.1.2, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 0/0/1 ms

Router#
```

这篇文章讲了一个类似的例子，看看。

https://www.cnblogs.com/mchina/archive/2012/07/18/2596515.html

看了我就明白了。我没有添加路由规则。

```
Router#show ip route
Codes: C - connected, S - static, I - IGRP, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
       * - candidate default, U - per-user static route, o - ODR
       P - periodic downloaded static route

Gateway of last resort is not set

C    192.168.0.0/24 is directly connected, FastEthernet0/0
C    192.168.1.0/24 is directly connected, FastEthernet0/1
```

在route0上这样设置：

```
Router(config)#ip route 192.168.2.0 255.255.255.0 192.168.1.2
Router(config)#end
Router#
```

再查看路由信息，可以看到增加了一条静态路由。

```
C    192.168.0.0/24 is directly connected, FastEthernet0/0
C    192.168.1.0/24 is directly connected, FastEthernet0/1
S    192.168.2.0/24 [1/0] via 192.168.1.2
```

同样的方法设置route1的。

```
Router(config)#ip route 192.168.0.0 255.255.255.0 192.168.1.1
Router(config)#end
```

查看路由信息。

```
S    192.168.0.0/24 [1/0] via 192.168.1.1
C    192.168.1.0/24 is directly connected, FastEthernet0/0
C    192.168.2.0/24 is directly connected, FastEthernet0/1
```

现在再ping一次看看。

可以通了。



# 参考资料

1、CISCO 1841参数

http://detail.zol.com.cn/109/108262/param.shtml

