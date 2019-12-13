---
title: Linux驱动之用户空间驱动
date: 2018-03-30 21:55:31
tags:
	- Linux驱动

---



用户空间驱动是一种思路。

尽管受到很多的限制，但是可以实现一些驱动。

用户空间驱动的优点：

1、可以跟C库链接。

2、可以用gdb来调试。

3、安全。驱动有问题，不会把内核崩掉。

用户空间驱动的缺点：

1、中断在用户空间不可用。

2、只有通过mmap和/dev/mem才能直接访问内存。

3、速度较慢。



XServer就是一个典型的用户空间驱动。



用户态直接操作寄存器的方法

用mmap。



# 参考资料

1、在用户空间编写驱动程序

https://blog.csdn.net/xiezhi123456/article/details/81004421

2、字符设备驱动另一种写法—mmap方法操作LED

https://www.cnblogs.com/weidongshan/p/8178937.html

3、linux下操作gpio寄存器的方法

https://www.cnblogs.com/mylinux/p/5639264.html

4、

http://www.360doc.com/content/15/0401/14/9075092_459810908.shtml

5、利用mmap()操作硬件寄存器

https://blog.csdn.net/litao31415/article/details/43759771

6、嵌入式编程中应如何使用 mmap 访问 CPU 寄存器

https://segmentfault.com/a/1190000008381626