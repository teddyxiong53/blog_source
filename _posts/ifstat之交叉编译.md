---
title: ifstat之交叉编译
date: 2018-11-16 16:01:17
tags:
	- Linux

---



代码下载地址：

http://freshmeat.sourceforge.net/projects/ifstat/

配置。

```
./configure --prefix=/opt/doss/gome/toolchain/gcc/linux-x86/arm/gcc-linaro-6.3.1-2017.05-x86_64_arm-linux-gnueabihf --target=arm CC=arm-linux-gnueabihf-gcc
```

这样还是不对，还需要手动到Makefile里改一下。

```
CC          = arm-linux-gnueabihf-gcc
```

然后make就好了。

