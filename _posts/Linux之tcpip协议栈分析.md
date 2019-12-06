---
title: Linux之tcpip协议栈分析
date: 2019-12-05 16:55:28
tags:
	- Linux
---

1

本文档的目的是让有一定的网络协议基础的人了解到网络数据包在协议栈中的传输流程。

从以太网的开始看。

linux/if_ether.h

```
1、struct ethhdr
2、以太网包类型宏。
	0800 ip包。
	0806 arp包。
	
```

linux/ip.h

```
struct iphdr
```

linux/udp.h

```
struct udphdr
```

linux/socket.h

```
struct msghdr 
```

linux/uio.h

```
struct iovec
```

linux/net.h

```
struct socket {
	socket_state		state;

	kmemcheck_bitfield_begin(type);
	short			type;
	kmemcheck_bitfield_end(type);

	unsigned long		flags;

	struct socket_wq	*wq;

	struct file		*file;
	struct sock		*sk;
	const struct proto_ops	*ops;
};
```

net/sock.h

```
struct sock
	这个结构体比较复杂。
```

net/inet_sock.h

```
struct inet_sock 
```

linux/udp.h

```
struct udp_sock
```

linux/net.h

```
struct proto_ops
```

net/sock.h

```
struct proto
```

linux/netdevice.h

```
struct softnet_data
	这个是per-cpu的。
	
```

linux/skbuff.h

```
struct skbuff
	这个是最重要的结构体。
	
```

linux/netdevice.h

```
struct net_device 
```

net/protocol.h

```
struct inet_protosw
struct net_protocol 
```

```
static struct inet_protosw inetsw_array[] =
{
	{
		.type =       SOCK_STREAM,
		.protocol =   IPPROTO_TCP,
		.prot =       &tcp_prot,
		.ops =        &inet_stream_ops,
		.no_check =   0,
		.flags =      INET_PROTOSW_PERMANENT |
			      INET_PROTOSW_ICSK,
	},

	{
		.type =       SOCK_DGRAM,
		.protocol =   IPPROTO_UDP,
		.prot =       &udp_prot,
		.ops =        &inet_dgram_ops,
		.no_check =   UDP_CSUM_DEFAULT,
		.flags =      INET_PROTOSW_PERMANENT,
       },


       {
	       .type =       SOCK_RAW,
	       .protocol =   IPPROTO_IP,	/* wild card */
	       .prot =       &raw_prot,
	       .ops =        &inet_sockraw_ops,
	       .no_check =   UDP_CSUM_DEFAULT,
	       .flags =      INET_PROTOSW_REUSE,
       }
};
```

linux/netdevice.h

```
struct packet_type 
```

net/route.h

```
struct rtable
```

net/dst.h

```
struct dst_entry
	包的去向。描述了包的去留、下一跳这些关键信息。
```

linux/netdevice.h

```
struct napi_struct 
	提供网络处理效率的技术。
	核心理念就是采用中断唤醒查询的方式。
	适合大量短包的场景。
```



主要关注的代码目录：

net/ethernet

net/core

net/ipv4



总的入口：

```
fs_initcall(inet_init);
	proto_register(&tcp_prot, 1);
	proto_register(&udp_prot, 1);
	
```



参考资料

1、linux内核网络协议栈架构分析，全流程分析-干货

https://www.cnblogs.com/liuhongru/p/11412363.html