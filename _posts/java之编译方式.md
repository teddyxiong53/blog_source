---
title: java之编译方式
date: 2019-04-04 09:31:30
tags:
	- java

---





java有三种编译方式：

1、前端编译。

2、即时编译。也叫后端编译。

3、静态提前编译。



# 前端编译

就是我们平时用的最普通的方式。用javac把java文件编译为class文件。

```
优点：
1、很多的java语法新特性，都是靠前端编译器实现的。
2、class文件可以交给jvm解释执行。

缺点：
1、对于代码运行效率几乎没有优化措施。
2、解释执行效率低。
```

# 即时编译

在运行时把class字节码编译为本地机器码的过程。

```
优点：
1、在运行时收集监控信息，把字节码转成本地机器码，进行了很多优化。

缺点：
1、收集监控信息影响程序执行。
2、会使得程序启动时间变长。
3、会多占用内存。

```

对应的编译器有：Hot Spot C1、C2、编译。

# 静态提前编译

AOT，Ahead Of Time。

这种方式用得少。不实用。



bin目录下javac，只是一个平台相关的入口。实际上真正起作用的是tools.jar文件。

标准的jdk没有提供javac的源代码。我们可以看openjdk里的实现。





参考资料

1、Java编译（一） Java三种编译方式：前端编译 JIT编译 AOT编译

https://blog.csdn.net/tjiyu/article/details/53748965

2、深入理解JVM读书笔记四： （早期）编译器优化

https://blog.csdn.net/jiankunking/article/details/52863249

3、Java编译（二） Java前端编译：Java源代码编译成Class文件的过程

https://blog.csdn.net/tjiyu/article/details/53786262