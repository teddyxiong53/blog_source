---
title: cpp之future
date: 2018-10-08 17:52:17
tags:
	- cpp

---



std::future是c++11新增的特性。

简单来说，**future可以用来获取异步任务的结果**。因此可以把它当成一种**简单的线程间同步的手段**。

**future通常由某个provider提供**，你可以把provider想象成一个异步任务的提供者。

provider可以是函数或者类，有三种可能：

1、std::async函数。

2、std::promise::get_future函数。

3、std::packaged_task::get_future函数。

future头文件内容：

```
类：
	future
	future_error
	packaged_task
	promise
	shared_future
函数
	async
	future_category
```

future提供了一种访问异步操作结果的方式。

从字面上看，它代表了未来，一般异步操作我们不能马上得到结果，只能在为了某个时间得到。

我们可以用同步查询等待的方式来获取。

这个是通过查询future_status来做。

future_status有3种情况：

```
deferred
	异步操作还没有开始。
ready
	异步操作已经完成。
timeout
	异步操作已经超时。
```

获取future结果的方式有3种。

```
get
	等待异步操作结束并返回结果。
wait
	只是等待结束，没有返回结果。
wait_for
	参数是一个时间值，等待超时。
```



一个简单例子。

```
#include <iostream>
#include <future>
#include <chrono>

bool is_prime(int x)
{
	for(int i=2; i<x; i++) {
		if(x%i == 0) {
			return false;
		}
	}
	return true;
}

int main()
{
	std::future<bool> f = std::async(is_prime, 4444444444443);
	std::cout<< "checking, please wait" << "\n";
	std::chrono::milliseconds span(10);
	while(f.wait_for(span) == std::future_status::timeout) {
		std::cout << ".";
	}
	bool x = f.get();
	std::cout << "is prime: " << x << "\n";
	return 0;
}
```

另外一个简单例子。

```
#include <functional>//std::ref
#include <future>
#include <stdio.h>
#include <unistd.h>

void thread_proc(std::future<int>& fut)
{
    printf("thread begin\n");
    int val = fut.get();
    printf("get value:%d\n",val);
    printf("thread end\n");
}

int main()
{
    std::promise<int> prom;
    std::future<int> fut = prom.get_future();
    std::thread t1 = std::thread(thread_proc, std::ref(fut));
    printf("before set value\n");
    prom.set_value(10);
    sleep(1);
    printf("after set value\n");
    t1.join();
    return 0;
}
```

`std::promise<void>`泛型也可以是void的，这样prom.set_value()就好了，不用带参数。



# 参考资料

1、C++并发编程之std::future

http://www.cnblogs.com/zhanghu52030/p/9522287.html

2、C++11 多线程 future/promise简介

https://blog.csdn.net/jiange_zh/article/details/51602938