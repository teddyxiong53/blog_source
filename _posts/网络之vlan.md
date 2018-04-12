---
title: 网络之vlan
date: 2017-08-09 22:45:15
tags:
	- 网络

---

# 什么是vlan

讲vlan，就要先讲lan。lan是局域网。我们家里面的几台电脑组成的网络就是一个局域网。

vlan就是虚拟局域网。vlan的边界由路由器来划分。

广播域是指广播帧可以到达的范围。也就是可用直接通信的范围。广播帧无法透过路由器。

为什么要划分广播域呢？如果没有广播域，当一个网络内计算机很多的时候，进行一次arp广播的成本就很高，造成很多不必要的负载。而网络中的广播其实是非常多而且频繁的。

进行广播域分割的时候，一般都必须使用路由器，一般路由器有几个接口，就可以划分几个广播域。

这就带来一个明显的问题，就是路由器的网络接口一般是1到4个，数量不多。

vlan的出现，就是为了用交换机来实现广播域的分割。

只有vlan id一致的，广播帧才能传递过去。



vlan是一组逻辑上的设备和用户，它们不受物理位置的限制，可以根据部门、功能等条件组织起来，它们之间相互通信就像在同一个网段了一样。

vlan是一种比较新的技术，工作在osi模型的第二层和第三层。

一个vlan就是一个广播域。

vlan之间的通信是靠第三层的路由器来完成。

相比传统的lan技术，vlan的优点有：

1、设备的管理开销更小。

2、可以控制广播活动。

3、提高安全性。

# 发展历史

1、1999年，IEEE发布了用于标准化vlan实现方案的802.1Q协议草案。这个草案，一般叫做“Dot One Q”

2、交换技术的发展，也加快了vlan的应用速度。



vlan的出现，就是为了解决以太网的广播问题和安全性。

它是通过在以太网帧的基础上增加了vlan投。用vlan id把用户划分为更小的组。

# 帧格式

标准的以太网帧

```
|dst mac | src mac | type | data | crc|
```

加入vlan字段的以太网帧

```
|dst mac| scr mac | tpid|tci| type| data | crc |
```

tpid：2个字节。0x8100 。这个值固定不变。

tci：2个字节。低12bit为vlan id。



# lwip里的vlan

是受这个宏的控制的。

```
#define ETHARP_SUPPORT_VLAN             0
```

都限制在etharp.c这个文件里。不多。

1、etharp_ip_input函数里。

```
#if ETHARP_SUPPORT_VLAN
  if (ethhdr->type == PP_HTONS(ETHTYPE_VLAN)) {//看是不是0x8100，是就说明是vlan帧。需要跳过的。
    iphdr = (struct ip_hdr *)((u8_t*)ethhdr + SIZEOF_ETH_HDR + SIZEOF_VLAN_HDR);
  }
#endif /* ETHARP_SUPPORT_VLAN */
```

2、etharp_arp_input函数。

```
#if ETHARP_SUPPORT_VLAN
  if (ethhdr->type == PP_HTONS(ETHTYPE_VLAN)) {
    hdr = (struct etharp_hdr *)(((u8_t*)ethhdr) + SIZEOF_ETH_HDR + SIZEOF_VLAN_HDR);
  }
#endif /* ETHARP_SUPPORT_VLAN */
```

3、ethernet_input函数。这里是输入的总入口，它调用了上面的2个函数。

```
#if LWIP_ARP || ETHARP_SUPPORT_VLAN
  s16_t ip_hdr_offset = SIZEOF_ETH_HDR;
#endif /* LWIP_ARP || ETHARP_SUPPORT_VLAN */
这里后面还有检查vlan id，如果不匹配，就直接扔掉了。
```



# 标准

按端口划分vlan



# 参考资料

1、vlan

https://baike.baidu.com/item/虚拟局域网/419962?fr=aladdin