---
title: cpp之override和overload
date: 2020-06-09 13:40:08
tags:
	- cpp

---

1

cpp里的类层次里的同名函数，有三种关系

1、重载。overload。

2、重写。override。

3、隐藏。oversee。



# overload

特点：

1、在相同的作用范围内容。例如，同一个类里面。

2、函数名相同，参数不同。返回值没有关系。

3、virtual关键字可有可无。

```
class A
{
	void func(int x);//这2个函数就是overload的关系。
	void func(int x, int y);
}
```

# override

特点：

1、在子类里有跟父类同名的函数。

2、在基类里，对应的函数前面必须用virtual修饰。

# oversee

就是基类里同名函数没有用virtual修饰。

而子类里有完全同名的函数，则子类里的函数oversee了基类里的对应函数。





参考资料

1、C++ 类成员函数的重载(overload)，重写/覆盖(override)，隐藏

https://blog.csdn.net/qq_26437925/article/details/54933326