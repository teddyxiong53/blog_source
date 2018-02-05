---
title: mylwip编写（二）
date: 2018-02-05 10:45:50
tags:
	- lwip

---



目前已经可以查看loop网卡的ifconfig信息了。

下一步，让loop可以ping 127.0.0.1。

依赖的东西：

从ping函数开始分析，

需要lwip_socket函数，lwip_sendto函数。需要lwip_setsockopt。lwip_recvfrom。

先从这里入手。这里应该就会引入很多文件了。

```
api目录
	api_msg.c：被api_lib.c的调用。
		里面函数都是lwip_netconn_do_xxx格式。
	api_msg和api_lib联系的纽带是api_msg结构体。
	都是在api_lib里定义一个局部变量msg，然后传递给api_msg用。
	api_lib.c：被sockes.c调用。
		里面函数都是netconn_xxx格式。
```

另外，跟api_msg结构体比较类似的是tcpip_msg，这个是lwip内部跟tcpip_thread通信的一个消息结构体。



#lwip_socket函数

1、需要引入netconn_new_with_proto_and_callback函数和event_callback。

要增加api/api_lib.c文件。

增加api/api_msg.c文件。这里面的函数多是lwip_netconn_do_xxx格式。主要参数都是struct api_msg。

在include/lwip/priv目录里下增加api_msg.h文件。不拷贝了。自己写。先写需要的内容。

开始涉及pcb了。

增加core/raw.c文件。增加lwip/raw.h文件。

增加ip.h。定义了ip包头。

增加core/ip.c。因为这里面一个全局变量struct ip_globals ip_data。

围绕这个全局变量定义了几个工具宏。我感觉这些宏也没有简化什么。我就不用了。直接用ip_data变量。

增加api/netbuf.c。这个文件的函数比较简单，都是封装了pbuf和memp的一些操作。

增加api/tcpip.c。实现tcpip_send_msg_wait_sem函数。

现在梳理一下lwip_socket中new一个netconn的过程：

```
lwip_socket
	netconn_new_with_proto_and_callback
		netconn_alloc
		netconn_apimsg带参数回调函数lwip_netconn_do_newconn
			tcpip_send_msg_wait_sem
				fn(apimsg);直接把回调执行了。相当于直接调用。没有信号什么的。这是一个同步过程。
```

这个调用过程上的函数都实现了。

现在继续看lwip_socket函数下面的内容。

现在看event_callback。这个回调是注册给了netconn结构体。

netconn为什么要一个回调呢？起什么作用？

netconn_evt的类型有：接收加，接收减，发送加，发送减。这么4种。

从event_callback来看，是发了一个sem出来，给select用的。就是给select用的。

event_callback先留空。

然后就是从sockets全局数组里拿出一个来，赋值好。把索引值返回。lwip_socket完成。

# lwip_sendto

增加get_socket内部函数。

增加netbuf_ref函数。是分配了PBUF_REF类型的pbuf。

增加函数netconn_send。

增加lwip_netconn_do_send。

增加raw_send和raw_sendto。

在在include/lwip/目录下增加proto目录。下面放ip4.h。就是定义了一个struct ip_hdr以及相关的操作宏。

在core/ipv4目录下增加ip4.c文件。

我觉得这个代码有问题。

```
struct netif *
ip4_route_src(const ip4_addr_t *dest, const ip4_addr_t *src)
{
  if (src != NULL) {
    /* when src==NULL, the hook is called from ip4_route(dest) */
    struct netif *netif = LWIP_HOOK_IP4_ROUTE_SRC(dest, src); //这个宏是空的，那么netif的值就是不确定。变量没有被初始化。
    if (netif != NULL) {
      return netif;
    }
  }
  return ip4_route(dest);
}
```

增加ip4-route函数，是通过比较netif的ip地址跟目标地址跟掩码运算后是一样的，则认为应该通过这个netif发出去。

我先都实现最简单的功能。很多分支先不写。

``` 
#define LWIP_INLINE_IP_CHKSUM   1
#define CHECKSUM_GEN_IP_INLINE  1
```

把ip_output的几个函数都写了。

现在流程到netif_loop_output 了。

现在要把netif_poll这个函数加上。

在netif_poll里，又连接到ip_input函数。

ip_input函数在core/ip.c里，这个文件主要函数就这个。

ip_input就直接调用ip4-input函数。这个函数就比较复杂了。

然后调用到raw_input函数。

按道理，raw-input是拿不走的。所以马上就让icmp_input来处理。

写到这里，已经有很多函数没有实现完整，但是先还是把流程串通了。然后再从头开始一个个函数完善。

增加core/ipv4/icmp.c文件。

增加include/lwip/proto/icmp.h。就定义了icmp_echo_hdr结构体。和几个宏。

增加core/inet_chksum.c。对应的头文件include/lwip/inet_chksum.h。

增加include/lwip/proto/ip.h。就定义了IP_PROTO_ICMP/UDP/TCP这几个宏。

在icmp_input的函数内部就进行了ip_output_if输出。这个输出还是会被自己收到，然后发现是ICMP_ER的，就把包直接丢掉。这样就完成了一下ping。感觉不是。



# lwip_recvfrom

1、实现netconn_recv函数。





