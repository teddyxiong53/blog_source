---
title: Linux之网络栈分析
date: 2018-03-05 20:12:57
tags:
	- Linux
	- 网络

---



选择从上层往下跟的方式来了解网络栈的情况。

另外跟rt-thread里的lwip进行对比分析。



1、socket函数的实现。

首先要看的一个文件是socket.h。linux里的这个，就是定义了一些宏和结构体。

实现在net/socket.c里。

```
SYSCALL_DEFINE3(socket, int, family, int, type, int, protocol)
	sock_create
		__sock_create
			security_socket_create//在security/security.c里，做了一些安全的保证。
			sock_alloc
			pf->create调用到net/ipv4/af_inet.c里的inet_create。
				sk_alloc在net/core/sock.c里。
					sk_prot_alloc
						kmem_cache_alloc
			security_socket_post_create
						
```



struct socket定义在linux/net.h里。

```
struct socket {
	socket_state		state;
	short			type;
	unsigned long		flags;
	struct socket_wq __rcu	*wq;
	struct file		*file;//socket也算是一个文件。
	struct sock		*sk;//这个很复杂的结构体。在net/sock.h里定义。
	const struct proto_ops	*ops;
}
```

2、bind的实现。

函数最后都会调用到af_inet.c里的这个结构体里的指针。

```
const struct proto_ops inet_stream_ops = {
	.family		   = PF_INET,
	.owner		   = THIS_MODULE,
	.release	   = inet_release,
	.bind		   = inet_bind,
	.connect	   = inet_stream_connect,
	.socketpair	   = sock_no_socketpair,
	.accept		   = inet_accept,
	.getname	   = inet_getname,
	.poll		   = tcp_poll,
	.ioctl		   = inet_ioctl,
	.listen		   = inet_listen,
	.shutdown	   = inet_shutdown,
	.setsockopt	   = sock_common_setsockopt,
	.getsockopt	   = sock_common_getsockopt,
	.sendmsg	   = inet_sendmsg,
	.recvmsg	   = inet_recvmsg,
	.mmap		   = sock_no_mmap,
	.sendpage	   = inet_sendpage,
	.splice_read	   = tcp_splice_read,
#ifdef CONFIG_COMPAT
	.compat_setsockopt = compat_sock_common_setsockopt,
	.compat_getsockopt = compat_sock_common_getsockopt,
	.compat_ioctl	   = inet_compat_ioctl,
#endif
};
```

3、看sendmsg的实现。





看ipv4的inet_init的初始化过程。

```
inet_init
	proto_register(&tcp_prot, 1);
	udp
	raw
	ping
	sock_register(&inet_family_ops);
	ip_static_sysctl_init();
	inet_add_protocol(&icmp_protocol, IPPROTO_ICMP)
	inet_add_protocol(&udp_protocol, IPPROTO_UDP) 
	arp_init();
	tcp_v4_init();
	tcp_init();
	udp_init();
	udplite4_register();
	ping_init();
	ipv4_proc_init();
	ipfrag_init();
	dev_add_pack(&ip_packet_type);
	ip_tunnel_core_init();
```

