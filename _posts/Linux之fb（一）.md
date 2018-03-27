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





