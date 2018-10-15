---
title: cpp之mutex和condition
date: 2018-10-10 19:30:51
tags:
	- cpp

---



自己写的一个简单例子。

```
#include <iostream>
#include <thread>
#include <chrono>
#include <condition_variable>
#include <mutex>
#include <unistd.h>

std::mutex mtx;
std::condition_variable cv;

void producer()
{
	std::cout << "begin produer\n";
	usleep(1000*2000);
	cv.notify_one();
	std::cout << "end producer\n";
}
void consumer()
{
	std::cout << "begin consumer\n";
	std::unique_lock<std::mutex> lock(mtx);
	cv.wait(lock, [] {
		std::cout << "consumer get condition\n";
		return true;
	});
	std::cout << "end consumer\n";
}
int main ()
{
	std::thread t_producer(producer);
	std::thread t_consumer(consumer);
	t_producer.detach();
	t_consumer.detach();

	std::this_thread::sleep_for(std::chrono::seconds(10));
}
```

需要注意的有：

1、不需要专门初始化。应该构造函数干了这个活。

2、notify不要lock，wait要lock。



# 参考资料

1、

https://www.cnblogs.com/haippy/p/3252041.html



