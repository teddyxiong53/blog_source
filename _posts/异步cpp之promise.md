---
title: cpp之promise
date: 2018-11-22 16:32:19
tags:
	- cpp

---



promise和future是一起用的。

一起构成了异步编程模型。

它可以让我们摆脱传统的回调陷阱。从而更加优雅地进行异步编程。



promise是一个模板类。

这是相关的3个声明。

```
template <class T>
promise;
template <class R&>
promise<R&>;
template <>
promise<void>; //这个T是void类型
```

promise对象里，保存了类型为T的值。

这个值可以通过future来获取。

我们看一个简单的例子。

```
#include <future>
#include <thread>
#include <functional> //to use std::ref
#include <iostream>

void print_int(std::future<int>& fut)
{
	int x = fut.get();
	std::cout << "value:" << x << std::endl;
}
int main()
{
	std::promise<int> prom;
	std::future<int> fut = prom.get_future();
	std::thread th1(print_int, std::ref(fut));
	prom.set_value(10);
	th1.join();
	return 0;
}
```



# 参考资料

1、现代c++开发利器folly教程系列之：future/promise

https://my.oschina.net/fileoptions/blog/881798

2、Linux下C++ 多线程编程（std::future）

https://www.jianshu.com/p/2b7590946bcb



