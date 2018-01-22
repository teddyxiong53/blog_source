---
title: easybcd工具了解
date: 2018-01-21 13:23:02
tags:
	- 系统

---



在弄双系统的时候，接触到easybcd这个工具，觉得很强大，所以想把相关情况了解清楚一些。

版本是2.3版本的。

看help里的信息。

1、easybcd是一个强大的bootloader修改工具。

2、支持引导所有桌面系统。但是该软件只能在windows上使用。

3、当在一个用UEFI模式启动的电脑上打开easybcd软件的时候，会弹窗提示：

```
EasyBcd检测到你的机器是用EFI模式启动的。因为微软的限制，很多的Easybcd多系统引导功能不能再EFI模式下使用。
```

这段话的具体含义有：

1）微软禁止了非windows从BCD菜单引导系统。

2）你可以到boot菜单里把UEFI的禁止掉。还是用传统的BIOS来引导。

3）你也可以安装grub到MBR上，然后把grub设置为pc的默认bootloader。然后启动的时候，你是从grub的菜单里选择启动哪个系统。



# mac和windows双系统

先安装的windows系统。

