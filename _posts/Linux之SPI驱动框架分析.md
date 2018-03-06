---
title: Linux之SPI驱动框架分析
date: 2018-03-06 15:51:34
tags:
	- Linux

---



spi框架比i2c的框架要简单很多，所以我们从这个入手。

代码上也很简单，就2个文件：

spi.c和spi.h。

# spi.h

1、结构体spi_master

```
1、是一个device。
2、list链表。
3、bus_num。
4、片选。是一个u16
5、dma对齐。
6、模式。
7、mask。
8、最大最小hz。
9、flags。
10、2把锁。一个spinlock，一个Mutex。
11、lock的flag。
12、4个函数指针：setup、transfer、cleanup、can_dma。
13、struct kthread_worker kworker和task_struct *kworker_task。
14、struct spi_message*cur_msg。当前消息。
15、完成量xfer_completion。
16、8个函数指针：发送相关的。
17、spi_statistics统计信息。
18、dma_chan dma通道，接收和发送各一个。
```

2、结构体spi_transfer。

```
1、发送buf和接受buf指针。
2、长度。
3、发送dma和接受dma。
4、分散聚合表sg_table。发送和接受。
5、list
6、其他的一些标志位。
```

3、声明变量bus_type spi_bus_type。

4、结构体spi_device

```
1、首先也是一个device。
2、包含spi_master指针。
3、中断号。
4、统计信息。
```

5、结构体spi_message。

```
1、list。
2、spi_device指针。
3、完成量执行的回调。
4、又一个list。
```

6、结构体spi_board_info

```
1、名字字符串。
2、void *platform_data
3、控制器data的void*指针。
4、irq中断号。
5、片选。
6、总线号。
7、模式。
```

7、一堆的函数。

都是以spi_xxx这个格式的。

# spi.c

这个文件按照使用顺序来看。

1、spi_init。这个是kernel初始化调用的。

```
1、kmalloc了32个字节，给一个static的char指针。
2、bus_register spi_bus_type。
3、class_register spi_master_class。
```

2、spi_register_driver。这个是spi设备驱动程序的入口。

```
不复杂，不细看。
```

3、看发送函数。

我们从enc28j60的代码开始看过来。

```
spi_write_buf(struct enc28j60_net *priv, int len,const u8 *data)
	//这个函数传递下来的数据，就是一个缓冲区。
	spi_write(struct spi_device *spi, const void *buf, size_t len)
		这里面需要一个spi_message结构体，一个spi_transfer结构体。
		初始化message，然后把message加到transfer的后面。
		然后spi_sync，传递下来的结构体是message。
			__spi_sync
				1、进一步对message结构体赋值。
				2、__spi_pump_messages
					master->transfer_one_message
					这个就是对应到cpu相关的函数了，在spi-bcm2835.c里。
				3、等待完成。
```



