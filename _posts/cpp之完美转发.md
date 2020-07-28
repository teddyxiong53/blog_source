---
title: cpp之完美转发
date: 2019-09-20 13:42:48
tags:
	- cpp

---

1

什么是完美转发？它为什么出现？

完美转发是为例配合函数模板的的工作。

**解决的是函数模板在向其他函数传递参数时，如何保留参数的左右值属性的问题。**

也就是说，函数模板在向其他函数传递自身形参的时候，如果参数本来是左值，它就应该被转发为左值，

如果它本来是右值，那么就应该被转发为右值。

因为很多函数对于左右值是采取不同的处理的。

一般是对左值参数采用拷贝语义，对于右值参数采用移动语义。

**如果不处理，那么转发后，就都变成了左值了。这样就难以优化。**



一个简单例子。

```
#include <iostream>

using namespace std;

void func(int &x) {
    cout << "left value ref" << endl;
}
void func(int &&x) {
    cout << "right value ref" << endl;
}
void func(const int &x) {
    cout << "const left value ref" << endl;
}
void func(const int &&x) {
    cout << "const right value ref" << endl;
}

template<typename T>
void PerfectForward(T &&t) {
    func(std::forward<T>(t));
}

int main()
{
    PerfectForward(10);//右值
    int a;
    PerfectForward(a);//左值
    PerfectForward(std::move(a));//右值
    const int b = 1;
    PerfectForward(b);//const左值
    PerfectForward(std::move(b));//const右值
    return 0;
}

```

运行：

```
right value ref
left value ref
right value ref
const left value ref
const right value ref
```

我们把上面的函数改一下：

```
template<typename T>
void PerfectForward(T &&t) {
    func(t);
}
```

再编译运行，则可以看到都变成了左值了。

```
left value ref
left value ref
left value ref
const left value ref
const left value ref
```







右值引用、完美转发，再加上可变模板参数，可以写一个万能的函数包装器。

```
template <class Function, class... Args>
inline auto FuncWrapper(Function&& f, Args&& ... args) -> decltype(f(std::forward<Args>(args)...))
{
    return f(std::forward<Args>(args)...);
}
void test0(string s)
{
    printf("hello %s\n", s.c_str());
}
int main()
{
    FuncWrapper(test0, "xx");
}

```



参考资料

1、C++11改进我们的程序之move和完美转发

https://www.cnblogs.com/qicosmos/p/3376241.html

2、C++11：完美转发的使用

https://blog.csdn.net/aqtata/article/details/35372769