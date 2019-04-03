---
title: java之Object的finalize方法
date: 2019-04-03 10:54:04
tags:
	- java

---



finalize方法，对象被垃圾回收器回收时，会被调用。

可以重写这个方法。

finalize，中文可以叫收尾机制。

相当于c++里的析构函数。



c++里支持局部对象（基于栈）和全局对象（基于堆）。

java里的所有对象都是全局对象（基于堆）。

c++的这个特性，需要自动构造和自动析构来支持。

java里不存在局部对象。

java的设计者就觉得java不需要析构函数。



```
public class FinalizeCase {

    private static Block holder = null;

    public static void main(String[] args) throws Exception {
        holder = new Block();
        holder = null;
        System.gc();
        //System.in.read();
    }

    static class Block {
        byte[] _200M = new byte[200*1024*1024];
    }
}
```



执行命令，加上打印gc日志的选项。

```
java -XX:+PrintGCDetails FinalizeCase
```



参考资料

1、java finalize方法的使用

https://blog.csdn.net/walkerjong/article/details/6950091

2、深入分析Object.finalize方法的实现原理

https://www.jianshu.com/p/9d2788fffd5f

3、GC日志查看分析

https://blog.csdn.net/TimHeath/article/details/53053106