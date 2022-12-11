---
title: C语言模拟面向对象
date: 2022-12-10 16:52:19
tags:
	- C语言

---

--

现在在用C语言实现snapcast的逻辑。

还是需要一些面向对象的技巧的。

还是系统学习一下其他人的经验。



C语言这种非面向对象的语言，

同样也可以使用面向对象的思路来编写程序的。

只是用面向对象的C++语言来实现面向对象编程会更简单一些，

但是C语言的高效性是其他面向对象编程语言无法比拟的。



当然使用C语言来实现面向对象的开发相对不容易理解，

这就是为什么大多数人学过C语言却看不懂Linux内核源码。



所以这个问题其实很好理解，

只要有一定C语言编程经验的读者都应该能明白：

面向过程的C语言和面向对象的C++语言相比，代码运行效率、代码量都有很大差异。

在性能不是很好、资源不是很多的MCU中使用C语言面向对象编程就显得尤为重要。



# 所具备的条件

要想使用C语言实现面向对象，首先需要具备一些基础知识。

比如：

（C语言中的）结构体、函数、指针，以及函数指针等，

（C++中的）基类、派生、多态、继承等。



# **封装** 

封装就是把数据和函数打包到一个类里面，其实大部分C语言编程者都已近接触过了。

C 标准库中的 fopen(), fclose(), fread(), fwrite()等函数的操作对象就是 FILE。

数据内容就是 FILE，

数据的读写操作就是 fread()、fwrite()，fopen() 类比于构造函数，fclose() 就是析构函数。

这个看起来似乎很好理解，那下面我们实现一下基本的封装特性。

编译下面代码的Makefile

```
.PHONY: all shape rect

all: shape rect

shape:
	gcc -c shape.c -o shape.o
	gcc -c shape_main.c -o shape_main.o
	gcc shape.o shape_main.o -o shape
rect:
	gcc -c shape.c -o shape.o
	gcc -c rect.c -o rect.o
	gcc -c rect_main.c -o rect_main.o
	gcc rect.o shape.o rect_main.o -o rect
```



## shape.h

```
#ifndef __SHAPE_H__
#define __SHAPE_H__

#include <stdint.h>

typedef struct {
    int x;
    int y;
} Shape;

void Shape_ctor(Shape *me, int x, int y);
void Shape_moveBy(Shape *me, int dx, int dy);
int Shape_getX(Shape *me);
int Shape_getY(Shape *me);

#endif // __SHAPE_H__
```

## shape.c

```
#include "shape.h"

void Shape_ctor(Shape *me, int x, int y)
{
    me->x = x;
    me->y = y;
}
void Shape_moveBy(Shape *me, int dx, int dy)
{
    me->x += dx;
    me->y += dy;
}
int Shape_getX(Shape *me)
{
    return me->x;
}
int Shape_getY(Shape *me)
{
    return me->y;
}
```

## main.c

```
#include "shape.h"

int main(int argc, char const *argv[])
{
    Shape s1, s2;
    Shape_ctor(&s1, 0,1);
    Shape_ctor(&s2, 2, 3);
    printf("s1(%d, %d)\n", s1.x, s1.y);
    return 0;
}

```

# 继承

在 C 语言里面，去实现单继承也非常简单，

只要把**基类放到继承类**的**第一个数据成员的位置**就行了。

例如，我们现在要创建一个 Rectangle 类，我们只要继承 Shape 类已经存在的属性和操作，再添加不同于 Shape 的属性和操作到 Rectangle 中。

## rect.h

```
#ifndef __RECT_H__
#define __RECT_H__

#include "shape.h"

typedef struct {
    Shape super;
    int w;
    int h;
} Rect;

void Rect_ctor(Rect *me, int x, int y, int w, int h);

#endif // __RECT_H__

```

## rect.c

```
#include "rect.h"

void Rect_ctor(Rect *me, int x, int y, int w, int h)
{
    //调用父类的构造。
    Shape_ctor(&me->super, x, y);
    me->w = w;
    me->h = h;
}

```

## rect_main.c

```
#include "rect.h"

int main(int argc, char const *argv[])
{
    Rect r1;
    Rect_ctor(&r1, 0, 1, 2 ,3);
    printf("rect x:%d\n", Shape_getX(&r1.super));
    //这样强制转换也可以的。
    printf("rect y:%d\n", Shape_getY((Shape *)&r1));
    return 0;
}

```

# 多态

C++ 语言实现多态就是使用虚函数。在 C 语言里面，也可以实现多态。

现在，我们又要增加一个圆形，并且在 Shape 要扩展功能，我们要增加 area() 和 draw() 函数。

但是 Shape 相当于抽象类，不知道怎么去计算自己的面积，更不知道怎么去画出来自己。

而且，矩形和圆形的面积计算方式和几何图像也是不一样的。

下面让我们重新声明一下 Shape 类：

## shape.h

```
#ifndef __SHAPE_H__
#define __SHAPE_H__

#include <stdint.h>

typedef struct {
    struct ShapeVtbl *vptr;
    int x;
    int y;
} Shape;

// Shape的虚表
struct ShapeVtbl {
    int (*area)(Shape *me);
    int (*draw)(Shape *me);
};

void Shape_ctor(Shape *me, int x, int y);
void Shape_moveBy(Shape *me, int dx, int dy);
int Shape_getX(Shape *me);
int Shape_getY(Shape *me);

static inline int Shape_area(Shape *me)
{
    return me->vptr->area(me);
}

static inline int Shape_draw(Shape *me)
{
    return me->vptr->draw(me);
}

#endif // __SHAPE_H__
```

## shape.c

```
static int Shape_area_(Shape *me)
{
    //这个是模拟虚函数，调用就报错。因为Shape是虚类。
    assert(0);
    return 0;
}

static void Shape_area_(Shape *me)
{
    //这个是模拟虚函数，调用就报错。因为Shape是虚类。
    assert(0);
}
void Shape_ctor(Shape *me, int x, int y)
{
    static struct ShapeVtbl vtbl = {
        &Shape_area_,
        &Shape_draw_
    };
    me->vptr = &vtbl;
    me->x = x;
    me->y = y;
}
```

## rect.c

需要继承vtbl和重载vptr。

上面已经提到过，基类包含 vptr，子类会自动继承。但是，vptr 需要被子类的虚表重新赋值。并且，这也必须发生在子类的构造函数中。下面是 Rectangle 的构造函数。



# 参考资料

1、

https://blog.csdn.net/slprogrammer/article/details/117648756

2、C语言实现面向对象编程 : 封装、继承、多态

https://blog.csdn.net/LxXlc468hW35lZn5/article/details/126112842