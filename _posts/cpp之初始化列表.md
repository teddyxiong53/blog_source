---
title: cpp之初始化列表
date: 2019-02-22 14:31:51
tags:
	- cpp
---





我这里说的初始化列表，不是构造函数的冒号初始化。

而是initializer_list。

是c++11新引入的特性。

以前，我们这样给vector赋值。

```
std::vector v;
v.push_back(1);
v.push_back(2);
v.push_back(3);
```

是不是很繁琐？

c++11里，你可以这样了：

```
std::vector v = {1, 2,3 };
```

这个就是initializer_list。

我们可以这样自己实现类。

```
#include <iostream>
#include <vector>

class MyNumber {
public:
	MyNumber(const std::initializer_list<int> &v) {
		for(auto i : v) {
			mVec.push_back(i);
		}
	}

private:
	std::vector<int> mVec;
};

int main()
{
	MyNumber num = {1, 2, 3};
}
```



再看一个例子。

```
class CompareClass {
public:
	CompareClass(int, int);
	CompareClass(std::initializer_list<int>);
};

int main() {
	CompareClass foo(1,2);
	CompareClass bar{1,2};//这就是为什么有的时候构造函数后面跟的是大括号了。
}
```



参考资料

1、c++11特性之initializer_list

https://blog.csdn.net/wangshubo1989/article/details/49622871