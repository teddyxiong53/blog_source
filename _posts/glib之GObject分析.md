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



所以，就是说，GObject每个类，都需要定义两个结构体。

例如，People类，就需要定义People和PeopleClass这2个结构体。

遵循下面的原则：

当第一次产生People类的实例的时候，会先分配PeopleClass的空间。否则直接只分配People结构体的空间。



需要定义这些工具宏。

```
//获取类型
#define JC_TYPE_BOY (jc_boy_get_type())
//实例类型转化
#define JC_BOY(obj)  (G_TYPE_CHECK_INSTANCE_CAST((obj), JC_TYPE_BOY, JcBoy))
//实例类型判定
#define JC_IS_BOY(obj)  (G_TYPE_CHECK_INSTANCE_TYPE((obj), JC_TYPE_BOY))
//类结构转化
#define JC_BOY_CLASS(klass) (G_TYPE_CHECK_CLASS_CAST((klass), JC_TYPE_BOY, JcBoyClass))
//类结构判定
#define JC_IS_BOY_CLASS(klass)  (G_TYPE_CHECK_CLASS_TYPE((klass), JC_TYPE_BOY))
//获取类结构
#define JC_BOY_GET_CLASS(obj)  (G_TYPE_INSTANCE_GET_CLASS((obj), JC_TYPE_BOY, JcBoyClass))
//获取私有结构，如果没有，可以不定义这个宏。
#define JC_BOY_GET_PRIVATE(obj)  (G_TYPE_INSTANCE_GET_PRIVATE((obj), JC_TYPE_BOY, JcBoyPrivate))
```

命名规律是：`域名_类名_xx`

域名，就是为了防止类型名字冲突。例如gtk的GTK_前缀。

上面代码，就是定义了JC这个域名（随便写的）下的Boy这个类。

然后就需要定义对应的结构体了。

```
typedef struct _JcBoy JcBoy;

struct _JcBoy {
	JcBaby parent_instance;
	/*public*/
	//...
	/*private*/
	JcBoyPrivate *priv;
};
typedef struct _JcBoyClass JcBoyClass;
struct _JcBoyClass {
	JcBabyClass parent_class;
	//class member var
	//...
	//virtual method or signal
	void (*play)(JcBaby *self);
};

typedef struct _JcBoyPrivate JcBoyPrivate;
struct _JcBoyPrivate {
	gchar *name;
	guint age;
	gchar *hobby;
};

```

我们把上面的代码，放入到jc_boy.h里。

现在开始写jc_boy.c文件。

```
static void jc_boy_init(JcBoy *self)
{
	JcBoyPrivate *priv = NULL;
	priv = self->priv = JC_BOY_GET_PRIVATE(self);
	priv->name = g_strdup("no-name");
	priv->hobby = g_strdup("nothing");
	priv->age = 0;
}

static void jc_boy_class_init(JcBoyClass *klass)
{
	g_type_class_add_private(klass, sizeof(JcBoyPrivate));
	klass->play = play;
}

void play()
{
	g_print("the boy is playing football \n");
}
```

首先写的是实例结构体和类结构体的初始化函数。

需要向GObject系统注册类型。

g_type_register_xx 这个函数是用来注册类型的。可以注册为static、dynamic、fundamental的。

fundamental是指没有父类的普通类。

static的最简单，我们先只了解这个。

```
GType g_type_register(
	GType parent_type, 
	const gchar *type_name, 
	const GTypeInfo *info,//这个是最复杂的。
	GTypeFlags flags
);
```

为了简化程序员的工作，GObject提供了宏来帮助我们快速定义类型。

例如G_DEFINE_TYPE。

```
G_DEFINE_TYPE(JcBoy, jc_boy, G_TYPE_OBJECT);
```

# 继承GObject类的好处

1、基于引用计数的内存管理。

2、对象的构造和析构函数。

3、可设置对象属性的set/get方法。

4、易于使用的信号机制。





参考资料

1、GObject对象系统

https://www.ibm.com/developerworks/cn/linux/l-gobject/

2、GObject学习手册

https://wenku.baidu.com/view/14d8ea8cec3a87c24028c4da.html?from=search

3、GObject:用C实现类是如何做到的

https://blog.csdn.net/xbl1986/article/details/6702336

4、Gobject的闭包

https://blog.csdn.net/evsqiezi/article/details/82695585

5、C语言面向对象开发法--GObject

这个讲得比较基础，比较好懂。

https://wenku.baidu.com/view/d7c8787f1711cc7931b716e1.html?sxts=1564108386035

6、GObject学习教程---第一章：GObject是有用并且简单的

这个教程似乎不错。

https://blog.csdn.net/knowledgebao/article/details/82387743