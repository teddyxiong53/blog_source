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

**默认情况下，操作符只支持基本数据类型。**

对于用户自定义的class，如果想进行比较大小等操作，就需要用户自己来实现。

**为什么叫重载？因为系统默认提供了一个默认实现。**



怎样声明一个重载的操作符？

**类似声明一个普通的成员函数，特别的一点就是包含operator关键字。**

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



# 可以重载的运算符

1、双目算术运算符。5个。

```
+ - * / %
```

2、关系运算符。6个。

```
> < >= <= == !=
```

3、逻辑运算符。3个。

```
&& || !
```

4、单目运算符。4个。

```
+(正) -(负) *(指针) &(取地址)
```

5、自增自减。2个。

```
++ --
```

6、位运算符。6个。

```
| & ~ ^ << >>
```

7、赋值运算符。11个。

```
=
+=
-=
*=
/=
%=
&=
|=
^=
<<=
>>=
```

8、空间申请释放。

```
new
delete
new[]
delete[]
```

9、其他。

```
() 函数调用。
-> 成员访问。
,  逗号。
[] 下标
```



# 不可重载的运算符

```
. 
.*
->*
::
sizeof
?:
#
```



# 单目运算符重载举例

```
#include <iostream>
using namespace std;

class Distance {
private:
	int feet;
	int inches;
public:
	Distance() {
		feet = 0;
		inches = 0;
	}
	Distance(int f, int i) {
		feet = f;
		inches = i;
	}
	void displayDistance() {
		cout << "F: " << feet << " I: " << inches << endl;
	}

	Distance operator- () {
		feet = -feet;
		inches = -inches;
		return Distance(feet, inches);
	}
};


int main(int argc, char const *argv[])
{
	Distance D1(11,10), D2(-5, 11);
	-D1;
	D1.displayDistance();
	-D2;
	D2.displayDistance();
	return 0;
}
```





有这么几点是我之前没有认识到的。

1、不等于是对等于的调用。只是把结果取反一下而已。

2、要用对象来调用，所以this是一个指针，要进行指针取值操作。



# new操作符的重载

```
A a = new A;
```

上面这一行语句，实际的执行步骤有：

1、分配内存。

2、调用A()构造函数。

分配内存的操作是靠operator new(size_t)来完成的。

类A可以选择自己是否对new这个操作符进行重载。

如果要重载，这样写：

```
void* operator new(size_t size) {
    //...
}
```

不过一般我们都是不重载的，那么就是调用全局的new。

```
::operator new(size_t)
```

全局的new，由C++运行时默认提供。



c++里的new有两种，一个是关键字new，一个是操作符new。

关键字new的行为就是 ：先调用操作符new分配内存，然后调用构造函数初始化对象。

关键字new不存在重载的概念。



在c++里，类的对象有两种建立方式。

1、静态方式。例如A a。

2、动态方式。A a = new A

可以通过一些方式，来限制只能建立静态的对象或者动态的对象。

要让类只能建立动态对象，可以通过把析构函数设置为protected来做。

因为栈上的对象，出了作用范围就要自动调用析构函数。但是我们把析构函数没有对外暴露。这样编译器就会报错的。

但是我们的动态对象，也没法析构了。这就需要另外定义一个destroy函数来帮助我们进行析构操作。

但是new来产生对象，却用destroy来释放对象，挺奇怪的。

我们可以做一下对称封装，如下。

```
class A {
protected:
	A();
	~A();
public:
	static A* create() {
        return new A();
	}
	void destroy() {
        delete this;
	}
	
};
```

如果要限制为只允许在栈上建立对象呢？

重载操作符new为私有的就可以了。

重载了操作符new，就需要同时把delete也重载了。

```
class A{
private:
	void* operator new(size_t size) {}
	void operator delete(void *ptr){}
public:
	A();
	~A();
};
```



# 全局operator重载

什么时候需要全局operator重载？

1、没有必须这样做的理由。

2、如果有一个操作数是类 类型的，例如string类这样的。那么对于对称操作符（例如==），最好定义为全局的。





#参考资料

1、C++中operator关键字（重载操作符）
https://www.cnblogs.com/wangduo/p/5561922.html

2、C++ 重载运算符和重载函数

http://www.runoob.com/cplusplus/cpp-overloading.html

3、C++ 内存分配(new，operator new)详解

<https://www.cnblogs.com/raichen/p/5808766.html>