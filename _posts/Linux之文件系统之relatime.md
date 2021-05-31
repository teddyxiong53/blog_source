---
title: Linux之rtcwake
date: 2021-05-27 11:35:11
tags:
	- Linux

---

--

noatime：直接没有atime，让系统中的atime失效；

relatime：只有当mtime/ctime的时间戳晚于atime的时候才去更新atime；

lazytime：如果仅有inode变脏，那么控制inode下发的时间。



参考资料

1、文件系统中 atime,lazytime,relatime 详聊

https://blog.csdn.net/weixin_30247159/article/details/98049533

