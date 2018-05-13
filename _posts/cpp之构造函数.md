---
title: cpp之构造函数
date: 2018-05-13 19:46:42
tags:
	- cpp

---



c++ 的构造函数也不肯老老实实地按常规方式来做。非得弄出一堆花来。吐槽一下。



一个最基本的构造函数。

```
class Test {
public:
	Test(int var) :m_var(var) {

	}
private:
	int m_var;
};
```

为什么要搞这么怪异的语法呢？

这里还真可以展开说一说。

```
#include <iostream>

using namespace std;

class Test {
public:
	Test(int a, int b) {
		m_a = a;
		m_b = b;
	}

	int m_a;
	int m_b;
};
int main(int argc, char const *argv[])
{
	Test t(3, 4);
	cout << "t.a: " << t.m_a << " t.b: " << t.m_b << endl;

	return 0;
}
```

这种情况，成员变量都是普通变量，这种方式和写成冒号的方式没有区别。

但是如果有成员变量是引用类型、const变量这种不能成为左值的时候，就不能这样了，就必须写在冒号后面了。







# 参考资料

1、C++各种构造函数的写法

https://blog.csdn.net/baiyq369/article/details/54926983

2、C++类成员冒号初始化以及构造函数内赋值

https://blog.csdn.net/zj510/article/details/8135556