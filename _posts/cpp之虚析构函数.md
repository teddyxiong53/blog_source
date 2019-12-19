---
title: cpp之虚析构函数
date: 2019-02-22 13:21:51
tags:
	- cpp
---





为什么基类里的析构函数要声明为虚析构函数？

用对象指针来调用一个函数，有两种情况：

```
1、如果函数是虚函数，就会调用子类里的版本。
2、如果不是虚函数，就调用指针类型的对象的实现版本。
```

析构函数也遵循这个原则。

**如果我们删除一个指向Derived对象的Base指针，而Base类的析构函数又不是virtual的话，就调用了Base的析构函数，导致Derived的析构没有被调用到，这样就造成了资源泄露。**

举例如下：

```
#include <iostream>

class Base {
public:
	Base() {
		std::cout << "Base construct" << std::endl;
	}
	~Base() {
		std::cout << "Base destruct" << std::endl;
	}
};

class Derived : public Base {
public:
	Derived() {
		std::cout << "Derived construct " << std::endl;
	}
	~Derived() {
		std::cout << "Derived destruct" << std::endl;
	}
};

int main()
{
	Base *p = new Derived();
	delete p;
	return 0;
}
```

输出如下：

```
Base construct
Derived construct 
Base destruct
```

可见，没有调用Derived的析构函数。

只要把Base的析构函数改成这样：

```
virtual ~Base() {
		std::cout << "Base destruct" << std::endl;
	}
```

就可以了。

```
Base construct
Derived construct 
Derived destruct
Base destruct
```

为什么c++默认的析构函数不设置为虚函数呢？

因为虚函数需要额外的虚函数表和虚表指针。这样占用额外的空间。

一个类，如果不会称为父类，那么是没有必要浪费这个空间的。



参考资料

1、

https://www.nowcoder.com/tutorial/93/8f38bec08f974de192275e5366d8ae24