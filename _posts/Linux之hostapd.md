---
title: Linux之hostapd
date: 2018-10-30 13:19:14
tags:
	- Linux

---



简单来说，hostapd就是用来把无线网卡模拟成一个ap热点的工具。

模拟的ap称为Soft AP。

hostapd就是作为softap的认证服务。

负责接入设备的认证。

怎样查看一款无线网卡是否支持ap模式呢？

用iw工具。

```
iwlist
```

```
# iwlist
Usage: iwlist [interface] scanning [essid NNN] [last]
              [interface] frequency 
              [interface] channel 
              [interface] bitrate 
              [interface] rate 
              [interface] encryption 
              [interface] keys 
              [interface] power 
              [interface] txpower 
              [interface] retry 
              [interface] ap 
              [interface] accesspoints 
              [interface] peers 
              [interface] event 
              [interface] auth 
              [interface] wpakeys 
              [interface] genie 
              [interface] modulation 
```



```
ssid=xxxyyy
hw_mode=g
channel=10
interface=wlan0
driver=nl80211
ignore_broadcast_ssid=0
macaddr_acl=0
```

这样启动的热点是不带密码的。

然后还需要dnsmasq这个进程来配合。

这个直接启动就好。默认的配置文件是在/etc/dnsmasq.conf里。内容是这样：

```
user=root
listen-address=10.201.126.1
dhcp-range=10.201.126.50,10.201.126.150
server=/google/8.8.8.8
```

然后执行下面的操作：

```
#如果有启动sta模式的wpa这些进程，先kill掉。
killall -9 wpa_supplicant
#给网卡配置ip地址，这个必须做，而且是在前面做。不然结果就是一直无法连接到这个ap了。
ifconfig wlan0 10.201.126.1 netmask 255.255.255.0
#启动hostapd
hostapd /oem/hostapd.conf -B
#启动dnsmasq
dnsmasq
```

然后打开手机就可以连接上去了。





# 参考资料

1、Linux下软AP功能之Hostapd介绍

https://blog.csdn.net/hinyunsin/article/details/6029663

2、（一）hostapd是干嘛的

https://www.kancloud.cn/digest/wlan/141028

3、hostapd基本配置

https://www.cnblogs.com/zhuwenger/archive/2011/03/11/1980294.html

4、配置wifi为AP模式 -- 接入点hostapd基本配置

https://blog.csdn.net/wh_19910525/article/details/52244604