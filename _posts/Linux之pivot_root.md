---
title: Linux之pivot_root
date: 2021-05-27 15:00:11
tags:
	- Linux

---

--

pivot_root: 改变root文件系统
  用法：pivot_root new_root put_old
  描述：pivot_root把当前进程的root文件系统放到put_old目录，而使new_root成为新的root文件系统。

pivot_root和chroot的主要区别是，pivot_root主要是把整个系统切换到一个新的root目录，而移除对之前root文件系统的依赖，这样你就能够umount原先的root文件系统。而chroot是针对某个进程，而系统的其它部分依旧运行于老的root目录。

参考资料

1、Linux中chroot与pivot_root的区别

https://blog.csdn.net/linuxchyu/article/details/21109335