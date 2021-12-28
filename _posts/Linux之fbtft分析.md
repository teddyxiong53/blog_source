---
title: Linux之fbtft分析
date: 2021-12-17 15:20:11
tags:
	- Linux

---

--

fbtft的基本信息

```
Linux Framebuffer drivers for small TFT LCD display modules.
The module 'fbtft' makes writing drivers for some of these displays very easy.

Development is done on a Raspberry Pi running the Raspbian "wheezy" distribution.
```

是专门针对tft小型lcd屏幕开发的。

基于树莓派进行验证。

让在linux上开发小型tft lcd驱动变得简单。

主要的文件：

```
fb_st7798v.c
	这个是每个lcd不同的，主要实现4个函数：
		init_display
		set_var
		set_gamma
		blank
fbtft-bus.c
	定义了fbtft_write_reg8_bus8这样的一些函数。
fbtft-core.c
	这个是核心逻辑。
fbtft-io.c
	fbtft_write_spi 这样一些函数。
fbtft-sysfs.c
	调试用途。
fbtft.h
	所有函数都在这里声明。
fbtft_device.c
	这个罗列了很多的板子的情况。
	从这个看，这个就难以被放入kernel的正式驱动里。
```



fbtft_device_init

这个初始化的时候被调用。

```
arch_initcall(fbtft_device_init);
```

不是，这个必须被作为module来编译，如果编译进内核，则不行。

因为需要一些参数。这些参数必须在insmod的时候被传递进来。

arch_initcall在定义了MODULE宏的时候，是被定义为module_init的。

这个没有问题。

当前内核默认有编译哪些为module的？

有的

```
./drivers/amlogic/ddr_tool/ddr_window.ko
```

也被安装到文件系统里去了。

```
./lib/modules/4.9.113/kernel/drivers/amlogic/ddr_tool/ddr_window.ko
```

所以这个就不用我操心。可以编译为module。

后续只需要把fbtft的选配为module就好了。

现在再看fbtft_device.c里的displays数组里，没有st7789v的。

这个displays数组，还是违反了设备树的原则，在c文件里写了很多的信息。

我应该是要自己把自己的板子的情况加进去。



insmod传递的参数示例

```

```



dc的确是区分数据和命令的。

- **dc-gpios**
  Data/Command (sometimes called RS)

- **led-gpios**
  Backlight

初始化序列也可以在设备树里写。



fbtft_device.c 是不被推荐使用的。

fbtft will now only work with Device Tree due to the above mentioned disruptive gpio rework

这个是需要单独被配置的。

```
obj-$(CONFIG_FB_TFT_FBTFT_DEVICE) += fbtft_device.o
```

所以，当fbtft_device.c 不存在就好了。



这样使用x window来测试

```
FRAMEBUFFER=/dev/fb1 startx
```



现在实际的入口函数是fbtft_probe_common

里面调用了解析fbtft_probe_dt设备树。

设备树里解析这些

```
pdata->display.width = fbtft_of_value(node, "width");
	pdata->display.height = fbtft_of_value(node, "height");
	pdata->display.regwidth = fbtft_of_value(node, "regwidth");
	pdata->display.buswidth = fbtft_of_value(node, "buswidth");
	pdata->display.backlight = fbtft_of_value(node, "backlight");
	pdata->display.bpp = fbtft_of_value(node, "bpp");
	pdata->display.debug = fbtft_of_value(node, "debug");
	pdata->rotate = fbtft_of_value(node, "rotate");
	pdata->bgr = of_property_read_bool(node, "bgr");
	pdata->fps = fbtft_of_value(node, "fps");
	pdata->txbuflen = fbtft_of_value(node, "txbuflen");
	pdata->startbyte = fbtft_of_value(node, "startbyte");
	of_property_read_string(node, "gamma", (const char **)&pdata->gamma);

	if (of_find_property(node, "led-gpios", NULL))
		pdata->display.backlight = 1;
	if (of_find_property(node, "init", NULL))
```

gpio的单独在这里解析

```
ret = fbtft_request_one_gpio(par, "reset-gpios", 0, &par->gpio.reset);
	if (ret)
		return ret;
	ret = fbtft_request_one_gpio(par, "dc-gpios", 0, &par->gpio.dc);
	if (ret)
		return ret;
	ret = fbtft_request_one_gpio(par, "rd-gpios", 0, &par->gpio.rd);
	if (ret)
		return ret;
	ret = fbtft_request_one_gpio(par, "wr-gpios", 0, &par->gpio.wr);
	if (ret)
		return ret;
	ret = fbtft_request_one_gpio(par, "cs-gpios", 0, &par->gpio.cs);
	if (ret)
		return ret;
	ret = fbtft_request_one_gpio(par, "latch-gpios", 0, &par->gpio.latch);
	if (ret)
		return ret;
	for (i = 0; i < 16; i++) {
		ret = fbtft_request_one_gpio(par, "db-gpios", i,
						&par->gpio.db[i]);
		if (ret)
			return ret;
		ret = fbtft_request_one_gpio(par, "led-gpios", i,
						&par->gpio.led[i]);
		if (ret)
			return ret;
		ret = fbtft_request_one_gpio(par, "aux-gpios", i,
						&par->gpio.aux[i]);
		if (ret)
			return ret;
	}
```

# 驱动框架

同时注册了spi 设备和platform设备。

```
static int __init fbtft_driver_module_init(void)                           \
{                                                                          \
	int ret;                                                           \
									   \
	ret = spi_register_driver(&fbtft_driver_spi_driver);               \
	if (ret < 0)                                                       \
		return ret;                                                \
	return platform_driver_register(&fbtft_driver_platform_driver);    \
}  
```



旋转是这么处理的

```
	switch (pdata->rotate) {
	case 90:
	case 270:
		width =  display->height;
		height = display->width;
		break;
	default:
		width =  display->width;
		height = display->height;
	}
```



# X11启动流程

自己完全整理带显示屏的x11的图形界面启动流程。

以fbtft的为切入点。

这个文档还是非常齐全的。各个环节都涉及到了。

https://github.com/notro/fbtft/wiki/Bootsplash#prerequisites

## bootsplash

这个是什么概念？splash是泼溅的意思。

在U-Boot中使用Splash Screen，可以实现U-Boot启动后，在LCD上显示自定义图片，起到友好的界面显示作用。使用Splash Screen需要在配置文件中使能BMP图片功能和SPLASH功能：

\#define CONFIG_CMD_BMP
\#define CONFIG_SPLASH_SCREEN

现在要实现splash screen，需要进行操作，先下载一个图片到内存中，然后擦除FLASH的splashimage区域，接着将图片写入splashimage区域，最后设置并保存splashimage环境变量即可。

```

    U-Boot> tftp a0008000 logo.bmp                   ；下载文件到内存
    U-Boot> erase 1:23-31                                 ；擦除Flash的splashimage区域
    U-Boot> cp.b a0008000 00180000 $filesize    ；将logo写到Flash的splashimage区域
    U-Boot> setenv splashimage 00180000         ；设置splashimage环境变量
    U-Boot> saveenv                                         ；保存环境变量
```

```
u-boot启动后，输入bmp d $splashimage即可在LCD上显示logo图片。为了实现开机就显示logo，可以修改 common/lcd.c文件，在其中加入实现 bmp d $splashimage的代码即可。
```

Linux内核原版中是没有bootsplash功能的，就是启动进度条和console的背景图的功能。需要对其进行打补丁才能实现。
官方网站：http://www.bootsplash.org ，下载对应内核版本的bootsplash补丁，这样内核配置里就能选择了。



参考资料

1、

https://blog.csdn.net/CSDN_logo/article/details/46890843

2、

https://blog.csdn.net/shooter556/article/details/2462609

# 参考资料

1、fbtft的设备树配置

https://github.com/notro/fbtft/wiki/Device-Tree