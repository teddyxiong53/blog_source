---
title: Linux之arm-none和arm-linux区别
date: 2018-03-13 21:07:53
tags:
	- Linux

---



arm工具链，有的叫arm-none-eabi，有的叫arm-none-linux-eabi，区别是什么？



命名规则是：

```
arch-vendor-os-eabi
```

最好都用arm-none-linux-eabi

因为arm-none-eabi的不能编译busybox这种应用层的东西。



在Ubuntu系统上都可以用apt-get来安装。

可以先用apt-cache search模糊搜索一下，找到名字再安装。

