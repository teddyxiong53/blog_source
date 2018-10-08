---
title: cpp之std之move
date: 2018-09-29 15:25:51
tags:
	- cpp

---



move函数是用来把左值引用转化为右值引用的。

为什么需要move函数？

1、提高性能。

2、避免不必要的拷贝。

作用是把对象的所有权从一个对象转移到另一个对象。

只是转移，没有内存拷贝过程。



一个简单的例子。

```
int main()
{
	std::string str = "hello";
	std::vector<std::string> v ;
	v.push_back(str);
	std::cout << "after copy, str is \"" << str << "\"\n";
	v.push_back(std::move(str));
	std::cout << "after move, str is \"" << str << "\"\n";
	std::cout << "the content of v is :" << std::endl;
	std::cout << "v[0]" << v[0] << "\n";
	std::cout << "v[1]" << v[1] << "\n";
}
```



# 左值和右值概念

左值是可以放在=左边的东西。左值必须在内存中有实体。

右值是放在=右边的东西，右值可以在内存里，也可以在cpu寄存器里。

一个对象被用作右值时，使用的是它的内容。

一个对象被用作左值时，用的是它的地址。



# 引用

引用是c++语法做的优化，引用的本质还是靠指针来实现的。

引用的基本原则：

1、定义引用的时候，必须初始化，不能改变引用。

2、对引用的一切操作，都相当于对原对象的操作。



# 左值引用和右值引用

左值引用

```
type &引用名= 左值表达式
```

右值引用

```
type &&引用名= 右值表达式
```



参考资料

1、C++11右值引用和std::move语句实例解析

https://www.cnblogs.com/ldlchina/p/6608154.html

2、c++11 std::move() 的使用

https://www.cnblogs.com/SZxiaochun/p/8017349.html