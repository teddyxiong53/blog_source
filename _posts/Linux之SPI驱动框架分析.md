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



# spi和i2c驱动对比

spi_board_info对应i2c_board_info。

spi_master相当于i2c_adapter和i2c_alogrithm。host端。
spi_device相当于i2c_client。设备端。
spi_message对应i2c_msg。
spi_driver对应i2c_driver。

## board_info

用来在bsp里的machine_init里注册信息。

```
struct spi_board_info {
	char		modalias[SPI_NAME_SIZE];
	const void	*platform_data;
	void		*controller_data;
	int		irq;
	u32		max_speed_hz;
	u16		bus_num;
	u16		chip_select;
	u16		mode;
};
```

```
struct i2c_board_info {
	char		type[I2C_NAME_SIZE];
	unsigned short	flags;
	unsigned short	addr;
	void		*platform_data;
	struct dev_archdata	*archdata;
	struct device_node *of_node;
	struct fwnode_handle *fwnode;
	int		irq;
};
```

## host端

可以看到，spi_master内容特别多。相当于i2c_adapter和i2c_algorithm的总和。

```
struct spi_master {
	struct device	dev;
	struct list_head list;
	s16			bus_num;
	u16			num_chipselect;
	u16			dma_alignment;
	u16			mode_bits;

	u32			bits_per_word_mask;
	u32			min_speed_hz;
	u32			max_speed_hz;
	u16			flags;
	spinlock_t		bus_lock_spinlock;
	struct mutex		bus_lock_mutex;
	bool			bus_lock_flag;
	int			(*setup)(struct spi_device *spi);
	int			(*transfer)(struct spi_device *spi,
						struct spi_message *mesg);
	void			(*cleanup)(struct spi_device *spi);

	bool			(*can_dma)(struct spi_master *master,
					   struct spi_device *spi,
					   struct spi_transfer *xfer);
	bool				queued;
	struct kthread_worker		kworker;
	struct task_struct		*kworker_task;
	struct kthread_work		pump_messages;
	spinlock_t			queue_lock;
	struct list_head		queue;
	struct spi_message		*cur_msg;
	bool				idling;
	bool				busy;
	bool				running;
	bool				rt;
	bool				auto_runtime_pm;
	bool                            cur_msg_prepared;
	bool				cur_msg_mapped;
	struct completion               xfer_completion;
	size_t				max_dma_len;
	int (*prepare_transfer_hardware)(struct spi_master *master);
	int (*transfer_one_message)(struct spi_master *master,
				    struct spi_message *mesg);
	int (*unprepare_transfer_hardware)(struct spi_master *master);
	int (*prepare_message)(struct spi_master *master,
			       struct spi_message *message);
	int (*unprepare_message)(struct spi_master *master,
				 struct spi_message *message);
	void (*set_cs)(struct spi_device *spi, bool enable);
	int (*transfer_one)(struct spi_master *master, struct spi_device *spi,
			    struct spi_transfer *transfer);
	void (*handle_err)(struct spi_master *master,
			   struct spi_message *message);
	int			*cs_gpios;
	struct spi_statistics	statistics;
	struct dma_chan		*dma_tx;
	struct dma_chan		*dma_rx;
	void			*dummy_rx;
	void			*dummy_tx;
};
```

```
struct i2c_adapter {
	struct module *owner;
	unsigned int class;		  /* classes to allow probing for */
	const struct i2c_algorithm *algo; /* the algorithm to access the bus */
	void *algo_data;
	struct rt_mutex bus_lock;
	int timeout;			/* in jiffies */
	int retries;
	struct device dev;		/* the adapter device */
	int nr;
	char name[48];
	struct completion dev_released;
	struct mutex userspace_clients_lock;
	struct list_head userspace_clients;
	struct i2c_bus_recovery_info *bus_recovery_info;
	const struct i2c_adapter_quirks *quirks;
};
```

## 设备端

设备端都不复杂。都有device成员，都有irq。都持有host端的指针。都有一个名字。

```
struct spi_device {
	struct device		dev;
	struct spi_master	*master;
	u32			max_speed_hz;
	u8			chip_select;
	u8			bits_per_word;
	u16			mode;
	int			irq;
	void			*controller_state;
	void			*controller_data;
	char			modalias[SPI_NAME_SIZE];
	int			cs_gpio;	/* chip select gpio */
};
```

```
struct i2c_client {
	unsigned short flags;		
	unsigned short addr;		
	char name[I2C_NAME_SIZE];
	struct i2c_adapter *adapter;	
	struct device dev;		
	int irq;			
	struct list_head detected;
};
```

## 消息

spi的要复杂很多。

```
struct spi_message {
	struct list_head	transfers;
	struct spi_device	*spi;
	unsigned		is_dma_mapped:1;
	void			(*complete)(void *context);
	void			*context;
	unsigned		frame_length;
	unsigned		actual_length;
	int			status;
	struct list_head	queue;
	void			*state;
};

struct spi_transfer {
	const void	*tx_buf;
	void		*rx_buf;
	unsigned	len;
	dma_addr_t	tx_dma;
	dma_addr_t	rx_dma;
	struct sg_table tx_sg;
	struct sg_table rx_sg;
	unsigned	cs_change:1;
	unsigned	tx_nbits:3;
	unsigned	rx_nbits:3;
	u8		bits_per_word;
	u16		delay_usecs;
	u32		speed_hz;
	struct list_head transfer_list;
};

```

```
struct i2c_msg {
	__u16 addr;	/* slave address			*/
	__u16 flags;
	__u16 len;		/* msg length				*/
	__u8 *buf;		/* pointer to msg data			*/
};
```

## 驱动

```
struct spi_driver {
	const struct spi_device_id *id_table;
	int			(*probe)(struct spi_device *spi);
	int			(*remove)(struct spi_device *spi);
	void			(*shutdown)(struct spi_device *spi);
	struct device_driver	driver;
};
```

```
struct i2c_driver {
	unsigned int class;
	int (*attach_adapter)(struct i2c_adapter *) __deprecated;
	int (*probe)(struct i2c_client *, const struct i2c_device_id *);
	int (*remove)(struct i2c_client *);
	void (*shutdown)(struct i2c_client *);
	void (*alert)(struct i2c_client *, unsigned int data);
	int (*command)(struct i2c_client *client, unsigned int cmd, void *arg);
	struct device_driver driver;
	const struct i2c_device_id *id_table;
	int (*detect)(struct i2c_client *, struct i2c_board_info *);
	const unsigned short *address_list;
	struct list_head clients;
};
```



# 硬件

**4 线 SPI 器件有四个信号：**

● 时钟(SPICLK,SCLK)
● 片选(CS)主机输出
● 从机输入(MOSI)主机输入
● 从机输出(MISO)



SPI比较混乱，主要是没有标准的协议，只有moto的事实标准。所以衍生出多个版本，但没有本质的差异。

常见的SPI信号有：SS片选、SCK同步时钟、MISO、MOSI（也有叫SDI、SDO的）数据输入和输出，还的有包括DCX命令数据选择。

SPI分4线和3线，

4线接口：包括SCLK、SDO、SDI、SS；

3线接口：包括SCLK、SDA、SS。

所以3线和4线的不同在于，4线接口可以实现的是master in和master out。

但3线只有master out。

不管是3线还是4线，SS是必须有的。

master使用不同的SS信号可以连接多个salve



# 参考资料

https://blog.csdn.net/wofreeo/article/details/89159059