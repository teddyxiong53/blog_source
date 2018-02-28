---
title: Linux内核之platform device的注册
date: 2017-08-27 21:41:39
tags:
	- kernel

---



适配Linux到一块新的板子，platform device的注册是一个重要的步骤。

函数的调用过程是：

init_machine

​	platform_add_devices：这里重要的就是这里传递进去的platform_device结构体数组。

一个例子如下：

```
static struct platform_device *bast_devices[] __initdata = {
	&s3c_device_ohci,
	&s3c_device_lcd,
	&s3c_device_wdt,
	&s3c_device_i2c0,
 	&s3c_device_rtc,
	&s3c_device_nand,
	&s3c_device_adc,
	&s3c_device_hwmon,
	&bast_device_dm9k,
	&bast_device_asix,
	&bast_device_axpp,
	&bast_sio,
};

static struct platform_device bast_device_dm9k = {
	.name		= "dm9000",
	.id		= 0,
	.num_resources	= ARRAY_SIZE(bast_dm9k_resource),
	.resource	= bast_dm9k_resource,
	.dev		= {
		.platform_data = &bast_dm9k_platdata,
	}
};

static struct resource bast_dm9k_resource[] = {
	[0] = {
		.start = S3C2410_CS5 + BAST_PA_DM9000,
		.end   = S3C2410_CS5 + BAST_PA_DM9000 + 3,
		.flags = IORESOURCE_MEM,
	},
	[1] = {
		.start = S3C2410_CS5 + BAST_PA_DM9000 + 0x40,
		.end   = S3C2410_CS5 + BAST_PA_DM9000 + 0x40 + 0x3f,
		.flags = IORESOURCE_MEM,
	},
	[2] = {
		.start = IRQ_DM9000,
		.end   = IRQ_DM9000,
		.flags = IORESOURCE_IRQ | IORESOURCE_IRQ_HIGHLEVEL,
	}

};

```



# 其他方式

上面这种方式需要改板级文件，那就是需要重新编译kernel，这个动作也太大了。

我们只需要在驱动里这样写：

```
struct platform_device test_device = {
  .name = "test_platform",
  .id = -1,
};
struct platform_driver test_driver = {
  .probe = test_probe,
  .remove = test_remove,
  .driver = {
    .name = "test_platform",
    .owner = THIS_MODULE,
  },
};
static int test_init(void)
{
  platform_device_register(&test_device);
  platform_driver_register(&test_driver);
}
```



