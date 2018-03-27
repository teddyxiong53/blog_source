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



# 参考资料

1、嵌入式Linux通过帧缓存截图

https://www.crifan.com/the_frame_buffer_embedded_linux_screenshot_-_framebuffer_screenshot_in_embedded_linux/

