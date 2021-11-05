---
title: uboot之设备模型
date: 2020-01-13 11:05:08
tags:
	- uboot

---

1

配置宏是CONFIG_DM。

入口函数是：initf_dm。

以rockchip的serial驱动为例。

代码在drivers/serial/serial_rockchip.c里。

```
U_BOOT_DRIVER(rockchip_rk3288_uart) = {
	.name	= "rockchip_rk3288_uart",
	.id	= UCLASS_SERIAL,
	.priv_auto_alloc_size = sizeof(struct NS16550),
	.platdata_auto_alloc_size = sizeof(struct rockchip_uart_platdata),
	.probe	= rockchip_serial_probe,
	.ops	= &ns16550_serial_ops,
	.flags	= DM_FLAG_PRE_RELOC,
};
```

U_BOOT_DRIVER宏解析：

```
U_BOOT_DRIVER(rockchip_rk3288_uart) 
是定义了一个struct driver结构体。
这个结构体放在指定的section里。
struct driver _u_boot_list_2_driver_2_rockchip_rk3288_uart ;
```

```
struct driver
	在include/dm/device.h里。
	char *name
	enun uclass_id id;
		这个表示驱动的类型。
		类型有：ROOT、adc、eth、gpio、i2c、clk、i2c_eeprom、i2c_generic、keyboard、
			led、mmc、misc、pwm、rtc、usb、
			root这个是个特殊的设备。是一定有的。
			在drivers/core/root.c。
	of_match
		就是进行设备树的compatible匹配的。
	8个函数指针，
		都是以udevice指针为参数的。
		bind/probe/remove/unbind。
	void *ops
	flags
	
```

只有使能了CONFIG_SPL_BUILD，才进行这个的编译。所以当前并没有使用这个。

```
ifdef CONFIG_SPL_BUILD
obj-$(CONFIG_ROCKCHIP_SERIAL) += serial_rockchip.o
endif
```

下面这2个是使能的。所以串口是arm标准的pl01x.o的。

```
ifdef CONFIG_DM_SERIAL
obj-$(CONFIG_$(SPL_TPL_)DM_SERIAL) += serial-uclass.o
obj-$(CONFIG_PL01X_SERIAL) += serial_pl01x.o
```

对应的注释里这样写着：

```
/* Simple U-Boot driver for the PrimeCell PL010/PL011 UARTs */
```

```
U_BOOT_DRIVER(serial_pl01x) = {
	.name	= "serial_pl01x",
	.id	= UCLASS_SERIAL,
	.of_match = of_match_ptr(pl01x_serial_id),
	.ofdata_to_platdata = of_match_ptr(pl01x_serial_ofdata_to_platdata),
	.platdata_auto_alloc_size = sizeof(struct pl01x_serial_platdata),
	.probe = pl01x_serial_probe,
	.ops	= &pl01x_serial_ops,
	.flags = DM_FLAG_PRE_RELOC,
	.priv_auto_alloc_size = sizeof(struct pl01x_priv),
};
```

下面看入口函数initf_dm。

```
就三行
bootstage_start(BOOTSTATE_ID_ACCUM_DM_F, "dm_f");//这个是统计运行时间的。
ret = dm_init_and_scan(true);
bootstage_accum(BOOTSTATE_ID_ACCUM_DM_F);
```

重点是dm_init_and_scan这个函数。

```
dm_init
	
```

root设备和驱动

```
/* This is the root driver - all drivers are children of this */
U_BOOT_DRIVER(root_driver) = {
	.name	= "root_driver",
	.id	= UCLASS_ROOT,
	.priv_auto_alloc_size = sizeof(struct root_priv),
};

/* This is the root uclass */
UCLASS_DRIVER(root) = {
	.name	= "root",
	.id	= UCLASS_ROOT,
};

```

uboot设备树是用自己的设备树，而不是用kernel的那个。

不对，那download-key，这个明显是在kernel的设备树里改的。



# amlogic uboot相关分析

以drivers/gpio/amlogic_gpio.c为例分析。

入口

```
U_BOOT_DRIVER(gpio_aml) = {
	.name	= "gpio_aml",
	.id	= UCLASS_GPIO,
	.ops	= &gpio_aml_ops,
	.probe	= aml_gpio_probe,
};
```

ops是这样：

```
static const struct dm_gpio_ops gpio_aml_ops = {
	.request			= aml_gpio_request,
	.direction_input	= aml_gpio_direction_input,
	.direction_output	= aml_gpio_direction_output,
	.get_value		= aml_gpio_get_value,
	.set_value		= aml_gpio_set_value,
	.get_function		= aml_gpio_get_function,
};
```



上层使用的接口是在gpio-uclass.c里的函数。

以i2c的作为gpio的使用者的来分析。

```
./drivers/i2c/i2c-gpio.c:327:   if (gpio_request(i2c->sda, plat->sda))
```



```
gpio_request
gpio_requestf
gpio_free
gpio_direction_input
gpio_direction_output
gpio_get_value
gpio_set_value
```



参考资料

1、uboot 设备驱动模型

https://abcamus.github.io/2016/12/23/uboot-%E8%AE%BE%E5%A4%87%E9%A9%B1%E5%8A%A8%E6%A8%A1%E5%9E%8B/