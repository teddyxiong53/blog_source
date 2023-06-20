---
title: Linux之console
date: 2020-06-16 10:11:49
tags:
	- Linux

---

--

# 多个console

可以同时指定多个console输出。

在kernel的启动参数里可以这样：

```
console=ttyS1,9600 console=tty0
```

defines that opening `/dev/console` will get you the current foreground virtual console, and kernel messages will appear on both the VGA console and the 2nd serial port (ttyS1 or COM2) at 9600 baud.

显示屏默认是console。

If no console device is specified, the first device found capable of acting as a system console will be used. 

**首先就是找VGA显示器作为console。**

**然后才是找串口。**

也可以配置网络作为console。

看printk.c代码里。

有一个register_console函数。在内核里搜索一下。

```
./arch/arm/kernel/early_printk.c:42:    register_console(&early_console_dev);
```

```
static struct console early_console_dev = {
	.name =		"earlycon",
	.write =	early_console_write,
	.flags =	CON_PRINTBUFFER | CON_BOOT,
	.index =	-1,
};

static int __init setup_early_printk(char *buf)
{
	early_console = &early_console_dev;
	register_console(&early_console_dev);
	return 0;
}

early_param("earlyprintk", setup_early_printk);

```

```
__setup("console=", console_setup);
```



# vt220和xterm的区别

VT220和xterm都是计算机终端仿真器，用于在计算机上模拟物理终端的功能。它们之间有以下几个区别：

1. 发展历史：VT220是Digital Equipment Corporation（DEC）于1983年推出的终端型号，属于VT系列终端的一部分。而xterm是一个在X Window System环境下运行的终端仿真器，最早是为X Window System开发的，后来被移植到许多其他平台上使用。

2. 设备类型：VT220是一种硬件终端设备，具有特定的物理外壳和键盘。而xterm是一个软件终端仿真器，完全在计算机的图形界面中运行，并通过图形界面来显示和处理终端会话。

3. 显示功能：VT220使用基于字符的显示，它能够显示文本和控制字符，但不支持图形元素。xterm则支持更丰富的显示功能，包括文本、控制字符以及对彩色、字体、粗体和斜体等的支持。它还能够显示图形元素，如图标、窗口等。

4. 操作系统支持：VT220最初是为DEC的VMS和UNIX操作系统设计的，但也能够与其他操作系统兼容。xterm则可以在多种操作系统上运行，包括UNIX、Linux和Windows等。

5. 配置和定制：VT220是一个硬件设备，通常不具备灵活的配置选项和用户定制能力。而xterm作为软件终端仿真器，提供了广泛的配置选项和定制能力，用户可以根据自己的需要调整外观、键绑定和其他行为。

总之，VT220是一种硬件终端设备，而xterm是一个跨平台的软件终端仿真器。xterm在显示功能、操作系统支持和定制能力方面更加强大和灵活，适用于各种计算机系统和环境。



# VT102

我看嵌入式的默认基本是这个vt。这个有什么特点？



# 参考资料

1、Linux Serial Console

https://www.kernel.org/doc/html/v4.18/admin-guide/serial-console.html