---
title: java之内存泄漏
date: 2019-03-29 16:07:32
tags:
	- java

---



java有自动垃圾收集，不需要程序员自己手动管理内存。理论上是不会有内存泄漏的，但是实际上还是有可能的。

首先我们看看java里的内存是如何进行管理的。

在java里，我们都是用new来为对象分配内存。

这些都是在heap上分配的内存。

```
public class Test {
    public static void main(String[] args) {
        Object obj1 = new Object();
        Object obj2 = new Ojbect();
        obj2 = obj1;//到这里之后，obj2之前分配的那块内存已经是可以被回收了。
    }
}
```

下面这个代码会有暂时的内存泄漏。

```
public class Test {
    public void func1() {
        Object obj = new Object();
        //其他代码
    }
}
```

obj只在

参考资料

1、JAVA 内存泄漏详解（原因、例子及解决）

https://blog.csdn.net/anxpp/article/details/51325838