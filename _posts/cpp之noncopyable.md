---
title: cpp之noncopyable
date: 2019-02-21 11:05:33
tags:
	- cpp
---



拷贝是编程语言里必不可少的操作。

cpp里的拷贝分为两种：

```
1、等号拷贝。Foo foo,foo2; foo2 = foo;
2、构造拷贝。Foo foo3(foo);
```

等号拷贝和构造拷贝都可以被重载。

默认的行为是把每个类的成员依次进行拷贝。



什么时候需要不可拷贝类？

我们看矩阵类的情况。

```
template<typename _T>
class Matrix {
public:
    int w;
    int h;
    _T *data;

    Matrix(int _w, int _h): w(_w),h(_h) {
        data = new _T[w*h];
    }

    ~Matrix() {
        delete [] data;
    }
}
```

对于这样一个类，在拷贝后，data指针就被覆盖了。而拷贝前之前的data指向的内存没有被释放，这就造成了内存泄露了。

解决办法有：自己重载实现拷贝函数。等号和构造拷贝都进行重载。

```
Matrix<_T>& operator=(const Matrix<_T>& cpy) {
        w = cpy.w;
        h = cpy.h;
        delete [] data;
        data = new _T[w*h];
        memcpy(data, cpy.data, sizeof(_T)*w*h);
        return *this;
    }

    Matrix(const Matrix<_T>& cpy): w(cpy.w), h(cpy.h) {
        data = new _T[w*h];
        memcpy(data, cpy.data, sizeof(_T)*w*h);
    }
```

但是这样做，也有不好的地方。

在数据量很大的时候，例如图像处理的矩阵就很大。这样很影响效率。

解决的办法是设计专门的拷贝接口。copyFrom。来取代等号拷贝。

另外，禁用构造拷贝函数。

有3种方式可以做到：

```
1、使用boost库的noncopyable类。继承这个类就好了。
2、自己把拷贝构造函数设置为private的。
3、c++11提供了delete关键字来禁用拷贝构造函数。
```





参考资料

1、C++: 不可拷贝（noncopyable）类

https://fzheng.me/2016/11/20/cpp_noncopyable_class/