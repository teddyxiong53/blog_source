---
title: cpp之operator重载
date: 2018-09-17 17:52:04
tags:
	- cpp

---

operator是c++里的关键字，它和运算符一起使用，表示一个运算符函数。

在理解的时候，应该把`operator=`当成一个整体来理解，看做一个函数名。

这个是cpp扩展运算符功能的方法。



为什么需要操作符重载？

默认情况下，操作符只支持基本数据类型。

对于用户自定义的class，如果想进行比较大小等操作，就需要用户自己来实现。

为什么叫重载？因为系统默认提供了一个默认实现。



怎样声明一个重载的操作符？

类似声明一个普通的成员函数，特别的一点就是包含operator关键字。

例如：

```
class person {
private:
	int age;
public:
	person(int a) {
    	this->age = a;
	}
	bool operator == (const person &p) const;
};
```

实现如下：

```
bool person::operator== (const person &p) const
{
	if(this->age == p.age) {
      	return true;
	}
	return false;
}
```

调用如下：

````
int main()
{
  	person p1(10);
  	person p2(20);
  	if(p1 == p2) {
      	cout << "the age is equal" << endl;
  	}
}
````

理解：

因为== 相当于person这个类里的一个成员函数，所以p1就可以使用这个成员函数，p2相当于这个函数的参数。



#参考资料

1、C++中operator关键字（重载操作符）
https://www.cnblogs.com/wangduo/p/5561922.html
