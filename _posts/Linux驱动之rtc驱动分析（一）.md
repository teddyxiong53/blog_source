---
title: Linux驱动之rtc驱动分析（一）
date: 2018-01-28 12:04:57
tags:
	- Linux驱动
	- rtc

---



rtc是一个简单的设备，我希望通过这个来把Linux的驱动相关知识串起来。

分析的代码是linux2.6版本。

以s3c2440的为入口。文件是drivers/rtc/rtc-s3c.c。这个文件代码大概600行。

rtc设备是平台设备。

```
s3c_rtc_init
	platform_driver_register(&s3c_rtc_driver)
```

关键看probe函数。

```
static struct platform_driver s3c_rtc_driver = {
	.probe		= s3c_rtc_probe,
```



##s3c_rtc_probe函数分析：

1、platform_get_irq，要0和1号。为什么这里可以get到呢？irq属于一种resource。
这个resource，linux是怎么知道的呢？肯定是有地方注册给linux知道的。

我本来是打算用arch/arm/mach-24xx/mach-smdk2440.c的来分析，但是看这个没有注册rtc的，所以我就选用mach-at2440evb.c的来看。

在这个文件里，我们找到：

```
static struct platform_device *at2440evb_devices[] __initdata = {
	&s3c_device_ohci,
	&s3c_device_wdt,
	&s3c_device_adc,
	&s3c_device_i2c0,
	&s3c_device_rtc,//这里。
```

s3c_device_rtc这个结构体在哪里定义呢？

在arch/arm/plat-s3c24xx/devs.c里定义。

```
struct platform_device s3c_device_rtc = {
	.name		  = "s3c2410-rtc",
	.id		  = -1,
	.num_resources	  = ARRAY_SIZE(s3c_rtc_resource),
	.resource	  = s3c_rtc_resource,
};
```

然后我们看s3c_rtc_resource这个结构体。注册的resource是一块内存，2个中断。

```
static struct resource s3c_rtc_resource[] = {
	[0] = {
		.start = S3C24XX_PA_RTC,
		.end   = S3C24XX_PA_RTC + 0xff,
		.flags = IORESOURCE_MEM,
	},
	[1] = {
		.start = IRQ_RTC,
		.end   = IRQ_RTC,
		.flags = IORESOURCE_IRQ,
	},
	[2] = {
		.start = IRQ_TICK,
		.end   = IRQ_TICK,
		.flags = IORESOURCE_IRQ
	}
};
```

我们再回到at2440evb_devices这个结构体。在这里注册到平台设备里去了。这边放进去了，那边才有得拿。

```
static void __init at2440evb_init(void)
{
	s3c24xx_fb_set_platdata(&at2440evb_fb_info);
	s3c24xx_mci_set_platdata(&at2440evb_mci_pdata);
	s3c_nand_set_platdata(&at2440evb_nand_info);
	s3c_i2c0_set_platdata(NULL);

	platform_add_devices(at2440evb_devices, ARRAY_SIZE(at2440evb_devices));
}
```

我们继续回到s3c_rtc_probe函数。

2、用request_mem_region来声明对某块内存区域的占用。返回不是null就是成功的。这个是一个标记行为。是为了避免其他的驱动来使用这块区域。

ioremap则是完成了物理地址到虚拟地址的转换。得到虚拟地址，这样在驱动里，就用虚拟地址进行操作就好了。

这2个函数都是配套使用的。

3、基于上面ioremap得到的虚拟地址。来读取rtc相关寄存器，使能rtc。

4、调用drivers/rtc/class.c里的rtc_device_register函数来注册rtc设备。传递进去的一个重要结构体是：s3c_rtcops。返回值是rtc_device指针。这个下面再看。

5、把rtc_device指针传递给platform_set_drvdata。

probe函数到这里就完成了。

## 看看s3c_rtcops结构体

结构体的类型是rtc_class_ops。定义在include/linux/rtc.h里。

包括这些功能：函数的参数都是struct device。

1、打开。

2、关闭。

3、ioctl。

4、读取时间。

5、设置时间。

6、读取闹钟。

7、设置闹钟。

8、proc。

9、set_mmss。

10、irq设置状态。

11、irq设置频率。

12、闹钟中断使能。

13、update中断使能。

我们依次看看rtc-s3c.c里的实现。

1、打开。

```
1、先用to_platform_device(struct device)，拿到platform_device指针。
2、用platform_get_drvdata拿到rtc_device指针。
3、用request_irq注册Alarm和tick中断。
```

2、关闭。

```
就是freeirq。
```

3、ioctl。

```
没有实现。
```

4、读取时间。

```
1、容纳时间的是在include/linux/rtc.h里定义的struct rtc_time结构体。处理年月日时分秒和星期，还有一个夏令时。
2、然后就是去寄存器，放入到结构体中。用readb。
```

5、设置时间。

```
用writeb写寄存器。
```

6和7省略。一样的读写寄存器。

8、proc。就读了一个寄存器。不管。（补充；后续发现有用，是在/proc/driver/rtc里打印会用到这个信息）

9、没实现。

10和11也就是写寄存器。

------

到这里，rtc-s3c.c内容基本分析完了。

然后我们要看rtc_device_register所在的drivers/rtc/class.c文件。

##drivers/rtc/class.c文件

文件大概200行。

主要函数：rtc_init。rtc_device_register。

### rtc_init函数

这个函数是static的。另外在drivers/char/rtc.c里，也有一个叫rtc_init的函数。不知道这2个是什么关系。

大概看了下，drivers/rtc/rtc.c这个文件是外接的rtc设备。我们不管 。

1、class_create。调用这个，代表在sysfs下面会产生一个节点。一般和class_device_create一起用，这样当insmod的时候，udev就会在sysfs和/dev下面各产生一个节点。

2、调用rtc-dev.c里的rtc_dev_init。

3、调用rtc-sysfs.c里的rtc_sysfs_init。

就这些。rtc_init是在系统初始化的时候自动调用的。作用是在sysfs里产生了对应的节点。这个时候，真正的rtc设备还没有ok。

### rtc_device_register

这个才是重点。当板端初始化的时候，在rtc probe的时候，会调用都这个函数。

1、获取到rtc_idr。idr是一种内核机制，用来建立int和ptr的对应关系的。然后得到一个int类型的id。

2、用kzmalloc分配一个rtc_device结构体。

3、对rtc的成员赋值。

4、调用rtc_dev_prepare。这里面调用了cdev_init函数。这里有个fops结构体。下面要看下。

5、调用device_register函数。

6、rtc_dev_add_device，里面就是调用cdev_add。

7、rtc_sysfs_add_device。里面调用device_create_file。

8、rtc_proc_add_device。调用proc_create_data("driver/rtc")

## rtc-dev.c里的rtc_dev_fops

1、open函数。

```
调用了open rtc_device的device的parent
```

2、release函数。

```
调用了关闭中断的函数？没太看懂。
```

其余不细看了。支持了异步通知。



## rtc_device结构体

1、有struct device dev

2、有struct cdev char_dev

3、flags。这个bit0是用来检测busy状态的。

支持异步通知，SIGIO。



##rtc在实际系统里的表现

我是在一个VMware里的跑alpine系统，查看rtc相关情况的。

1、/dev目录：

```
rtc   rtc0
```

2、/proc目录：

```
vm-alpine-0:/proc/driver# tree
.
└── rtc

0 directories, 1 file
vm-alpine-0:/proc/driver# cat rtc 
rtc_time        : 08:55:40
rtc_date        : 2018-01-28
alrm_time       : 00:00:00
alrm_date       : 2018-01-28
alarm_IRQ       : no
alrm_pending    : no
update IRQ enabled      : no
periodic IRQ enabled    : no
periodic IRQ frequency  : 1024
max user IRQ frequency  : 64
24hr            : yes
periodic_IRQ    : no
update_IRQ      : no
HPET_emulated   : yes
BCD             : yes
DST_enable      : no
periodic_freq   : 1024
batt_status     : okay
```

3、/sys目录：

```
vm-alpine-0:/proc/driver# cd /sys/class/rtc/rtc0/
vm-alpine-0:/sys/devices/pnp0/00:01/rtc/rtc0# ls
date           device         max_user_freq  power          subsystem      uevent
dev            hctosys        name           since_epoch    time           wakealarm
vm-alpine-0:/sys/devices/pnp0/00:01/rtc/rtc0# tree
.
├── date
├── dev
├── device -> ../../../00:01
├── hctosys
├── max_user_freq
├── name
├── power
│   ├── autosuspend_delay_ms
│   ├── control
│   ├── runtime_active_time
│   ├── runtime_status
│   └── runtime_suspended_time
├── since_epoch
├── subsystem -> ../../../../../class/rtc
├── time
├── uevent
└── wakealarm

3 directories, 14 files
```



## 结合实际情况再看代码

上面我们看到/proc/driver/rtc/rtc0里有不少信息。这个就是在rtc-proc.c里实现的。我们看看这个文件。

### rtc-dev.c

主要显示这个数据的函数是rtc_proc_show函数。

```
1、rtc_read_time，得到时间。这个函数在drivers/rtc/interface.c里。
2、rt_read_alarm。

```

##总结

涉及的文件：

```
1、rtc-s3c.c：板子相关。入口在这里。
2、class.c：相当于是rtc-dev、rtc-sysfs.c、rtc-proc.c的汇总。
3、rtc-dev.c：dev的节点。
4、rtc-sysfs.c：syfs节点。
5、rtc-proc.c：proc节点。
6、interface.c：被proc的调用。
```



