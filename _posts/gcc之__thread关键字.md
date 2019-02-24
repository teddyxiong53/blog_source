---
title: gcc之__thread关键字
date: 2019-02-23 15:20:17
tags:
	- gcc
---





这个关键字是为thread的local变量准备的。

用这个关键字修饰的变量，每个线程都会有一份。

这种变量，命名这样：

```
__thread int t_cachedTid = 0;
__thread char t_tidString[32];
```

t表示thread。



参考资料

1、gcc __thread关键字

https://blog.csdn.net/xj178926426/article/details/54345449