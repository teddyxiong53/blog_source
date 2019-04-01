---
title: Android之多线程
date: 2019-04-01 16:44:04
tags:
	- Android

---



当我们启动一个Android app的时候，系统就会启动一个Linux进程。

这个进程里默认只有一个线程，叫做Main Thread。也叫UI Thread。

在主线程里，做了这些事情：

```
1、处理系统事件。
2、处理用户输入。
3、绘制ui。
4、定时。
```

我们的操作如果很耗时，就需要另外起线程来做。

我们的操作完成后，需要把结果反馈给主线程来刷新界面。

Android里提供了4种多线程方式：

```
1、Handler + Thread。
2、AsyncTask。
3、ThreadPoolExecutor。
4、IntentService。
```



参考资料

1、Android多线程的四种方式

https://www.jianshu.com/p/2b634a7c49ec

2、Android 多线程编程的总结

https://www.diycode.cc/topics/213