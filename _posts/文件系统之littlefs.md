---
title: 文件系统之littlefs
date: 2023-09-29 13:06:11
tags:
	- 文件系统
---

--

作为一款在嵌入式设备上使用的文件系统，出问题时，一般是需要将数据dump出来进行分析的。此时就需要PC端的调试工具了。

# littlefs-fuse简介

这个项目提供了一个littlefs的FUSE封装，也就是你可以借助此项目，在PC上直接将littlefs镜像挂载起来，并正常进行一些文件系统的操作。

源码位于：[https://github.com/ARMmbed/littlefs-fuse](https://cloud.tencent.com/developer/tools/blog-entry?target=https%3A%2F%2Fgithub.com%2FARMmbed%2Flittlefs-fuse)





参考资料

1、

https://blog.csdn.net/weixin_43908815/article/details/130179573

2、

https://zhuanlan.zhihu.com/p/652074347

3、

https://article.itxueyuan.com/GoA0e4

4、使用littlefs-fuse在PC端调试littlefs文件系统

https://cloud.tencent.com/developer/article/1560535

5、片上flash使用文件系统笔记

https://club.rt-thread.org/ask/article/a5c8b007eed2584e.html