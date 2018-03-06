---
title: Linux之以太网框架分析
date: 2018-03-06 16:25:06
tags:
	- Linux

---



以树莓派上的ENC28J60驱动为入口进行分析。

看probe函数使用到的net相关接口：

1、net_device结构体。

```
在linux/netdevice.h里定义。
1、名字。
2、名字list。
3、别名。
4、内存start、end、base、irq。
5、状态。
6、一堆的list。dev_list、napi_list。
7、一堆的特征。
8、网卡index。
9、统计。
10、net_device_ops结构体。
11、ethtools_ops结构体。
12、header_ops结构体。
13、其他信息。
```

2、net_device_ops结构体

```
一堆的ndo_xxx函数指针。
驱动需要实现。
```

3、ethtools_ops结构体。

```
一堆的get、set。
驱动需要实现。
```

4、alloc_etherdev

得到一个net_device结构体。后面会多分配一块，用来放enc28j60_net。

通过netdev_priv索引到多分的那块内存。

5、register_netdev。



注册驱动的过程就是上面这些步骤。

现在我们看数据收发是怎么走的。

先看发送。ENC28J60的收发都是用work_struct来做的。这个是一种buttom half机制。

我们还是从socket层的send函数往下跟。

```
send
	inet_sendmsg
		sk->sk_prot->sendmsg
			udp_sendmsg
				udp_send_skb
					ip_send_skb
						ip_local_out
							dst_output
								skb_dst(skb)->output
									neigh_resolve_output
										dev_queue_xmit
											__dev_queue_xmit
												dev_hard_start_xmit
													xmit_one
														netdev_start_xmit
															ops->ndo_start_xmit
															这里就关联到网卡了。
															对应28j60的enc28j60_send_packet
															
```

enc28j60_send_packet过程

```
enc28j60_send_packet
	schedule_work(&priv->tx_work);
	--转到enc28j60_tx_work_handler
		enc28j60_hw_tx
			enc28j60_packet_write
				spi_write_buf
```

所以整个的过程就是这样的。



sk_buff是贯穿了发送过程的结构体。我们分析一下这个结构体的情况。

1、在udp_sendmsg函数这里面，才开始出现skb结构体。前面都只是普通buf。

```
udp_sendmsg
	skb = ip_make_skb
		1、定义了一个sk_buff_head的queue（这个queue很简单，就2个指针和1个长度）。
		2、__ip_append_data
			这里分配的。
		3、__ip_make_skb
			设置了skb结构体内容。
```

2、后面skb就一直没有什么变化，一直到enc28j60_hw_tx里，把数据取出来用。







