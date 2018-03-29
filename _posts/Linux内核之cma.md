---
title: Linux内核之cma
date: 2018-03-28 11:09:14
tags:
	- Linux内核

---



看mx2的内核代码。看到`m040_reserve_mem`里有涉及cma这个内容。了解一下。

先看看mx2预留了哪些内存。

```
static const char map[] __initconst =
		"ram_console=ram_console;"
		"logger=logger;"
		"android_pmem.0=pmem;android_pmem.1=pmem_gpu1;"
		"s3cfb.0/fimd=fimd;exynos4-fb.0/fimd=fimd;"
		"s3c-fimc.0=fimc0;s3c-fimc.1=fimc1;s3c-fimc.2=fimc2;s3c-fimc.3=fimc3;"
		"exynos4210-fimc.0=fimc0;exynos4210-fimc.1=fimc1;exynos4210-fimc.2=fimc2;exynos4210-fimc.3=fimc3;"
		"s3c-mfc/A=mfc0,mfc-secure;"
		"s3c-mfc/B=mfc1,mfc-normal;"
		"s3c-mfc/AB=mfc;"
		"samsung-rp=srp;"
		"s5p-jpeg=jpeg;"
		"jpeg_v1=jpeg;"
		"jpeg_v2=jpeg;"
		"exynos4-fimc-is/f=fimc_is;"
		"s5p-mixer=tv;"
		"s5p-fimg2d=fimg2d;"
		"ion-exynos=ion,fimd,fimc0,fimc1,fimc2,fimc3,fw,b1,b2;"
		"s5p-smem/mfc=mfc0,mfc-secure;"
		"s5p-smem/fimc=fimc3;"
		"s5p-smem/mfc-shm=mfc1,mfc-normal;";

	cma_set_defaults(NULL, map);
```

我们看内核里的contiguous-memory.txt文件。

#什么是cma

cma是一个框架，用来建立机器相关的连续物理内存管理。

给device分配的内存就从预留的cma区域里分配。

cma的主要目的不是分配内存，而是解析和管理内存配置。

它不跟任何的内存分配方法关联。

# 为什么需要cma

有些设备不支持分散聚合，所以需要连续的物理内存的支持。

例如相机、硬件视频编解码。

这些设备往往还需要很大一块内存。例如200万像素，就需要超过6MB的空间，kmalloc对此无能为力。

（如果不特别设置，kmalloc最大是128KB）。

有些设备需要的内存要在特别位置对齐之类的要求。

# 设计

1、cma的核心并不分配和管理内存。要专门的分配器来做这个事情。

2、请求内存的时候，device需要介绍自己的身份。好到对应的位置取内存。

3、如果不指定类型，就从common里分配。

4、为了更加灵活和可扩展，cma框架允许设备驱动注册自己的私有区域。这个私有区域只能被自己使用。

5、cma允许在运行时进行配置，在cmdline里配置，这样就不需要重新编译内核。

# 案例分析

我们假设有这么一个系统，有一个video decoder和一个camera，各需要20MB的内存，但是他们肯定是不会同时运行的。

代码就这么写：

```
static struct cma_region regions[] = {
  {.name = "region", .size=20<<20},
  {}
};
char map[] = "video,camera=region";
cma_set_default(regions, map);
```

map还可以这么写：

```
char map[] = "*=region";
```

如果还有一堆设备，需要共享一块5MB的内存。就这样写。

```
static struct cma_region regions[] = {
  {.name = "region", .size=20<<20},
  {.name = "common", .size=5<<20},
  {}
};
char map[] = "video,camera=region;*=common";
cma_set_default(regions, map);
```

# 语法分析

我们上面看到，cma主要由cma_region和map构成。

里面内容，有规定写法。



# api接口

除了上面的字符串方式，还有3个接口，你可以在驱动里用来分配cma内存。

1、cma_alloc。

2、cma_free。

3、cma_info。



动态和私有的region。





# 参考资料

1、Linux内核最新的连续内存分配器(CMA)——避免预留大块内存

https://blog.csdn.net/21cnbao/article/details/7309757

2、Documentation的contiguous-memory.txt文件。