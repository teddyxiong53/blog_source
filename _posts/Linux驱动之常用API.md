---
title: Linux驱动之常用API
date: 2018-03-26 11:18:57
tags:
	- Linux驱动

---



# 关于priv

platform_device那里的。是用pdev->dev.platform_data 

platform_driver那里。是用platform_set_drvdata。

常见的就是这2个私有数据。

platform可以替换为spi等其他总线。





#device.h里常用api

```
1、dev_get_platdata
	在驱动probe里获取到platform device 那里注册进来的platform数据。
2、dev_error(&pdev->dev, "xxx");
	dev_dbg
	驱动里打印错误。
3、devm_kzalloc(&pdev->dev, sizeof(struct s3c24xx_i2c), GFP_KERNEL);
	分配内存。
4、clk = devm_clk_get(&pdev->dev, "i2c");
	获取时钟。
5、devm_ioremap_resource
6、错误返回。
	if (IS_ERR(i2c->regs))
		return PTR_ERR(i2c->regs);
```



#etherdevice.h

```
1、alloc_etherdev(sizeof_priv)
	返回一个net_device结构体指针。把私有数据的内存也分配了，就挨着放的。
2、netdev_priv
	取得私有数据。
3、register_netdev
	注册net_device。
```



# i2c host端编程常用API

总共分为2个部分：

1、bsp里的。

2、host控制器的。在drivers/i2c目录下。

bsp的先被执行。

## 在bsp文件里

1、定义一个i2c_board_info结构体。

```
struct i2c_board_info __initdata i2c_dev1[] = {
  {
    I2C_BOARD_INFO("max77686", (0x12>>1)),
    .platform_data = &m040_max_77686_info,
  },
};
```

2、定义资源和平台设备

```
static struct resource s3c_i2c_resource[] = {
  [0] = {
    .start = ,
    .end = ,
    .flags = IORESOURCE_MEM,
  },
  [1] = {
    .start = ,
    .end = ,
    .flags = IORESOURCE_IRQ,
  },
};
struct platform_device s3c_device_i2c1  = {
  .name = "s3c2410-i2c",
  .id = 1,
  .num_resources = ARRAY_SIZE(s3c_i2c_resource),
  .resource = s3c_i2c_resource,
};
```

3、定义平台数据platform_data。

```
struct s3c2410_platform_i2c m040_default_i2c1_data __initdata = {
  .flags = 0,
  .slave_addr = 0x10,
  .frequency = 400*1000,
  .sda_delay = 100,
  .bus_num = 1,
};
```

4、在machine_init里，先注册平台设备。再注册板信息。这里就产生i2c_client结构体。

```
s3c_i2c1_set_platdata(&m040_default_i2c1_data);
i2c_register_board_info(1, i2c_devs1, ARRAY_SIZE(i2c_devs1));
```

## host控制器的

1、入口。因为是集成在soc上的，所以是一个平台设备。

```
static int __init i2c_adap_s3c_init(void)
{
	return platform_driver_register(&s3c24xx_i2c_driver);
}
arch_initcall(i2c_adap_s3c_init);
```

2、probe函数里用到的函数和结构体。这个也是一个典型的平台设备的注册过程。

这个结构体是为了区别不同变种。

```
struct platform_device_id {
  char name[20];
  ulong driver_data;
}
```

例如：

```
static struct platform_device_id s3c24xx_driver_ids[] = {
	{
		.name		= "s3c2410-i2c",
		.driver_data	= TYPE_S3C2410,
	}, {
		.name		= "s3c2440-i2c",
		.driver_data	= TYPE_S3C2440,
	}, {
		.name		= "s3c2440-hdmiphy-i2c",
		.driver_data	= TYPE_S3C2440_HDMIPHY,
	}, { },
};
```

获取时钟。

```
i2c->clk = clk_get(&pdev->dev, "i2c");
```

使能时钟。

```
clk_enable(i2c->clk);
```

获取mem资源。

```
res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
```

拿到物理寄存器的虚拟地址。

```
i2c->regs = ioremap(res->start, resource_size(res));
```

调用平台数据里的内容，配置引脚频率。

```
ret = s3c24xx_i2c_init(i2c);
```

获取中断资源。

```\
i2c->irq = ret = platform_get_irq(pdev, 0);
```

注册中断。

```
ret = request_irq(i2c->irq, s3c24xx_i2c_irq, IRQF_DISABLED,
			  dev_name(&pdev->dev), i2c);
```

注册i2c 适配器。

```
ret = i2c_add_numbered_adapter(&i2c->adap);
```

设置平台驱动数据。

```
platform_set_drvdata(pdev, i2c);
```

# i2c设备端常用API

我还是以mx2上的i2c1上的max77686这个多功能芯片为例。

这个芯片是电源管理芯片，同时有rtc的功能。代码分布在3个目录下：

1、drivers/mfd/max77686.c

2、drivers/regulator/max77686.c

3、drivers/rtc/rtc-max77686.c。

这个多功能是靠设备有2个i2c地址来做的。

```
struct i2c_client *i2c; /* 0xcc / PMIC, Battery Control, and FLASH */
struct i2c_client *rtc; /* slave addr 0x0c */
```

##mfd

mfd下面的是总的。从这里开始看。

1、定义了一个i2c_driver结构体。

```
static int __init max77686_i2c_init(void)
{
	return i2c_add_driver(&max77686_i2c_driver);
}
```

定义多功能结构体数组。

```
static struct mfd_cell max77686_devs[] = {
	{ .name = "max77686-pmic", },
#ifdef CONFIG_RTC_DRV_MAX77686
	{ .name = "max77686-rtc", },
#endif
};
```



2、probe函数分析。

分配一个max77686_dev结构体。

```
max77686 = kzalloc(sizeof(struct max77686_dev), GFP_KERNEL);
```

设置i2c client数据。

```
i2c_set_clientdata(i2c, max77686);
```

可以用i2c进行寄存器读取了。

```
max77686_read_reg(i2c, MAX77686_REG_DEVICE_ID, &data)
	ret = i2c_smbus_read_byte_data(i2c, reg);
```

分配一个空的i2c client。

```
max77686->rtc = i2c_new_dummy(i2c->adapter, I2C_ADDR_RTC);
	i2c_set_clientdata(max77686->rtc, max77686);
```

添加多功能设备。

```
ret = mfd_add_devices(max77686->dev, -1, max77686_devs,
			      ARRAY_SIZE(max77686_devs), NULL, 0);
```

## regulator

这里是作为一个平台设备的。

```
static int __init max77686_pmic_init(void)
{
	pr_debug("%s\n", __func__);
	return platform_driver_register(&max77686_pmic_driver);
}
```

## rtc

这里也是作为一个平台设备。

```
static int __init max77686_rtc_init(void)
{
	return platform_driver_register(&max77686_rtc_driver);
}
```

