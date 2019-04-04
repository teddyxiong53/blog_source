---
title: java之静态内部类
date: 2019-04-04 15:21:30
tags:
	- java

---



什么是静态内部类？

```
class Test {
    static class XXX {//这个XXX就是静态内部类了。
        
    }
}
```

有什么特点？



静态内部类和非静态内部类的区别：

```
区别就是，如果你在这个类里面需要外面类的引用，就不要用static。反之就尽量用static，这样可以提高性能。Effective Java里面讨论过这个问题，建议看一下。
```



参考资料

1、Java静态内部类(static class)

https://blog.csdn.net/yaomingyang/article/details/79363631

2、为什么Java内部类要设计成静态和非静态两种？

https://www.zhihu.com/question/28197253