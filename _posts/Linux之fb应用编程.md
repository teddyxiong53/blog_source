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



还是要确认fb是否正常。
1、获取fb的基本信息。
2、画线，决定位置信息。
3、颜色切换，看看颜色是否正确。



# 画线

```
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <linux/fb.h>
#include <sys/ioctl.h>
#include <sys/mman.h>

// 宏定义
#define FBDEVICE    "/dev/fb0"
#define WIDTH       720   
#define HEIGHT      720

#define WHITE       0xffffffff          // test ok
#define BLACK       0x00000000
#define RED         0xffff0000
#define GREEN       0xff00ff00          // test ok
#define BLUE        0xff0000ff         
#define GREENP      0x0000ff00          // 一样，说明前2个ff透明位不起作用

// 函数声明
void draw_back(unsigned int width, unsigned int height, unsigned int color);
void draw_line(unsigned int color);

// 全局变量
unsigned int *pfb = NULL;


int main(void)
{
    int fd = -1, ret = -1;
   
   
    struct fb_fix_screeninfo finfo = {0};
    struct fb_var_screeninfo vinfo = {0};
   
    // 第1步：打开设备
    fd = open(FBDEVICE, O_RDWR);
    if (fd < 0)
    {
        perror("open");
        return -1;
    }
    printf("open %s success.\n", FBDEVICE);
   
    // 第2步：获取设备的硬件信息
    ret = ioctl(fd, FBIOGET_FSCREENINFO, &finfo);
    if (ret < 0)
    {
        perror("ioctl");
        return -1;
    }
    printf("smem_start = 0x%x, smem_len = %u.\n", finfo.smem_start, finfo.smem_len);
   
    ret = ioctl(fd, FBIOGET_VSCREENINFO, &vinfo);
    if (ret < 0)
    {
        perror("ioctl");
        return -1;
    }
    printf("xres = %u, yres = %u.\n", vinfo.xres, vinfo.yres);
    printf("xres_virtual = %u, yres_virtual = %u.\n", vinfo.xres_virtual, vinfo.yres_virtual);
    printf("bpp = %u.\n", vinfo.bits_per_pixel);

   
    // 第3步：进行mmap
    unsigned long len = vinfo.xres_virtual * vinfo.yres_virtual * vinfo.bits_per_pixel / 8;
    printf("len = %ld\n", len);
    pfb = mmap(NULL, len, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (NULL == pfb)
    {
        perror("mmap");
        return -1;
    }
    printf("pfb = %p.\n", pfb);
   
    draw_back(WIDTH, HEIGHT, WHITE);
    draw_line(RED);
   

    close(fd);
   
    return 0;
}


//刷背景函数
void draw_back(unsigned int width, unsigned int height, unsigned int color)
{
    unsigned int x, y;
   
    for (y=0; y<height; y++)
    {
        for (x=0; x<width; x++)
        {
            *(pfb + y * WIDTH + x) = color;
        }
    }
}

//画线函数
void draw_line(unsigned int color)
{
    unsigned int x, y;
   
    for (x=50; x<600; x++)
    {
        *(pfb + 200 * WIDTH + x) = color;
    }
}
```



参考资料

1、

https://www.codenong.com/cs106598190/