---
title: Linux驱动之ENC28J60
date: 2018-03-01 19:57:11
tags:
	- Linux驱动
typora-root-url: ..\
---



ENC28J60是一个简单的spi接口的网卡芯片，是microchip出品的。

因为简单，所以适合用来做spi驱动分析和网卡驱动分析的材料。



不支持自动协商。是10Mbps的。



# 引脚连接

1、芯片有28个脚。

2、连接拓扑是`cpu-->ENC28J60-->RJ45`。

3、与cpu的连接引脚：

```
1、spi的4个脚：in、out、sclk、cs。
2、int中断脚。
3、rst复位脚。
```

4、与RJ45的引脚有：

```
1、2个led：leda和ledb。
2、TPOUT+和TPOUT-。
```

# 芯片寄存器

我们先从linux里的驱动代码开始看。

ENC28J60的寄存器都在ENC28J60_hw.h里定义了。

寄存器分为3种：

1、control寄存器。

2、eth寄存器。

3、phy寄存器。



寄存器地址是8位，总共最多是256个地址。

这8位又有细分为3段。

0到4位：是寄存器地址，最多32个寄存器。4个bank，每个bank里32个寄存器。4个bank里的最后5个寄存器是重叠的。

```
#define EIE		0x1B
#define EIR		0x1C
#define ESTAT		0x1D
#define ECON2		0x1E
#define ECON1		0x1F
```

5到6位：bank。总共4个bank。

7位：区分phy和mac寄存器。



处理寄存器，还有7个寄存器操作命令：

```
1、读控制寄存器。
2、读缓冲区。
3、写控制寄存器。
4、写缓冲区。
5、置位。
6、清零。
7、复位。
```

# 缓冲区配置

ENC28J60里有一个8K的缓冲区。我们要把这个划分为发送buf和接收buf。

要划分，就要2个start_addr和2个len来划分。

这4个值需要8个寄存器（寄存器是8位的）来存放。

因为发送的包长度是1518字节左右，所以大概给这个长度给发送buf就好，其余的都给接收buf。

我们发送buf给0x600，就是1536字节。



# linux下的驱动代码

1、首先是spi_register_driver。主要结构体是spi_driver的enc28j60_driver。

2、在probe函数里，最后register_netdev。是一个netdev。



# 与dm9000的代码对比

1、enc28j60的没有看到涉及rmii相关的东西。

应该是ENC28J60的已经包括了。而dm9000包括的东西少一些。dm9000还需要额外的phy芯片。

这里还需要进一步思考。

2、ENC28J60采用的是work_struct来进行中断底半段的处理。

而dm9000则是全部在中断里做了。应该是dm9000的硬件处理速度快，不占用cpu的时间，所以这样处理。



从注释看，是因为用到了spi_sync。这个接口会阻塞，所以没有用tasklet等方式。而用了work_struct。

```
static irqreturn_t enc28j60_irq(int irq, void *dev_id)
{
	struct enc28j60_net *priv = dev_id;

	/*
	 * Can't do anything in interrupt context because we need to
	 * block (spi_sync() is blocking) so fire of the interrupt
	 * handling workqueue.
	 * Remember that we access enc28j60 registers through SPI bus
	 * via spi_sync() call.
	 */
	schedule_work(&priv->irq_work);

	return IRQ_HANDLED;
}
```



看接收一个包的过程。

```
enc28j60_irq_work_handler
	enc28j60_rx_interrupt
		enc28j60_hw_rx
			enc28j60_mem_read
			skb = netdev_alloc_skb(ndev, len + NET_IP_ALIGN);
			netif_rx_ni(skb);
				netif_rx_internal
					enqueue_to_backlog
						sd = &per_cpu(softnet_data, cpu);
						__skb_queue_tail(&sd->input_pkt_queue, skb);
							这个就是加入到一个list里了。
```



```
static int __init net_dev_init(void)
	skb_queue_head_init(&sd->input_pkt_queue);
	sd->backlog.poll = process_backlog;
```

process_backlog就是循环处理。

```
process_backlog
	while 1
		while ((skb = __skb_dequeue(&sd->process_queue))) {
			rcu_read_lock();
			local_irq_enable();
			__netif_receive_skb(skb);//这里拿数据的。
```

```
__netif_receive_skb
	__netif_receive_skb_core
		deliver_skb
			调用到回调。
			ip_rcv	
```

# 芯片手册

## 以太网控制器的特点

1、兼容802.3 .

2、集成了mac和10Base-T的phy。

3、支持全双工和半双工模式。

4、可编程的冲突自动重传。

5、可编程的crc生成。

6、可编程的自动丢弃错误包。

7、spi接口时钟可以到20MHz。

## 缓冲区

1、8K字节的收发sram。

2、收发buffer大小可以配置。

3、硬件管理环形接收fifo。

4、8bit位宽，

5、内部dma。

6、硬件支持crc计算。

## mac特点

1、支持单播、组播、广播包。

2、

## phy特点

1、loopback模式。

2、2个可编程的led，用来指示连接、收发状态。

## 芯片引脚

cs、so、si、sck、int、rst。只需要接着6个引脚就可以了。

![](/images/Linux网络之ENC28J60-框图.png)





# 代码再阅读

```
enc28j60_soft_reset
通过spi，往地址0上写0xff。随便哪个地址都可以。
```





