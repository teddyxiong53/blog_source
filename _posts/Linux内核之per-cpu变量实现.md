---
title: Linux内核之per-cpu变量实现
date: 2018-04-07 20:27:24
tags:
	- Linux

---

--

Linux内核里，为了提高smp系统的性能，加入了per-cpu变量的机制。

**用来给每个CPU都生成一个变量的副本，从而不需要加锁，达到提高性能的目的。**

每cpu变量是最简单也是最重要的同步技术。

每cpu变量主要是数据结构数组，系统的每个cpu对应数组的一个元素。

一个cpu不应该访问与其它cpu对应的数组元素，

另外，它可以随意读或修改它自己的元素而不用担心出现竞争条件，

因为它是唯一有资格这么做的cpu。

**这也意味着每cpu变量基本上只能在特殊情况下使用**，也就是当它确定在系统的cpu上的数据在逻辑上是独立的时候。



在arm平台上，armv6之前，swp和swpb指令被用来支持对shared memory的访问。

```
swp Rt, Rt2, Rn
```

Rn里保存了swp指令要操作的内存地址，

把Rn指向的内存数据加载到Rt寄存器。

同时把Rt2寄存器的值写入到Rn指向的内存里去。





# 相关的使用接口

声明和定义

```
DECLARE_PER_CPU(type, name)
DEFINE_PER_CPU(type, name)
还有一些变种，不管先。
```

静态定义的per-cpu变量不能直接访问，要通过特定接口进行读写。

```
get_cpu_var(var)
put_cpu_var(var)
```

这2个接口已经禁止了抢占了。

如果用户确认自己当前的调用上下文是比禁止抢占更高的，例如关闭中断了。

那么也就可以使用lock-free版本的：`__get_cpu_var`。

动态分配和释放：

```
alloc_percpu(type)
void free_percpu(void __percpu *ptr)
```

访问动态的per-cpu变量，也要专门的接口。

```
get_cpu_ptr
put_cpu_ptr
per_cpu_ptr(ptr, cpu)
```





# 参考资料

1、

https://blog.csdn.net/eric_zl_zhang/article/details/6893840

2、Linux内核同步机制之（二）：Per-CPU变量

https://www.cnblogs.com/dirt2/p/5616513.html