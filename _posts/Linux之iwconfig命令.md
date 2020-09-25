---
title: Linux之iwconfig命令
date: 2020-09-25 15:05:30
tags:
	- Linux

---

1

iwconfig，是用来操作无线网卡的。

它有哪些主要的用法？

iwconfig，不带任何参数，是列出本机的无线网卡。

在笔记本上：

```
wlan0     IEEE 802.11  ESSID:"OpenWrt"  
          Mode:Managed  Frequency:2.462 GHz  Access Point: B8:27:EB:55:1B:9F   
          Bit Rate=72.2 Mb/s   Tx-Power=20 dBm   
          Retry short limit:7   RTS thr=2347 B   Fragment thr:off
          Power Management:on
          Link Quality=52/70  Signal level=-58 dBm  
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:0  Invalid misc:842   Missed beacon:0
```

在路由器上：

```
wlan0     IEEE 802.11  Mode:Master  Tx-Power=31 dBm   
          RTS thr:off   Fragment thr:off
          Power Management:on
          
```

主要用来设置网卡的无线射频参数。

读取的信息是来自于/proc/net/wireless

主要设置的：

```
iwconfig interface [essid X] [nwid N] [mode M] [freq F]
                          [channel C][sens S ][ap A ][nick NN ]
                          [rate R] [rts RT] [frag FT] [txpower T]
                          [enc E] [key K] [power P] [retry R]
                          [modu M] [commit]
```



# essid

设置无线网卡的ESSID(Extension Service Set ID)。

通过ESSID来区分不同的无线网络，

正常情况下只有相同ESSID的无线站点才可以互相通讯，除非想监听无线网络。

其后的参 数为双引号括起的ESSID字符串，或者是any/on/off，

如果ESSID字符串中包含any/no/off，则需要在前面加"--"。

```
iwconfig wlan0 essid any #这个表示设置为混杂模式。
iwconfig wlan0 essid "xhl" 
iwconfig wlan0 essid -- "any"
```

# nwid

这个过时了。不管。

# mode

设置无线网卡的工作模式。

无线网络有两种建网模式，Ad-hoc和Infrastructure模式：

Infrastructure－－无线网与有线网通过一接入点来进行通讯。

Ad-hoc模式－－带有无线设备的计算机之间**直接进行通讯**（类似有线网络的双机互联）

Ad-Hoc模式又叫做IBBS (独立基础服务集Independent Basic Service Set)模式,

**用于创建一个没有AP的无线网络.**

所有在IBSS范围内的工作站都自己管理网络. **Ad-Hoc在两个或更多电脑之间连接没有AP设备的环境.**

mode有：

```
Ad-Hoc
Managed
Master
	这个就是ap。
Repeater
	中继器。
Secondary
	备份的的master或者repeater。
Monitor
	监听模式。
Auto
	自动模式。
```

# nickname

就是这个以容易记住的名字。

# freq/channel

```
iwconfig wlan0 freq 2422000000
iwconfig wlan0 freq 2.422G
iwconfig wlan0 channel 3
iwconfig wlan0 channel auto
```



参考资料

1、man手册

2、iwconfig命令

https://blog.csdn.net/qq_35654080/article/details/89372214

3、无线路由模式——Ad-hoc、Infrastructure、AP、Station

https://blog.csdn.net/bytxl/article/details/50419585