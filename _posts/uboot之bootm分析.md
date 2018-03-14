---
title: uboot之bootm分析
date: 2018-03-04 11:08:44
tags:
	- uboot

---



bootm会先对uImage解压，解压后的位置是内核入口地址。

如果内核是用go的方式运行，那么就不会解压，内核要自解压。



bootm 0x80008000这个命令的执行过程分析：

```

```

