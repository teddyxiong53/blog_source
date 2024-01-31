---
title: Linux内核之gki
date: 2022-10-20 19:40:33
tags:
	- Linux内核
---

--

看amlogic的buildroot/linux/Config.in里有添加GKI的相关内容，了解一下这个。

Google在android11-5.4分支上开始要求所有下游厂商使用Generic Kernel Image（GKI），

需要将**SoC和device相关的代码从核心内核剥离到可加载模块中**（下文称之为GKI改造），

**从而解决内核碎片化问题。**

GKI为内核模块提供了稳定的内核模块接口（KMI），模块和内核可以独立更新。

本文主要介绍了在GKI改造过程中需遵循的原则、遇到的问题和解决方法。



不过对于buildroot，并没有打开这个特性：

```
# BR2_LINUX_KERNEL_GKI is not set
```

这个是Android的要求。



# 参考资料

1、GKI改造原则、机制和方法

https://blog.csdn.net/feelabclihu/article/details/113409593

2、Linux GKI开发指南 中文完整版PDF

https://www.jb51.net/books/916755.html

3、

https://wuxianlin.com/2023/02/10/android-gsi-and-gki/