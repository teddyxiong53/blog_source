---
title: java之openjdk
date: 2018-11-04 10:44:30
tags:
	- java

---



openjdk是谁开发的？

是Sun公司开发的开源版本。完全自由。

是2006年的JavaOne大会上推出的。

2009年4月15日正式发布。

但是2010年，Oracle就收购了Sun。

2016年，谷歌在Android7.0里，把jdk换成了openjdk。以彻底解决java的专利问题。

官网在这里：http://openjdk.java.net/



主流linux发现版本，都把openjdk作为默认的java SE实现。

openjdk使用gpl v2协议开源。



openjdk不包含Deployment（部署）功能。

openjdk只包含最精简的jdk。

从这里下载源代码

http://hg.openjdk.java.net/jdk8/jdk8/jdk/archive/tip.zip

代码目录，主要在src/share目录下。

```
back
	不知道是什么。
bin
	bin工具代码。
classes
	java源代码。
demo
	demo程序。
instrument
	？
javavm
	？
lib
	？
native
	java对应类的C底层。
	例如String.java对应的String.c。
npt
	？
sample
	？
transport
	？
```

jvm的入口是在bin/java.c里。



# 参考资料

1、维基百科

https://zh.wikipedia.org/zh-hans/OpenJDK

2、openJdk和sun Jdk区别和安装

https://blog.csdn.net/lpjishu/article/details/53260099

3、openJDK源码分析

https://blog.csdn.net/anhuidelinger/article/details/14044853

4、JVM源码—教你傻瓜式编译openjdk7

http://www.importnew.com/23031.html