---
title: python之pypy
date: 2020-04-26 23:37:22
tags:		
	- python

---

1

pypy是什么？

就是用python语言实现的python解释器，就是自举。

默认的python解释器是用C语言实现的。也叫cpython。

还有java实现的python解释器，叫jython。

pypy总的来说，还是一个研究性质的东西。还不具备生产可用性。

python有多种实现，而且与其他语言不同，**python并没有一个专门的机构负责实现，而是由多个社区来实现。**

而PyPy使用了JIT(即时编译)技术，在性能上得到了提升。



CPython：是用C语言实现Pyhon，是目前应用最广泛的解释器。最新的语言特性都是在这个上面先实现，基本包含了所有第三方库支持，但是CPython有几个缺陷，一是(GIL)全局锁使Python在多线程效能上表现不佳，二是CPython无法支持JIT（即时编译），导致其执行速度不及Java和Javascipt等语言。

于是出现了Pypy。

Pypy：是用Python自身实现的解释器。针对CPython的缺点进行了各方面的改良，性能得到很大的提升。最重要的一点就是Pypy集成了JIT。但是，Pypy无法支持官方的C/Python API，导致无法使用例如Numpy，Scipy等重要的第三方库。这也是现在Pypy没有被广泛使用的原因吧。

PyPy，它使用了JIT（即时编译）技术，混合了动态编译和静态编译的特性，仍然是一句一句编译源代码，但是会将翻译过的代码缓存起来以降低性能损耗。相对于静态编译代码，即时编译的代码可以处理延迟绑定并增强安全性。绝大部分 Python代码都可以在PyPy下运行，但是PyPy和CPython有一些是不同的。





参考资料

1、PyPy 为什么会比 CPython 还要快？

https://blog.csdn.net/jqc_ustc/article/details/79968399

2、百科

https://baike.baidu.com/item/PyPy/9780733?fr=aladdin