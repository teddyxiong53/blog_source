---
title: glibc（1）
date: 2023-02-08 10:42:17
tags:
	- glibc

---

glibc是非常基础的库，值得研究一下。

查看glibc的版本：

```
ldd --version
```

例如这样：

```
ldd (Ubuntu GLIBC 2.31-0ubuntu9.7) 2.31
```

glibc的版本有什么需要注意的？



# 什么是 glibc？

GNU C 库项目为 GNU 系统和 GNU/Linux 系统以及许多其他使用 Linux 作为内核的系统提供*核心*库。

这些库提供关键 API，

包括 ISO C11、POSIX.1-2008、BSD、特定于操作系统的 API 等。

这些 API 包括诸如`open`、 `read`、`write`、`malloc`、`printf`、 `getaddrinfo`、`dlopen`、`pthread_create`、 `crypt`、`login`、`exit`等基础设施。



在20世纪90年代初，[Linux内核](https://zh.wikipedia.org/wiki/Linux内核)的开发团队[分叉](https://zh.wikipedia.org/wiki/分叉_(软件开发))了Glibc，名为“Linux libc”并单独维护。

当FSF在1997年1月发布glibc 2.0时，**由于glibc 2.0更符合POSIX标准**，内核开发者停止了Linux libc的开发。[[9\]](https://zh.wikipedia.org/zh-cn/GNU_C函式庫#cite_note-9) glibc 2.0还具有更好的[国际化](https://zh.wikipedia.org/wiki/国际化与本地化)和翻译、[IPv6](https://zh.wikipedia.org/wiki/IPv6)功能、64位数据访问、[多线程](https://zh.wikipedia.org/wiki/多线程)支持、未来版本的兼容性，而且代码更加可移植。



从2014年开始，[EGLIBC](https://zh.wikipedia.org/wiki/EGLIBC)不再开发，因为它“现在的目标是在glibc上直接解决问题”。



对于大多数系统来说，glibc的版本可以通过解析lib文件（例如，/lib/libc.so.6）获得。

glibc还提供了在开发[GNU](https://zh.wikipedia.org/wiki/GNU)时被认为有用或必要的扩展。



GNU C 库旨在成为一个向后兼容、可移植且高性能的 ISO C 库。它旨在遵循所有相关标准，



该项目大约于 1988 年开始，至今已有 30 多年的历史。

GNU C 库每 6 个月发布一次。有关详细信息，请参阅 glibc 源中的[新闻文件](https://sourceware.org/git/?p=glibc.git;a=blob_plain;f=NEWS;hb=HEAD)。

- glibc 当前的稳定版本是 2.37，发布于 2023 年 2 月 1 日。
- glibc 当前的开发版本为 2.38，发布时间为 2023 年 8 月 1 日左右。

# glibc vs musl

musl是一个比较简单的libc。

以musl作为参照系，来看看glibc。

musl遵循POSIX 2008规格和 C99 标准，采用MIT许可证授权，使用Musl的Linux发行版和项目包括sabotage，bootstrap-linux，LightCube OS等等。



然而musl的源代码很简单, 不像glibc的代码一样乱如垃圾场, 将性能较慢的函数换掉就能取得较大的性能提升.



# 参考资料

1、官网

https://www.gnu.org/software/libc/

2、维基百科

https://zh.wikipedia.org/zh-cn/GNU_C%E5%87%BD%E5%BC%8F%E5%BA%AB

3、官方手册

https://www.gnu.org/software/libc/manual/

4、glibc和musl对比

https://wiki.musl-libc.org/functional-differences-from-glibc.html

5、musl和glibc，性能区别到底有多大？

https://www.zhihu.com/question/550951106