---
title: 树莓派之打开wifi热点
date: 2018-04-20 13:56:48
tags:
	- 树莓派

---



树莓派默认没有开启wifi热点的。

我们看看怎么打开，把树莓派变成一个简单的路由器。

需要的软件有：

1、hostapd。

2、dnsmasq。



下面的操作步骤。

1、修改 /etc/network/interfaces。加上这些。

```
allow-hotplug wlan0
iface wlan0 inet static
        address 192.168.1.1
        netmask 255.255.255.0
        network 192.168.1.0
        broadcast 192.168.1.255
```

2、重启dhcp服务。

```
sudo service dhcpd restart
sudo ifdown wlan0
sudo ifup wlan0
```

查看ifconfig。

```
wlan0     Link encap:Ethernet  HWaddr b8:27:eb:55:1b:9f  
          inet addr:192.168.1.1  Bcast:192.168.1.255  Mask:255.255.255.0
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
```

3、配置hostapd。修改/etc/hostapd/hostapd.conf文件。

```
interface=wlan0
driver=nl80211
ssid=mypi
hw_mode=g
channel=1
ieee80211n=1
macaddr_acl=0

auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=12345678
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

4、启动hostapd。

```
sudo hostapd /etc/hostapd/hostapd.conf
```

现在我们用手机，可以搜索到上面配置的叫mypi的热点了。

我们连接看看。

```
wlan0: STA b4:0b:44:ed:fc:0d IEEE 802.11: associated
wlan0: AP-STA-CONNECTED b4:0b:44:ed:fc:0d
wlan0: STA b4:0b:44:ed:fc:0d RADIUS: starting accounting session 5AD98257-00000000
wlan0: STA b4:0b:44:ed:fc:0d WPA: pairwise key handshake completed (RSN)
wlan0: STA b4:0b:44:ed:fc:0d IEEE 802.11: disassociated
wlan0: AP-STA-DISCONNECTED b4:0b:44:ed:fc:0d
wlan0: STA b4:0b:44:ed:fc:0d IEEE 802.11: disassociated
```

连接不上。



# 参考资料

1、使用树莓派3B开启WIFI热点

https://blog.csdn.net/Lioker/article/details/77825477