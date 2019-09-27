---
title: cpp之enable_shared_from_this
date: 2019-03-21 10:52:32
tags:
	- cpp

---



1

用途就是把this裸指针也产生一个智能指针版本。

对应的智能指针，用shared_from_this()的方式来使用。



在智能指针的使用过程中，我们会遇到这样一种情况。

我们在类的成员函数里调用某一个函数func1。

func1需要一个当前对象的智能指针作为参数。

这个时候，我们就需要在成员函数里获取到自己的智能指针。

在多线程编程中，也存在这样的情况：

```
如果我们的thread_entry函数绑定的是一个成员函数。
我们可以通过把该对象的智能指针作为参数传递到thread_entry函数里。

这种做法是人为增加了对象的引用计数。
延长了对象的生命周期。
防止了thread_entry函数在执行的时候，对象被释放而导致内存错误。

```

说了这么多，就是为了说明：

在实际编码中，我们有获取当前对象的智能指针的需求。



但是，我们不能人为地用this来构造一个当前对象的shared_ptr指针。

例如下面这样做。（是错误的做法）。

```
void func1(std::shared_ptr<TestClass> tt) {

}

class TestClass {
public:
    void TestPtr() {
        std::shared_ptr<TestClass> tt = std::shared_ptr<TestClass> (this);
        func1(tt);
    }
};
```

这个里面的问题是：

tt的生命周期很短，是个局部变量。



为了解决这个问题，c++11引入了enable_shared_from_this这个模板类。

这个模板类提供了一个方法：

```
shared_from_this
```

来获取指向自己的智能指针。



改造后的例子是这：

```
class TestClass:public enable_shared_from_this<TestClass>{
public:
    void TestPtr() {
        std::shared_ptr<TestClass> tt = shared_from_this();
        func1(tt);
    }
};
```

这样就不会出错了。





参考资料

1、关于std::enable_shared_from_this 的继承和 shared_from_this调用崩溃的解析

https://blog.csdn.net/fm_VAE/article/details/79660768