---
title: Linux驱动之字符设备代码分析
date: 2018-03-07 19:35:54
tags:
	- Linux

---



主设备号有12位，所以取值范围是0到4095 。

而char_dev.c里的一个数组的长度是这么多。

```
#define CHRDEV_MAJOR_HASH_SIZE	255
```

所以major为257的和major为2的，都在在index为2的指针链表里。

这个数组是一个hash表。

major系统，minor不重叠，就没事。

不过系统一般让主设备号不超过254的。取值范围是1到254 。

