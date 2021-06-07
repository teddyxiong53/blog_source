---
title: qemu之客户机联网
date: 2018-02-06 14:15:08
tags:
	- qemu

---



在qemu里跑了一个系统，想让这个系统可以联网。

选择tap/tun的方案。

# host执行操作

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

# 重新尝试

启动docker。

安装这个，是为了得到tunctl工具。

```
sudo apt-get install uml-utilities
```

创建一个tun网卡。

```
sudo tunctl -t tap0
```

打开网卡：

```
sudo ifconfig tap0 up
```

在qemu的启动命令后加上：

```
-net nic,model=lan9118 -net tap,ifname=tap0,script=no,downscript=no 
```

启动qemu，里面执行：

```
ifconfig eth0 172.17.0.30 netmask 255.255.0.0
route add default gw 172.17.0.1
```

172.17.0.1这个是docker0这个网卡的ip，它的掩码是255.255.0.0。

这样配置后，还是不能上网。ping不通172.17.0.1 。

host里查看，tap0的网卡信息是这样：

```
tap0      Link encap:以太网  硬件地址 3e:59:a2:ce:70:89  
          inet 地址:169.254.149.41  广播:169.254.255.255  掩码:255.255.0.0
```

我在qemu里再把ip配置为169.254.149.50/16的。这样至少可以ping通169.254.149.41。

但是ping不通114.114.114.114 。



qemu提供了4种不同模式的网络

```
1、基于网桥。
2、基于nat。
3、qemu内置的usermode network。
4、直接分配网络设备。
```



# 再次尝试

```
sudo apt-get install uml-utilities
sudo apt-get install bridge-utils
```

查看是否有这个设备 /dev/net/tun 

如果有，说明内核支持tun。从ubuntu12.04就开始支持。

添加 /etc/qemu-ifup 和/etc/qemu-ifdown 脚本。



qemu默认使用tap设备，



# 参考资料

1、一种简单的qemu网络配置方法

https://blog.csdn.net/wujianyongw4/article/details/80497528

2、详解QEMU网络配置的方法

https://blog.csdn.net/rfidunion/article/details/55096935

3、

https://topic.alibabacloud.com/a/configuring-qemus-network-capabilities-with-qemu-simulation-vexpress-a9-_8_8_31314529.html