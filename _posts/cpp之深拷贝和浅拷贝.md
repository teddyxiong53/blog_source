---
title: cpp之深拷贝和浅拷贝
date: 2018-10-11 19:58:51
tags:
	- cpp
---

1

深拷贝叫member-wise-copy，浅拷贝叫bit-wise-copy。



对于基础类型变量来说，它们之间的拷贝是很简单的。

```
int a = 10;
int b = a;
```

而对于类对象来说，比较复杂，因为类里面存在各种成员变量。

先看一个例子。

```
#include <iostream>

using namespace std;

class CExample {
private:
    int a;
public:
    CExample(int b) {
        a = b;
    }
    void show() {
        cout << a << endl;
    }
};

int main()
{
    CExample A(100);
    CExample B = A;
    B.show();
	return 0;
}
```

得到的结果是100 。

对类对象来说，相同类型的的类对象，是通过拷贝构造函数来完成复制过程的。

下面我们看看拷贝构造函数的工作过程。

```
class CExample {
private:
    int a;
public:
    CExample(int b) {
        a = b;
    }
    CExample(const CExample& C) {//这个就是拷贝构造函数。
        a = C.a;
    }
    void show() {
        cout << a << endl;
    }
};
```

我们自己写一个拷贝构造函数，如上。

拷贝构造函数的特点：

唯一的参数是类名本身的一个引用，而且是const类型。

这些情况都会调用到拷贝构造函数：

1、一个对象以值传递的方式作为函数参数。

2、函数返回以值的方式。

3、一个对象需要通过另外一个对象进行初始化。

如果你没有实现拷贝构造函数，编译器会默认帮你生成一个。

**这个默认拷贝构造函数，完成的是浅拷贝。**

很多时候，成员变量是一个指针，如果把一个对象的内容完全拷贝给另外一个对象，那么一个对象释放内存，另外一个对象里的指针，就变成了野指针了。

所以，深拷贝，就是新的对象，在指针初始化时，不是完全拷贝，而且另外分配。





# 参考资料

1、C++拷贝构造函数(深拷贝，浅拷贝)

https://www.cnblogs.com/BlueTzar/articles/1223313.html

2、深入分析深拷贝(Memberwise Copy)和浅拷贝(Bitwise Copy)

https://blog.csdn.net/songshiMVP1/article/details/51248658