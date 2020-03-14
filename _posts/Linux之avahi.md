---
title: Linux之avahi
date: 2020-01-16 11:51:19
tags:
	- Linux
---

1

什么是avahi？有什么用？

要了解avahi，需要先了解zeroconf。

zeroconf，就是零配置。是一个网络技术。自动生成可用ip地址的网络技术。

zeroconf是apple公司提出的技术规范。

avahi就是zeroconf技术的开源实现，主要用在Linux上。



avahi允许程序在不手动配置网络的情况下，**在一个局域网内发布和获取各种服务和主机。**

例如，当一台计算机接入到某个局域网，这台计算机上运行了avahi程序，那么avahi就会自动进行广播，这样就可以从局域网里发现可用的打印机、共享文件等等。



avahi在Linux下的进程是avahi-daemon。



回到问题的本质，avahi，最终的目的，应该就是让你可以这样在局域网来进行访问需要的服务：

xxx.local

你不用管这个服务在哪个机器上，端口是多少。

具体到snapcast上来，就是client启动后，都直接去连接snapserver.local这样的地址就完事了。你不用指定172.16.xx这种ip了。





代码在这里：

https://github.com/lathiat/avahi



The fact that `eth0:avahi` appears means that the system failed to get an IP on the `eth0` interface (your wired network interface).

说是因为eth0获取ip失败，所以会出现eth0:avahi这个网卡。

我的wifi联网成功之前，也是出现了一个wlan0:avahi，wifi的联网成功后，这个wlan0:avahi就不见了。

看起来这个说法有道理。

我找了一根网线，把树莓派的网口跟路由器是的lan口连接好之后，eth0:avahi也就没有了。





现在我最大的困惑就是我应该怎么使用这一堆的工具，如何配置，如何启动。

>  man 5 avahi-daemon.conf

这样查看这个配置文件的信息。

avahi-daemon 这个就是mdns进程了。其他的命令都是跟这个进程来进行交互的。

```
host-name=xxx # 不设置的话，就是机器的hostname。
domain-name=local # 不设置的话，默认就是local。
allow-interfaces= # 为空的话，则出了loopback网卡之后的，都会使用。

```

teamviewer好像也用到avahi。

```
_teamviewer._tcp     local
```

这个命令是解析某个服务的具体端口信息。

```
avahi-browse -r _snapcast-tcp._tcp
```

树莓派上启动snapclient后，就可以看到对应的服务。

```
# avahi-browse -a
+  wlan0 IPv6 Music Player @ snapcast                       _mpd._tcp            local
+  wlan0 IPv4 Music Player @ snapcast                       _mpd._tcp            local
+   eth0 IPv4 Music Player @ snapcast                       _mpd._tcp            local
```

解析出来的信息：

```
# avahi-browse -r _mpd._tcp 
+  wlan0 IPv6 Music Player @ snapcast                       _mpd._tcp            local
+  wlan0 IPv4 Music Player @ snapcast                       _mpd._tcp            local
+   eth0 IPv4 Music Player @ snapcast                       _mpd._tcp            local
=  wlan0 IPv6 Music Player @ snapcast                       _mpd._tcp            local
   hostname = [snapcast.local]
   address = [fe80::ba27:ebff:fe55:1b9f]
   port = [6600]
   txt = []
```

我把树莓派和笔记本都连到我手里的一个腾达的路由器上。

现在可以用snapcast.local这样来直接ping通了。





注册一个服务到avahi。

是在/etc/avahi/services目录下。

新建一个service文件。

目前snapos下面是有2个service文件。

```
sftp-ssh.service  ssh.service
```

但是实际上当前启动snapclient之后，可以看到三个服务。

```
# avahi-browse -a
+  wlan0 IPv6 Music Player @ snapcast                       _mpd._tcp            local
+  wlan0 IPv4 Music Player @ snapcast                       _mpd._tcp            local
+   eth0 IPv4 Music Player @ snapcast                       _mpd._tcp            local
+  wlan0 IPv6 snapcast                                      _sftp-ssh._tcp       local
+  wlan0 IPv4 snapcast                                      _sftp-ssh._tcp       local
+   eth0 IPv4 snapcast                                      _sftp-ssh._tcp       local
+  wlan0 IPv6 snapcast                                      _ssh._tcp            local
+  wlan0 IPv4 snapcast                                      _ssh._tcp            local
+   eth0 IPv4 snapcast                                      _ssh._tcp            local
```

应该是snapclient里用C代码进行了服务注册。

```
# avahi-resolve-host-name -4 snapcast.local
snapcast.local  169.254.8.40
```





/etc/avahi/hosts

这个配置文件

目前是空的。里面给了2个例子。

```
# Examples:
# 192.168.0.1 router.local
# 2001::81:1 test.local
```

这个是static host name file。

作用其实就跟/etc/hosts的类似，就是写在这里的域名跟写的ip地址，就固定了，不要费心思去进行解析了。



# snapcast对avahi的使用

具体avahi怎么个用法，我看到snapcast里有依赖这个，具体怎么用的呢？



有一整套命令工具

```
avahi-autoipd            
avahi-browse-domains     
avahi-dnsconfd           
avahi-publish-address    
avahi-resolve            
avahi-resolve-host-name
avahi-browse             
avahi-daemon             
avahi-publish            
avahi-publish-service    
avahi-resolve-address    
avahi-set-host-name
```

## avahi-browse

在运行snapcast的树莓派上执行，情况如下：

```
# avahi-browse -a
+  wlan0 IPv6 snapcast                                      _sftp-ssh._tcp       local
+  wlan0 IPv6 snapcast                                      _ssh._tcp            local
+  wlan0 IPv4 snapcast                                      _sftp-ssh._tcp       local
+  wlan0 IPv4 snapcast                                      _ssh._tcp            local
+   eth0 IPv4 snapcast                                      _sftp-ssh._tcp       local
+   eth0 IPv4 snapcast                                      _ssh._tcp            local
```



```
# ifconfig -a
eth0      Link encap:Ethernet  HWaddr B8:27:EB:00:4E:CA  
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

eth0:avahi Link encap:Ethernet  HWaddr B8:27:EB:00:4E:CA  
          inet addr:169.254.8.40  Bcast:169.254.255.255  Mask:255.255.0.0
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
```

eth0:avahi 这个应该怎样来理解？



参考资料

1、linux服务——Avahi

https://blog.csdn.net/updba/article/details/7389733

2、维基百科

https://en.wikipedia.org/wiki/Avahi_%28software%29

3、

https://wiki.archlinux.org/index.php/Avahi

4、Using Zero Config and Avahi with the DT78xx

https://www.mccdaq.com/PDFs/Manuals/DT7837_WebHelp/Using_Zero_Config_and_Avahi_with_the_DT78xx.htm