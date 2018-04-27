---
title: 网络之dhcp协议
date: 2018-04-27 16:08:33
tags:
	- 网络
typora-root-url: ..\
---



dhcp是局域网协议，基于udp。

主要有2个用途：

1、分配ip。

2、管理局域网的计算机。

对应的rfc文档是2131 。

使用了3个端口。

udp的67和68号端口。67为dhcp server，68为dhcp client。

另外，546号端口是dhcpv6的client。默认没有打开的。



主要目的是简化局域网的网络配置。防止地址冲突。

实现了这些功能：

1、某个ip地址在同一时刻，只能被一台dhcp客户机使用。

2、可以给某些机器分配永久的ip地址。

3、应该可以手动配置的ip地址共存。

4、兼容bootp。



#消息格式

dhcp的消息格式是基于bootp的（Bootstrap protocol）。

![](/images/网络之dhcp-协议格式.png)

op：操作码。request是1，response是2 。就这2个值。

htype：硬件类型，一般是1，表示以太网。

hlen：硬件地址长度。以太网的就是6 。

hops：不知是什么。一般是0 。

xid：会话id。随机数。

secs：举例最近一次发送ip请求过去的描述。

flags：标志位。目前只用到了bit0，如果是1，表示是广播。

client ip：客户端的ip地址，如果当前client没有ip，就填入0 。

your ip：这个是server发送给client的。

server ip：client引导的时候，需要的另一个服务器的ip地址。

gw ip：网关ip。

server name：一般写0 。

boot file name：一般 写0 。

option：下面具体讲。

## dhcp option

dhcp从bootp发展而来。

如果没有option，那么dhcp就跟bootp是一样的。

所以dhcp就是带了option的bootp。

option的格式，就像命令行的选项一样，分为两种，一种带值，一种不带值。

option占一个字节，从0到255 。

如果带值，则对应条目是

```
option len value
```

len也是一个字节。

常用的option有：

0：pad。填充用的。没有意义。

1：netmask。

50：请求的ip地址。

53：dhcp 消息类型。



我们看看53号选项。对应的value从1到13，总共13种消息类型。



我们看一下新机器加入到网络里的时候，

![](/images/网络之dhcp-新机器加入.png)



已有机器续约。

![](/images/网络之dhcp-已有机器续约.png)



# lwip里dhcp的实现

涉及的文件是

lwip/prot/dhcp.h

core/ipv4/dhcp.c

lwip/dhcp.h

##prot/dhcp.h

1、消息结构体定义。

```
struct dhcp_msg {
	u8 op;
	u8 htype;
	u8 hlen;
	u8 hops;

	u32 xid;
	u16 secs;
	u16 flags;

	u32 ciaddr;
	u32 yiaddr;
	u32 siaddr;
	u32 giaddr;

	u8 chaddr[16];
	u8 sname[64];
	u8 file[128];

	u32 cookie;//这个cookie是一个魔数。0x63 82 53 63 。
	u8 options[68];
};
```

2、dhcp client状态。

```
typedef enum  {
	DHCP_STATE_OFF = 0,
	requesting = 1,
	init = 2,
	rebooting = 3,
	rebinding = 4,
	renewing = 5,
	selecting = 6,
	informing = 7,
	checking = 8,//这个是收到offer的ip地址，调用etharp来查询是否其他人持有这个ip。这个过程要好几秒。
	permanent = 9,
	bound = 10, 
	releasing = 11,
	backing_off = 12,//就backoff的进行时。表示give up当前的ip。
} dhcp_state_enum_t;
```

3、dhcp消息类型。

```
#define DHCP_DISCOVER 1
offer 2
request 3
decline 4
ack 5
nak 6
release 7
inform 8
```

主要就是上面这3个东西。

## dhcp.h

这个里面，主要就是struct dhcp。

```
struct dhcp {
	u32 xid;
	struct dhcp_msg *msg_in;
	u8 pcb_allocated;
	u8 state;
	u8 tries;

	u8 subnet_mask_given;
	
	struct pbuf *p_out;
	struct dhcp_msg *msg_out;

	u16 options_out_len;
	u16 request_timeout;
	u16 t1_timeout;
	u16 t2_timeout;

	u16 t1_renew_time;
	u16 t2_rebind_time;

	u16 lease_used;
	u16 t0_timeout;

	u32 server_ip_addr;
	u32 offered_ip_addr;
	u32 offered_sn_mask;
	732 offered_gw_addr;

	u32 offered_t0_lease;
	u32 offered_t1_renew;
	u32 offered_t2_rebind;

};
```



##dhcp.c

dhcp.c代码长度也有近2000行。

一个重要入口是dhcp_start函数。

这里是做为dhcp client。在网卡启动的时候，

```
#if LWIP_DHCP
        /* set interface up */
        netif_set_up(ethif->netif);
        /* if this interface uses DHCP, start the DHCP client */
        dhcp_start(ethif->netif);
#else
```

```
dhcp_start函数处理过程
1、在netif结构体里，有个void *client_data指针数组。放priv数据的。
	尝试从这里获取struct dhcp，
2、如果没有获取到，就memp_alloc一个，然后赋值给netif。
	netif_set_client_data
3、dhcp_inc_pcb_refcount。
	1）用udp_new，新建一个udp的pcb。名字叫dhcp_pcb。
	2）设置dhcp_pcb选项为SOF_BROADCAST。
	3）udp_bind到68号端口。udp_connect到67号端口。
	4）udp_recv注册dhcp_pcb的接收函数为dhcp_recv。
4、dhcp_discover。	
```

下面我们看dhcp_discover。

```
dhcp_discover函数处理过程。
1、设置dhcp状态为selecting。枚举值是6 。
2、调用dhcp_create_msg创建消息。是一个DISCOVER消息。
3、发送，然后把消息销毁掉。
```

所以discover就是发了一个discover消息。

然后我们要关注的就是dhcp_recv函数。

## lwip里的dhcp单元测试

看看单元测试代码是如何写的。

代码在lwip/test/unit/dhcp/test_dhcp.c里。

代码大概有1000行。

基本思路：

1、定义一个虚拟的网卡。net_test。

```
struct netif net_test;
IP4_ADDR(&addr, 0, 0, 0, 0);
IP4_ADDR(&netmask, 0, 0, 0, 0);
IP4_ADDR(&gw, 0, 0, 0, 0);

netif_add(&net_test, &addr, &netmask, &gw, &net_test, testif_init, ethernet_input);
netif_set_up(&net_test);
```

testif_init

```
static err_t testif_init(struct netif *netif)
{
  netif->name[0] = 'c';
  netif->name[1] = 'h';
  netif->output = etharp_output;//只要是以太网网卡，都是这个。
  netif->linkoutput = lwip_tx_func;//这个就是在这里模拟硬件的行为的。
  netif->mtu = 1500;
  netif->hwaddr_len = 6;
  netif->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP;//支持广播和arp。

  netif->hwaddr[0] = 0x00;
  netif->hwaddr[1] = 0x23;
  netif->hwaddr[2] = 0xC1;
  netif->hwaddr[3] = 0xDE;
  netif->hwaddr[4] = 0xD0;
  netif->hwaddr[5] = 0x0D;

  return ERR_OK;
}
```

lwip_tx_func这个函数，本来应该是往硬件上送的。数据来源是协议栈。

现在只需要在这个函数里检查生成的dhcp包的内容就好了。



但是怎样可以把这些测试用例跑起来呢？

注册命令是可行方式。

最简单的方式，就当成app的一部分。拷贝需要的文件到

# 参考资料

1、dhcp

https://baike.baidu.com/item/DHCP/218195