---
title: Linux内核之网络子系统（四）
date: 2018-04-18 11:03:53
tags:
	- Linux内核

---



看看协议栈的初始化。

在net/ipv4/af_inet.c里的inet_init。

这个是通过fs_initcall来调用到的。

inet_init主要内容：

```
1、注册tcp协议。proto_register(&tcp_prot, 1);
2、注册udp协议。proto_register(&udp_prot, 1);
3、注册raw协议。proto_register(&raw_prot, 1);
4、注册sock。sock_register(&inet_family_ops);
5、初始化sysctl。ip_static_sysctl_init
6、添加协议。
inet_add_protocol(&icmp_protocol, IPPROTO_ICMP) 
inet_add_protocol(&udp_protocol, IPPROTO_UDP)
inet_add_protocol(&tcp_protocol, IPPROTO_TCP)
inet_add_protocol(&igmp_protocol, IPPROTO_IGMP)
7、注册协议。
for (q = inetsw_array; q < &inetsw_array[INETSW_ARRAY_LEN]; ++q)
		inet_register_protosw(q);
8、arp_init。
9、ip_init。
10、tcp_v4_init。
11、tcp_init。
12、udp_init。
13、udplite4_register。
14、icmp_init。
15、ipv4_proc_init。
16、ipfrag_init。
17、dev_add_pack(&ip_packet_type）。
```

这个函数里很有料啊。

我们先看看proto_register这个函数做了什么。

这个函数在net/core/sock.c里。

```
主要做的事情，就是把tcp_prot添加到一个全局的list里面。
```

涉及到include/net/sock.h里的一个结构体。

```
struct proto {
  void (*close)(struct socke *sk, long timeout);
  int (*connect)(struct sock sk, struct sockaddr *uaddr, int addr_len);
  ...
}
```

我们要看看tcp_prot这个全局变量在哪里定义。

在net/ipv4/tcp_ipv4.c里。

```
struct proto tcp_prot = {
  .name ="TCP",
  .owner = THIS_MODULE,
  .close = tcp_close,
  ...
};
```

udp_prot在net/ipv4/udp.c里定义。

```
struct proto udp_prot = {
  .name = "UDP",
  .close = udp_lib_close,
  ...
}
```

raw_prot在net/ipv4/raw.c里定义。

看到这里，我们有必要看一下net目录下的文件分布情况了。

```
teddy@teddy-ubuntu:~/work/linux2.6/linux/net$ tree -L 1
.
├── 802：下面就10个文件。看起来不复杂。
├── 8021q：8个文件，也不多。
├── 9p：是一种远程文件系统协议。我觉得跟nfs差不多。
├── activity_stats.c：活动统计。proc文件系统里的东西。
├── appletalk：苹果的协议。
├── atm：过时的协议了。
├── ax25：不管。
├── bluetooth：蓝牙协议栈。
├── bridge：网桥。
├── caif：
├── can：can总线？就5个文件。
├── compat.c
├── core：核心目录。有dev.c、skbuff.c、sock.c等。
├── dcb：就一个文件。不知做什么的。
├── dccp：文件较多。
├── decnet：
├── dsa
├── econet
├── ethernet：这个重点看。就2个文件，一个eth.c，一个pe2.c。
├── ieee802154
├── ipv4：重点。70个文件左右。
├── ipv6：暂时不看。
├── ipx
├── irda
├── iucv
├── Kconfig
├── key
├── l2tp
├── lapb
├── llc
├── mac80211
├── Makefile
├── netfilter：很复杂。不管。
├── netlabel
├── netlink：重点。就2个文件。af_netlink.c和genelink.c。
├── netrom
├── nonet.c
├── packet
├── phonet
├── rds
├── rfkill
├── rose
├── rxrpc
├── sched
├── sctp
├── socket.c：
├── sunrpc
├── sysctl_net.c
├── tipc
├── TUNABLE
├── unix
├── wanrouter
├── wimax
├── wireless
├── x25
└── xfrm
```

我看不少目录下，都有af_xxx.c这种文件，看看里面是些什么内容。

以netlink的为例。

入口函数是netlink_proto_init。

```
int err = proto_register(&netlink_proto, 0);
```

可见，这个也是用来注册协议的。

回过头来，继续看inet_init函数里的内容。

```
sock_register(&inet_family_ops);
```

inet_family_ops这个全局变量定义在net/ipv4/af_inet.c里。

```
struct net_proto_family inet_family_ops = {
  .family = PF_INET,
  .create = inet_create,
  .owner = THIS_MODULE,
};
```

这个变量里没有太多内容。

sock_register这个则比较重要，我搜索了一下，每一种协议里，都有调用函数来这么一下。

```
sock_register(&bt_sock_family_ops);
sock_register(&inet_family_ops);
sock_register(&unix_family_ops);
sock_register(&netlink_family_ops);
```

我就重点看看这几个的。

最重要的就是create这个函数指针，每个协议的不一样。

sock_register，是放入到在net/socket.c里的一个全局数组里去了。

```
static const struct net_proto_family *net_families[NPROTO];
```

函数内部处理很简单。

再看`inet_add_protocol(&icmp_protocol, IPPROTO_ICMP) `这个。

icmp_protocol内容：

```
struct net_protocol icmp_protocol = {
  .handler = icmp_rcv,
  .no_policy = 1,
  .netns_ok = 1,
};
```

net_protocol这个东西，

```
static const struct net_protocol igmp_protocol = {
static const struct net_protocol tcp_protocol = {
static const struct net_protocol udp_protocol = {
static const struct net_protocol icmp_protocol = {
```

inet_add_protocol就是加入到一个全局数组里去。

```
const struct net_protocol *inet_protos[MAX_INET_PROTOS];//256 个
```

继续看这个。

```
for (q = inetsw_array; q < &inetsw_array[INETSW_ARRAY_LEN]; ++q)
		inet_register_protosw(q);
```

inetsw_array这个全局数组，很重要。

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



inet_init函数看得差不多了。

我们继续从arp_init这个点进行深入。函数很简单。

```
void __init arp_init(void)
{
	neigh_table_init(&arp_tbl);
	dev_add_pack(&arp_packet_type);
	arp_proc_init();
#ifdef CONFIG_SYSCTL
	neigh_sysctl_register(NULL, &arp_tbl.parms, "ipv4", NULL);
#endif
	register_netdevice_notifier(&arp_netdev_notifier);
}
```



涉及的概念和对应的结构体

```
struct packet_type。
```

在以太网上，包类型有：

1、最常见的ip包（0x0800）、arp包（0x0806）。

2、还有rarp包（0x0835）。

3、PPPOE的发现包（0x8863）等等。

在linux/if_ether.h里。

```
#define ETH_P_IP	0x0800		/* Internet Protocol packet	*/
#define ETH_P_X25	0x0805		/* CCITT X.25			*/
#define ETH_P_ARP	0x0806		/* Address Resolution packet	*/
```

是通过dev_add_pack进行注册的。

```
dev_add_pack(&ip_packet_type);
dev_add_pack(&vlan_packet_type);
...
```

看arp的proc信息。

```
static int __init arp_proc_init(void)
{
	return register_pernet_subsys(&arp_net_ops);
}
```

register_pernet_subsys这个函数在net/core/net_namespace.c里调用的。

看看arp命令和arp proc文件的内容。

```
/proc/800/net # arp
? (192.168.0.1) at 3a:0e:87:45:88:e3 [ether]  on eth0
/proc/800/net # cat arp 
IP address       HW type     Flags       HW address            Mask     Device
192.168.0.1      0x1         0x2         3a:0e:87:45:88:e3     *        eth0
/proc/800/net # 
```

arp命令的输出，就是把proc里的arp文件解析，然后用特定的格式打印出来。



我们看一下sendto函数在内核栈里的调用过程。

对应的系统调用在这里。

```
./net/socket.c:1647:SYSCALL_DEFINE6(sendto, int, fd, void __user *, buff, size_t, len,
```

```
sendto系统调用
	sock_sendmsg
		__sock_sendmsg 这里开始引入struct kiocb iocb;这个变量。不过在udp_sendmsg里完全没用。
			sock->ops->sendmsg //这个就挂接到具体的协议了。例如udp。
				udp_sendmsg
					ip_route_output_flow
```

