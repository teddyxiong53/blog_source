---
title: Android之优化
date: 2019-04-01 17:53:04
tags:
	- Android

---



应用按照启动场景的不同可以分为三种启动方式：

```
1、冷启动。
	应用进程没有创建。
2、暖启动。
	应用进程已经创建。但是当前页面的Activity已经被销毁或者还未创建。
3、热启动。
	应用和当前Activity都存在。
```



启动优化主要就是针对冷启动的。



参考资料

1、Android应用优化：启动优化

https://guoxiaoxing.gitbooks.io/android-open-source-project-analysis/content/doc/Android%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91%E5%AE%9E%E8%B7%B5%E7%AF%87/Android%E5%BA%94%E7%94%A8%E4%BC%98%E5%8C%96/02Android%E5%BA%94%E7%94%A8%E4%BC%98%E5%8C%96%EF%BC%9A%E5%90%AF%E5%8A%A8%E4%BC%98%E5%8C%96.html

