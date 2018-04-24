---
title: lwip（四）架构分析
date: 2018-03-12 11:02:16
tags:
	- lwip
typora-root-url: ..\
---



lwip的调用层次图。

![lwip架构](/images/lwip架构.png)



#通信机制

采用的是主线程加消息的设计方式。这个跟Android上的ui线程是一样的。

其他线程不能执行操作，而是要发消息给主线程来操作。

整个机制不复杂。

其他线程跟主线程的通信是用mbox来做的。



#消息设计

```
enum tcpip_msg_type {
  TCPIP_MSG_API,
  TCPIP_MSG_API_CALL,
  TCPIP_MSG_INPKT,
```

主要就是API和INPKT这2个。CALL这个很少用。

INPKT只在收包的时候用。其余的都是API消息。

然后设计的tcpip_msg结构体。就是tcpip_msg_type。然后加上各种类型的struct得到的 一个union。



# 结构体设计

![lwip结构体设计](/images/lwip结构体设计.png)



所谓bind过程，就是把ip地址和端口跟tcp的pcb结构体里的成员进行赋值。

而这个pcb对应netconn，也就是对应lwip_socket，也就是对应sockfd了。

再看listen。



accept。

```
里面其实就是在等一个acceptmbox。邮箱的内容就是一个netconn指针。
那么这个指针的内容谁来分配的呢？
有accept的前提，是有tcp连接进来，那就是有tcp包进来嘛。
所以是tcp_input，然后一路调用到对应的回调accept_function
	netconn_alloc
	sys_mbox_trypost(&conn->acceptmbox,
```



recv

```
recv
	lwip_recv
		lwip_recvfrom
			netconn_recv_tcp_pbuf
				netconn_recv_data
					发消息，do_recv。
```





# 代码文件层次

```
teddy@teddy-ubuntu:~/work/rt-thread/rt-thread/components/net/lwip-1.4.1/src$ tree
.
├── api
│   ├── api_lib.c：netconn_xx接口，被sockets.c里的调用。
│   ├── api_msg.c：do_xx接口，被api_lib.c里的调用。
│   ├── err.c：就一个lwip_strerr接口。
│   ├── netbuf.c：netbuf_alloc、netbuf_free等接口。
│   ├── netdb.c：lwip_gethostbyname等接口。
│   ├── netifapi.c：netifapi_netif_add接口，被netif目录下的ethernetif.c调用。
│   ├── sockets.c：lwip_socket等接口。
│   └── tcpip.c：对外的初始化接口。tcpip_init。主线程tcpip_thread。
├── arch
│   ├── include
│   │   └── arch
│   │       ├── bpstruct.h
│   │       ├── cc.h
│   │       ├── epstruct.h
│   │       ├── perf.h
│   │       └── sys_arch.h
│   └── sys_arch.c：移植需要实现的。各种基础函数。
├── core
│   ├── def.c：htons等4个函数。
│   ├── dhcp.c：dhcp_xx函数，对外接口dhcp_network_changed。被netif.c里调用。在网卡up的时候。
│   ├── dns.c：dns_xx函数。对外接口dns_init。
│   ├── init.c：一个函数，lwip_init。被tcpip_init调用。
│   ├── ipv4
│   │   ├── autoip.c：这个是在dhcp失败之后，生成一个ip地址，有防止冲突的机制。
│   │   ├── icmp.c：
│   │   ├── igmp.c
│   │   ├── inet.c：就包含了头文件，没有什么意义。
│   │   ├── inet_chksum.c：就是inet_chksum函数。
│   │   ├── ip_addr.c：ipaddr_aton和ipaddr_ntoa。
│   │   ├── ip.c：ip层。ip_input和ip_output。
│   │   └── ip_frag.c：ip_frag函数。
│   ├── ipv6
│   │   ├── icmp6.c
│   │   ├── inet6.c
│   │   ├── ip6_addr.c
│   │   ├── ip6.c
│   │   └── README
│   ├── mem.c：实现mem_malloc和mem_free函数。
│   ├── memp.c：实现memp_malloc和memp_free函数。
│   ├── netif.c：netif_init、netif_add。
│   ├── pbuf.c：pbuf_alloc、pbuf_free。
│   ├── raw.c：raw socket的实现。raw_send、raw_recv。
│   ├── snmp
│   │   ├── asn1_dec.c
│   │   ├── asn1_enc.c
│   │   ├── mib2.c
│   │   ├── mib_structs.c
│   │   ├── msg_in.c
│   │   └── msg_out.c
│   ├── stats.c：统计信息。
│   ├── sys.c：就一个sys_msleep函数。
│   ├── tcp.c：tcp_alloc、tcp_bind。
│   ├── tcp_in.c：tcp_input函数。
│   ├── tcp_out.c：tcp_output函数。
│   ├── timers.c：超时函数。
│   └── udp.c：udp_input和udp_output函数。
├── FILES
├── include
│   ├── ipv4
│   │   └── lwip
│   │       ├── autoip.h
│   │       ├── icmp.h
│   │       ├── igmp.h
│   │       ├── inet_chksum.h
│   │       ├── inet.h
│   │       ├── ip_addr.h
│   │       ├── ip_frag.h
│   │       └── ip.h
│   ├── ipv6
│   │   └── lwip
│   │       ├── icmp.h
│   │       ├── inet.h
│   │       ├── ip_addr.h
│   │       └── ip.h
│   ├── lwip
│   │   ├── api.h
│   │   ├── api_msg.h
│   │   ├── arch.h
│   │   ├── debug.h
│   │   ├── def.h
│   │   ├── dhcp.h
│   │   ├── dns.h
│   │   ├── err.h
│   │   ├── init.h
│   │   ├── mem.h
│   │   ├── memp.h
│   │   ├── memp_std.h
│   │   ├── netbuf.h
│   │   ├── netdb.h
│   │   ├── netifapi.h
│   │   ├── netif.h
│   │   ├── opt.h
│   │   ├── pbuf.h
│   │   ├── raw.h
│   │   ├── sio.h
│   │   ├── snmp_asn1.h
│   │   ├── snmp.h
│   │   ├── snmp_msg.h
│   │   ├── snmp_structs.h
│   │   ├── sockets.h
│   │   ├── stats.h
│   │   ├── sys.h
│   │   ├── tcp.h
│   │   ├── tcp_impl.h
│   │   ├── tcpip.h
│   │   ├── timers.h
│   │   └── udp.h
│   ├── netif
│   │   ├── etharp.h
│   │   ├── ethernetif.h
│   │   ├── ppp_oe.h
│   │   └── slipif.h
│   └── posix
│       ├── netdb.h
│       └── sys
│           └── socket.h
├── lwipopts.h
└── netif
    ├── etharp.c
    ├── ethernetif.c
    ├── FILES
    ├── ppp目录。
    └── slipif.c
```

另外还有驱动代码。以stm32的dm9000为例。

要实现eth_device的eth_rx和eth_tx函数。





# pbuf的层次

pbuf涉及到2个枚举。

```
typedef enum {
  PBUF_TRANSPORT,
  PBUF_IP,
  PBUF_LINK,
  PBUF_RAW
} pbuf_layer;

typedef enum {
  PBUF_RAM, /* pbuf data is stored in RAM */
  PBUF_ROM, /* pbuf data is stored in ROM */
  PBUF_REF, /* pbuf comes from the pbuf pool */
  PBUF_POOL /* pbuf payload refers to RAM */
} pbuf_type;
```

我们先看pbuf_layer这个枚举。

层次的使用是这样的规律。

在dns、dhcp这些应用层，是使用PBUF_TRANSPORT这样来分配的。

规律就是，当前层分配，是用下一层的layer。

至于pbuf_type，我们就只关注ram和ref就好了。











现在看看tcp协议的内容。

思路的话，我觉得以tcp的状态机为核心，根据状态变迁的过程来看。

首先是LISTEN状态。

好像这样看不下去。还是从代码的入口来看。

主要c文件是3个：tcp.c、tcp_in.c、tcp_out.c。

# tcp.c

1、tcp_init。空的。

2、tcp_tmr。

```
1、250ms调用一次。
2、
	tcp_fasttmr
		处理tcp_active_pcbs的。
	tcp_slowtmr
		除了处理tcp_active_pcbs。
		还处理tcp_tw_pcbs。
```



