---
title: 智能音箱之ap配网方式
date: 2020-03-17 16:19:11
tags:
	- 智能音箱
---

--

讨论ap配网方式之前，我们先看看wifi热点的配置和使用。

# wifi ap热点

softapDemo的打印如下：

```
# softapDemo 
DEBUG 287: 
softap_version: 1.0
[ 1117.217225] Current WiFi chip is RTL8723DS.
DEBUG 276: check_wifi_chip_type_string: RTL8723DSDEBUG 290: 
wifi type: RTL8723DS
ap_name=RK_SOFTAP_TEST
DEBUG 33: cmdline = killall dnsmasq
DEBUG 33: cmdline = killall hostapd
killall: hostapd: no process killed
DEBUG 33: cmdline = killall udhcpc
killall: udhcpc: no process killed
DEBUG 321: start softap with name: RK_SOFTAP_TEST---DEBUG 33: cmdline = ifconfig p2p0 down
DEBUG 33: cmdline = rm -rf /userdata/bin/p2p0
DEBUG 33: cmdline = killall dnsmasq
killall: dnsmasq: no process killed
DEBUG 33: cmdline = ifconfig p2p0 up
[ 1117.338849] IPv6: ADDRCONF(NETDEV_UP): p2p0: link is not ready
DEBUG 33: cmdline = ifconfig p2p0 192.168.188.1 netmask 255.255.255.0
DEBUG 33: cmdline = route add default gw 192.168.188.1 p2p0
DEBUG 33: cmdline = dnsmasq -C /userdata/bin/dnsmasq.conf --interface=p2p0
DEBUG 33: cmdline = hostapd /userdata/bin/hostapd.conf &
# Configuration file: /userdata/bin/hostapd.conf
[ 1117.519209] RTW: port switch - port0(p2p0), port1(wlan0)
Using interface p2p0 with hwaddr 02:e0:4c:b8:ed:49 and ssid "RK_SOFTAP_TEST"
[ 1117.631214] RTW: assoc success
[ 1117.631328] IPv6: ADDRCONF(NETDEV_CHANGE): p2p0: link becomes ready
p2p0: interface state UNINITIALIZED->ENABLED
p2p0: AP-ENABLED 
```

概括流程如下：

1、从/sys/class/rkwifi/chip里得到模组的名字（这个文件里就一句话）。因为需要根据不同的模组设置不同的wifi热点名字。对于RTL8723ds，设置wifi网络设备名字为p2p0（跟eth0、wlan0一个类型）。（为什么这个名字？）其他情况设置为wifi1。打开wifi热点后。作为sta的wifi0还存在的。（这个应该就是模组的特性了）

sta的wlan0虽然还在，但是实际上网络不通了。

设置wifi热点名字为RK_SOFTAP_TEST。

2、kill掉dnsmasq和hostapd。这个不是必须的，主要是为了反复测试的健壮性。

3、ifconfig p2p0 up ，启动这个p2p0网卡。配置ip地址为192.168.188.1 ，配置网关。

4、启动dnsmasq和hostapd。

现在就可以接收其他设备的连接了。

如果设备还有一个有线可以上网，再打开ip_forward功能，设备现在就相当于一个简单的路由器了。

dnsmasq和hostapd，都需要一个配置文件。



# wifi配网

在上面热点的基础上。

1、本地打开一个tcp socket 8443，等待设备连接。

2、我用笔记本连上ap热点，用nc连接ap上的socket。

```
nc 192.168.188.1 8443
```

3、笔记本在nc连接后输入：

```
/provision/wifiListInfo
```

这个就是请求ap这边把wifi列表发过来。是下面这种效果。

```
teddy@teddy-ThinkPad-SL410:~/work/buildroot/buildroot-2020.02/output_rpi/images$ nc 192.168.188.1 8443
/provision/wifiListInfo
HTTP/1.1 200 OK
Content-Type:text/html
Content-Length:162

{"type":"WifiList","content":[{"bssid":"88:66:39:25:28:02","frequency":"2412","signalLevel":"-43","flags":"[WPA-PSK-CCMP][WPA2-PSK-CCMP][ESS]","ssid":"DOSS_YF"}]}
```

总的来说，就是通过socket把wifi配置信息发过来，ap这边进行保存。







参考资料

1、

