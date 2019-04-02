---
title: java之内存模型
date: 2019-04-02 17:53:04
tags:
	- java

---



java内存模型，Java Memory Model。缩写为JMM。

JMM定义了jvm在内存里的工作方式。

如果我们要深入理解Java的并发编程，就需要把JMM理解透彻。

java内存模型定义了：

1、多线程之间共享变量的可见性。

2、如何在需要的时候对共享变量进行同步。

之前版本的内存模型效果不好，在jdk1.5的时候，进行了重构，沿用至今。



在并发编程领域，有两个关键问题：线程之间的通信和同步。



参考资料

1、全面理解Java内存模型

https://blog.csdn.net/suifeng3051/article/details/52611310

