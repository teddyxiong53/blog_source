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



# 拷贝构造函数

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