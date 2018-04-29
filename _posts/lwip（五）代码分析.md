---
title: lwip（五）代码分析
date: 2018-04-25 15:11:31
tags:
	- lwip
typora-root-url: ..\
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



继续看tcp的。一切以tcp_pcb为核心来展开。

要把里面的每个成员，每个宏的用途弄清楚。



tcp_hdr里，没有表示长度的成员。有个表示头部长度的值。



现在搭建实验环境。

qemu运行rt-thread。ip配置为192.168.1.30 。（因为默认命令是用这个举例的）。

Ubuntu里配置ip为192.168.1.1 。网卡啊tap0 。

rt-thread运行tcpserv，在5000端口上。

连接时，抓包如下。

```
teddy@teddy-ubuntu:~$ sudo tcpdump -i tap0 -vv -t -X 'port 5000'
tcpdump: listening on tap0, link-type EN10MB (Ethernet), capture size 262144 bytes
IP (tos 0x0, ttl 64, id 65245, offset 0, flags [DF], proto TCP (6), length 60)
    192.168.1.1.37244 > 192.168.1.30.5000: Flags [S], cksum 0x2527 (correct), seq 2223887629, win 29200, options [mss 1460,sackOK,TS val 48835536 ecr 0,nop,wscale 7], length 0
        0x0000:  4500 003c fedd 4000 4006 b86e c0a8 0101  E..<..@.@..n....
        0x0010:  c0a8 011e 917c 1388 848d d50d 0000 0000  .....|..........
        0x0020:  a002 7210 2527 0000 0204 05b4 0402 080a  ..r.%'..........
        0x0030:  02e9 2bd0 0000 0000 0103 0307            ..+.........
IP (tos 0x0, ttl 255, id 30, offset 0, flags [none], proto TCP (6), length 44)
    192.168.1.30.5000 > 192.168.1.1.37244: Flags [S.], cksum 0xdc93 (correct), seq 6510, ack 2223887630, win 8196, options [mss 1460], length 0
        0x0000:  4500 002c 001e 0000 ff06 383e c0a8 011e  E..,......8>....
        0x0010:  c0a8 0101 1388 917c 0000 196e 848d d50e  .......|...n....
        0x0020:  6012 2004 dc93 0000 0204 05b4            `...........
IP (tos 0x0, ttl 64, id 65246, offset 0, flags [DF], proto TCP (6), length 40)
    192.168.1.1.37244 > 192.168.1.30.5000: Flags [.], cksum 0xa244 (correct), seq 1, ack 1, win 29200, length 0
        0x0000:  4500 0028 fede 4000 4006 b881 c0a8 0101  E..(..@.@.......
        0x0010:  c0a8 011e 917c 1388 848d d50e 0000 196f  .....|.........o
        0x0020:  5010 7210 a244 0000                      P.r..D..
IP (tos 0x0, ttl 255, id 31, offset 0, flags [none], proto TCP (6), length 74)
    192.168.1.30.5000 > 192.168.1.1.37244: Flags [P.], cksum 0x216f (correct), seq 1:35, ack 1, win 8196, length 34
        0x0000:  4500 004a 001f 0000 ff06 381f c0a8 011e  E..J......8.....
        0x0010:  c0a8 0101 1388 917c 0000 196f 848d d50e  .......|...o....
        0x0020:  5018 2004 216f 0000 5468 6973 2069 7320  P...!o..This.is.
        0x0030:  5443 5020 5365 7276 6572 2066 726f 6d20  TCP.Server.from.
        0x0040:  5254 2d54 6872 6561 642e                 RT-Thread.
IP (tos 0x0, ttl 64, id 65247, offset 0, flags [DF], proto TCP (6), length 40)
    192.168.1.1.37244 > 192.168.1.30.5000: Flags [.], cksum 0xa222 (correct), seq 1, ack 35, win 29200, length 0
        0x0000:  4500 0028 fedf 4000 4006 b880 c0a8 0101  E..(..@.@.......
        0x0010:  c0a8 011e 917c 1388 848d d50e 0000 1991  .....|..........
        0x0020:  5010 7210 a222 0000                      P.r.."..
```

可以看到，1.1给1.30发送SYN的时候，带了额外选项。

tcp的额外选项的格式是：

```
kind：1个字节。
len：1个字节。表示的是kind+len+info的总长度。而不是info的长度。
info：长度指定的字节数。
```

常用的选项有这7个。

![](/images/tcp常用额外选项类型.jpg)

kind为0，是选项表结束的意思。

kind为1，表示空操作。一般用来对齐4字节。

kind为2，就是设置mss。

kind为3，表示窗口扩大因子。

kind为4，表示打开sack这个选项。

kind为8，表示时间戳。



现在连接建立了。我从1.1发送“1234”这4个字符给1.30 。

```
IP (tos 0x0, ttl 64, id 65248, offset 0, flags [DF], proto TCP (6), length 45)
    192.168.1.1.37244 > 192.168.1.30.5000: Flags [P.], cksum 0x33af (correct), seq 1:6, ack 35, win 29200, length 5
        0x0000:  4500 002d fee0 4000 4006 b87a c0a8 0101  E..-..@.@..z....
        0x0010:  c0a8 011e 917c 1388 848d d50e 0000 1991  .....|..........
        0x0020:  5018 7210 33af 0000 3132 3334 0a         P.r.3...1234.
IP (tos 0x0, ttl 255, id 412, offset 0, flags [none], proto TCP (6), length 74)
    192.168.1.30.5000 > 192.168.1.1.37244: Flags [P.], cksum 0x214d (correct), seq 35:69, ack 6, win 8191, length 34
        0x0000:  4500 004a 019c 0000 ff06 36a2 c0a8 011e  E..J......6.....
        0x0010:  c0a8 0101 1388 917c 0000 1991 848d d513  .......|........
        0x0020:  5018 1fff 214d 0000 5468 6973 2069 7320  P...!M..This.is.
        0x0030:  5443 5020 5365 7276 6572 2066 726f 6d20  TCP.Server.from.
        0x0040:  5254 2d54 6872 6561 642e                 RT-Thread.
IP (tos 0x0, ttl 64, id 65249, offset 0, flags [DF], proto TCP (6), length 40)
    192.168.1.1.37244 > 192.168.1.30.5000: Flags [.], cksum 0xa1fb (correct), seq 6, ack 69, win 29200, length 0
        0x0000:  4500 0028 fee1 4000 4006 b87e c0a8 0101  E..(..@.@..~....
        0x0010:  c0a8 011e 917c 1388 848d d513 0000 19b3  .....|..........
        0x0020:  5010 7210 a1fb 0000                      P.r.....
```

现在1.1断开连接。

```
IP (tos 0x0, ttl 64, id 65250, offset 0, flags [DF], proto TCP (6), length 40)
    192.168.1.1.37244 > 192.168.1.30.5000: Flags [F.], cksum 0xa1fa (correct), seq 6, ack 69, win 29200, length 0
        0x0000:  4500 0028 fee2 4000 4006 b87d c0a8 0101  E..(..@.@..}....
        0x0010:  c0a8 011e 917c 1388 848d d513 0000 19b3  .....|..........
        0x0020:  5011 7210 a1fa 0000                      P.r.....
IP (tos 0x0, ttl 255, id 432, offset 0, flags [none], proto TCP (6), length 40)
    192.168.1.30.5000 > 192.168.1.1.37244: Flags [.], cksum 0xf40c (correct), seq 69, ack 7, win 8190, length 0
        0x0000:  4500 0028 01b0 0000 ff06 36b0 c0a8 011e  E..(......6.....
        0x0010:  c0a8 0101 1388 917c 0000 19b3 848d d514  .......|........
        0x0020:  5010 1ffe f40c 0000                      P.......
IP (tos 0x0, ttl 255, id 433, offset 0, flags [none], proto TCP (6), length 74)
    192.168.1.30.5000 > 192.168.1.1.37244: Flags [P.], cksum 0x212b (correct), seq 69:103, ack 7, win 8190, length 34
        0x0000:  4500 004a 01b1 0000 ff06 368d c0a8 011e  E..J......6.....
        0x0010:  c0a8 0101 1388 917c 0000 19b3 848d d514  .......|........
        0x0020:  5018 1ffe 212b 0000 5468 6973 2069 7320  P...!+..This.is.
        0x0030:  5443 5020 5365 7276 6572 2066 726f 6d20  TCP.Server.from.
        0x0040:  5254 2d54 6872 6561 642e                 RT-Thread.
IP (tos 0x0, ttl 64, id 7327, offset 0, flags [DF], proto TCP (6), length 40)
    192.168.1.1.37244 > 192.168.1.30.5000: Flags [R], cksum 0x2dca (correct), seq 2223887636, win 0, length 0
        0x0000:  4500 0028 1c9f 4000 4006 9ac1 c0a8 0101  E..(..@.@.......
        0x0010:  c0a8 011e 917c 1388 848d d514 0000 0000  .....|..........
        0x0020:  5004 0000 2dca 0000                      P...-...
```



现在打开lwip的调试功能。

```
finsh />tcpserv()
lwip_socket(PF_INET, SOCK_STREAM, 0) = 0
lwip_bind(0, addr=0.0.0.0 port=5000)
tcp_bind: bind to port 5000
lwip_bind(0) succeeded
lwip_listen(0, backlog=5)

TCPServer Waiting for client on port 5000...
lwip_accept(0)...
tcpip_thread: PACKET 600cb860
tcpip_thread: PACKET 600cb860
tcpip_thread: PACKET 600cb860
```

然后我从1.1连接过来。

```
tcpip_thread: PACKET 600cb860
TCP header:
+-------------------------------+
|    37250      |     5000      | (src port, dest port)
+-------------------------------+
|           1278940514          | (seq no)
+-------------------------------+
|           0000000000          | (ack no)
+-------------------------------+
| 10 |   |000010|     29200     | (hdrlen, flags (SYN 
), win)
+-------------------------------+
|    0x454f     |         0     | (chksum, urgp)
+-------------------------------+
tcp_input: packed for LISTENing connection.
TCP connection request 37250 -> 5000.
tcp_parseopt: MSS
tcp_parseopt: other
tcp_parseopt: other
tcp_parseopt: NOP
tcp_parseopt: other
tcp_enqueue_flags: queueing 6510:6511 (0x12)
tcp_output: snd_wnd 29200, cwnd 1, wnd 1, effwnd 0, seq 6510, ack 6510
tcp_output: snd_wnd 29200, cwnd 1, wnd 1, effwnd 0, seq 6510, ack 6510, i 0
tcp_output_segment: rtseq 6510
tcp_output_segment: 6510:6510
tcpip_thread: PACKET 600cb860
TCP header:
+-------------------------------+
|    37250      |     5000      | (src port, dest port)
+-------------------------------+
|           1278940515          | (seq no)
+-------------------------------+
|           0000006511          | (ack no)
+-------------------------------+
|  5 |   |010000|     29200     | (hdrlen, flags (ACK 
), win)
+-------------------------------+
|    0x9a3c     |         0     | (chksum, urgp)
+-------------------------------+
+-+-+-+-+-+-+-+-+-+-+-+-+-+- tcp_input: flags ACK 
-+-+-+-+-+-+-+-+-+-+-+-+-+-+
State: SYN_RCVD
TCP connection established 37250 -> 5000.
tcp_receive: window update 29200
tcp_receive: slow start cwnd 1461
tcp_receive: ACK for 6511, unacked->seqno 6510:6511
tcp_receive: removing 6510:6511 from pcb->unacked
tcp_receive: pcb->rttest 0 rtseq 6510 ackno 6511
tcp_process (SYN_RCVD): cwnd 4380 ssthresh 8196
tcp_output: nothing to send (00000000)
tcp_output: snd_wnd 29200, cwnd 4380, wnd 4380, seg == NULL, ack 6511
State: ESTABLISHED
lwip_accept(0) returning new sock=2 addr=192.168.1.1 port=37250
I got a connection from (192.168.1.1 , 37250)
lwip_send(2, data=600a918c, size=34, flags=0x0)
tcp_write(pcb=600c4480, data=600a918c, len=34, apiflags=1)
tcp_write: queueing 6511:6545
tcp_output: snd_wnd 29200, cwnd 4380, wnd 4380, effwnd 34, seq 6511, ack 6511
tcp_output: snd_wnd 29200, cwnd 4380, wnd 4380, effwnd 34, seq 6511, ack 6511, i 0
tcp_output_segment: rtseq 6511
tcp_output_segment: 6511:6545
tcpip_thread: PACKET 600cb860
TCP header:
+-------------------------------+
|    37250      |     5000      | (src port, dest port)
+-------------------------------+
|           1278940515          | (seq no)
+-------------------------------+
|           0000006545          | (ack no)
+-------------------------------+
|  5 |   |010000|     29200     | (hdrlen, flags (ACK 
), win)
+-------------------------------+
|    0x9a1a     |         0     | (chksum, urgp)
+-------------------------------+
+-+-+-+-+-+-+-+-+-+-+-+-+-+- tcp_input: flags ACK 
-+-+-+-+-+-+-+-+-+-+-+-+-+-+
State: ESTABLISHED
tcp_receive: window update 29200
tcp_receive: slow start cwnd 5840
tcp_receive: ACK for 6545, unacked->seqno 6511:6545
tcp_receive: removing 6511:6545 from pcb->unacked
tcp_receive: pcb->rttest 0 rtseq 6511 ackno 6545
tcp_output: nothing to send (00000000)
tcp_output: snd_wnd 29200, cwnd 5840, wnd 5840, seg == NULL, ack 6545
State: ESTABLISHED
lwip_send(2) err=0 written=34
lwip_recvfrom(2, 600cc4f4, 1024, 0x0, ..)
lwip_recvfrom: top while sock->lastdata=00000000
tcp_slowtmr: processing active pcb
tcp_slowtmr: processing active pcb
tcp_slowtmr: polling application
tcp_output: nothing to send (00000000)
tcp_output: snd_wnd 29200, cwnd 5840, wnd 5840, seg == NULL, ack 6545
tcp_slowtmr: processing active pcb
tcp_slowtmr: processing active pcb
tcp_slowtmr: polling application
```



api_msg.c里的这个函数很重要。

```
static void setup_tcp(struct netconn *conn)
{
	struct tcp_pcb *pcb;
	pcb = conn->pcb.tcp;
	tpc_arg(pcb, conn);
	tcp_recv(pcb, recv_tcp);
	tcp_sent(pcb, sent_tcp);
	tcp_poll(pcb, poll_tcp, 2);
	tcp_err(pcb, err_tcp);
}
```



do_write是tcp调用的，其他的是调用do_send。



do_write调用了tcp_write和tcp_output。

tcp_write里操作很多，是很重要的。



```
pbuf_copy在哪些地方调用了？
1、api_msg里的recv_raw里。
2、etharp.c里的etharp_query里。
3、icmp.c里的icmp_input函数。
4、netif.c里的netif_loop_output里。
5、udp.c里的udp_input函数。
主要就这5个地方。可以看出，tcp里没有进行拷贝。
拷贝的，都是无连接的。
```



# 参考资料

1、3.2.2　TCP头部选项

http://book.51cto.com/art/201306/400263.htm

