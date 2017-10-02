---
title: Linux之urandom和random设备区别
date: 2017-10-01 10:28:49
tags:
	- Linux
	- random

---



Linux下有/dev/random和/dev/urandom这2个设备。产生随机数的方式都是这样：

```
Linux 产生随机数的两种方式
cat  /dev/urandom | od -x | sed 's/\s*//g' |cut -c 8-16 |less 
cat  /dev/random | od -x | sed 's/\s*//g' |cut -c 8-16 |less 
```



区别何在呢？

random会把设备锁住，直到系统产生的随机数已经够用，耗时较长。

而urandom不会把设备锁住。数据的随机数不高，但是够用了。



简而言之，用urandom好些。





