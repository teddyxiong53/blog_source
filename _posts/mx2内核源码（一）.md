---
title: mx2内核源码（一）
date: 2018-03-28 09:47:18
tags:
	- Linux内核

---



现在研究一下mx2的内核，选择这个的原因是，我有一台mx2。

下载地址在这里https://github.com/meizuosc/m040 。大小刚好100M。

内核版本是3.0.39的。

看起来确实是专用的内核源码。因为把mx2用不到的东西都删掉了。arch/arm目录下就剩下三星的。

所有文件也只有12000个左右。我用source insight可以直接全部添加进来。方便。

（后面发现不太对，怎么source insight有些文件没有自动添加进来？）

这个内核版本有点老。我的arm-linux-gnueabi是5版本的，编译会报错。

但是我的arm-none-eabi是4.7的，用这个编译就没事。

可以看到piggy.o用lzo进行了压缩。

最后得到的uImage是3.8M左右。

当前arm架构还没有引入设备树。所以看起来还是比较直观的。



开始看代码之前，还是尽可能了解一下这个手机的硬件构成。

```
发布时间2012年12月。
CPU是Exynos 4412四核处理器，是32位的。A9架构，1.6G主频。属于三星的S5P系列的。
内存是2G的DDR2。
显示屏是4.4寸，1280x800的。
Sensor是富士通的。
```

内部传感器的芯片信号看不到。从代码里去找吧。

这里有个小米3的电路图。参考一下。

https://wenku.baidu.com/view/86be9e3031b765ce050814fd.html?from=search

先看bsp文件。

是arch/arm/mach-exynos/mach-m040.c。

```
MACHINE_START(M041, "MX2")
//MACHINE_START(M040, "SMDK4X12")
	/* Maintainer: WenbinWu <wenbinwu@meizu.com> */
	.boot_params	= S5P_PA_SDRAM + 0x100,
	.init_irq	= exynos4_init_irq,
	.map_io		= m040_map_io,
	.init_machine	= m040_machine_init,
	.timer		= &exynos4_timer,
MACHINE_END
```

既然是2G的内存，看看S5P_PA_SDRAM物理地址的起始放在上面地方。

是在这里：

```
#define EXYNOS4_PA_SDRAM		0x40000000
```

寄存器都安排在这个前面。前面的空间足够大，容纳足够多的外设了。

既然是手机处理器，就可以比较专注，支持的启动介质不用那么多。

芯片手册特别长，大概2800页。不看。我专注看外设的。

先从i2c的入手。

在mach-exynos/i2c-m040.c里。

总共8个I2C设备。地址全部是0x10 。

i2c0：音频芯片。

i2c1：max77686 。电源管理芯片。

i2c2：未知。

i2c3：

i2c4：音频去噪。

i2c5：相机的ISP。

i2c6：lcd背光。

i2c7：触摸屏。

从i2c8开始，就是用gpio模拟的。一直到i2c17 。



我现在就从i2c1的设备开始追踪。

在bsp文件里的m040_machine_init里。

```
s3c_i2c1_set_platdata(&m040_default_i2c1_data);
i2c_register_board_info(1, i2c_devs1, ARRAY_SIZE(i2c_devs1));
```

顺便看一下bsp里所有的平台设备。

现在到drivers/regulator/max77686.c里。为什么这个是一个platform设备呢？

里面用了i2c的东西。

是用i2c_client来进行操作的。

这个就是一个典型的mfd设备（多功能设备）。这一块我还不太了解，刚好借此机会好好了解一下。

```
 [*]   Maxim Semiconductor MAX77686 PMIC Support 
  [*]   MX QMatrix Sensor for touchpad & leds   
```

mx2里刚好就这2个东西。

max77686就是有2个概念，一个是做电源芯片，一个是做rtc。这是人格分裂啊。

在drivers/mfd/max77686.c里。（有2个叫max77686.c的文件）

```
static struct mfd_cell max77686_devs[] = {
	{ .name = "max77686-pmic", },
#ifdef CONFIG_RTC_DRV_MAX77686
	{ .name = "max77686-rtc", },
#endif
};
```

这里还注册了

```
static int __init max77686_i2c_init(void)
{
	return i2c_add_driver(&max77686_i2c_driver);
}
/* init early so consumer devices can complete system boot */
arch_initcall(max77686_i2c_init);
```

果然在drivers/rtc/rtc-max77686.c里。治疗了还注册了rtc设备。

```
static int __init max77686_rtc_init(void)
{
	return platform_driver_register(&max77686_rtc_driver);
}
```

mfd下面那个相当于是统领全局的。

```
struct max77686_dev {
	struct device *dev;
	struct i2c_client *i2c; /* 0xcc / PMIC, Battery Control, and FLASH */
	struct i2c_client *rtc; /* slave addr 0x0c */
	struct mutex iolock;
```

这个的流程看完了。

从这里也可以看出i2c的确是非常重要。大量的外设芯片都是通过i2c跟CPU通信，因为占用管脚小。很多芯片并不需要传递大量的数据。

还是回到bsp文件。

看看按键的。

总共4个按键，电源、音量加、音量减、home键。

使用的是gpio_keys.h的结构体。

```
static struct platform_device m040_gpio_keys = {
	.name			= "gpio-keys",
	.dev			= {
		.platform_data	= &m040_gpio_keys_data,
	},
};
```

需要配置2个宏。

```
obj-$(CONFIG_INPUT_KEYBOARD)	+= keyboard/
obj-$(CONFIG_KEYBOARD_GPIO)		+= gpio_keys.o
```

这里按键是用中断方式进行检测的。

```
gpio_keys_setup_key
	1、gpio_request
	2、gpio_direction_input
	3、gpio_set_debounce
	4、gpio_to_irq(button->gpio);//这里最后调用了samsung_gpiolib_to_irq来转换的。
	5、request_any_context_irq(irq, gpio_keys_isr, irqflags, desc, bdata);
```

中断处理函数，是调度了一个work。

```
static irqreturn_t gpio_keys_isr(int irq, void *dev_id)
{
	struct gpio_button_data *bdata = dev_id;
	struct gpio_keys_button *button = bdata->button;

	BUG_ON(irq != gpio_to_irq(button->gpio));

	if (bdata->timer_debounce)
		mod_timer(&bdata->timer,
			jiffies + msecs_to_jiffies(bdata->timer_debounce));
	else
		schedule_work(&bdata->work);

	return IRQ_HANDLED;
}

```



work里做的事情是：

```
static void gpio_keys_work_func(struct work_struct *work)
{
	struct gpio_button_data *bdata =
		container_of(work, struct gpio_button_data, work);

	gpio_keys_report_event(bdata);
}
```

最后的效果就是在中断里触发把这个事情上报到/dev/input/event里了。

中断情况。

```
shell@mx2:/ $ cat /proc/interrupts
           CPU0
 16:        380  s3c-uart  s5pv210-uart
 18:        371  s3c-uart  s5pv210-uart
 26:          2  s3c-uart
 98:          0       GIC  s3c-pl330.0
 99:          0       GIC  s3c-pl330.1
100:          0       GIC  s3c-pl330.2
107:          0       GIC  s3c2410-wdt
119:          0       GIC  debug
121:         12       GIC  mct_comp_irq
122:       2819       GIC  s3c2440-i2c.0
123:      82831       GIC  s3c2440-i2c.1
126:      73076       GIC  s3c2440-i2c.4
127:      10357       GIC  s3c2440-i2c.5
128:       2802       GIC  s3c2440-i2c.6
129:      17644       GIC  s3c2440-i2c.7
134:        437       GIC  ehci_hcd:usb1
135:       7136       GIC  s3c-udc
140:     116695       GIC  mmc1
141:     131848       GIC  mmc0
142:          0       GIC  s3c-csis0
143:          4       GIC  s5p-mipi-dsim.0
147:          0       GIC  s5p-rotator
148:          0       GIC  s3c-fimc0
149:          0       GIC  s3c-fimc1
150:          0       GIC  s3c-fimc2
151:          0       GIC  s3c-fimc3
152:          0       GIC  jpeg_v2
153:          0       GIC  s5p-fimg2d
155:          0       GIC  s5p-mixer
156:          0       GIC  s5p-hdmi
158:          0       GIC  s3c-mfc
161:       1154       GIC
182:          0       GIC  Mali_PP0_MMU
183:          0       GIC  Mali_PP1_MMU
184:          0       GIC  Mali_PP2_MMU
185:          0       GIC  Mali_PP3_MMU
186:          0       GIC  Mali_GP_MMU
187:      10778       GIC  Mali_PP0
188:      10776       GIC  Mali_PP1
189:      10721       GIC  Mali_PP2
190:      10725       GIC  Mali_PP3
191:      11418       GIC  Mali_GP
212:          0  COMBINER  exynos4-tmu
231:          0  COMBINER  exynos-sysmmu.15
256:          0  COMBINER  exynos4-ppmu.4
257:          0  COMBINER  exynos4-ppmu.5
258:          0  COMBINER  exynos4-ppmu.3
275:        260  COMBINER  samsung-adc-v4
280:          0  COMBINER  s3cfb
281:       5939  COMBINER  s3cfb
352:          6  exynos-eint  gpio-keys: KEY_POWER
353:        530  exynos-eint  7-0020
354:         28  exynos-eint  RMI VBUS IRQ
355:         55  exynos-eint  max77665-irq
356:          0  exynos-eint  max77686-irq
357:          0  exynos-eint  gpio-keys: KEY_HOME
358:          8  exynos-eint  gp2ap020a00f
360:          4  exynos-eint  mx-touch-keypad
364:      23163  exynos-eint  bcmsdh_sdmmc
367:          0  exynos-eint  fsa8108 jack interrupt
369:         44  exynos-eint  bt host_wake
372:         50  exynos-eint  modem_hostwake
373:          3  exynos-eint  gpio-keys: KEY_VOLUMEUP
374:          0  exynos-eint  max77665_dock
375:          0  exynos-eint  sii9234
376:         20  exynos-eint  low_bat
378:          3  exynos-eint  gpio-keys: KEY_VOLUMEDOWN
379:          2  exynos-eint  CP_RESET_INT
383:          1  exynos-eint  hpd
387:          1  s5p_gpioint  m6mo
427:          0  max77686  rtc-alarm0
428:          0  max77686  rtc-alarm1
440:         35  max77665  max77665-charger
449:          0  max77665  max77665_adc
450:          0  max77665  max77665_adclow
451:          0  max77665  max77665_adcerr
452:          0  max77665  max77665_adc1k
IPI0:          0          0          0          0  Timer broadcast interrupts
IPI1:     154119      81428      70899     205252  Rescheduling interrupts
IPI2:         43         36         39         41  Function call interrupts
IPI3:         20          3          0         47  Single function call interrupts
IPI4:          0          0          0          0  CPU stop interrupts
IPI5:          0          0          0          0  CPU backtrace
LOC:     860939     105545     102266     208525  Local timer interrupts
```







```
machine_desc->map_io是在mmu.c里的devicemaps_init里调用。是在paging_init里。
machine_desc->init_irq是在init_IRQ里调用。这个是在start_kernel里调用。
machine_desc->init_machine是在customize_machine里调用。这个被
arch_initcall(customize_machine);这样调用到。

map_io也两个地方有，一个machine的，一个是cpu的。
各自建立一部分的固定映射。

machine_init里做的事情：
1、设置platform device的私有数据，
	然后i2c_register_board_info。
	好几个i2c的依次做。
	然后是是其他的平台设备的。
2、最后platform_add_devices用这个一锅端了。
```









