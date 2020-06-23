---
title: cpp之pimpl模式
date: 2020-06-22 15:13:49
tags:
	- cpp

---

1

pimpl是一个c++的一种写代码的模式。

是指通过一个private pointer，来实现具体实现的隐藏。

看一个例子就很清楚了。

普通的写法：

```
//x.h
class X {
public:
	void func();
private:
	int i;
};

//c.h
#include "x.h"
class C {
public:
	void func();
private:
	X x;//这里就跟X强耦合了。
};
```

使用pimpl模式来改造，如下：

```
//c.h
class X;//替换#include "x.h"
class C {
public:
	void func();
private :
	X *pImpl;
};
```

pimpl带来的好处有：

1、降低模块的耦合。因为隐藏了类的实现，被隐藏的类相当于不可见。对被隐藏类的修改，可以不编译C这个类。

2、接口与实现分离，提高接口的稳定性。



参考资料

1、【C++自我精讲】基础系列六 PIMPL模式

https://www.cnblogs.com/joinclear/p/3908661.html