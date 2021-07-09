---
title: gui之directfb
date: 2021-06-09 13:23:11
tags:
	- gui

---

--

DirectFB是一个**轻量级**的**提供硬件图形加速**，输入设备处理和抽象的**图形库**，

它集成了支持**半透明的视窗系统**以及在LinuxFramebuffer驱动之上的**多层显示**。

它是一个用软件封装当前硬件无法支持的图形算法来完成硬件加速的层。

DirectFB是为嵌入式系统而设计。

**它是以最小的资源开销来实现最高的硬件加速性能。**



DirectFB是图形API

存在于Frame Buffer层之上

高级图形管理层如GTK+等之下的。



它可以以很小的系统资源占用来提供图形硬件加速功能，

提供类如多路a通道渲染模型等高级图像操作。

**它不修改Linux内核，除了标准C库没有其他库的依赖。**

应用在了基于Linux系统的DTV显示系统的研发和其他有关Linux显示界面的项目上。

支持市面上绝大多数显示卡，支持键盘、鼠标、遥控器、游戏手柄、触摸屏等输入设备。

支持JPEG、PNG、GIF、mpeg1/2、AVI、MOV、Flash、Video4Linux、DirectFB bitmap font和TrueType等音视频文件和字体。



![img](../images/random_name/20140913150108414)



![img](../images/random_name/20140913150530946)



 对于底层的驱动来说，DirectFB里面负责和硬件打交道的显卡的驱动（gfxdriver）和显示系统（system），**这里面gfxdriver是和各个硬件平台相关的，有可能需要自己写。** 为了更易于理解DirectFB，需要先介绍几个DirectFB里面的概念：

- Layers：代表互相独立的图形缓存。大多数嵌入式设备都有多个layer。多个layer根据对应的alpha值混合 在一起，从而显示出来。 
- Surface：代表一块预留的内存，来保存像素数据。DirectFB中的Drawing，Bilitting操作就是基于 surface的。Surface的内存根据设定，可以从系统中分配，也可以从显卡的内存中分配。
- Primary Surface：代表一个特殊layer的特殊surface。如果primary surface是单缓冲的，任何对于 primary surface的操作都会直接反应到显示屏上。
- Subsurface：是一个surfac的子集，但是自身并不占有任何内存。
- Window/Windowstack：控制一个layer中的surface该显示什么。Window属于某个背景可以设定的layer。 每个window有自己的surface，window用这个surface来组合图像。 



 比如说下图中有三个Layer，最下面的Layer是一幅背景图，中间的Layer是一个透明的带有一个“igel”的Layer，最上面是一个透明的带有subtitle的Layer，最后我们在显示器中看到的就是各个Layer的混合。

![img](../images/random_name/20140913151204098)



**DirectFB的移植**

 如果要移植DirectFB需要用到以下的第三方库，如下图所示：

![img](../images/random_name/20140913152105341)



DirectFB需要用到第三方库简介：

- fontconfig-2.10.92：管理系统安装的字体，根据应用程序的字体配置，match（匹配）一种字体，填充match字体的各种属性。
- freetype-2.5.0：FreeType库是一个完全免费（开源）的、高质量的且可移植的字体引擎，它提供统一的接口来访问多种字体格式文件，包括TrueType, OpenType, Type1, CID, CFF, Windows FON/FNT, X11 PCF等。
- jpeg-8d：jpeg开源库
- libpng-1.5.8：PNG 库是用来创立和操作PNG 格式的图像文件，PNG 格式是设计来替代GIF，他对于更小范围的TIFF(标记图象文件格式)来说，有了非常多的进步和拓展并且减少了关于专利权的麻烦。
- libsigc++-2.2.8：libsigc++是实现类型安全回调的一个C++模板库。libsigc++提供了信号(signal)和槽(slot)的概念，实现了信号机制。slot对应一个回调函数，信号(signal)与槽(slot)相关联(attach)，当一个信号被发射(emit)时，相对应的槽被调用。
- libxml2-2.6.28：包含了对 XPath 表达式使用的支持来检索匹配一个指定准则的结点集。libxml2软件包提供允许用户操控XML文件的函数库,包含有读、修改和写XML和HTML文件支持。

directfb在buildroot里已经有集成了。所以不需要自己去移植了。

我们看看directfb的package里的内容。

这个就是指定gfx驱动的。我的当前是amlgfx这个名字。

```
DIRECTFB_GFX = \
	$(if $(BR2_PACKAGE_DIRECTFB_AMLGFX),amlgfx) \
	$(if $(BR2_PACKAGE_DIRECTFB_ATI128),ati128) \
	$(if $(BR2_PACKAGE_DIRECTFB_CYBER5K),cyber5k) \
	$(if $(BR2_PACKAGE_DIRECTFB_MATROX),matrox) \
	$(if $(BR2_PACKAGE_DIRECTFB_PXA3XX),pxa3xx) \
	$(if $(BR2_PACKAGE_DIRECTFB_I830),i830) \
	$(if $(BR2_PACKAGE_DIRECTFB_EP9X),ep9x)

ifeq ($(strip $(DIRECTFB_GFX)),)
DIRECTFB_CONF_OPTS += --with-gfxdrivers=none
else
DIRECTFB_CONF_OPTS += \
	--with-gfxdrivers=$(subst $(space),$(comma),$(strip $(DIRECTFB_GFX)))
endif
```

这样来指定input驱动。

```
DIRECTFB_INPUT = \
	$(if $(BR2_PACKAGE_DIRECTFB_LINUXINPUT),linuxinput) \
	$(if $(BR2_PACKAGE_DIRECTFB_KEYBOARD),keyboard) \
	$(if $(BR2_PACKAGE_DIRECTFB_PS2MOUSE),ps2mouse) \
	$(if $(BR2_PACKAGE_DIRECTFB_SERIALMOUSE),serialmouse) \
	$(if $(BR2_PACKAGE_DIRECTFB_TSLIB),tslib)

ifeq ($(BR2_PACKAGE_DIRECTFB_TSLIB),y)
DIRECTFB_DEPENDENCIES += tslib
endif

ifeq ($(strip $(DIRECTFB_INPUT)),)
DIRECTFB_CONF_OPTS += --with-inputdrivers=none
else
DIRECTFB_CONF_OPTS += \
	--with-inputdrivers=$(subst $(space),$(comma),$(strip $(DIRECTFB_INPUT)))
endif
```

在menuconfig里是这样呈现的。

![image-20210609140058670](../images/random_name/image-20210609140058670.png)

当前qt的勾选了

![image-20210609140214699](../images/random_name/image-20210609140214699.png)

qt这个选项表示设置默认的图形平台。

当前没有指定，所以运行qt example的时候，总要加上参数。

```
Available platform plugins are: linuxfb, minimal, offscreen, vnc.
```



![image-20210609140239077](../images/random_name/image-20210609140239077.png)



1）dual frame buffers（双帧buffer）对于QT本身来说是不支持双buffer切换的，只能借助于DirectFB，但是实际测试的DirectFB会存在很多问题，比如有一些无法显示，效率不高，甚至还会crash等问题
2）目前我们使用的QT是直接使用GE2D将数据搬运到FB中，没有使用DirectFB



还是需要研究一下directfb。

我们的ge2d还是要借助directfb来做的。

我先不管ge2d的。现在把qt的后端配置为directfb。运行一下例子程序看看。

只需要改一下环境变量就好了。

但是现在运行完全看不到显示效果。

```
/usr/lib/qt/examples/quickcontrols2/wearable # ./wearable
(*) Direct/Thread: Started 'SigHandler' (2792) [CRITICAL - OTHER/0] <8388608>...

   ~~~~~~~~~~~~~~~~~~~~~~~~~| DirectFB 1.7.7 |~~~~~~~~~~~~~~~~~~~~~~~~~~
        (c) 2012-2015  DirectFB integrated media GmbH
        (c) 2001-2015  The world wide DirectFB Open Source Community
        (c) 2000-2004  Convergence (integrated media) GmbH
      ----------------------------------------------------------------

(*) DirectFB/Core: Single Application Core. (2021-05-11 03:34)
(*) Direct/Memcpy: Using libc memcpy()
(*) Direct/Thread: Started 'Fusion Dispatch' (2793) [MESSAGING - OTHER/0] <8388608>...
```

直接用dfbshow来测试看看。这个后面是跟一个图片的名字。

试了还是出不来。

先看一下directfb的代码。

directfb-1.7.7\gfxdrivers\amlgfx\ 这个下面，的确有ge2d的代码。



运行时的配置文件是/etc/directfbrc

```
#
system        = fbdev
fbdev         = /dev/fb0
mode = 720x720
depth = 32
pixelformat = ARGB
#no-hardware
hardware
#accelerator=49
# Disable Cursor
#no-cursor
#debug
#desktop-buffer-mode=backsystem
```

当前我是这样配置的。

选配directfb相关的组件，编译好，重新烧录镜像。

运行：

```
dfbshow ./home.png
```

可以正常显示。

```
export QT_QPA_PLATFORM=directfb
```

然后执行qt程序。显示的大小不对。

大概只显示了屏幕的1/4。

我改directfb的尺寸大小为1440x1440的。这个实际上跟屏幕尺寸对不上。

难道是pixelformat不对？

改一下看看。改成24bit，format为RGB的，大小还是改回720x720 。

还是不对。

跟format没有关系。

我现在再试，又是完全没有反应了。

现在看ge2d的中断，一个都没有。

那么就看看ge2d在设备树里有没有使能了。

是使能的。

ge2d有测试程序吗？

现在重新用dfbshow来显示图片。的确显示出来了。也不是我看错了。显示位置也正常。

但是ge2d的中断就是没有。

```
/usr/lib/qt/examples/quickcontrols2/wearable/images # dfbshow ./home.png
(*) Direct/Thread: Started 'SigHandler' (3344) [CRITICAL - OTHER/0] <8388608>...

   ~~~~~~~~~~~~~~~~~~~~~~~~~| DirectFB 1.7.7 |~~~~~~~~~~~~~~~~~~~~~~~~~~
        (c) 2012-2015  DirectFB integrated media GmbH
        (c) 2001-2015  The world wide DirectFB Open Source Community
        (c) 2000-2004  Convergence (integrated media) GmbH
      ----------------------------------------------------------------

(*) DirectFB/Core: Single Application Core. (2021-06-24 11:29) [ DEBUG ][ TRACE ]
(*) Direct/Memcpy: Using armasm_memcpy()
(*) Direct/Thread: Started 'Fusion Dispatch' (3345) [MESSAGING - OTHER/0] <8388608>...
(*) Direct/Thread: Started 'VT Switcher' (3348) [CRITICAL - OTHER/0] <8388608>...
(*) Direct/Thread: Started 'VT Flusher' (3349) [DEFAULT - OTHER/0] <8388608>...
(*) DirectFB/FBDev: Found 'OSD FB' (ID 0) with frame buffer at 0x3e300000, 24576k (MMIO 0x00000000, 0k)
(*) Direct/Thread: Started 'Keyboard Input' (3350) [INPUT - OTHER/0] <8388608>...
(*) DirectFB/Input: Keyboard 0.9 (directfb.org)
(*) Direct/Thread: Started 'PS/2 Input' (3351) [INPUT - OTHER/0] <8388608>...
(*) DirectFB/Input: IMPS/2 Mouse (1) 1.0 (directfb.org)
(*) Direct/Thread: Started 'PS/2 Input' (3352) [INPUT - OTHER/0] <8388608>...
(*) DirectFB/Input: IMPS/2 Mouse (2) 1.0 (directfb.org)
(*) Direct/Thread: Started 'Linux Input' (3353) [INPUT - OTHER/0] <8388608>...
(*) DirectFB/Input: aml_keypad (1) 0.1 (directfb.org)
(*) Direct/Thread: Started 'Linux Input' (3354) [INPUT - OTHER/0] <8388608>...
(*) DirectFB/Input: adc_keypad (2) 0.1 (directfb.org)
(*) Direct/Thread: Started 'Hotplug with Linux Input' (3355) [INPUT - OTHER/0] <8388608>...
(*) DirectFB/Input: Hot-plug detection enabled with Linux Input Driver
(*) DirectFB/Graphics: Generic Software Rasterizer 0.7 (directfb.org)
(*) DirectFB/Core/WM: Default 0.3 (directfb.org)
(*) Direct/Thread: Started 'Genefx' (3356) [DEFAULT - OTHER/0] <8388608>...
(*) FBDev/Mode: Setting 720x720 ARGB
(*) FBDev/Mode: Switched to 720x720 (virtual 720x720) at 32 bit (ARGB), pitch 2880
(*) FBDev/Mode: Setting 720x720 ARGB
(*) FBDev/Mode: Switched to 720x720 (virtual 720x720) at 32 bit (ARGB), pitch 2880
(*) Direct/Interface: Loaded 'PNG' implementation of 'IDirectFBImageProvider'.
(*) FBDev/Mode: Setting 720x720 ARGB
(*) FBDev/Mode: Switched to 720x720 (virtual 720x2160) at 32 bit (ARGB), pitch 2880
```

从这个运行打印看，这一句是不是表示当前使用的是软件的方式？

```
(*) DirectFB/Graphics: Generic Software Rasterizer 0.7 (directfb.org)
```

看了一下.config文件，的确是没有配置进来。

的确是我忘了配置了。

```
[*] GE2D library                          
()    amlogic libge2d local path (NEW)    
```

这个路径是需要指定的吧。

怎么指定呢？

参考这个

```
BR2_KERNEL_TOOLCHAIN_PATH [=$(TOPDIR)/../toolchain/gcc/linux-x86/aarch64/gcc-linaro-6.3.1-2017.02-x86_64_aarch64-linux-gnu]   
```

而路径，在这里有：

```
./ipc_driver.config:1:BR2_PACKAGE_AML_LIBGE2D_LOCAL_PATH="$(TOPDIR)/../hardware/aml-4.9/amlogic/libge2d"
```

选中 了libge2d，则自动把依赖的BR2_PACKAGE_AML_LIBION=y选上了。

这个也要配置路径。

路径是这里：

```
./ipc_driver.config:3:BR2_PACKAGE_AML_LIBION_LOCAL_PATH="$(TOPDIR)/../hardware/aml-4.9/amlogic/libion"
```

这样编译后，是不是只要把库放进去就好了。

重烧太耗费时间了。

先试一下。

应该就是这2个库。

```
./usr/lib/libge2d.so
./usr/lib/libion.so
```

不行的。

再看看配置，directfb应该也需要重新编译才行吧。怎么看有没有去调用ge2d的gfxdriver呢？

```
./a113_s400.config:2:#include "directfb.config"
```

directfb是一个单独的配置文件，默认有包含。

这个里面就这些。可能directfb默认就是用的fb。

```
BR2_PACKAGE_DIRECTFB=y
BR2_PACKAGE_FBDUMP=y
BR2_PACKAGE_FBGRAB=y
BR2_PACKAGE_FBSET=y
BR2_PACKAGE_FBTERM=y
BR2_PACKAGE_FB_TEST_APP=y
```

应该就是这个选项

```
./a113_s400.config:64:BR2_PACKAGE_DIRECTFB_AMLGFX=y
```

我当前是已经选中了的。

看这个变量怎么被使用的。

就是这里了。

```

DIRECTFB_GFX = \
        $(if $(BR2_PACKAGE_DIRECTFB_AMLGFX),amlgfx) \
        $(if $(BR2_PACKAGE_DIRECTFB_ATI128),ati128) \
        $(if $(BR2_PACKAGE_DIRECTFB_CYBER5K),cyber5k) \
        $(if $(BR2_PACKAGE_DIRECTFB_MATROX),matrox) \
        $(if $(BR2_PACKAGE_DIRECTFB_PXA3XX),pxa3xx) \
        $(if $(BR2_PACKAGE_DIRECTFB_I830),i830) \
        $(if $(BR2_PACKAGE_DIRECTFB_EP9X),ep9x)

ifeq ($(strip $(DIRECTFB_GFX)),)
DIRECTFB_CONF_OPTS += --with-gfxdrivers=none
else
DIRECTFB_CONF_OPTS += \
        --with-gfxdrivers=$(subst $(space),$(comma),$(strip $(DIRECTFB_GFX)))
endif
```

那么就把directfb都删掉重新编译一下。

看看编译时的打印，分析一下。

```
./configure 
--target=arm-linux-gnueabihf 
--host=arm-linux-gnueabihf 
--build=x86_64-pc-linux-gnu 
--prefix=/usr 
--exec-prefix=/usr 
--sysconfdir=/etc 
--localstatedir=/var 
--program-prefix="" 
--disable-gtk-doc 
--disable-gtk-doc-html 
--disable-doc 
--disable-docs 
--disable-documentation 
--with-xmlto=no 
--with-fop=no 
--disable-dependency-tracking 
--enable-ipv6 
--disable-nls 
--disable-static 
--enable-shared  
--enable-zlib 
--enable-freetype 
--enable-fbdev 
--disable-sdl 
--disable-vnc 
--disable-osx 
--disable-video4linux 
--disable-video4linux2 
--without-tools 
--disable-x11 
--disable-multi 
--disable-multi-kernel 
--enable-debug-support 
--enable-debug 
--enable-trace 
--disable-divine 
--disable-sawman 
--with-gfxdrivers=amlgfx 
--with-inputdrivers=linuxinput,keyboard,ps2mouse,serialmouse 
--enable-gif 
--disable-tiff 
--enable-png 
--enable-jpeg 
--enable-svg 
--disable-imlib2 
--with-dither-rgb16=none
```

重点是这里，已经配置了。

```
--with-gfxdrivers=amlgfx 
```

看到还有一个这样的so文件。

libdirectfb_amlgfx.so

直接重新烧录镜像吧。

再运行。

还是没有ge2d的。

这是为什么？

gfxdriver是怎么被使用的？

我估计是dlopen这种方式。



通过前面对DirectFB中用类似面向对象的设计方法分析后，同理可知我们的gfxdrivers也是一个个的so被加载进来的，那问题来，当gfxdrivers下存在多个gfx驱动的时它是匹配哪一个呢？

我们先找到初始化gfxdrivers的地方，它在文件src/core/gfxcard.c中，

```
/* Load driver */
     if (dfb_system_caps() & CSCAPS_ACCELERATION)
          dfb_gfxcard_find_driver( core );
```



这个从哪里获取硬件加速信息呢？

```cpp
int
dfb_system_get_accelerator( void )
{
     D_ASSERT( system_funcs != NULL );

     return system_funcs->GetAccelerator();
}
```

在directfbrc里，有这样的配置项：

```
system        = fbdev
fbdev         = /dev/fb0
```

这个是不是说默认使用的的fb呢？

如果我要改成ge2d的。配置应该怎么改？

```
[no-]hardware
Turns hardware acceleration on. By default hardware acceleration is auto-detected. If you disable hardware acceleration, the driver for your graphics card will still be loaded and used to access additional display layers (if there are any), but all graphics operations will be performed by the software renderer.
```

我还是先想办法测试一下ge2d是否正常。

这里有个测试报告，看看。不合适。这个里面提到的我操作不了。

https://wiki-china.amlogic.com/Platform/ChipBringup/AXG/TestReports/GE2D

ge2d_load_test 这个二进制在哪里？

在板端输入df，再按tab补全，可以看到不少的命令，这些都是directfb相关的命令。

例如df_dok。这个命令执行输入就可以了。是一直进行各种性能测试。

可以看到显示是正常的。

这个只能说directfb正常工作了。

要让ge2d工作，只需要在directfbrc里，把这一行打开：

```
#accelerator=49
```

这个是amlgfx对应的宏的数字。

现在运行df_dok。可以看到ge2d有中断了。

但是当前directfb+qt的方式，之前就验证是有问题。

所以采用的实际是：qt+ge2d的方式，直接给qt打patch来对接ge2d。

我没有打开directfb之前的配置，按道理就是应该qt+ge2d的方式了。

但是我当前调试的是5.12版本，而之前是在5.8版本里放的patch文件。



# directfbrc配置

我当前的打印信息比较少。可不可以在directfbrc文件里配置日志级别？

在src/misc/conf.c里，dfb_config_set函数里，有对各个参数的解析。这里可以看出支持哪些参数。

DFBConfig 还有这个结构体。

```
     bool      software_only;                     /* disable hardware acceleration */
     bool      hardware_only;                     /* disable software fallbacks */
```

config_usage_strings 这个列得很清楚了。

```

```



directfbrc 是 DirectFB 的配置文件。

 它被所有的 DirectFB 应用程序在启动时读取，

有 两个这样的文件，

一个是存放在 /etc/direcfbrc ，是个全局的，

另一个是存放在 $HOME/.directfbrc ，它是个局部的，可以覆盖系统的设置。

需要注意的是，这两个文 件都不是默认存在的，是需要你自己建立的

在 *directfbrc* 使用的参数也可以在命 令行里传递给 *DirectFB* 应用程序，只需要加上前缀： *--dfb:*

*directfbrc* 文件每一行包含一个变量。注释行以井号“ *#* ”开始，一直到行尾。空行被忽略。

许多参数只是一种开关， 控制着一些特性的开 */* 关。这些开关选项有一个 *no-* 变量，可以关闭相应的特性。下面介绍一些实用的参数和一些默认的参数。

## system

*system=<system>*

​    设定使用的图形系统。默认使用 *Linux frame buffer (fbdev)* ，但你也可以在 *SDL* （ *sdl* ）上运行 *DirectFB* 应用程序。其它的系统在将来可能会被扩展近来。

那么可以的取值是：x11、drmkms、fbdev。

```
if (getenv( "DISPLAY" ))
          dfb_config->system = D_STRDUP( "x11" );
     else if (!access( "/dev/dri/card0", O_RDWR ))
          dfb_config->system = D_STRDUP( "drmkms" );
     else if (!access( "/dev/fb0", O_RDWR ))
          dfb_config->system = D_STRDUP( "fbdev" );
```



# 代码分析

桌面GUI系统涉及很多图像运算，

比如画点、画线、填充、透明度处理、平滑度处理、层的叠加、字体处理、贴图等等。

如果这些运算都由CPU来处理，那这将是对CPU的一个很大的负载。

在QT的文档中曾说到，

假如一个图形运算让加速设备来做需要1到2个CLK，

同样的图形运算让CPU来算则至少需要20个CLK，

而且，对于嵌入式SoC来说，CPU的频率和SDRAM/DRAM的带宽始终是图形运算的瓶颈。

所以这些芯片的图形加速能力有无、高低，最终决定其目标GUI的质量。



近两年嵌入式设备主芯片越来越多的嵌入了2D/3D加速功能，

由此软件可以搭建越来越复杂、炫酷、先进的桌面系统，如Qt/Android等。

这些加速硬件，通常也因其是否拥有私有内存、是否支持3D、加速接口是否可编程等特性而分为三六九等。

硬件的加速功能如果要在目标GUI系统中跑起来，

还得需要一些软件中间层为不同的硬件加速提供同一的接口，并且为上层GUI提供服务。

DirectFB就是这样一个软件中间层,它主要为上层提供2D加速服务。

**OpenGL/ES 主要为上层提供3D加速服务。**

DirectFB是一个专门针对Linux图形库设计的图形加速中间层。

它的上层直接面向图形库比如QT，提供如显示、画图、输入设备控制等服务，

他的下层直接面向GFX加速硬件，**要求硬件驱动实现全部或部分预定的画图函数**。



 DirectFB由超级接口IDirectFB为上层提供接口调用，其他所有接口都由此接口生成，这些接口内容包括：

  =========================
  . IDirectFBScreen
  . IDirectbFBDisplayLayer

   IDirectFBSurface



# ge2d对接

```
static GraphicsDriverFuncs driver_funcs = {
     .Probe              = driver_probe,
     .GetDriverInfo      = driver_get_info,
     .InitDriver         = driver_init_driver,
     .InitDevice         = driver_init_device,
     .CloseDevice        = driver_close_device,
     .CloseDriver        = driver_close_driver
};
```

对接是这样一个结构体的实现。

driver_probe 这个直接返回1就好了（bool语义）

driver_get_info 这个就填充一些字符串信息。

driver_init_driver

```
这个就是重要入口。
2个数据结构
AMLGFX_DriverData
AMLGFX_DeviceData

amldrv->ge2d_fd = open("/dev/ge2d", O_RDWR);

GraphicsDeviceFuncs
这个是重要的函数结构体。需要实现十几个函数。

```



DFBAccelerationMask

这个枚举，列举了可以进行加速的操作。

```
fill rectangle
draw rectangle
draw line
fill triangle
fill trapezoid 不规则四边形
fill quadrangle 四边形。
fill span 
draw monoglyph
blit 块传输
stretch blit
text triangle
blit2 
tile blit
draw string
all
all drawn
all blit
```

总的调用逻辑是：填充一些结构体，然后ioctl传递下去。

目前看，只实现了这几个函数。

```
	funcs->CheckState    = amlCheckState;
	funcs->SetState      = amlSetState;
	funcs->EngineSync    = amlEngineSync;
	funcs->EngineReset   = amlEngineReset;
	funcs->FlushTextureCache  = amlFlushTextureCache;

	funcs->FillRectangle = amlFillRectangle;
	funcs->Blit          = amlBlit;
	funcs->StretchBlit = amlStretchBlit;
```

还有几个还是空函数。

可以对比看一下VMware的实现。



# qt和directfb的对接

配置：

```
export QT_QPA_PLATFORM=directfb
export QT_QUICK_BACKEND=softwarecontext
```

执行：/usr/lib/qt/examples/quick/text

```
Not support amlBlit please check configure
=====GE2D_NOT_SUPPORT=====
!!!!!!aml_state.c 460 > DSPD_SRC_OVER flags[0x3]***NULL
Not support amlBlit please check configure
=====GE2D_NOT_SUPPORT=====
!!!!!!aml_state.c 460 > DSPD_SRC_OVER flags[0x3]***NULL
Not support amlBlit please check configure
=====GE2D_NOT_SUPPORT=====
!!!!!!aml_state.c 460 > DSPD_SRC_OVER flags[0x3]***NULL
Not support amlBlit please check configure
=====GE2D_NOT_SUPPORT=====
!!!!!!aml_state.c 460 > DSPD_SRC_OVER flags[0x3]***NULL
Not support amlBlit please check configure
=====GE2D_NOT_SUPPORT=====
!!!!!!aml_state.c 460 > DSPD_SRC_OVER flags[0x3]***NULL
Not support amlBlit please check configure
=====GE2D_NOT_SUPPORT=====
```

把/etc/directfbrc里的format从ARGB改成RGB。

至少可以显示图形出来了。

虽然尺寸还不对。

是因为directfb不能自动缩放导致的？

我找一个720x720的图片放进来看看。

```
(*) Direct/Interface: Loaded 'BMP' implementation of 'IDirectFBImageProvider'.
(!) IDirectFBImageProvider_BMP: Unsupported compression 3!
CreateImageProvider -> The requested operation or an argument is (currently) not supported

Caught exception!
  -- CreateImageProvider -> The requested operation or an argument is (currently) not supported
(*) FBDev/Mode: Setting 720x720 RGB16
```

用dfbshow来进行显示看看。

不行。

我把bmp文件转成jpg的再试一下。可以正常显示。

为什么直接使用fb可以素材自动适应屏幕的大小。

而directfb的不行？

看之前的邮件，还提到了directfb慢的问题。

当前首先是要解决显示尺寸的问题。

然后才能讨论效果和效率。

就选择wearable这个例子来看。





# argb还是rgb

当前argb是不行的，rgb是可以的。

这个是谁来决定的？

屏幕参数决定的？

不对，我现在试了，RGB和ARGB都是可以的。

而且效果没有区别。

但是使用ge2d的时候，

我试了这样是正常的：

```
depth = 24 #32也可以。
pixelformat = RGB
```

pixelformat是ARGB是一定不正常。

不要指定这2个参数。

运行qt会自动切换的。

```
(*) Direct/Thread: Started 'Genefx' (19068) [DEFAULT - OTHER/0] <8388608>...
(*) FBDev/Mode: Setting 720x720 RGB16
(*) FBDev/Mode: Switched to 720x720 (virtual 720x720) at 16 bit (RGB16), pitch 1440
(*) FBDev/Mode: Setting 720x720 RGB16
(*) FBDev/Mode: Switched to 720x720 (virtual 720x1440) at 16 bit (RGB16), pitch 1440
```

primarySetRegion这个函数打印的？

但是不对啊，现在为什么还是走fbdev的？

走应该还是要走。

```
Not support amlBlit please check configure
```

这个打印又是为什么呢？

现在先不管

重点先看这个。

```
 (!!!)  *** UNIMPLEMENTED [fusion_get_fusionee_pid] *** [fusion.c:4147]
```

这个函数的确是没有实现。

```
DirectResult
fusion_get_fusionee_pid( const FusionWorld *world,
                         FusionID           fusion_id,
                         pid_t             *ret_pid )
{
     D_UNIMPLEMENTED();

     return DR_UNIMPLEMENTED;
}
```

lcd支持的像素格式，是怎么确定的？

我用自己的fb_basic_info运行，得到的数据：

```
/data # ./fb_basic_info
-----------fix info-------------
                        id:OSD FB
                        smem_start:1043333120
                        smem_len:25165824
                        type:0
                        type_aux:0
                        visual:2
                        xpanstep:1
                        ypanstep:1
                        line_length:0
                        mmio_len:1440
                        accel:0

--------------------------------
-----------var info-------------
                                                xres:720
                        yres:720
                        xres_virtual:720
                        yres_virtual:720
                        xoffset:0
                        yoffset:0
                        bits_per_pixel:16
                        nonstd:0
                        activate:0
                        height:0
                        width:0
                        accel_flags:0
                        pixclock:0
                        left_margin:0
                        right_margin:0
                        upper_margin:0
                        lower_margin:0
                        hsync_len:0
                        vsync_len:0
                        vmode:0

--------------------------------
```

bits_per_pixel:16

现在需要看一下osd fb的驱动。

看看设备树

```
display_mode_default = "1080p60hz";
```

```
ret = of_property_read_u32_array(pdev->dev.of_node,
					"display_size_default",
					&var_screeninfo[0], 5);
这里是把display_size_default = <720 720 720 1440 32>;
这个信息给解析出来。填充给fb_var结构体。
但是按照这个，bpp应该是32位的啊。
```

重启一下机器，从kernel的开机打印

```
[   11.156859@0]- fb: init fbdev bpp is:32
[   11.161115@2]- fb: set osd0 reverse as NONE
[   11.174060@0]- fb: osd probe OK
```

可以看到是32bit的。

我这时候再执行一下fb_basic_info。看到的信息是这样：

```
-----------fix info-------------
                        id:OSD FB 
                        smem_start:104333312
                        smem_len:25165824
                        type:0
                        type_aux:0
                        visual:2
                        xpanstep:1
                        ypanstep:1
                        line_length:0
                        mmio_len:2880
                        accel:0

--------------------------------
-----------var info-------------
                                                xres:720
                        yres:720
                        xres_virtual:720
                        yres_virtual:1440
                        xoffset:0
                        yoffset:0
                        bits_per_pixel:32
                        nonstd:0
                        activate:0
                        height:0
                        width:0
                        accel_flags:0
                        pixclock:0
                        left_margin:0
                        right_margin:0
                        upper_margin:0
                        lower_margin:0
                        hsync_len:0
                        vsync_len:0
                        vmode:0

--------------------------------
```

难度变化的是因为directfb执行时修改导致的？

应该是的。

现在我不在directfbrc里填入depth和pixelformat。

运行基于directfb的qt，打印这个。

```
(*) FBDev/Mode: Setting 720x720 RGB32
(*) FBDev/Mode: Switched to 720x720 (virtual 720x720) at 32 bit (RGB32), pitch 2880
(*) FBDev/Mode: Setting 720x720 RGB32
(*) FBDev/Mode: Switched to 720x720 (virtual 720x1440) at 32 bit (RGB32), pitch 2880
```

但是这个是没有任何的显示。



我给一张720x720的jpg图片。用df_dok --load-image的方式显示，不正常。

用dfbshow的方式显示，图片正常。

这二者有什么不同？

df_dok里是这样：

```
IDirectFBImageProvider *provider;

          /* create a surface and render an image to it */
          DFBCHECK(dfb->CreateImageProvider( dfb, filename, &provider ));
          DFBCHECK(provider->GetSurfaceDescription( provider, &dsc ));
          if (imageformat)
               dsc.pixelformat = imageformat;
          if (!surface)
               DFBCHECK(dfb->CreateSurface( dfb, &dsc, &surface ));
          DFBCHECK(provider->RenderTo( provider, surface, NULL ));
          DFBCHECK(provider->Release( provider ));
```

dfbshow是c++ demo。继承了DFBApp这个类。

代码看起来很接近。

看一下二者的打印。

db_dok的最后几行打印

```
(*) FBDev/Mode: Setting 720x720 RGB32
(*) FBDev/Mode: Switched to 720x720 (virtual 720x720) at 32 bit (RGB32), pitch 2880
(*) Direct/Interface: Loaded 'PNG' implementation of 'IDirectFBImageProvider'.
(*) Direct/Interface: Loaded 'FT2' implementation of 'IDirectFBFont'.
(*) FBDev/Mode: Setting 720x720 RGB32
(*) FBDev/Mode: Switched to 720x720 (virtual 720x720) at 32 bit (RGB32), pitch 2880
(*) Direct/Interface: Loaded 'GIF' implementation of 'IDirectFBImageProvider'.
```

dfbshow的最后几行打印：

```
(*) FBDev/Mode: Setting 720x720 RGB32
(*) FBDev/Mode: Switched to 720x720 (virtual 720x720) at 32 bit (RGB32), pitch 2880
(*) FBDev/Mode: Setting 720x720 RGB32
(*) FBDev/Mode: Switched to 720x720 (virtual 720x1440) at 32 bit (RGB32), pitch 2880
(*) Direct/Interface: Loaded 'JPEG' implementation of 'IDirectFBImageProvider'.
(*) FBDev/Mode: Setting 720x720 RGB32
(*) FBDev/Mode: Switched to 720x720 (virtual 720x2160) at 32 bit (RGB32), pitch 2880
```

可以看到df_dok，virtual的尺寸不同。

而且是使用了png的provider。

那我直接给一张png格式的图片。

一闪而过。

这个不是关键。

关键还是qt为什么显示的尺寸不能铺满。





# 像素深度

像素深度（bits per pixel，简称bpp）

一个像素的颜色在计算机中由多少个字节数据来描述。计算机中用二进制位来表示一个像素的数据，用来表示一个像素的数据位越多，则这个像素的颜色值更加丰富、分的更细，颜色深度就更深。

一般来说像素深度有这么几种：1位、8位、16位、24位、32位。

像素深度bpp和像素格式pix_format关系：

像素格式是人为规定的用来填充像素深度bpp的。比如像素深度为16，说明用16位二进制表示一个像素，那到底是怎样的数据形式来表示填充呢，人为可以规定RGB565,也可以规定BGR565。这个格式就要看具体驱动和应用代码了。



# df_dok

只需要研究这一个测试程序就可以了。

查看--help，可以看到很多的选项，可以测试不同的子项目。

以df_dok --fill-rect来作为典型测试。

当前使用硬件加速，不正常。并没有继续进行后面的测试。

直接使用fb，则是正常的。

查看ge2d的中断数，刚开始运行会有，过一会就没有中断增加了。



面对嵌入式设备的特殊需求环境，我们为图形加速和图形增强支持开发了一个小巧、强大和易于使用的技术：directfb。

directfb是一个瘦函数库，

为开发者提供硬件加速，

输入设备处理，

并在Linux FB设备之上抽象、集成了支持**半透明窗口和多层显示**的窗口系统。

它是一个完全的硬件抽象层，

**在每个图形操作上都具有软件后备机制，**

用于那些不被底层硬件支持的功能。

DFB让嵌入式系统图形功能更强大，并在Linux上建立了一个新的标准。




# 参考资料

1、DirectFB简介以及移植[一]

https://blog.csdn.net/sunjing_/article/details/90519808

2、

https://sites.google.com/site/myembededlife/Home/s3c2440/hidden-cursor-in-dfb

3、DirectFB图形加速在嵌入式系统中的应用

https://wenku.baidu.com/view/2e4a0ded102de2bd96058885.html

4、

http://www.cxyzjd.com/article/jxgz_leo/69787916

5、directfbrc文件的使用及参数的详细说明

https://blog.csdn.net/yangzhongxuan/article/details/6539711

6、man手册

https://linux.die.net/man/5/directfbrc

7、

https://elinux.org/DirectFB

8、DirectFB的接口详解

https://blog.csdn.net/yinjiabin/article/details/7674053

9、

https://www.raspberrypi.org/forums/viewtopic.php?t=22802

10、

https://blog.csdn.net/zhangliang_571/article/details/28265255

11、LCD显示问题-lcd中像素深度bpp和像素格式（比如RGB,YUV）的关系

https://blog.csdn.net/u013165704/article/details/80590652

12、

https://higfxback.github.io/DirectFB.html

13、

http://www.mianshigee.com/tutorial/tinyclub-elinux/dev_portals-multimedia-porting_directfb-porting_directfb.md