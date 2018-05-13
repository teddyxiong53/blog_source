---
title: cpp之线程
date: 2018-05-13 20:30:20
tags:
	- cpp

---



先看一个简单例子。

```
#include <iostream>
#include <thread>
using namespace std;

void t1() 
{
	for(int i=0; i<20; i++) {
		cout << "1111" << endl;
	}
}
void t2() 
{
	for(int i=0; i<20; i++) {
		cout << "2222" << endl;
	}
}


int main(int argc, char const *argv[])
{
	thread th1(t1);
	thread th2(t2);

	cout << "main thread" << endl;
	return 0;
}
```

编译运行。

```
teddy@teddy-ubuntu:~/work/test/cpp$ g++ test.cpp -lpthread
teddy@teddy-ubuntu:~/work/test/cpp$ ./a.out 
main thread
terminate called without an active exception
1111
1111
1111
1111
1111
1111
1111
1111
1111
1111
1111
1111
Aborted (core dumped)
```

可以看到，挂了。

原则是，main线程没有等待t1和t2的完成。

我们在main里加上这两行就好了。

```
	th1.join();
	th2.join();
```



# 参考资料

1、C++:线程(std::thread)

https://www.cnblogs.com/whlook/p/6573659.html

