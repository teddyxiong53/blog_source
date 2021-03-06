---
title: Linux之console
date: 2020-06-16 10:11:49
tags:
	- Linux

---

1

可以同时指定多个console输出。

在kernel的启动参数里可以这样：

```
console=ttyS1,9600 console=tty0
```

defines that opening `/dev/console` will get you the current foreground virtual console, and kernel messages will appear on both the VGA console and the 2nd serial port (ttyS1 or COM2) at 9600 baud.

显示屏默认是console。

If no console device is specified, the first device found capable of acting as a system console will be used. 

首先就是找VGA显示器作为console。

然后才是找串口。

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



参考资料

1、Linux Serial Console

https://www.kernel.org/doc/html/v4.18/admin-guide/serial-console.html