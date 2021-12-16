---
title: Linux驱动之regmap
date: 2020-01-07 17:31:08
tags:
	- Linux

---

1

什么是regmap？主要用来做什么？

regmap是内核3.1版本引入的一套控制总线通用接口。

什么是控制总线？i2c和spi就是控制总线。

在没有regmap之前，当设备驱动使用i2c或者spi的时候，都需要写一堆的boardinfo。然后注册到系统。

光是注册就很麻烦了，更何况还存在i2c和spi的读写接口不一致的情况。

regmap就是为了改善这种情况，提供了一层抽象。

有了regmap，不管底层是i2c还是spi，读写接口都是一样的。

还可以在驱动和硬件ic之间做一层缓存，减少跟外部芯片操作的次数。



架构层次

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



一般怎么使用的呢？

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