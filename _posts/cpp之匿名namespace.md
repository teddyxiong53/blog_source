---
title: cpp之匿名namespace
date: 2019-02-28 09:28:17
tags:
	- cpp

---



当定义一个namespace的时候，可以不指定名字。

这样的namespace就叫做匿名namespace。

这个编译的处理，是自动生成了一个唯一的名字。然后使用using这个唯一的名字。

在匿名空间里的变量、函数、类这些符合，也被自动附加了唯一的名字。

匿名namespace的只能在当前文件里用。效果跟static类似。

推荐使用匿名namespace来达到static的效果。而且，static无法秀时候类。





参考资料

1、C++匿名命名空间

https://www.cnblogs.com/youxin/p/4308364.html