---
title: amlogic之显示屏调试
date: 2021-06-21 17:20:33
tags:
	- amlogic

---

--

分为：屏幕驱动和fb驱动。

又进一步分为：uboot下的驱动和kernel下的驱动。

开始是完全不显示，通过回退版本对比，发现是某一次修改时序相关的寄存器导致了无法显示。

去掉对应的修改，显示屏可以正常驱动。

uboot和kernel做一样的修改，都可以驱动显示屏。

现在uboot和kernel 的fb显示都不正常。

uboot下的表现是：显示的logo是完全乱的。

kernel下的表现是：完全显示不出来。

```
cat /dev/urandom > /dev/fb0
```

这个命令没有看到效果。

uboot的logo显示是乱的，是因为uboot针对新的CPU做了修改。没有兼顾到老的CPU。

就一个宏，新的芯片是64字节对齐，而老的芯片是32字节对齐。改了就好了。

kernel同一个宏也要做一样的修改。

这个时候，kernel里的显示还不正常。

还需要修改：

1、uboot里的fb_width和fb_height要设置为正确值。

2、设备树里的meson-fb也要设置这个为正确值。

```
display_size_default = <720 720 720 1440 32>;
```

现在执行fb的测试程序。就正常了。

用urandom随机数也可以正常了。

接下来就是qt的测试。qt直接就正常的了。

然后是触摸屏和qt触摸屏的结合。这个在《qt之触摸支持.md》里有写。

跑wearable这个qt的官方例子，是比较符合我们的需求的。

然后是性能评估。这个需要梳理一下总体的思路。

经过对directfb和ge2d的编译验证。

现在的方向是：qt+ge2d。不要使用directfb。

directfb有问题。

而当前我的qt之所以还没有用上ge2d。是因为我当前用的是5.12版本的qt。

而之前他们的补丁都是在5.8上做的。

当前我有两个选择：

1、把5.8的patch放到5.12上来用。

2、使用5.8版本的qt。

先看看5.8的patch能不能打到5.12上来。

我看看5.8版本和5.9版本的patch的区别有多大。

区别不大，5.9版本的补丁更加集中一些。

我尝试用5.9版本的补丁打到5.12的看看。

当前没有看到哪里配置了5.12啊。

在package/qt5/qt5.mk里配置的。

```
QT5_VERSION_MAJOR = 5.12
QT5_VERSION = $(QT5_VERSION_MAJOR).7
```

补丁打不上去。所以还是使用5.9.2的版本吧。

需要改动这些：

```
QT5_VERSION_MAJOR = 5.9
QT5_VERSION = $(QT5_VERSION_MAJOR).2
QT5_SOURCE_TARBALL_PREFIX = opensource-src # opensource现在的版本是叫everywhere
```

make一下。

报错。

```
ERROR: No hash found for qtbase-opensource-src-5.9.2.tar.xz
```

这个方向可能更加麻烦。

我还是尝试一下把补丁内容合入到5.12版本里。

先试一下。看改动并不多。

src/gui/kernel/qplatformintegration.cpp

加了一个空函数。

```
unsigned long QPlatformIntegration::get_phy_info(unsigned long mem)
{
}
```

src/gui/kernel/qplatformintegration.h

加上声明。

```
virtual unsigned long get_phy_info(unsigned long mem);
```

src/gui/painting/ge2d.h

新增这个文件。

src/gui/painting/ge2d_com.h

新增这个文件。

src/gui/painting/ge2d_port.h

新增

src/gui/painting/painting.pri

加上这2个文件。

```
+        painting/qpathsimplifier_p.h \
+        painting/qdrawhelper_ge2d_p.h
```

```
+        painting/qpathsimplifier.cpp \
+        painting/qdrawhelper_ge2d.cpp
```

src/gui/painting/qdrawhelper.cpp

```

```

都手动把修改点改了。

3个补丁自己修改自己。我就合并成一个补丁了。

```
diff -uprN qt5base-5.12.7 qt5base-5.12.7-modify > 0005-qt5base-fix-ge2d.patch
```

把补丁放入目录。

然后编译qt5base。没有报错。

很好。

完整编译，烧录镜像看看。

现在看ge2d的中断还是没有。

看看开机过程的ge2d相关打印。只有这4行。

```
[    6.845663@3]- ge2d: ge2d_init_module
[    6.846764@3]- ge2d: ge2d clock is 249 MHZ
[    6.850006@3]- ge2d: reserved mem is not used
[    6.854314@3]- ge2d: ge2d start monitor
```

那就要到qt里加打印调试了。

ge2d是怎样控制的？有设备节点吗？

发现有一个ge2d_feature_test的程序。

执行一下，提示：

```
[ion.c - ion_open:111]open /dev/ion failed: No such file or directory
ionmem error: No such file or directory failed: '(null)'
```

libion这个库是做什么用到？

 ION是google在Android4.0 为了解决内存碎片管理而引入的通用内存管理器,

在面向程序员编程方面，它和ashmem很相似。但是终究还是ION更胜一筹。

目前系统里倒是有一个/dev/ionvideo的节点。

ge2d_feature_test在这个目录下 hardware\aml-4.9\amlogic\libge2d\

看readme里有这样的描述

```

if dma buffer is allocated by ge2d, please add content blow in DTS:

/ {
    /* ...... */
    reserved-memory {
        /* ...... */
            ge2d_cma_reserved:linux,ge2d_cma {
                compatible = "shared-dma-pool";
                reusable;
                status = "okay";
                size = <0x0 0x1800000>;
                alignment = <0x0 0x400000>;
            };
    }
    /* ...... */
    ge2d {
        /* ...... */
        memory-region = <&ge2d_cma_reserved>;
    };
}
```

目前设备树里没有为ge2d预留内存。

这个好像就是一大块预留的内存，也配了一个设备节点来进行操作。代码很简单。

```
int ion_open() {
    int fd = open("/dev/ion", O_RDONLY | O_CLOEXEC);
    if (fd < 0) ALOGE("open /dev/ion failed: %s", strerror(errno));

    return fd;
}
```

这个暂时不管。这个是这个测试程序需要的东西。

把qt里针对ge2d的改动梳理一下。

改动主要涉及：

```
src/gui/kernel
	这个下面是平台集成。加了一个空函数。
	get_phy_info 这个要返回值的，都没有返回，那么默认就是返回0估计。写了个代码验证了一下，是返回0.
src/gui/painting
	这个加的多一点。
	加了qdrawerhelper_ge2d.cpp，还有几个头文件。
	
```

看qdrawerhelper.cpp里

```
static bool is_format_support_ge2d(int format, int *pxiel_format)
{
enum  {
    PIXEL_FORMAT_RGBA_8888          = 1,
    PIXEL_FORMAT_RGBX_8888          = 2,
    PIXEL_FORMAT_RGB_888            = 3,
    PIXEL_FORMAT_RGB_565            = 4,
    PIXEL_FORMAT_BGRA_8888          = 5,
    PIXEL_FORMAT_ARGB_8888          = 6,
}pixel_format_t;
```

只支持这些格式，那么我当前用的又是哪种格式呢？

PIXEL_FORMAT_ARGB_8888 这个的可能性比较大。

感觉加的这个代码分支进不来。

```
    int ge2d_src_format, ge2d_dst_format;
    if (is_continous_phys_addr(src_addr, &src_addr_phys) && is_continous_phys_addr(dst_addr, &dst_addr_phys) &&
        is_format_support_ge2d(src_format, &ge2d_src_format) && is_format_support_ge2d(dst_format,&ge2d_dst_format)) {
        aml_ge2d_info_t ge2dinfo;
        ge2dinfo.src_info[0].canvas_w = src_width;
        ge2dinfo.src_info[0].canvas_h = src_height;
```



```
#define FILE_NAME_GE2D        "/dev/ge2d"
```





# 参考资料

1、ION详细分析

https://blog.csdn.net/pillarbuaa/article/details/79206224