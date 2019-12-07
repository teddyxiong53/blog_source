---
title: Linux内核之compiler.h头文件
date: 2019-12-07 10:07:30
tags:
	- Linux内核
---

1

```
__ASSEMBLY__
	这个变量实际是在编译汇编代码的时候，由编译器使用-D这样的参数加进去的，AFLAGS这个变量也定义了这个变量
	因为汇编的时候，__user这些宏需要是空的。
__CHECKER__
	make C=1的时候，会有这个宏定义。
	会调用一个叫Sparse的工具
	__user 这些就是靠sparse工具来检查的。
	
这里把程序空间分成了3个部分，0表示normal space，即普通地址空间，对内核代码来说，当然就是内核空间地址了。1表示用户地址空间，这个不用多讲，还有一个2，表示是设备地址映射空间，例如硬件设备的寄存器在内核里所映射的地址空间。
```



参考资料

1、

https://blog.csdn.net/jiebaoabcabc/article/details/29855901