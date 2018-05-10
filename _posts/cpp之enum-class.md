---
title: cpp之enum class
date: 2018-05-10 17:23:46
tags:
	- cpp

---



# 老版本enum存在的问题

1、整型提升问题。

2、无法指定底层所使用的数据类型。

3、enum的作用域。

4、不同编译器处理该问题的方法不统一。



现在我们看看分别如何应对这4个问题。

1、整型提升问题。

在c++11还没有出来的时候，可以选择把enum封装到class内部。

这样可以抵抗整型提升。这种方式导致寄存器变量无法被放进寄存器当中，会影响效率。

2、无法指定底层使用的数据类型。

这个导致struct的对齐的麻烦。

enum在不同的编译器上表现各不相同。

3、enum的作用域。

enum的作用域不受大括号的限制。

我们有时候觉得这个很方便，但是这个就是问题所在。

解决办法是在namespace里定义。

4、不同编译器处理不同。

这个enum就影响了程序的可移植性。



# 关于enum class和enum struct

enum class等价于enum struct。

所以下面就只讨论enum class。

相比于enum，enum class的优点：

1、更好的类型安全

2、有类似封装的特性。

```
enum class color {
  read,
  green
};
```

enum class不会跟int进行隐式类型转换，但是可以强转。

```
enum class color {red, green, blue};
int main()
{
  int x(static_cast<int>(color::red));//enum to int
  color c(static_cast<color>(1));//int to enum 
}
```



```
enum class color {
	red,
	green,
	blue
};


int main(int argc, char const *argv[])
{
	cout << "sizeof(enum class):" << sizeof(color) << endl;
	return 0;
}
```

sizeof(enum class)是4 。



# 参考资料

1、C++11的enum class & enum struct和enum

https://www.cnblogs.com/diegodu/p/6169808.html