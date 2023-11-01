---
title: Linux驱动之regmap
date: 2020-01-07 17:31:08
tags:
	- Linux

---

--

什么是regmap？主要用来做什么？

regmap是内核3.1版本引入的一套控制总线通用接口。

什么是控制总线？i2c和spi就是控制总线。

在没有regmap之前，当设备驱动使用i2c或者spi的时候，都需要写一堆的boardinfo。然后注册到系统。

光是注册就很麻烦了，更何况还存在i2c和spi的读写接口不一致的情况。

regmap就是为了改善这种情况，提供了一层抽象。

有了regmap，不管底层是i2c还是spi，读写接口都是一样的。

还可以在驱动和硬件ic之间做一层缓存，减少跟外部芯片操作的次数。



# 为什么要推出struct regmap

`struct regmap` 是Linux内核中的一个结构体，用于在设备驱动中进行寄存器映射（Register Map）和访问寄存器的抽象，它的推出有以下几个原因：

1. **硬件抽象**：`struct regmap` 提供了一个硬件寄存器访问的抽象层，它允许设备驱动程序与底层硬件的寄存器访问细节分离。这种抽象可以==帮助驱动程序编写更具可移植性的代码==，因为它们不需要了解特定硬件的寄存器访问方式。

2. **寄存器映射**：硬件通常有大量的寄存器，用于配置和控制设备的各个方面。`struct regmap` 提供了一种方便的方式来==将这些寄存器映射到内存中==，以便在设备驱动中进行读写操作。

3. **原子性操作**：`struct regmap` ==提供了原子性寄存器操作，这对于多线程或多CPU系统非常重要==。它确保在多个线程或CPU同时访问寄存器时不会出现竞争条件。

4. **缓存和优化**：`struct regmap` ==支持寄存器值的缓存==，可以减少对硬件寄存器的访问，从而提高性能。它还可以优化寄存器访问，以减少对硬件的访问。

5. **错误处理**：`struct regmap` 可以==处理寄存器访问中的错误==，包括寄存器访问超时、寄存器不存在等情况。这有助于提高驱动程序的稳定性和可靠性。

6. **可扩展性**：`struct regmap` 可以==轻松地扩展到支持不同类型的寄存器访问==，包括寄存器位宽、地址映射和字节顺序等。

总之，`struct regmap` 的推出旨在提供一种更高级、更抽象的接口，使设备驱动开发更容易，提高代码的可移植性，并提供更多的功能，以满足不同硬件的需求。这对于在Linux内核中支持各种硬件设备非常有用。



Linux驱动开发中，对于一些外设型器件驱动，

如ADC、DAC、EEPROM、Sensor，

这里器件通常是以uart、i2c、spi、mipi为控制接口，

==通过配置器件寄存器来设置芯片工作模式、运行参数、校准值等等，==

==并通过获取寄存器值来获得有效数据。==

普通的做法，我们是根据不同的控制总线接口来实现寄存器访问，

这样的方式是需要根据总线类型来调整访问接口、数据结构，这样显得繁琐。

比如，目前有个ADC器件，支持spi和i2c接口；

在此之前采用的是spi接口；

后面因cpu spi接口不够用，线需要改为i2c控制。

这样，该ADC驱动程序得修改，从spi改为i2c驱动，虽然工作量不大，但是也得花费一定时间。

那么大体工作量有：

spi_write/spi_rea接口修改为 i2c_transfer

spi片选（cs）修改为i2c从地址寻址

数据结构修改， struct spi_message修改为struct rt_i2c_msg

==基于代码代码复用的原则之一，Linux在3.1内核后引入了regmap模型，==

将寄存器访问的共同逻辑抽象出来，

只需初始化时指定总线类型、寄存器位宽等关键参数，

即可通过regmap模型接口来操作器件寄存器。

当然，regmap同样适用于操作cpu自身的寄存器。



# 支持的总线类型



# 架构层次

![img](images/random_name/v2-c64ccc4da41569314f75b38862d936b0_720w.webp)

分为3层

```
regmap   |  regmap_read 和regmap_write
-----------------------------------
regcache | flat   lzo  rbtree
-----------------------------------
bus      |    i2c spi   mmio  ac97
```

有3个核心结构体：

```
regmap_config
regmap_ops
regmap_bus
```

代码在drivers/base/regmap目录下。

```
static struct regmap_bus regmap_i2c = {
	.write = regmap_i2c_write,
	.gather_write = regmap_i2c_gather_write,
	.read = regmap_i2c_read,
	.reg_format_endian_default = REGMAP_ENDIAN_BIG,
	.val_format_endian_default = REGMAP_ENDIAN_BIG,
};
```



# 一般怎么使用的呢？

使用regmap比较简单，使用前，只需根据外设属性配置总线类型、寄存器位宽、缓存类型、读写属性等参数；接着注册一个regmap实例；然后调用抽象访问接口访问寄存器。

- 第一步，配置regmap信息
- 第二步，注册regmap实例
- 第三步，访问寄存器
- 第四步，释放regmap实例



以i2c为例，以伪代码访问寄存器比较传统方式和通过regmap访问方式。

传统方式

```

static int read_regs(struct i2c_client *client, uint8_t reg, uint8_t *pdata, int size)
{
	int ret = 0;
	struct i2c_msg msg[2];
	if(size == 0)
	{
		return 0;
	}
	msg[0].addr  = client->addr;  	 
    msg[0].buf   = &reg;               
    msg[0].len   = 1;                     
    msg[0].flags = 0; 
	msg[1].addr  = client->addr;  	 
    msg[1].buf   = pdata;               
    msg[1].len   = size;                     
    msg[1].flags = I2C_M_RD; 

	if(i2c_transfer(client->adapter, msg, 2) != 2)
	{
		ret =-1;
	}

	return ret;
}
```

使用regmap方式

```

/* 第一步配置信息 */
static const struct regmap_config regmap_config = 
{     
	.reg_bits = 8,     
	.val_bits = 8,       
	.max_register = 255,     
	.cache_type = REGCACHE_RBTREE,     
	.volatile_reg = false,
};   

/* 第二步，注册regmap实例 */
regmap = regmap_init_i2c(i2c_client, &regmap_config);  

/* 第三步，访问操作 */
static int read_regs(uint8_t reg, uint8_t *pdata, int size)
{
	 return regmap_raw_read(regmap, reg, pdata, size);
}
```



# 参考资料

1、设备驱动中的regmap

https://blog.csdn.net/viewsky11/article/details/54295679

2、regmap简介

https://blog.csdn.net/lk07828/article/details/50587879

3、

https://blog.csdn.net/qq_20553613/article/details/110357322

4、

https://zhuanlan.zhihu.com/p/550695692