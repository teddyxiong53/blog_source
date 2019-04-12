---
title: cpp之右值引用
date: 2019-04-12 16:31:30
tags:
	- cpp

---



c++11引入了右值引用和move语义。

可以避免不必要的复制，提高了程序性能。

相应的，c++11容器增加了一些右值版本的插入函数。

讨论之前，我们先看看，什么是左值和右值。

```
左值
表达式结束后，依然存在的持久对象。

右值
表达式结束后，就不存在了的临时对象。
```

一个简单的区分方法就是，看看能不能对表达式取地址，如果能，就是左值，如果不能，就是右值。

在c++11里，右值由2个概念组成；

```
1、将亡值。
	xvalue。
	expiring value
	c++11新增的，与右值引用相关的表达式。
	将要被move的对象。
	T&&函数返回值。
	std::move返回值
2、纯右值。
	prvalue
	PureRight Value
	非引用返回的临时变量。
	运算表达式产生的临时变量。
	原始字面量。
	lambda表达式。
```



右值不具名，所以我们只能通过引用的方式找到它。



```
#include <iostream>
using namespace std;

int g_constructCount = 0;
int g_copyConstructCount = 0;
int g_destructCount = 0;

struct A {
    A() {
        cout << "construct: " << ++g_constructCount << endl;
    }
    ~A() {
        cout << "destruct: " << ++g_destructCount << endl;
    }
    A(const A& a) {
        cout << "copy construct: " << ++g_copyConstructCount << endl;
    }

};
A getA() {
    return A();
}
int main()
{
    A a = getA();
    return 0;
}
```

编译的时候，加上这个选项：

```
-fno-elide-constructors
```

运行效果：

```
construct: 1 这个是getA()里面的构造函数。
copy construct: 1 
destruct: 1
copy construct: 2 
destruct: 2
destruct: 3
```

可以看到，拷贝构造函数执行了2次。

一次是：getA函数内部创建的对象返回后，构造一个临时对象产生的。

一次是：main函数里构造a对象时产生的。

如果我们使用右值引用，则效果是这样：

```
A&& a = getA();
```

```
construct: 1
copy construct: 1
destruct: 1
destruct: 2
```

只执行了一次拷贝构造。

原因在于右值引用绑定了右值，让临时右值的生命周期延长了。

我们可以利用这个特性做一些性能优化。



实际上，T&&并不一定是右值，它绑定的类型的未定的。也叫通用引用。

```
template <typename T>
void f(T&& param) ;

f(10);//传递右值
int x = 10;
f(x);//传递左值
```

只有在发送自动类型推导时，&&才是一个通用引用。



std::move可以把一个左值转化成右值。



用移动构造避免深拷贝。



参考资料

1、《深入应用c++11》



