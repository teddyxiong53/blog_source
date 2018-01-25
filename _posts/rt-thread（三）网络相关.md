---
title: rt-thread（三）网络相关
date: 2018-01-24 13:43:05
tags:
	- rt-thread

---



vexpress在qemu里运行起来。

主机上ifconfig可以看到一个叫tap0的网卡。

```
tap0      Link encap:Ethernet  HWaddr 0a:a8:c6:43:90:dd  
          inet addr:192.168.1.1  Bcast:192.168.1.255  Mask:255.255.255.0
          inet6 addr: fe80::8a8:c6ff:fe43:90dd/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:312 errors:0 dropped:0 overruns:0 frame:0
          TX packets:37 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:109200 (109.2 KB)  TX bytes:4855 (4.8 KB)
```

地址是我手动配置为192.168.1.1，掩码为255.255.255.0 。

```
sudo ifconfig tap0 192.168.1.0 netmask 255.255.255.0
```



然后在rt-thread里，

```
msh /rtt>ifconfig e0 192.168.1.10 192.168.1.1 255.255.255.0 
config : e0
IP addr: 192.168.1.10
Gateway: 192.168.1.1
netmask: 255.255.255.0
```

然后在主机里ping一下：

```
teddy@teddy-ubuntu:~/work/rt-thread/rt-thread/bsp/qemu-vexpress-a9$ ping 192.168.1.10
PING 192.168.1.10 (192.168.1.10) 56(84) bytes of data.
64 bytes from 192.168.1.10: icmp_seq=1 ttl=255 time=3.59 ms
64 bytes from 192.168.1.10: icmp_seq=2 ttl=255 time=0.514 ms
```

是可以通的。

每次重新启动qemu后，tap0的ip地址就没了。

