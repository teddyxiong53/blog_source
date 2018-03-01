---
title: 树莓派之cmdline
date: 2018-03-01 16:39:14
tags:
	- 树莓派

---



我的树莓派的cmdline.txt当前是这样的：

```
dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=/dev/sda2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait
```



#dwc_otg

关于dwc_otg的配置项目，这里有详细说明。

http://www.cl.cam.ac.uk/~atm26/ephemeral/rpi/dwc_otg/doc/html/module%20parameters.html



# rootwait

rootwait和rootdelay用在这样的场景：文件系统不能立即访问，例如SD卡、U盘上等。

在树莓派上，如果不rootwait，你就没法挂载跟文件系统。



# elevator=deadline 

电梯调度算法。

