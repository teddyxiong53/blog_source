---
title: Linux内核之压缩
date: 2020-07-24 10:06:51
tags:
	- Linux

---

--

有压缩的，也有非压缩的，

比如现在的arm64内核默认就不压缩，而且arm64内核也不提供自解压功能。

**如果内核压缩，一般要内核的头部加一段自解压的代码**，比如arm32通常都是这样。

arm64也可以编译出压缩的内核(**因为arm64内核不支持自解压，所以这个解压的任务要让bootloader来做**)，

而且有好几种压缩算法可以选，比如gzip lz4 lzma bzip2， 具体选哪个，看你是追求压缩比还是解压速度。



参考资料

1、为什么linux内核要压缩？

https://www.zhihu.com/question/64328724/answer/951270239

2、

https://www.cnblogs.com/danxi/p/6640471.html