---
title: cpp11之可变参数模板
date: 2020-10-13 13:57:30
tags:
	- cpp
---

1

C++11新增的最强大的特性之一，它对参数进行了高度泛化，它能表示0到任意个数、任意类型的参数。

在C++11之前，类模板和函数模板只能有固定数量的模板参数。

可变参数模板和普通模板的语义是一样的，只是写法上稍有区别，声明可变参数模板时需要在typename或class后面带上省略号“…”

```
template<class ... T> void func(T ... args)//T叫模板参数包，args叫函数参数包
{//可变参数模板函数

}
```

省略号“…”的作用有两个：

- 声明一个参数包，这个参数包中可以包含0到任意个模板参数
- 在模板定义的右边，可以将参数包展开成一个一个独立的参数



模板参数包

```
template<typename... A> class Car;  
```

```
//typename...就表示一个模板参数包。可以这么来实例化模板：
Car<int, char> car; 
```

包扩展

```
template<typename... a> class Car{};
template<typename... A> class BMW: public Car<A...>{};
BMW<int, char> car;
//A...就叫做包扩展（pack extension）。
//包扩展是可以传递的。
```

特性

```
template <class... T>
void f(T... args)
{
	cout << sizeof...(args) << endl;
}
f();//打印0，0个参数。
f(1,2);//打印2
f(1,2.5,"");//打印3
```



下面分可变参数模板函数和可变参数模板类这2类来讲解。

# 可变参数模板函数

可变参数模板函数的定义如下：

```
#include <iostream>
using namespace std;

template<typename... T>
void func(T... args)
{
    cout << "num=" << sizeof...(args) << endl;
}
int main(int argc, char const *argv[])
{
    func();
    func(1);
    func(1,2);
    return 0;
}
```

## 函数包的展开

### 递归方式展开

需要提供一个参数包展开函数和一个递归终止函数。

```
#include <iostream>
using namespace std;

//递归终止函数
void debug()
{
    cout << "empty\n";
}
//展开函数
template<class T, class... Args>
void debug(T first, Args... last)
{
    cout << "param: " << first << endl;
    debug(last...);
}
int main(int argc, char const *argv[])
{
    debug(1,2,3);
    return 0;
}
```

### 非递归方式展开

```
#include <iostream>
using namespace std;

template <class T>
void print(T arg)
{
    cout << arg << endl;
}

template <class... Args>
void expand(Args... args)
{
    int a[] = {(print(args), 0)...};
}

int main(int argc, char const *argv[])
{
    expand(1,2,3);
    return 0;
}
```

expand函数的逗号表达式：(print(args), 0)， 也是按照这个执行顺序，先执行print(args)，再得到逗号表达式的结果0。

同时，通过初始化列表来初始化一个变长数组，{ (print(args), 0)… }将会展开成( (print(args1), 0), (print(args2), 0), (print(args3), 0), etc…), 最终会创建一个元素只都为0的数组int a[sizeof…(args)]。

# 可变参数模板类

## 继承的方式来展开参数包

可变参数模板类的展开，一般需要定义2到3个类。

包括：类声明和特化的模板类。

```
#include <iostream>
#include <typeinfo>

using namespace std;

template<typename... A>
class BMW {};//变长模板的声明

template<typename Head, typename... Tail> //递归的偏特化定义
class BMW<Head, Tail...> : public BMW<Tail...>
{
    //当实例化对象的时候，会引起基类的递归构造。
public:
    BMW() {
        printf("type:%s\n", typeid(Head).name());
    }
    Head head;
};

template<>
class BMW<>{};//边界条件

int main(int argc, char const *argv[])
{
    BMW<int, char, float> car;
    
    return 0;
}
```

输出是这样：

```
type:f
type:c
type:i
```

## 模板递归和特化方式展开参数包

```
#include <iostream>
#include <typeinfo>

using namespace std;

template<long... nums>
struct Multiply;//变长模板的声明

template<long first, long... last>
struct Multiply<first, last...>
{
    static const long val = first * Multiply<last...>::val;
};
template<>
struct Multiply<> //边界条件
{
    static const long val = 1;
};
int main(int argc, char const *argv[])
{
    cout << Multiply<2,3,4>::val << endl;
    return 0;
}
```



参考资料

1、可变参数模板(C++11)

https://blog.csdn.net/tony__lin/article/details/84677316

2、C++11：可变参数的模板

https://blog.csdn.net/tennysonsky/article/details/77389891