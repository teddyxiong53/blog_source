---
title: Android之手机安装busybox
date: 2018-01-03 10:20:56
tags:
	- Android

---



有个魅族的mx2手机，已经卡到无法操作了，打算让它发挥一下余热，让我可以从电脑上telnet到手机上进行一些操作。这样可以跑一些脚本。本来打算是用sshd的。但是quicksshd安装上去不能用。

我的mx2的情况：

```
1、安卓版本是5.01。有PIE限制了。quicksshd又找不到源代码来重新编译。放弃。
2、cpu是Cortex A9的，属于armv7架构。
```

1、先下载二进制的busybox包。

https://busybox.net/downloads/binaries/1.26.2-defconfig-multiarch/

这个目录下，看到应该busybox-armv6l可以用。下载下来。改名为busybox。

2、用usb线把手机连接到电脑上。打开usb调试功能。把下载的busybox拷贝到手机的存储的根目录。

电脑上打开cmd窗口。

先用`adb devices`命令看看设备有没有正常识别到。

然后输入`adb shell`进入到adb的命令行环境。

3、接下来的操作都是在adb的环境里进行。

先把把/system分区重新挂载一下，因为默认的挂载是只读的。我们要加上可写权限再挂载一次。

命令如下：

```
mount -o remount,rw -t yaffs2 /dev/block/mtdblock3 /system
```

我的mx2就在这里碰到权限不允许的问题。因为这些操作都是需要root权限的，我的mx2是用的官方root，官方root还是一个不彻底的root。我在手机上另外下载一个KingRoot进行root。然后再执行上面的命令，通过了。

然后是把busybox文件拷贝到/system/xbin目录下，root后的手机这个目录都是存在的，如果不存在，就是自己手机建立一个。

然后给busybox加上可执行权限。

```
chmod 755 busybox
```

然后是busybox安装，这样就可以避免每次要`busybox ls`这样来执行命令。

```
busybox --install .
```

到这里，就已经安装好了。

我的最终目的是在手机上启动一个telnetd。这个在另外的文章里写。