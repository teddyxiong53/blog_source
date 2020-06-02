---
title: libevent之cpp封装
date: 2020-06-02 16:46:08
tags:
	- 网络

---

1

我觉得libevent依赖的东西，没有muduo那么多。

我可以把libevent用c++封装一下，比把muduo集成到自己的项目里，应该要更加方便一些。



仔细看了一下libevent的代码，其实比muduo还要复杂。

我不需要跨平台特性。也不需要自动选择各种io复用机制。

我还是自己基于select来做好了。



关键在于自己做好应用层的缓冲区。



参考资料

1、

https://blog.csdn.net/atp1992/article/details/99708245

2、服务器模型的C++封装类（libevent+多线程实现）

https://www.cnblogs.com/walker-lc/articles/3601128.html