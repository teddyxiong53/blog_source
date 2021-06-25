---
title: uboot之logo显示
date: 2021-06-21 10:46:33
tags:
	- uboot

---

--

uboot 通过osd1显示启动logo，希望在kernel起来以后，osd1关闭之前，logo不会消失。

为了实现这个功能，需要将uboot中启动logo的地址(logo_addr)与kernel osd1 fb(fb1_addr)地址保持一致。

实现方式 (linux 4.9)

实现方式,通过dts file，将kernel 里logo_addr传给uboot,

同时让fb_reserved_base=logo_addr, 具体分为2种。



参考资料

1、



