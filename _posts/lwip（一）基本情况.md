---
title: lwip（一）
date: 2018-02-03 16:31:23
tags:
	- lwip

---



之前也看过lwip，但是很多点都没有弄懂。现在在系统性学习rt-thread，就把lwip的也重新学习一遍。

抛弃之前的认识，从头开始来。

我现在基于qemu和vexpress-a9来学习。有qemu虚拟机可以跟主机进行通信。环境非常完美。

既然是从头学习，我们从维基百科的介绍开始看。

# lwip基本情况

1、lwip是广泛使用的嵌入式设备用的tcpip协议栈。

2、最初是由Adam Dunkels开发。现在开源社区维护。

3、设计主要考虑就是减少协议栈的资源占用。

## lwip各层的实现情况

1、链路层。

```
ppp
arp
```

2、网络层。

```
IP
ICMP
IGMP
```

3、传输层。

```
TCP
UDP
RAW
```

4、应用层。

```
DNS
SNMP
DHCP
```

5、其他。

```
1、raw/native API。
2、socket API。
3、http server等一些server和client。
```

# 参考文档

最好的文档肯定是官方文档了。

我用的lwip版本是2.0.2的。因为rt-thread默认用了这个版本。我对版本没有要求。新一点的当然好。

执行命令：

```
teddy@teddy-ubuntu:~/work/rt-thread/rt-thread/components/net/lwip-2.0.2/doc/doxygen$ ./generate.sh
```

就会生成html文档。

我们接下来主要就参考这份文档，另外有疑问随时谷歌搜索。

现在lwip有了自己的wiki站点。http://lwip.wikia.com/wiki/LwIP_Wiki

不过看起来没有太多东西。

有邮件列表，可以订阅一下。

# lwip API

lwip提供了3种api。

1、raw api。是基于回调。也叫native API。事件驱动，是给没有os的系统用的。 

2、seq api。是netconn_xxx这种接口。有点像socket接口。要求tcpip线程和应用线程是分开的（这个肯定的）。

3、socket API。我们一般用这个。

## 关于线程安全

lwip最开始是给没有os的系统写的。后面才增加的多线程支持。

只有在这些文件里列出来的函数才是线程安全的。

```
api.h
netbuf.h
netdb.h
netifapi.h
pppapi.h
sockets.h
sys.h
```



# 代码目录分析

src目录下，总共260个文件左右。

我们先把目录和文件的作用理一遍。

```
teddy@teddy-ubuntu:~/work/rt-thread/rt-thread/components/net/lwip-2.0.2/src$ tree -L 2
.
├── api
│   ├── api_lib.c：里面都是netconn_xxx这种函数。这个算是lwip的嫡系API了。
│   ├── api_msg.c：跟api_lib.c的配合工作。
│   ├── err.c：提供lwip_strerr函数。
│   ├── netbuf.c：提供netbuf_xxx函数。
│   ├── netdb.c：提供lwip_gethostbyname等函数。
│   ├── netifapi.c：提供netifapi_xxx函数。
│   ├── sockets.c：socket接口定义。
│   └── tcpip.c：入口文件。
├── apps：这个都是一些应用的代码。不属于核心内容。不用看。
│   ├── httpd
│   ├── lwiperf
│   ├── mdns
│   ├── mqtt
│   ├── netbiosns
│   ├── ping
│   ├── README.md
│   ├── SConscript
│   ├── snmp
│   ├── sntp
│   └── tftp
├── arch
│   ├── include
│   └── sys_arch.c：这个就是和rtos对接的核心文件。重要。
├── core：核心代码。
│   ├── def.c：提供了hton等函数。
│   ├── dns.c：
│   ├── inet_chksum.c
│   ├── init.c：lwip_init在这里。入口文件。
│   ├── ip.c：提供ip_input函数。
│   ├── ipv4
│   ├── ipv6
│   ├── mem.c：malloc的实现。算法跟rt-thread里的mem.c是一样的。
│   ├── memp.c：
│   ├── netif.c：netif_xxx函数。
│   ├── pbuf.c
│   ├── raw.c
│   ├── stats.c
│   ├── sys.c
│   ├── tcp.c
│   ├── tcp_in.c
│   ├── tcp_out.c
│   ├── timeouts.c
│   └── udp.c
├── Filelists.mk
├── FILES
├── include
│   ├── lwip
│   ├── netif
│   └── posix
├── lwipopts.h
├── lwippools.h
└── netif
    ├── ethernet.c
    ├── ethernetif.c
    ├── FILES
    ├── lowpan6.c
    ├── ppp
    └── slipif.c
```





