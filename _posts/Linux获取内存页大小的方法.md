---
title: Linux获取内存页大小的方法
date: 2017-05-18 19:25:03
tags:

	- linux

---

第一种方法是用getconf命令来获取，如下：

```
pi@raspberrypi:~$ getconf PAGE_SIZE
4096
pi@raspberrypi:~$ getconf PAGESIZE
4096
pi@raspberrypi:~$ 
```

可见页的大小是4096字节。也就是4K。

第二种方法是用getpagesize函数。

