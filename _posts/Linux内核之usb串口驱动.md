---
title: Linux内核之usb串口驱动
date: 2020-08-28 16:37:47
tags:
	- Linux

---

1

以ch341的为例进行分析。

对外的输出是：

```
module_usb_serial_driver(serial_drivers, id_table);
```

这个实际上封装了module_init和module_exit。

主要是实现这个结构体。

```
struct usb_serial_driver ch341_device
```



```
usb_serial_port
usb_serial

```



参考资料

1、

