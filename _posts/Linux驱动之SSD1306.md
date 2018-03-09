---
title: Linux驱动之SSD1306
date: 2018-03-08 19:45:20
tags:
	- Linux驱动

---



ssd1306是一款I2C接口的oled显示屏。

尺寸是126x64的。

这里有一套完整的代码。

https://github.com/notro/fbtft



# deferred io

Documentation/fb/deferred_io.txt里。

deferred io是一种延迟和重新定位的io。它使用host memory作为buffer和mmu页错误作为一个触发条件，来执行device io操作。

1、用户App mmap framebuffer。

2、延迟io和驱动建立错误和页写handler。

3、用户App试图去写mmap的内存。

4、产生了页错误。

5、处理处理程序返回物理页。

6、我们拿到页，添加到list。

7、在一个delay之后，调度一个workqueue任务，

8、App继续往这个页上写。这里效率很高，是这种方式是最大收益。

9、workqueue的任务执行，清理list上的页。这里是跟设备交互的实际工作。

10、app尝试去写地址，这里已经被清理了。

11、产生页错误，然后又重新走上面的流程。



允许burst写fb，代价很小。