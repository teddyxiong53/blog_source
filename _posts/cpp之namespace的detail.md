---
title: cpp之namespace的detail
date: 2019-03-22 15:47:32
tags:
	- cpp

---





看muduo的代码，有不少的detail的namespace，看得出来，这是一种常用的编码实践。

还有的是命名为internal。

不少的大型开源软件都这么写的。

这样有什么好处呢？

就是避免暴露不必要的东西给外部。





参考资料

1、What is the detail namespace commonly used for

https://stackoverflow.com/questions/26546265/what-is-the-detail-namespace-commonly-used-for