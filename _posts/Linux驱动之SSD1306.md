---
title: Linux驱动之SSD1306
date: 2018-03-08 19:45:20
tags:
	- Linux驱动

---



ssd1306是一款I2C接口的oled显示屏。

尺寸是128x64的。

这里有一套完整的代码。

https://github.com/notro/fbtft

详细介绍在这里：

https://github.com/notro/fbtft/wiki



# deferred io

Documentation/fb/deferred_io.txt里。

deferred io是一种延迟和重新定位的io。它使用host memory作为buffer和mmu页错误作为一个触发条件，来执行device io操作。

1、用户App mmap framebuffer。

2、延迟io和驱动建立错误和页写handler。

3、用户App试图去写mmap的内存。

4、产生了页错误。

5、处理处理程序返回物理页。

6、我们拿到页，添加到list。

7、在一个delay之后，调度一个workqueue任务，

8、App继续往这个页上写。这里效率很高，是这种方式是最大收益。

9、workqueue的任务执行，清理list上的页。这里是跟设备交互的实际工作。

10、app尝试去写地址，这里已经被清理了。

11、产生页错误，然后又重新走上面的流程。



允许burst写fb，代价很小。

# fbtft相关背景

fbdev的维护者不再接收任何新的fbdev drivers，所以这个驱动不能放到linux的发布包里。

fbdev是一个过时的框架。

现在更新的显示框架是DRM（Direct Rendering Manager）。对应的代码在drivers/gpu/drm目录下。

介绍在这里：http://www.wikiwand.com/en/Direct_Rendering_Manager#/media/File:Access_to_video_card_with_DRM.svg

其实这个架构有点大，小屏幕用起来有点大材小用的味道。

所以最新的kernel里提供了drivers/gpu/drm/tinydrm专门给小屏用的。

可以很方便地把fbtft转成drm。

## fbtft和tinydrm的比较

1、tinydrm只在用户请求更新的时候才更新。而fbtft则是定时刷新的。

2、fbtft只能更新整行的显示，而drm没有限制。

3、drm支持双缓冲。

4、drm支持gpu渲染。

kernel是4.11开始加入tinydrm的支持的。

##spi device和platform device

platform device是给并口设备用的。像ssd1306就没有必要。



为了说明，作者写了一个假想的lcd，叫easylcd的设备的驱动。

## 关于在Raspbian里使用fbtft

1、Raspbian强制使用/dev/fb0给X windows用。

2、关于触控板。





# 框架设计

这套驱动框架兼容了多款TFT屏幕。做得很巧妙。值得学习。

我分析其中两块屏幕的情况。

ssd1306，这个接口简单。

ili9341，我用过这个屏幕。

看看是怎样抽象的。怎样提取公共代码。

文件分布：

```
fbtft.h：定义结构体。
fbtft-bus.c：
fbtft-core.c
fbtft-io.c：spi函数。
fbtft-sysfs.c
fbtft_device.c
fb_ili9341.c
fb_ssd1306.c
```

这个的开发工作就是在树莓派上完成的。

你可以这样来编译安装：

1、把fbtft目录放到内核的drivers/video/fbdev目录下。

2、修改编译脚本。

```
Add to drivers/video/fbdev/Kconfig:   source "drivers/video/fbdev/fbtft/Kconfig"
    Add to drivers/video/fbdev/Makefile:  obj-y += fbtft/
```



#fbtft_device.c

这个模块插入需要带的参数不少：

```
insmod fbtft_device.ko name=ssd1306 rotate=0 busnum=0 cs=0 speed=100000 mode=0 gpios=reset:23,dc=24 fps=60 width=128 height=64
```

如果是

```
insmod fbtft_device.ko name=list
```

就会把支持的列表打印出来。