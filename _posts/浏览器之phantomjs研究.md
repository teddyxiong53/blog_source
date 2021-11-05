---
title: 浏览器之phantomjs研究
date: 2021-11-02 14:04:25
tags:
	- 浏览器

---

--

现在对os的兴趣下降，对浏览器的兴趣大增。

想找一个简单的浏览器来读一下代码。

看phantomjs这个无头浏览器，代码似乎并不多。而且这个工具也比较实用。

所以读一读。

先把代码下载下来简单看看。

https://github.com/ariya/phantomjs

先还是看一下基本用法。

PhantomJS是一个基于webkit的javaScript API。

它使用QtWebKit作为它核心浏览器的功能，

使用webkit来编译解释执行javaScript代码。

任何你可以基于在webkit浏览器做的事情，它都能做到。

它不仅是个隐性的浏览器，

提供了诸如css选择器、支持wen标准、DOM操作、json、HTML5等，

同时也提供了处理文件I/O的操作，

从而使你可以向操作系统读写文件等。

phantomJS的用处可谓非常广泛诸如网络监测、网页截屏、无需浏览器的wen测试、页面访问自动化等。

所以依赖了qt库。



代码看起来还比较干净，可以作为qt库实用的学习材料。



参考资料

1、

https://blog.csdn.net/qq_37245397/article/details/81543450