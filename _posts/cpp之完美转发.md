---
title: cpp之完美转发
date: 2019-09-20 13:42:48
tags:
	- cpp

---

1

```
#include <iostream>
#include <memory>
#include <stdio.h>
using namespace std;

template <typename T>
void PrintT(T &t)
{
    cout << "lvaue" << endl;
}

template <typename T>
void PrintT(T &&t)
{
    cout << "rvalue" << endl;
}

template <typename T>
void TestForward(T &&v)
{
    PrintT(v);
    PrintT(std::forward<T>(v));
    PrintT(std::move(v));
}

void Test()
{
    TestForward(1);
    int x = 1;
    TestForward(x);
    TestForward(std::forward<int>(x));
}
int main()
{
    Test();
}

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