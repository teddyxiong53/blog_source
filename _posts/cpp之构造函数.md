---
title: cpp之构造函数
date: 2018-05-13 19:46:42
tags:
	- cpp

---



c++ 的构造函数也不肯老老实实地按常规方式来做。非得弄出一堆花来。吐槽一下。



一个最基本的构造函数。

```
class Test {
public:
	Test(int var) :m_var(var) {

	}
private:
	int m_var;
};
```

为什么要搞这么怪异的语法呢？

这里还真可以展开说一说。

```
#include <iostream>

using namespace std;

class Test {
public:
	Test(int a, int b) {
		m_a = a;
		m_b = b;
	}

	int m_a;
	int m_b;
};
int main(int argc, char const *argv[])
{
	Test t(3, 4);
	cout << "t.a: " << t.m_a << " t.b: " << t.m_b << endl;

	return 0;
}
```

这种情况，成员变量都是普通变量，这种方式和写成冒号的方式没有区别。

但是如果有成员变量是引用类型、const变量这种不能成为左值的时候，就不能这样了，就必须写在冒号后面了。

冒号初始化相当于：

```
int a = 10;
```

而函数里面语句初始化相当于：

```
int a;
a = 10;
```

构造函数执行的步骤：

```
1、传参。
2、给类的成员分配空间。
3、执行冒号初始化。
4、执行大括号里的语句。
```



# 拷贝构造函数

拷贝构造函数的参数只能是引用类型。

这些情况下会调用拷贝构造函数。

```
1、用一个已有对象初始化一个新的对象时。
2、将一个对象以值传递的方式传递给形参的时候。
3、函数返回一个对象时。
```

如果构造函数里不需要malloc这一类的操作，直接用默认的拷贝构造函数就够了。

否则就需要自己重载拷贝构造函数了。



自己写的一个简单例子。

```
#include <iostream>

class Test {
public:
	Test(int a) {
		m_a = a;
		std::cout << "Test Construct\n";
	}
	#if 1
	Test(const Test& t) { //自定义的拷贝构造函数。
		m_a = t.m_a;
		std::cout << "Test Copy Construct\n";
	}
	#else
	Test(Test&) = default;//使用编译器默认的拷贝构造函数。
	#endif
	Test& operator=(Test&) = default;
	int m_a;
};

int main()
{
	Test t1(1);
	Test t2 = t1;
	std::cout << t2.m_a << std::endl;
	
}
```



# 移动构造move

移动构造是c++11新增的特性。

跟拷贝构造类似，也有两种方式，一个是用构造函数，一个是用赋值的方式。

看一个例子。

```
#include <iostream>
using namespace std;

class A {
public:
	int x;
	A(int x): x(x) {
		cout << "construct method" << endl;
	}
	A(A& a): x(a.x) {
		cout << "copy construct method" << endl;
	}
	A& operator= (A& a) {
		x = a.x;
		cout << "copy assignment method" << endl;
		return *this;
	}
	A(A&& a) : x(a.x) {
		cout << "move construct method" << endl;
	}
	A& operator=(A&& a) {
		x = a.x;
		cout << "move assignment method" << endl;
		return *this;
	}

};

A getA() {
	return A(1);
}

A&& moveA() {
	return A(1);
}

int main() {
	cout << "1" <<endl;
	A a(1);//构造函数
	cout << "2" <<endl;
	A b = a;//拷贝构造
	cout << "3" <<endl;
	A c(a);//拷贝构造
	cout << "4" <<endl;
	b = a;//拷贝赋值构造
	cout << "5" <<endl;
	A d = A(1);//构造函数
	cout << "6" <<endl;
	A e = move(a);//移动构造函数
	cout << "7" <<endl;
	A f = getA();//构造函数
	cout << "8" <<endl;
	A&& g = moveA();//构造函数。
	cout << "9" <<endl;
	d = A(1);//移动赋值构造。
	return 0;
}
```



临时变量自动作为右值。这样代码不用改，只需要重新编译，就可以得到性能的提升。



出于安全考虑，有这些限制：

```
1、有名字的变量都是左值，即使它被你强行用T&&声明为右值。
2、为了获得右值必须用std::move来显式地进行转化。
```



# 子类如何调用父类构造函数？

构造方法不能被继承。

所以，在创建子类对象的时候，为了初始化从父类继承来的数据成员，需要调用父类的构造方法。

使用的规则是：

1、如果子类没有定义构造方法，调用父类的无参构造方法。

2、如果子类定义了构造方法，无论子类是无参构造还是有参构造，都是先调用父类的无参构造函数。

3、如果子类调用父类的有参构造方法，则需要用冒号的方式提供参数初始化。（是父类的构造函数要这么写）所以稳妥起见，是所有的初始化参数都这么写。



# 参考资料

1、C++各种构造函数的写法

https://blog.csdn.net/baiyq369/article/details/54926983

2、C++类成员冒号初始化以及构造函数内赋值

https://blog.csdn.net/zj510/article/details/8135556

3、C++调用父类的构造函数规则

https://www.cnblogs.com/bonelee/p/5825885.html

4、拷贝构造函数和移动构造函数

https://www.jianshu.com/p/f5d48a7f5a52