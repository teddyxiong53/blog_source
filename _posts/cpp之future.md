---
title: cpp之future
date: 2018-10-08 17:52:17
tags:
	- cpp

---



std::future是c++11新增的特性。

简单来说，future可以用来获取异步任务的结果。因此可以把它当成一种简单的线程间同步的手段。

future通常由某个provider提供，你可以把provider想象成一个异步任务的提供者。

provider可以是函数或者类，有三种可能：

1、std::async函数。

2、std::promise::get_future函数。

3、std::packaged_task::get_future函数。



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



# 参考资料

1、C++并发编程之std::future

http://www.cnblogs.com/zhanghu52030/p/9522287.html