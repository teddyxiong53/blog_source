---
title: qemu之模拟树莓派
date: 2018-03-25 17:12:23
tags:
	- qemu
	- 树莓派

---



```
qemu-system-arm.exe -M versatilepb -cpu arm1176 -hda 2012-07-15-wheezy-raspbian.img -kernel kernel-qemu -m 192 -append "root=/dev/sda2"
```

