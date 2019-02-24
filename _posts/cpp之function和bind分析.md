---
title: cpp之function和bind分析
date: 2019-02-23 14:34:17
tags:
	- cpp

---



关于std::function的用法，可以理解为函数指针。

保存自由函数。

```
void printA(int a) {
	std::cout << a << std::endl;
}


int main()
{
	std::function<void(int a)> func;
	func = printA;
	func(1);
}
```

保存lambda表达式。

```
std::function<void()> func = []() {std::cout << "save lambda func\n";};
func();
```

简单的写法，可以用auto来做。

```
auto func = []() {std::cout << "save lambda func\n";};
func();
```



参考资料

1、C++11 中std::function和std::bind的用法

https://blog.csdn.net/liukang325/article/details/53668046

2、应该用bind+function取代虚函数吗？

https://www.cnblogs.com/qicosmos/p/4527804.html

3、以boost::function和boost:bind取代虚函数

https://blog.csdn.net/Solstice/article/details/3066268