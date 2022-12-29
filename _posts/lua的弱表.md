---
title: lua的弱表
date: 2022-12-18 15:45:51
tags:
	- lua

---

--

什么是弱表？

弱表就是表内的item是弱引用的表。

那么什么是弱引用？

先看lua里什么是引用。

table、function、thread、userdata这4种类型，都是引用类型。

从代码上一看就清楚了。

```
typedef union Value {
  GCObject *gc;    /* collectable objects */
  void *p;         /* light userdata */
  int b;           /* booleans */
  lua_CFunction f; /* light C functions */
  lua_Integer i;   /* integer numbers */
  lua_Number n;    /* float numbers */
} Value;
```

是指针类型的都是属于引用类型。

引用类型的特点就是只传递指针，不会另外分配一块内存。

**weak表是一个表，它拥有metatable，并且metatable定义了__mode字段**；

```
__mode字段可以取以下三个值：k、v、kv。
k表示table.key是weak的，也就是table的keys能够被自动gc；
v表示table.value是weak的，也就是table的values能被自动gc；
kv就是二者的组合。任何情况下，只要key和value中的一个被gc，那么这个key-value pair就被从表中移除了
```



**对于普通的强引用表，当你把对象放进表中的时候，就产生了一个引用，那么即使其他地方没有对表中元素的任何引用，gc也不会被回收这些对象。**

那么你的选择只有两种：手动释放表元素或者让它们常驻内存。



# 参考资料

1、

https://blog.csdn.net/shimazhuge/article/details/40310233