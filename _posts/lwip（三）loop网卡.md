---
title: lwip（三）loop网卡
date: 2018-02-03 18:05:39
tags:
	- lwip

---



loop网卡很简单的一个东西，我从这里切入，看看系统里有哪些处理。

默认loop没有打开。要在lwipopt.h里打开。

所有代码都是在src/core/netif.c文件里。

1、定义全局变量。

```
static struct netif loop_netif;
```

2、netif_init里。

```
1、赋值
loop_addr 127.0.0.1
loop_gw 127.0.0.1
loop_netmask 255.0.0.0 
2、向系统加入网卡。
netif_add(&loop_netif, addr/gw/netmask, init func, input func)
3、link up
netif_set_link_up对应NETIF_FLAG_LINK_UP
4、up
netif_set_up，对应NETIF_FLAG_UP
```

3、init func。上面函数里传递进去的。

传递进去就直接用了，不是注册。

netif_loopif_init

```
1、netif的名字只有2个字节的长度，loop的就给lo。
2、把netif_loop_output_ipv4赋值给netif的output指针。这样网卡的input和output都指定了。input函数是tcpip_input。
```

4、netif_loop_output_ipv4。



# ping场景分析

我们就以ping 127.0.0.1这个场景来进行分析。

从ping命令这里开始读。

发送流程：

```
ping
	lwip_sendto
		netconn_send
			lwip_netconn_do_send
				raw_sendto:这一步开始得到了netif指针了。
					ip_output_if
						ip4_output_if
							ip4_output_if_src
								netif_loop_output
							
```

接收流程：

```
netif_loop_output
	netif_poll ：触发了这个。
		ip_input
			ip4_input
				
```



我们可以用gdb来调试一下。

但是不行。网络相关的内容，用gdb调试很难。因为要相互协调的。

```
.gdbinit:2: Error in sourced command file:
Remote communication error.  Target disconnected.: Connection reset by peer.
```

使用加打印的方式吧。

可以改配置，把lwip的debug打开。先只打开ICMP的看看。

这样只多了一行打印。

```
msh />ping 127.0.0.1
icmp_input: ping 多了这一行打印。
60 bytes from 127.0.0.1 icmp_seq=0 ttl=255 time=3 ticks
```

把开关调成这个样子。

```
#define SYS_DEBUG                   LWIP_DBG_ON
#define ETHARP_DEBUG                LWIP_DBG_OFF
#define PPP_DEBUG                   LWIP_DBG_OFF
#define MEM_DEBUG                   LWIP_DBG_OFF
#define MEMP_DEBUG                  LWIP_DBG_ON
#define PBUF_DEBUG                  LWIP_DBG_ON
#define API_LIB_DEBUG               LWIP_DBG_ON
#define API_MSG_DEBUG               LWIP_DBG_ON
#define TCPIP_DEBUG                 LWIP_DBG_ON
#define NETIF_DEBUG                 LWIP_DBG_ON
#define SOCKETS_DEBUG               LWIP_DBG_ON
#define DNS_DEBUG                   LWIP_DBG_OFF
#define AUTOIP_DEBUG                LWIP_DBG_OFF
#define DHCP_DEBUG                  LWIP_DBG_OFF
#define IP_DEBUG                    LWIP_DBG_OFF
#define IP_REASS_DEBUG              LWIP_DBG_OFF
#define ICMP_DEBUG                  LWIP_DBG_ON
#define IGMP_DEBUG                  LWIP_DBG_OFF
#define UDP_DEBUG                   LWIP_DBG_OFF
#define TCP_DEBUG                   LWIP_DBG_ON
#define TCP_INPUT_DEBUG             LWIP_DBG_ON
#define TCP_OUTPUT_DEBUG            LWIP_DBG_ON
#define TCP_RTO_DEBUG               LWIP_DBG_ON
#define TCP_CWND_DEBUG              LWIP_DBG_ON
#define TCP_WND_DEBUG               LWIP_DBG_OFF
#define TCP_FR_DEBUG                LWIP_DBG_OFF
#define TCP_QLEN_DEBUG              LWIP_DBG_OFF
#define TCP_RST_DEBUG               LWIP_DBG_OFF
```

然后ping一下。我让ping只发一次包。（改ping的源代码）。

```
msh />ping 127.0.0.1

lwip_socket(PF_INET, SOCK_RAW, 1) = 0
lwip_sendto(0, data=60125aac, short_size=40, flags=0x0 to=127.0.0.1 port=0
pbuf_alloc(length=0)
pbuf_alloc(length=0) == 6011e1e8
netconn_send: sending 40 bytes //这一步是一个节点。
pbuf_alloc(length=0)
pbuf_alloc(length=0) == 60125ae0
pbuf_chain: 60125ae0 references 6011e1e8
pbuf_header: old 60125b14 new 60125b00 (20)
pbuf_alloc(length=60)
pbuf_alloc(length=60) == 60125b20
pbuf_copy(60125b20, 60125ae0)
pbuf_copy: end of chain reached.
pbuf_free(60125ae0)
pbuf_free: deallocating 60125ae0
pbuf_free: 6011e1e8 has ref 1, ending here.
tcpip_thread: CALLBACK 6011d350//这个是主线程收到了邮箱。
pbuf_alloc(length=60)
pbuf_alloc(length=60) == 60125b88
pbuf_copy(60125b88, 60125b20)
pbuf_copy: end of chain reached.
pbuf_header: old 60125b40 new 60125b54 (-20)
icmp_input: ping  //这里自己收到了自己的ping包了。
pbuf_header: old 60125b54 new 60125b30 (36)
pbuf_header: old 60125b30 new 60125b54 (-36)
pbuf_header: old 60125b54 new 60125b40 (20)
pbuf_alloc(length=60)
pbuf_alloc(length=60) == 60125be0
pbuf_copy(60125be0, 60125b20)
pbuf_copy: end of chain reached.
pbuf_free(60125b20)
pbuf_free: deallocating 60125b20
pbuf_alloc(length=60)
pbuf_alloc(length=60) == 60125ae0
pbuf_copy(60125ae0, 60125be0)
pbuf_copy: end of chain reached.
pbuf_free(60125ae0)
pbuf_free: deallocating 60125ae0
pbuf_header: old 60125c00 new 60125c14 (-20)
pbuf_free(60125be0)
pbuf_free: deallocating 60125be0
tcpip_thread: CALLBACK 6011d314 //这边是自己回复的邮箱到了主线程。
pbuf_free(6011e1e8)
pbuf_free: deallocating 6011e1e8
lwip_recvfrom(0, 60117624, 64, 0x0, ..)
lwip_recvfrom: top while sock->lastdata=00000000
netconn_recv_data: received 6011bb30, len=60
lwip_recvfrom: netconn_recv err=0, netbuf=6011bb30
lwip_recvfrom: buflen=60 len=64 off=0 sock->lastoffset=0
lwip_recvfrom(0): addr=127.0.0.1 port=1 len=60
lwip_recvfrom: deleting netbuf=6011bb30
pbuf_free(60125b88)
pbuf_free: deallocating 60125b88
60 bytes from 127.0.0.1 icmp_seq=0 ttl=255 time=4 ticks
lwip_close(0)
```



大概流程就是上面列出来的。现在要认真分析每一步。

1、lwip_sendto。

```
输入：
	1、int的socket
	2、data及长度。
	3、sockaddr，里面含有127.0.0.1这个ip地址，没有port
处理：
	1、先get到lwip_sock，用socket这个int数。
	2、
```

