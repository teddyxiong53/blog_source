---
title: Android之binder
date: 2019-04-03 15:10:04
tags:
	- Android

---



1

binder通信采用C/S架构。

```
在应用层，有3个部分：
1、server。
2、client。
3、service manager。

过程是：
1、server向ServiceManager注册服务。
2、client从ServiceManager获取服务。
3、client跟server进行通信。
```



参考资料

1、Binder系列—开篇

http://gityuan.com/2015/10/31/binder-prepare/