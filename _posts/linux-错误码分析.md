---
title: linux 错误码分析
date: 2016-11-04 21:05:40
tags:
	- linux
---
linux的错误码主要分布在这几个文件里。以arm架构的为例。源代码是linux2.6.35.7。
```
./include/asm-generic/errno-base.h -- 定义了1到34号错误。是最基础的一个文件。
./include/asm-generic/errno.h --包含了errno-base.h，并定义了35到132号错误。
./arch/arm/include/asm/errno.h -- 这个就是包含了./include/asm-generic/errno.h，没别的内容。
./include/linux/errno.h --包含了./arch/arm/include/asm/errno.h，并且定义了512到530号错误。
```


