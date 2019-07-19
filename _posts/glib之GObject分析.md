---
title: glib之GObject分析
date: 2018-11-27 09:26:24
tags:
	- glib

---



大多数现代计算机语言都带有自己的类型和对象系统，并附带算法结构。

GObject对象系统提供了一种灵活的、可扩展的、容易映射的（到其他语言）的面向对象C语言框架。

它的实质可以概括为：

1、一个通用类型系统。

2、一个基本类型的实现集。

3、一个信号系统。



GObject 是基于GType的。

GType是glib运行时类型认证和管理系统。

理解GType是理解GObject的关键。



在GObject系统里，对象由三部分组成。

1、对象的id标识。

2、对象的类结构。

3、对象的实例。



C语言里模拟面向对象。只能靠结构体。

但是有不少的缺陷。需要通过设计来解决。

缺陷有：

```
1、语法比较别扭。
2、类型安全问题。
3、缺少封装。
4、空间的浪费。这个是最严重的。
	就是实例方法和类方法，其实都是一样的。
	这样定义一份就可以了。
```

所以进行了分开设计。

```
struct _GTypeClass //这个用来定义类型。
{
  GType g_type;//就是ulong类型。
};
struct _GTypeInstance //这个用来定义实例。
{
  GTypeClass *g_class;
};
```

实际使用是这样：

```
typedef strct _XxxOject XxxObject;
struct _XxxObject {//这个放所有的成员变量。
	GTypeInstance gtype;
	gint m_a;
	gchar *m_b;
	gfloat m_c;
};
typedef struct _XxxObjectClass XxxObjectClass;
struct _XxxObjectClass {//这个放函数。
	GTypeClass gtypeclass;
	void (*func1)(XxxObject *self, gint );
	void (*func2)(XxxObject *self, gchar *);
	void (*func3)(XxxObject *self, gfloat);
};
```





参考资料

1、GObject对象系统

https://www.ibm.com/developerworks/cn/linux/l-gobject/

2、GObject学习手册

https://wenku.baidu.com/view/14d8ea8cec3a87c24028c4da.html?from=search

3、GObject:用C实现类是如何做到的

https://blog.csdn.net/xbl1986/article/details/6702336