---
title: cpp之std thread常用函数
date: 2018-10-13 10:58:51
tags:
	- cpp
---

1

主要函数：

```
joinable
get_id
	返回值是std::thread::id 。
	是一个class。
native_handle
	这个是拿到C语言的句柄。

join
detach
```

简单例子。

```

class A {
public:
	std::thread m_thread;
	int m_a;
	//A();
	void threadProc();
	void init();
};
void A::threadProc() {
	int count = 0;
	std::cout << "this ptr:" << this << std::endl;
	std::cout << "m_a:" << m_a << std::endl;
	while(count++<3) {
		std::cout << "11" << std::endl;
		sleep(2);
	}
}
void A::init() {
	m_a = 0x55;
	m_thread = std::thread(&A::threadProc, this);
}

int main()
{
	A a;
	std::cout << "before init thread id:" << a.m_thread.get_id() << std::endl;

	a.init();
	std::cout << "after init thread id:" << a.m_thread.get_id() << std::endl;
	if(a.m_thread.joinable()) {
		std::cout << "before join" << std::endl;

		a.m_thread.join();
	}
	std::cout << "end of code\n" ;
}
```




参考资料

1、

https://zh.cppreference.com/w/cpp/thread/thread