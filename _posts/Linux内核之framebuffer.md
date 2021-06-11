---
title: Linux内核之framebuffer
date: 2018-03-26 20:16:33
tags:
	- Linux内核

---



framebuffer是从linux2.2版本开始出现在内核里的。

linux是工作在保护模式下，所以用户进程是无法像dos那样使用网卡bios里提供的中断调用来实现直接写屏。

所以linux就抽象出framebuffer这个设备，来用户程序来直接写屏可以实现。

framebuffer本身不会对数据进行处理，就像一个蓄水池一样。



我们可以用fbcat命令来进行截屏操作。

```
sudo cat /dev/fb0 > frame.raw
```

```
teddy@teddy-ubuntu:~$ file frame.raw 
frame.raw: PDP-11 UNIX/RT ldp
```

这个图片要用ffmpeg编码后才能看。我先不管了。



```
-----------fix info-------------
                        id:CLCD FB 
                        smem_start:1730150400
                        smem_len:1572864
                        type:0
                        type_aux:0
                        visual:2
                        xpanstep:0
                        ypanstep:0
                        line_length:0
                        mmio_len:2048
                        accel:4096

--------------------------------
-----------var info-------------
                                                xres:1024
                        yres:768
                        xres_virtual:1024
                        yres_virtual:768
                        xoffset:0
                        yoffset:0
                        bits_per_pixel:16
                        nonstd:0
                        activate:0
                        height:-1
                        width:-1
                        accel_flags:0
                        pixclock:15748
                        left_margin:152
                        right_margin:48
                        upper_margin:23
                        lower_margin:3
                        hsync_len:104
                        vsync_len:4
                        vmode:0
```



帧缓冲（framebuffer）是Linux系统为显示设备提供的一个接口，

它将显示缓冲区抽象，

屏蔽图像硬件的底层差异，

允许上层应用程序在**图形模式**下直接对显示缓冲区进行读写操作。

用户不必关心物理显示缓冲区的具体位置及存放方式，这些都是由帧缓冲设备驱动本身来完成。



framebuffer机制模仿显卡的功能，

将显卡硬件结构抽象为一系列的数据结构，

可以通过对framebuffer的读写直接对显存进行操作。

用户可以将framebuffer看成是显卡的一个映像，

将其映射到进程空间后，就可以直接读写操作，写操作会直接反映在屏幕上。



framebuffer是一个字符设备，主设备号是29，对应于/dev/fb%d设备文件。通常，使用如下方式（数字代表次设备号）

　　0 = /dev/fb0 第一个fb设备

　　1 = /dev/fb1 第二个fb设备

　　fb也是一种普通的内存设备，可以读写其内容。例如，屏幕抓屏：cp /dev/fb0 myfilefb  虽然可以向内存设备（/dev/mem）一样，对其read、write、seek以及mmap。但区别在于fb使用的不是整个内存区。而是显存部分。

 

对于应用程序而言，它和其它的设备并没有什么区别，

用户可以把fb看成是一块内存，既可以向内存中写数据，也可以读数据。

fb的显示缓冲区位于内核空间。

应用程序可以把此空间映射到自己的用户空间，再进行操作。

　　在应用程序中，操作/dev/fbn的一般步骤如下：

　　（1）打开/dev/fbn设备文件。

　　（2）用ioctl()操作取得当前显示屏幕的参数，如屏幕的分辨率、每个像素点的比特数。根据屏幕的参数可计算屏幕缓冲区的大小。

　　（3）用mmap（）函数，将屏幕缓冲区映射到用户空间。

　　（4）映射后就可以直接读/写屏幕缓冲区，进行绘图和图片显示。



framebuffer涉及的数据结构如下：

　　**（1）struct fb_info** 

　　　一个帧缓冲区对应一个struct fb_info结构，它包括了帧缓冲设备的属性和操作的完整集合，每个帧设备都有一个fb_info结构体。

　　**（2）struct fb_ops**

　　　　结构体用来实现对帧缓冲设备的操作，这些函数需要驱动开发人员编写，**
**

　　**（3）struct fb_fix_screeninfo**

　　　  该结构体记录了用户不能修改的固定显示控制器参数。这些固定的参数如缓冲区的物理地址、缓冲区的长度等等。

　　**（4）struct fb_var_screeninfo**

　　　　结构体中存储了用户可以修改的显示器控制参数，例如屏幕分辨率、透明度等等。

　　**（5）struct fb_cmap**

　　　　结构体中记录了颜色板信息，即调色板信息。，用户空间可以通过ioctl()的FBIOGETCMAP和 FBIOPUTCMAP命令读取或设定颜色表。

![img](../images/random_name/1553004-20181216093455197-25285508.png)



framebuffer设备在Linux中是以平台设备形式存在的，

fb设备驱动核心层

为上层提供了系统调用，

为底层驱动提供了接口，

核心层的主文件及其功能如下。

　　(1)drivers/video/fbmem.c。

主要任务：1、创建graphics类、注册FB的字符设备驱动、提供register_framebuffer接口给具体framebuffer驱动编写着来注册fb设备的。本文件相对于fb来说，地位和作用和misc.c文件相对于杂散类设备来说一样的，结构和分析方法也是类似的。

　　(2)drivers/video/fbsys.c。

这个文件是处理fb在/sys目录下的一些属性文件的。
　　(3)drivers/video/modedb.c。

这个文件是管理显示模式（譬如VGA、720P等就是显示模式）的
　　(4)drivers/video/fb_notify.c



# 参考资料

1、嵌入式Linux通过帧缓存截图

https://www.crifan.com/the_frame_buffer_embedded_linux_screenshot_-_framebuffer_screenshot_in_embedded_linux/

2、linux驱动之framebuffer

https://www.cnblogs.com/gzqblogs/p/10105804.html