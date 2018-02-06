---
title: qemu之客户机联网
date: 2018-02-06 14:15:08
tags:
	- qemu

---



在qemu里跑了一个系统，想让这个系统可以联网。

选择tap/tun的方案。

#host执行操作

1、我的host机器是Ubuntu16.04的。当qemu启动时，可以看到系统增加了一张网卡。

```
tap0      Link encap:Ethernet  HWaddr 2a:44:d5:33:7a:43  
          inet6 addr: fe80::2844:d5ff:fe33:7a43/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:6 errors:0 dropped:0 overruns:0 frame:0
          TX packets:18 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:2100 (2.1 KB)  TX bytes:2371 (2.3 KB)
```

我们可以手动配置ip地址：

```
 sudo ifconfig tap0 192.168.1.1
```

2、启动qemu机器。guest的ip地址是192.168.1.30 。可以ping通host。

但是ping www.baidu.com还不行。

3、现在要配置iptables。

````
sudo echo 1> /proc/sys/net/ipv4/ip_forward
sudo iptables -t nat -A POSTROUTING -o ens33 -s 192.168.1.0/24 -j MASQUERADE
````

但是我这样操作后，还是不行。看看到有种方案是配置网桥的。我暂时就不弄了。







