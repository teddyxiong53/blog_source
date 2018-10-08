---
title: cpp之std之function
date: 2018-09-30 09:52:51
tags:
	- cpp

---



std::function是一种通用的、多态的函数封装。

可以对任何可以调用的目标实体进行store、copy、call等操作。

目标实体包括：

1、普通函数。

2、lambda表达式。

3、函数指针。

4、其他函数对象。

std::function是对c++里现有的可调用实体的一种类型安全的包裹。

（例如函数指针，就是类型不安全的）。

最重要的作用是实现延时调用。



先看例子。

```
#include <functional>
#include <iostream>

using namespace std;
std::function<int(int)> Functional;

//普通函数
int TestFunc(int a)
{
	return a;
}

//lambda表达式
auto lambda = [](int a)->int{return a;};

//仿函数
class Functor {
public:
	int operator()(int a) {
		return a;
	}
};

//1. 类成员函数
//2. 类静态函数
class TestClass {
public:
	int ClassMember(int a) {
		return a;
	}
	static int StaticMember(int a) {
		return a;
	}
};

int main()
{
	Functional = TestFunc;
	int ret = Functional(10);
	std::cout << "normal function:" << ret << std::endl;
	
	Functional = lambda;
	ret = Functional(20);
	std::cout << "lambda: " << ret << std::endl;
	
	Functor testFunctor;
	Functional = testFunctor;
	ret = Functional(30);
	std::cout << "functor: " << ret << std::endl;
	
	TestClass testObj;
	Functional = std::bind(&TestClass::ClassMember, testObj, std::placeholders::_1);
	ret = Functional(40);
	std::cout << "class member: " << ret << std::endl;
	
	Functional = TestClass::StaticMember;
	ret = Functional(50);
	std::cout << "static member: " << ret << std::endl;
	
	return 0;
}
```



# std::bind

bind和function是一起用的，所以放在这里一起讨论。

还是先看例子。

```
#include <functional>
#include <iostream>
using namespace std;
class A {
public:
	void func_3(int k, int m) {
		cout << k << " " << m << endl;
	}
	
};

void func(int x, int y, int z)
{
	cout << x << " " << y << " " << z << endl;
}

void func_2(int &a, int &b)
{
	a++;
	b++;
	cout << a << " " << b << endl;
}

int main()
{
	auto f1 = std::bind(func, 1,2,3);
	f1();//print 1 2 3
	
	auto f2 = std::bind(func, placeholders::_1, placeholders::_2, 3);
	f2(1,2);//print 1 2 3
	
	int n = 2, m =3;
	auto f4 = std::bind(func_2, n, placeholders::_1);
	f4(m); //print 3 4
	cout << "m: " << m << endl;
	cout << "n: " << n << endl;
	
}
```



lambda表达式在绝大多数情况下可以替代bind。



参考资料

1、C++11中的std::function

https://www.cnblogs.com/diegodu/p/6180350.html

2、C++11 中std::function和std::bind的用法

https://blog.csdn.net/liukang325/article/details/53668046

3、std::bind技术内幕

https://www.cnblogs.com/qicosmos/p/3723388.html