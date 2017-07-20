---
title: Linux之fb应用编程
date: 2017-07-17 23:38:56
tags:

	- Linux

	- fb

---

fb（frame buffer）是Linux为显示设备提供的一个统一操作接口。通过fb来显示汉字，是Linux汉化的唯一可行方式。

fb在/dev/fb#，最多可以有32个fb设备，从fb0到fb31，一般是一个显卡对应一个fb。

主设备号是29，次设备号是0到31 。

# 1. 对fb可以进行的操作

1、读写。

`cp /dev/fb0 ./screen_pic`。可以把当前屏幕显示内容保存为图片。

`cp ./scrren_pic /dev/fb0`。则可以把文件内容输出到屏幕上。

2、映射。

由于Linux工作在保护模式，每个程序都自己的虚拟地址空间，在应用程序中是不能直接访问物理地址的。所以通过mmap把fb的物理地址映射到用户空间的虚拟地址上，应用就可以通过这个虚拟地址来操作fb了。

3、ioctl。

主要是获取和设置参数。



# 2. 应用中一般操作fb的步骤

1、打开/dev/fb设备。

2、用ioctl获取屏幕的参数。

3、mmap fb到用户空间。

```
#include <linux/fb.h>
#include <fcntl.h>
#include <stdio.h>


int main()
{
	int fd = 0;
	struct fb_var_screeninfo var_info;
	struct fb_fix_screeninfo fix_info;
	long screen_size;
	fd = open("/dev/fb0", O_RDWR);
	if(fd < 0)
	{
		printf("open fb failed \n");
		return -1;
	}
	ioctl(fd, FBIOGET_FSCREENINFO, &fix_info);
	ioctl(fd, FBIOGET_VSCREENINFO, &var_info);
	printf("-----------fix info-------------\n");
	printf("			id:%s \n\
			smem_start:%lu\n\
			smem_len:%lu\n\
			type:%d\n\
			type_aux:%d\n\
			visual:%d\n\
			xpanstep:%d\n\
			ypanstep:%d\n\
			line_length:%d\n\
			mmio_len:%d\n\
			accel:%d\n\
	\n", 
	fix_info.id,
	fix_info.smem_start,
	fix_info.smem_len,
	fix_info.type,
	fix_info.type_aux,
	fix_info.visual,
	fix_info.xpanstep,
	fix_info.ypanstep,
	fix_info.ywrapstep,
	fix_info.line_length,
	fix_info.mmio_len,
	fix_info.accel

	);
	
	printf("--------------------------------\n");
	
	printf("-----------var info-------------\n");
	printf("			\
			xres:%d\n\
			yres:%d\n\
			xres_virtual:%d\n\
			yres_virtual:%d\n\
			xoffset:%d\n\
			yoffset:%d\n\
			bits_per_pixel:%d\n\
			nonstd:%d\n\
			activate:%d\n\
			height:%d\n\
			width:%d\n\
			accel_flags:%d\n\
			pixclock:%d\n\
			left_margin:%d\n\
			right_margin:%d\n\
			upper_margin:%d\n\
			lower_margin:%d\n\
			hsync_len:%d\n\
			vsync_len:%d\n\
			vmode:%d\n\
	\n", 
	var_info.xres,
	var_info.yres,
	var_info.xres_virtual,
	var_info.yres_virtual,
	var_info.xoffset,
	var_info.yoffset,
	var_info.bits_per_pixel,
	var_info.nonstd,
	var_info.activate,
	var_info.height,
	var_info.width,
	var_info.accel_flags,
	var_info.pixclock,
	var_info.left_margin,
	var_info.right_margin,
	var_info.upper_margin,
	var_info.lower_margin,
	var_info.hsync_len,
	var_info.vsync_len,
	var_info.vmode
	
	);
	
	printf("--------------------------------\n");
	return 0;
}

```

# 3. fb.h里重要结构体分析

最高层次的结构体是fb_info。

```
fb_info
	fb_fix_screeninfo
	fb_var_screeninfo
	fb_ops
	fb_cmap
```

