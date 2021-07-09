---
title: fbset命令
date: 2021-07-05 15:20:33
tags:
	- gui

---

--

fbset是用来修改fb的设置的命令行工具。

不属于busybox，是一个单独的工具。

查看当前的设置情况：

```
fbset -s
fbset -i
	比-s查看的信息还多一些。用这个就好了。
```

我当前的屏幕的情况。

```
fbset -i

mode "720x720"
    geometry 720 720 720 1440 32
    timings 0 0 0 0 0 0 0
    rgba 8/16,8/8,8/0,8/24
endmode

Frame buffer device information:
    Name        : OSD FB
    Address     : 0x3e300000
    Size        : 25165824
    Type        : PACKED PIXELS
    Visual      : TRUECOLOR
    XPanStep    : 1
    YPanStep    : 1
    YWrapStep   : 0
    LineLength  : 2880
    Accelerator : No
```

fbset指令可用于设置景框缓冲区的大小，

还能调整画面之分辨率，位置，高低宽窄，色彩 深度，

并可决定是否启动显卡之各项硬件特性。

```
# fbset -g 800 688 1024 768//画面分辨率为800*600 桌面分辨率为1024*768
# fbset -accel true  // 启动硬件文本加速
# fbset -bcast true //启动广播功能
```



怎么确定pixel format的RGB的顺序？例如下面这样，说明了什么？

```
rgba 8/16,8/8,8/0,8/24
```



借助于framebuffer，我们能够在console下面作很多事情。

首先下载framebuffer的配置工具fbset:

```
apt-get install fbset 
```

下载完毕后，配置文件/etc/fb.modes随之产生。



参考资料

1、

https://linux.die.net/man/8/fbset

2、

https://www.runoob.com/linux/linux-comm-fbset.html

3、
https://www.raspberrypi.org/forums/viewtopic.php?t=22802

4、

https://e2e.ti.com/support/legacy_forums/embedded/linux/f/linux-forum-read-only/471756/framebuffer---image-appear-and-disappear

5、

https://blog.csdn.net/TJU355/article/details/6881389