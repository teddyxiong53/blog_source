---
title: Linux之串口驱动
date: 2020-07-27 15:42:51
tags:
	- Linux

---

1

在嵌入式Linux系统中，串口被看成终端设备，终端设备（tty）的驱动程序分为3部分：

tty_core

tty_disicipline 

tty_driver

包括3个结构体：uart_driver,uart_port,uart_ops（include/serial_core.h）。因此，实现一个平台的uart驱动程序只要实现这3个结构体即可。



uart_port用于描述一个UART端口（直接对应于一个串口）的I/O端口或I/O内存地址、FIFO大小、端口类型等信息



```
uart_register_driver
uart_add_one_port
uart_write_wakeup
```



参考资料

1、Linux驱动之串口（UART）

https://www.cnblogs.com/big-devil/p/8590050.html

2、

https://developer.aliyun.com/article/495932