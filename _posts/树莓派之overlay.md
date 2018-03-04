---
title: 树莓派之overlay
date: 2018-03-03 20:38:40
tags:
	- 树莓派

---



设备树让支持多种硬件配置，用一个kernel，不用指定模块。

设备树是通过config.txt来控制模块的开关的。

你如果要完全关闭这个功能，就加上这个：

```
device_tree=
```

start.elf文件选择dtb文件，读取到内存里，这个时候，所有的外设接口（i2c、spi等）都是禁用状态的。

指定模块的加载，有2个文件：

/etc/modules

/etc/modprobe.d/raspi-blacklist.conf

overlays通过在config.txt里的dtoverlay来指定被加载

例如lirc-rpi模块。lirc是Linux 红外控制的驱动。

要加载这个模块，在有device tree之前，你要在/etc/modules里加上，或者用modprobe命令来加载驱动。

有了device tree，你只需要再config.txt里加上：

```
dtoverlay=lirc-rpi
```

这个的效果是让/boot/overlays/lirc-rpi-overlay.dtb被加载，默认要使用gpio17（out）和gpio18（in）。

不过你可以用参数来修改：

```
dtoverlay=lirc-rpi,gpio_out_pin=17,gpio_in_pin=13
```



我们以enc28j60为例进行分析。

```
Name:   enc28j60
Info:   Overlay for the Microchip ENC28J60 Ethernet Controller (SPI)
Load:   dtoverlay=enc28j60,<param>=<val>
Params: int_pin                 GPIO used for INT (default 25)

        speed                   SPI bus speed (default 12000000)
```

看对应的dts文件。



一个现代的soc是一个很复杂的设备。把soc放在板子上，跟一堆的外设进行搭配，让情况就更加复杂了。

所以要dtsi要把公共的东西提取出来。

而树莓派这样的设备，支持外接的扩展板，问题就更加复杂。

每个可能的配置都要一个device tree来描述。



解决的方法是，用一种局部的device tree来描述可选设备。

把一个基础device tree跟这些局部device tree一起来构造一个完整的设备树。



在/proc/device-tree可以看到信息。

