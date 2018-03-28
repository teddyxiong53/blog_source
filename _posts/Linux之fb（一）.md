---
title: Linux之fb（一）
date: 2018-03-27 17:02:30
tags:
	- Linux

---



现在从应用入手。

测试环境是mylinuxlab。sudo make boot-ui。

当前通过这个程序，可以控制显示屏的颜色了。

```
#include <stdio.h>
#include <fcntl.h>
#include <linux/fb.h>
#include <sys/mman.h>
#include <stdlib.h>

struct fb_var_screeninfo vinfo;

int
main(int argc, char *argv[])
{
	int fbfd, fbsize, i;
	int red, green, blue;
	unsigned char *fbbuf;

	if (argc != 4)
	{
		printf("usage: use-fb red green blue/n");
		exit(0);
	}
	red = atoi(argv[1]);
	green = atoi(argv[2]);
	blue = atoi(argv[3]);

	/* Open video memory */
	if ((fbfd = open("/dev/fb0", O_RDWR)) < 0)
	{
		exit(1);
	}
	/* Get variable display parameters */
	if (ioctl(fbfd, FBIOGET_VSCREENINFO, &vinfo))
	{
		printf("Bad vscreeninfo ioctl/n");
		exit(2);
	}
	/* Size of frame buffer */
	fbsize = vinfo.xres*vinfo.yres*(vinfo.bits_per_pixel/8);
	/* Map video memory */
	if ((fbbuf = mmap(0, fbsize, PROT_READ | PROT_WRITE,
	                  MAP_SHARED, fbfd, 0)) == (void *) -1)
	{
		exit(3);
	}
	/* Clear the screen */
	for (i = 0; i < fbsize; i++)
	{
		*(fbbuf + i++) = red;
		*(fbbuf + i++) = green;
		*(fbbuf + i) = blue;
	}

	printf("clear screen with rgb:%s %s %s/n", argv[1], argv[2], argv[3]);
	munmap(fbbuf, fbsize);
	close(fbfd);
}
```

测试方法是：

```
./a.out 255 0 0
```

现在用minigui来做一个简单的界面看看。

先下载minigui代码，交叉编译好。

```
CC=arm-linux-gnueabi-gcc \
                 CXX=arm-linux-gnueabi-g++ \
                 LD=arm-linux-gnueabi-ld \
                 AS=arm-linux-gnueabi-as \
                 AR=arm-linux-gnueabi-ar \
                 ./configure --prefix=/usr/local/minigui  --build=x86_64-ubuntu-linux --host=arm-linux-gnueabihf 
```

然后make和sudo make install。

但是，这样得到的很多东西没有编译进来。



这个配置非常奇怪。我暂时不用minigui了。



研究一下configure。我感觉这个跟minigui的make menuconfig重叠了。

我就不用menuconfig，只用configure。

```
1、--prefix= 这个可以用。
2、
```



```
By default, `make install' will install all the files in
`/usr/local/bin', `/usr/local/lib' etc.  You can specify
an installation prefix other than `/usr/local' using `--prefix',
for instance `--prefix=$HOME'.
```

然后有一堆的enable。是可以加上的。很多默认都是no。

这个默认是no，这就是前面链接出问题的原因。

```
--enable-ctrlscrollview 
```



这些可以自己改。

```
Some influential environment variables:
  CC          C compiler command
  CFLAGS      C compiler flags
  LDFLAGS     linker flags, e.g. -L<lib dir> if you have libraries in a
              nonstandard directory <lib dir>
  LIBS        libraries to pass to the linker, e.g. -l<library>
  CPPFLAGS    (Objective) C/C++ preprocessor flags, e.g. -I<include dir> if
              you have headers in a nonstandard directory <include dir>
  CPP         C preprocessor
```



现在总结配置为：

```
 ./configure --prefix=/usr/local/minigui  --build=x86_64-ubuntu-linux --host=arm-linux-gnueabihf   --enable-ctrlscrollview=yes
```

这样配置后，完全重新编译安装。

编译helloworld.C文件。

```
arm-linux-gnueabihf-gcc helloworld.c -static -lminigui_procs -L/usr/local/minigui/lib -I/usr/local/minigui/include -lm
```

注意工具链也要带上hf的。不然会报浮点数错误。

现在运行报错。

```
/mnt/app/ui # ./a.out 
MISC: Can not locate your MiniGUI.cfg file or bad files!
KERNEL>InitGUI (step 2): Can not initialize miscellous things!
/mnt/app/ui # 

```



ui组件的也暂时不编译了。太浪费时间，当前对我来说没有价值。

# 通路分析

1、应用层，open /dev/fb0 。fb0这个设备是怎么注册进来的？

在drivers/video/fbdev/core/fbmem.c里的。

```
static int __init
fbmem_init(void)
{
	proc_create("fb", 0, NULL, &fb_proc_fops);

	if (register_chrdev(FB_MAJOR,"fb",&fb_fops))
```

这里注册了dev、proc、sysfs这3个文件节点。

fb_fops。

vexpress-a9是编译了哪个具体的fb驱动呢？

是这个。

```
obj-$(CONFIG_FB_ARMCLCD)	  += amba-clcd.o
```

这个文件就相当于fb_ssd1306.c这种文件的地位，是底层驱动。

通过register_framebuffer来向系统注册。

```
xhl -- func:amba_clcdfb_init, line:1068 
clcd-pl11x 10020000.clcd: PL111 designer 41 rev2 at 0x10020000
clcd-pl11x 10020000.clcd: /clcd@10020000 hardware, 1024x768@59 display
Console: switching to colour frame buffer device 128x48
clcd-pl11x 1001f000.clcd: PL111 designer 41 rev2 at 0x1001f000
clcd-pl11x 1001f000.clcd: /smb@4000000/motherboard/iofpga@7,00000000/clcd@1f000 hardware, 640x480@59 display
```

在内核里，module_init变成了这种。

```
#define module_init(x)	__initcall(x);
```



我看fb设备有2个，fb0和fb1，默认是操作fb0，对fb1操作不会报错，但是没有用。

