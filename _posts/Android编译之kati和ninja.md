---
title: Android编译之kati和ninja
date: 2020-04-11 16:58:51
tags:
	- Android

---

1

看Android编译有很多kita和ninja的描述，这2个东西我都不太了解。



soong这个是用来替代老的基于make的build工具。

之前是用Android.mk文件，现在是Android.bp文件。

soong的配置文件，使用了类似json的配置风格。

使用了go语言。

soong的信息，在aosp/build/soong目录下的readme.md里有写。



kati的信息在aosp/build/kati目录下的readme.md里。

kati是一个make的变种。主要目的是为了加快Android的编译速度。

kati用来把Makefile转成ninja配置文件。

单独ninja默认没有打开。你需要执行这个：

```
export USE_NINJA=true
```





参考资料

1、

