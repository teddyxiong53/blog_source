---
title: lwip（五）代码分析
date: 2018-04-25 15:11:31
tags:
	- lwip

---



本文记录阅读lwip代码的一些理解。



链路层头长度是16字节。那是除了6字节mac+6字节mac+2字节类型，还有2个字节的不知道是啥。可能是crc。

网络层是20字节。传输层的头也是20字节。

```
PBUF_LINK_ENCAPSULATION_HLEN:0, PBUF_LINK_HLEN :16, PBUF_IP_HLEN :20, PBUF_TRANSPORT_HLEN:20
```

分配一个传输层的pbuf，就会把传输层的header、网络层的header、链路层的header都预留好空间的。

pbuf的payload，就在自己后面。

因为分配的时候，是这样分配的。

```
mem_size_t alloc_len = LWIP_MEM_ALIGN_SIZE(SIZEOF_STRUCT_PBUF + offset) + LWIP_MEM_ALIGN_SIZE(length);
p = (struct pbuf*)mem_malloc(alloc_len);
```



```
lwip几大基础组件。
1、pbuf。
	单链表。
	1个buf，2个长度。
	类型、flags。
	ref引用计数。
	
2、netbuf。
	就4个成员，2个是pbuf指针。
	一个ip地址，一个端口号。
	
PBUF_REF的，就是数据区域是不跟pbuf挨着分配，是应用层就分配好的。
这个只需要分配一个小的pbuf，把payload指向之前有的数据区域。
sendto里面就是这么做的。
err = netbuf_ref(&buf, data, short_size);
ping这个程序，就会调用到raw_sendto函数。

3、netconn。
	1）连接类型。
	2）连接状态。
	3）pcb。union类型。
	4）最近的错误码。
	5）完成信号量。
	6）recv邮箱。
	7）accept邮箱。
	8）socket（int类型）
	9）发送超时
	10）接收超时。
	11）回调函数。netconn_callback。
	主要就是这11个。其余先忽略。
	
4、ip_pcb。
	本地ip，对端ip。
	socket选项。
	tos。服务类型。
	ttl。
	就这5个成员。
5、raw_pcb。
	包括ip_pcb。
	next指针。
	协议类型（u8）。
	接收函数。以及函数的参数。
	也就这5个成员。
	
6、udp_pcb。
	包括ip_pcb。
	next指针。
	flags。
	本地port和对端port。
	接收函数。以及函数的参数。
	也就这6个成员。
	
7、tcp_pcb。
	这个就很多了。暂时不展开看。
	
8、lwip_sock。
	这个是最上层的。里面主要就是一个netconn指针。其余都是int类型的事件等等。
```

```
api_msg
	1、netconn指针。
	2、错误码。
	3、一个union。成员名字叫msg。
		里面的可能有：
		1）b。netbuf指针。给lwip_netconn_do_send用的。
		2）n。里面就是一个u8的proto。给newconn用的。
		3）bc。里面是ip地址和port。给bind和connect用的。
		4）ad。里面是ip地址，port和一个u8的local。给getaddr用的。
		5）w。里面是buf、len、flag。给write用的。
		6）r。里面就是一个len。给recv用的。
		7）sd。给close用的。
```



mac多播地址是这样。

```
/** The 24-bit IANA IPv4-multicast OUI is 01-00-5e: */
#define LL_IP4_MULTICAST_ADDR_0 0x01
#define LL_IP4_MULTICAST_ADDR_1 0x00
#define LL_IP4_MULTICAST_ADDR_2 0x5e
```

根据ping.c的过程分析对应的接口。

输出的流程是。

```
lwip_sendto
	netconn_send
		lwip_netconn_do_send
			raw_sendto
				ip_output_if
					ip4_output_if_src
						调用到netif->output
netif->output 在ethernetif.c里，被赋值为etharp_output。
	etharp_output//在etharp.c里。
		ethernet_output //在ethernet.c里。
			netif->linkoutput //在ethernetif.c里，被赋值为etharp_output。ethernetif_linkoutput
				ethernetif_linkoutput //就在ethernetif.c里
					发送tx邮箱。等待ack。eth_tx_thread_mb
						 //在ethernetif.c里的发送线程里。
							smc911x_emac_tx，把pbuf拷贝到一个静态的数组里，2048长度的。
```



输入的流程是：

```
smc911x_isr 网卡中断函数。
	eth_device_ready //在ethernetif.c里。
		rt_mb_send(&eth_rx_thread_mb
			eth_rx_thread_entry 等待这个邮箱。
				device->eth_rx对应smc911x_emac_rx
				device->netif->input(p, device->netif)
					netifapi_netif_add(netif, &ipaddr, &netmask, &gw, dev, eth_netif_device_init, tcpip_input);注册了tcpip_input对应input指针。
					tcpip_inpkt(p, inp, ethernet_input);
					所以最后还是调用到ethernet_input函数。
						ip4_input(p, netif);
						etharp_input(p, netif);
						我们从ip4-input继续跟。
							ip4_reass(p);
							raw_input(p, inp) //这个处理不了，才会给下面处理。
							tcp_input。
							udp_input
						
```

注意一个叫recv_raw的函数。这个函数在api_msg.c里。

这个函数注册进去，会在raw_input的里面调用。这里会post邮箱。



看tcp的。

```
1、tcp.h。
	定义tcp_state枚举。
	定义tcp_pcb结构体。
	声明tcp_xxx函数。包括
		tcp_new。这些函数，对于socket接口来说，我们不调用。
		socket调用到的是tcp_alloc。不过tcp_new就是对tcp_alloc的简单封装。
		可以说是一模一样。
我们看看tcp_alloc后的初始化怎么赋值的。
TCP_SND_BUF这个是8196字节。
TCP_TTL 是255 。
INITIAL_MSS 是536 。

#define RT_MEMP_NUM_NETCONN 8
#define RT_LWIP_PBUF_NUM 16
#define RT_LWIP_RAW_PCB_NUM 4
#define RT_LWIP_UDP_PCB_NUM 4
#define RT_LWIP_TCP_PCB_NUM 4
#define RT_LWIP_TCP_SEG_NUM 40
#define RT_LWIP_TCP_SND_BUF 8196
#define RT_LWIP_TCP_WND 8196

看看bind是怎么做的。
就是把对应的pcb挂到一个链表里。用TCP_REG这个宏。
看listen。
也是挂到一个链表里。
看accept。
sys_arch_mbox_fetch等邮箱数据。邮箱数据就是一个netconn。
这个netconn的分配，是在listen的时候，注册的一个函数里做的。
tcp_accept(msg->conn->pcb.tcp, accept_function);

event_callback，这个就是注册给netconn的回调。里面做的事情挺多的。

accept重点是分配了一个netconn结构体。

看recv。
netconn_recv_tcp_pbuf
	lwip_netconn_do_recv
		tcp_recved
			tcp_ack_now(pcb);
			tcp_output(pcb);//确认收到某段数据了。 
				tcp_output_segment
					ip_output_if

看send。
send
	netconn_write_partly
		lwip_netconn_do_write
			lwip_netconn_do_writemore
				tcp_sndbuf
				tcp_write
```

```

tcp.c里，操作的核心数据是tcp_pcb。
api_lib.c里，操作的核心数据是netconn。
api_msg.c里，操作的核心数据是api_msg。
```

