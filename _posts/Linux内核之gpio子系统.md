---
title: Linux内核之gpio子系统
date: 2018-03-26 10:07:30
tags:
	- Linux内核

---



# 用户态对gpio操作

以树莓派为例。

```
pi@raspberrypi:/sys/class/gpio$ ls
export  gpiochip0  gpiochip100  gpiochip128  unexport
```

我比较好奇，gpiochip0这种是什么时候注册进来的。

还是在gpiolib_sysfs_init里。

```
spin_unlock_irqrestore(&gpio_lock, flags);
		status = gpiochip_sysfs_register(chip);
		spin_lock_irqsave(&gpio_lock, flags);
```

后面的数字，表示是base。就是gpio起始的位置。

```
dev = device_create_with_groups(&gpio_class, chip->dev, MKDEV(0, 0),
					chip, gpiochip_groups,
					"gpiochip%d", chip->base);
```



export和unexport，都是只有store，没有show，所以是只能写，不能读的。

```
static struct class_attribute gpio_class_attrs[] = {
	__ATTR(export, 0200, NULL, export_store),
	__ATTR(unexport, 0200, NULL, unexport_store),
	__ATTR_NULL,
};
```



操作：

你往export里写入一个数字，就会产生一个对应的目录。如下。

```
pi@raspberrypi:/sys/class/gpio$ ls
export  gpiochip0  gpiochip100  gpiochip128  unexport
pi@raspberrypi:/sys/class/gpio$ echo 4 > export
pi@raspberrypi:/sys/class/gpio$ ls
export  gpio4  gpiochip0  gpiochip100  gpiochip128  unexport
pi@raspberrypi:/sys/class/gpio$ cd gpio4
pi@raspberrypi:/sys/class/gpio/gpio4$ ls
active_low  device  direction  edge  power  subsystem  uevent  value
```

控制引脚的电平。

```
pi@raspberrypi:/sys/class/gpio/gpio4$ echo out > direction
pi@raspberrypi:/sys/class/gpio/gpio4$ echo 1 > value 
pi@raspberrypi:/sys/class/gpio/gpio4$ echo 0 > value 
```



# 用户态操作gpio的其他选择

1、用mmap把gpio的映射到用户空间来操作。





#内核代码分析

```
#ifdef CONFIG_GPIOLIB //定义了。
#ifdef CONFIG_ARCH_HAVE_CUSTOM_GPIO_H //也定义了。这个怎么配置？
#include <asm/gpio.h>
#else
```

只要是arm架构的，自动就配置了这个的。里面内容没有什么特别的。

```
Symbol: ARCH_HAVE_CUSTOM_GPIO_H [=y]  
Type  : boolean                       
  Defined at drivers/gpio/Kconfig:5   
  Selected by: ARM [=y]               
```



gpio_request这种接口是已经过时了的。

```
drivers/gpio/gpiolib-legacy.c   /^int gpio_request(unsigned gpio, const char *label)$/;" 
```

不过默认都还是编译进来的，新的接口和老的接口共存的。

```
obj-$(CONFIG_GPIOLIB)		+= gpiolib.o
obj-$(CONFIG_GPIOLIB)		+= gpiolib-legacy.o
obj-$(CONFIG_OF_GPIO)		+= gpiolib-of.o
obj-$(CONFIG_GPIO_SYSFS)	+= gpiolib-sysfs.o
```

gpiolib-legacy.c里的接口就是2对：

```
gpio_request
gpio_free
gpio_request_one
gpio_request_array
gpio_free_array
```

还有好几个是在gpio.h里 inline函数。

```
gpio_is_valid
gpio_direction_input
gpio_export
```



现在的内部实现，还是转到了gpiolib.c里的函数。

```
void gpio_free(unsigned gpio)
{
	gpiod_free(gpio_to_desc(gpio));//区别就是这里，以前的是int，现在的是一个desc。
}
```





drivers/gpio/gpio-samsung.c里。

```
s3c_gpio_cfgpin
```

被bsp文件里调用到。

另外，定义的gpio_chip是在这里。每一个chip，就是GPIOA这样的一组gpio。

```
struct samsung_gpio_chip s3c24xx_gpios[] = {
#ifdef CONFIG_PLAT_S3C24XX
	{
		.config	= &s3c24xx_gpiocfg_banka,
		.chip	= {
			.base			= S3C2410_GPA(0),
			.owner			= THIS_MODULE,
			.label			= "GPIOA",
			.ngpio			= 27,
			.direction_input	= s3c24xx_gpiolib_banka_input,
			.direction_output	= s3c24xx_gpiolib_banka_output,
		},
	}
```

三星的相关初始化过程是：

1、系统启动时，samsung_gpiolib_init

```
1、s3c24xx_gpiolib_add_chips(s3c24xx_gpios,//就是配置PA/PB等。
```

就这么多。



内核里其他地方要用，就用这些接口。

```
s3c_gpio_cfgpin
s3c_gpio_setpull
```





# 参考资料

1、linux内核中的GPIO系统之（1）：软件框架

http://www.wowotech.net/gpio_subsystem/io-port-control.html

2、Linux内核驱动之GPIO子系统(一)GPIO的使用

https://blog.csdn.net/mirkerson/article/details/8464290

3、Documentation/gpio目录文件。

4、树莓派学习笔记——Shell脚本操作GPIO

https://blog.csdn.net/xukai871105/article/details/18517729