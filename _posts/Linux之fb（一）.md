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



# lcd的分类

lcd就是液晶显示技术制作的显示屏。

lcd根据驱动方式可以分为：

1、静态驱动。

2、简单矩阵驱动。TN（液晶分子扭转90度）和STN（液晶分子扭转180度）。

3、主动矩阵驱动。TFT（液晶分子扭转90度）。

# oled和lcd的区别

oled是1979年华裔教授邓青云发现的。

oled是有机发光二极体的缩写。

oled的显示原理跟lcd的完全不同。它不需要背光，有机材料自动会发光。



# deferred io原理分析

主要文件是：fb_defio.c。

看看这个文件里的内容：

对外接口是3个。

```
1、fb_deferred_io_init。在fb被注册的时候，调用到。
	这里做的事情最多：
	1）info->fbops->fb_mmap = fb_deferred_io_mmap;
		注册自己特有的mmap。
	2）INIT_DELAYED_WORK(&info->deferred_work, fb_deferred_io_work);
	这2个很关键。是核心原理。
2、fb_deferred_io_open，在fb被open的时候，调用到。
3、fb_deferred_io_cleanup，在fb被close的时候，调用到。
```

fb_deferred_io_mmap

```
参数就是vma。
1、给vma->vm_ops赋值为fb_deferred_io_vm_ops
	
```

fb_deferred_io_vm_ops内容是这样的。

```
static const struct vm_operations_struct fb_deferred_io_vm_ops = {
	.fault		= fb_deferred_io_fault,
	.page_mkwrite	= fb_deferred_io_mkwrite,
};
```





这里很关键。

```
info->flags =              FBINFO_FLAG_DEFAULT | FBINFO_VIRTFB;
```



fb_mmap。这个就是我们在应用层mmap时会调用到的。

set_page_dirty会怎么样？会触发去把数据刷出去吗？



理一下过程：

1、应用层mmap。就是调用到fbmem.c里的fb_mmap。

但是底层的fbtft，并没有实现fb_info里的fb_mmap了。所以这个只到fb通用层这里。

为什么fbtft的驱动不实现呢？是没有必要了。通用层的够了。我看s3c2410的也是一样的。

这里mmap的内存，到底是对应哪里分配的呢？

```
fbi->screen_base,//这个是cpu地址。
fbi->fix.smem_start//这个的dma地址。所以三星的有，fbtft的没有。
```

应用层mmap，得到的地址指向vmalloc得到的screen_base。

2、然后我写入一屏的数据。怎么走？

当前写入数据，不是用write接口，而是直接操作内存的。

这个行为如何关联到驱动层呢？

往这个内存写数据，一定会触发缺页异常，就是靠这个来驱动的。

3、fbtft_deferred_io调用到update_display。这里面write_vmem，然后用spi接口把数据发出去。

我觉得fbtft这里也是坑啊。在发送前，有一次处理。每个像素都处理了一下。

```
	for (x = 0; x < par->info->var.xres; x++) {
		for (y = 0; y < par->info->var.yres/8; y++) {
			*buf = 0x00;
			for (i = 0; i < 8; i++)
				*buf |= (vmem16[(y*8+i)*par->info->var.xres+x] ? 1 : 0) << i;
			buf++;
		}
	}
```



看看三星的，如何用dma的方式把数据发送出去。





# 关于page cache

页高速缓存（page cache）是内核所使用的主要的磁盘高速缓存机制。

在大多数情况下，内核在读写磁盘的时候，都引用page cache。

在把一页数据传送到块设备之前，内核首先检查对应的页是否已经在page cache里了。

如果不在，就在page cache加上一项。然后把要写入磁盘的数据填充进来。

io并不会马上开始，而是要延迟几秒钟。这就是延迟写操作。

几乎所有的文件读和写操作都依赖page cache。

不过可以绕过，你open的时候，传递O_DIRECT标志。



page cache的核心对象是address_space结构体。

对address_space的操作有：

writepage、readpage、write_pages、set_page_dirty、direct_IO。



linux支持大道几个TB的文件。访问大文件的时候，page cache里就有太多的文件页。

这样要顺序扫描就很耗时。

所以这里就应用了radix tree技术。



**/sys/class/graphics**

# fb保留内存的作用

项目需要在spl中显示logo，

其中就需要分配framebuffer，

如果framebuffer较小，

一般可以直接用芯片的OCMC_RAM做framebuffer，

我的芯片上的**OCMC_RAM2**和**OCMC_RAM3** 的2M内存足够显示较小的图片。

当然，2M往往是不够的用的（比如使用bmp格式的image），

这时候就需要在DDR中分配framebuffer了，下面分配一个10MB的framebuffer为例：

gd->ram_size最终会保存到内核设备树的memory节点中，修改gd->ram_size会改变内核使用的的DDR大小！

因为logo在内核阶段也要显示，所以这里直接在gd->ram_size上修改。修改的时候如果**CONFIG_SYS_MEM_TOP_HIDE**没有用，直接定义这个宏在DDR顶端保留一段内存（当然也可以自己定义一个宏）：



amlogic的设备树里，有这样来保留内存。这个内存怎么被使用的？

```
fb_reserved:linux,meson-fb {
			//compatible = "amlogic, fb-memory";
			//reg = <0x0 0x3e000000 0x0 0x1f00000>;
			compatible = "shared-dma-pool";
			reusable;
			size = <0x0 0x2000000>;
			alignment = <0x0 0x400000>;
			alloc-ranges = <0x0 0x3e000000 0x0 0x2000000>;
		};
```

搜索shared-dma-pool

有这3个地方

```
./base/dma-contiguous.c:291:RESERVEDMEM_OF_DECLARE(cma, "shared-dma-pool", rmem_cma_setup);
./base/dma-coherent.c:337:RESERVEDMEM_OF_DECLARE(dma, "shared-dma-pool", rmem_dma_setup);
./of/of_reserved_mem.c:140:         && of_flat_dt_is_compatible(node, "shared-dma-pool")
```

先看of_reserved_mem.c

最多保留16个

```
#define MAX_RESERVED_REGIONS	16
```

用这个结构体来描述

```
struct reserved_mem {
	const char			*name;
	unsigned long			fdt_node;
	unsigned long			phandle;
	const struct reserved_mem_ops	*ops;
	phys_addr_t			base;
	phys_addr_t			size;
	void				*priv;
};
```



使用是这样被用到的

```
	meson-fb {
		compatible = "amlogic, meson-axg";
		memory-region = <&fb_reserved>;
```

我当前spi lcd，没有用到meson-fb的。



参考资料

https://blog.csdn.net/z1026544682/article/details/104775740

# 参考资料

1、



