---
title: Linux显示之Plymouth
date: 2021-12-20 11:07:11
tags:
	- Linux

---

--

看这个文档，提到了Plymouth。了解一下。

https://github.com/notro/fbtft/wiki/Bootsplash#prerequisites

什么是Plymouth？

首先这个是英国的地名普利茅斯 

Plymouth 是一个来自于Fedora社区的提供美化启动图形界面的功能的项目，

现在它被列入了freedesktop.org的软件列表之中。

它依靠KMS尽可能早的设置显示器的原始分辨率显示，之后产生美化的启动引导界面直至登陆界面。

Plymouth 依靠 KMS (Kernel Mode Setting) 显示图形界面。

在EFI/UEFI系统中，Plymouth可以使用EFI帧缓冲。

如果你无法启用KMS，比如你使用了私有驱动，或者你只是纯粹不想使用EFI帧缓冲，那么可以考虑使用Uvesafb来适配大屏分辨率。

如果既没有KMS也没有framebuffer，那么Plymouth将使用文本模式。



参考资料

1、

https://wiki.archlinux.org/title/Plymouth_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)