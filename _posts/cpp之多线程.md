---
title: cpp之多线程
date: 2018-10-10 19:33:51
tags:
	- cpp

---



下面讨论的都是c++11版本之后的。

在C语言里，用pthread这个库来做多线程。

而到了c++里，可以在语言层来做多线程了。

好处就是程序的可移植性得到很大的提高。

c++11引入了5个头文件来支持多线程编程

1、atomic。声明了2个类，std::atomic和std::atomic_flag。

2、thread。主要声明了类std::thread类。

3、mutex。

4、condition_variable

5、future。主要声明了std::promise和 std::package_task这2个provider类。以及std::future/std::shared_future这2个future类。



最简单的例子。

```
#include <iostream>
#include <thread>

void t1_func() {
	std::cout << "hello thread" << std::endl;
}
int main()
{
	std::thread t1(t1_func);
	t1.join();
	return 0;
}
```







# 参考资料

1、C++11 并发指南一(C++11 多线程初探)

这个系列文章都不错。

http://www.cnblogs.com/haippy/p/3235560.html



