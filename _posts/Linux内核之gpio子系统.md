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



具体的实现文件为gpiolib.c在配置内核的时候，我们必须使用CONFIG_GENERIC_GPIO这个宏来支持GPIO驱动。

mini2440打开了这个宏的。

CONFIG_GPIOLIB 



```
以gpio为入口，把三星的层次关系理清楚。
还有就是寄存器地址宏定义。
在plat-samsumg目录下
	有3个文件：
	gpio.c
		5个函数：
		s3c_gpiolib_input
		s3c_gpiolib_output
		s3c_gpiolib_set
		s3c_gpiolib_get
		s3c_gpiolib_add
			只被plat-s3c24xx里gpiolib.c用到。s3c24xx_gpiolib_init
		对外接口只有一个：s3c_gpiolib_add
		其余4个都是给s3c_gpiolib_add用的。
		
	gpio-config.c
		s3c_gpio_cfgpin
			用的比较多，在mach-mini2440.c里用到。
		s3c_gpio_getcfg
		s3c_gpio_setpull
			用的比较多，在mach-mini2440.c里用到。
		s3c_gpio_setcfg_s3c24xx
		s3c_gpio_getcfg_s3c24xx
	gpiolib.c
		这个文件没有用。
	
在plat-s3cx24xx目录下：
	有2个文件：
	gpio.c
		s3c2410_gpio_pullup
			只在drivers/led-s3c24xx.c里用到了。
		s3c2410_gpio_setpin
			只在drivers/led-s3c24xx.c里用到了。
		s3c2410_gpio_getpin
			没有用。
		s3c2410_modify_misccr
			没用。
	
	gpiolib.c
		对外接口只有一个：s3c24xx_gpiolib_init
		内核初始化自动调用。作用是把gpio_chip add到gpio子系统。
mach-mini2440.c
	这个里面就是使用gpio接口。看看如何使用的。
	gpio寄存器，都是访问的虚拟地址的了。
	被映射到F400 0000这个位置了。
	C0是配置为LEND，LEND是行结束的意思。lcd的一个引脚。
	G4被配置为背光引脚。然后打开。
	gpio_request(S3C2410_GPG(4), "backlight")
	gpio_direction_output(S3C2410_GPG(4), 1);
	B1被设置为上拉。输入。
	C5配置为输出，且输出0 
	所有按键配置为输入。
	s3c_gpio_setpull(mini2440_buttons[i].gpio, S3C_GPIO_PULL_UP);
	s3c_gpio_cfgpin(mini2440_buttons[i].gpio, S3C2410_GPIO_INPUT);
```



关于gpio，还有一种情况是i2c接口的外扩gpio芯片。



# 内核文档分析

legacy的接口是gpio_xx。

新的接口，是基于gpio_desc的，函数前缀是gpiod_xx的。

## 基于gpio的驱动

```
leds-gpio
gpio-keys
gpio_mouse
gpio-beeper
i2c_gpio
spi_gpio
gpio-fan
gpio-nand
```



# 参考资料

1、linux内核中的GPIO系统之（1）：软件框架

http://www.wowotech.net/gpio_subsystem/io-port-control.html

2、Linux内核驱动之GPIO子系统(一)GPIO的使用

https://blog.csdn.net/mirkerson/article/details/8464290

3、Documentation/gpio目录文件。

4、树莓派学习笔记——Shell脚本操作GPIO

https://blog.csdn.net/xukai871105/article/details/18517729

5、

https://tinylab.org/lwn-532714/

