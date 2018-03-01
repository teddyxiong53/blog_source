---
title: Linux驱动之ENC28J60
date: 2018-03-01 19:57:11
tags:
	- Linux驱动

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



