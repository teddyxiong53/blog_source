---
title: cpp之虚函数
date: 2018-05-10 16:32:27
tags:
	- cpp

---



要讨论虚函数，我们还是要从面向对象的三大特性谈起。

首先看多态。什么是多态？多态就是：

1、一个对象，收到不同消息有不同表现。

2、不同对象，收到相同消息有不同表现。

多态分为两种：

1、静态多态。也叫早绑定。

2、动态多态。也叫迟绑定。

我们还是通过实际的例子来看这个的具体含义。

```
class Rect {//早绑定。
public:
	int calcArea(int w);
	int calcArea(int w, int h);
};
int main(int argc, char const *argv[])
{
	Rect rect;
	rect.calcArea(2);
	rect.calcArea(2,3);
	return 0;
}
```

上面的代码，函数名字一样，参数不同，一看就是互为重载的2个函数。

这样的调用情况，在编译的时候，就已经确定了，所以叫早绑定。

我们再看迟绑定是怎么样的。

```
#include <iostream>
using namespace std;

class Shape {
public:
	double calcArea() {
		cout << "calc area " <<endl;
		return 0;
	}

};

class Circle:public Shape {
public:
	Circle(double r) {
		m_r = r;
	}
	double calcArea();
private:
	double m_r;
};

double Circle::calcArea()
{
	return  3.14*m_r*m_r;
}

class Rect: public Shape {
public:
	Rect(double w, double h) {
		m_w = w;
		m_h = h;
	}
	double calcArea() ;
private:
	double m_w;
	double m_h;
};

double Rect::calcArea()
{
	return m_w*m_h;
}


int main(int argc, char const *argv[])
{
	Shape *shape1 = new Circle(4.0);
	Shape *shape2 = new Rect(3.0, 4.0);
	shape1->calcArea();
	shape2->calcArea();
	return 0;
}
```

上面代码的运行结果是这样：

```
teddy@teddy-ubuntu:~/work/test/cpp$ ./a.out      
calc area 
calc area 
```

不符合我们的预期。

所以要实现迟绑定，就需要引入虚函数的概念了。

我们对上面的代码做这样的修改 ：

```
在所有的calcArea函数声明的地方签名加上virtual关键字。
```

这样就可以看到预期的效果了。



多态中存在的问题

可能会内存泄漏。

因为这个，所以需要引入虚析构函数。



#virtual关键字在函数中的使用限制

1、普通函数不能是虚函数。就是说，必须是类的成员函数。否则编译报错。

2、static和virtual不能同时修饰同一个函数。

3、inline函数也不能是virtual的。

4、构造函数不能是virtual的。



# 虚函数实现原理

首先，弄清楚，什么是函数指针。

指针可以指向对象，也可以指向函数。

函数的本质就是一段二进制代码。



多态的实现原理。

首先，有个虚函数表指针。这个是隐含在class里的。就是靠这个来找到对应的函数的。



# 纯虚函数

看例子。

```
class Shape {
public:
	virtual double calcArea() {

	}
	virtual double calcPerimeter()=0;//纯虚函数。
};
```

可以看到纯虚函数的特点：

1、后面加上“=0“。只能写成这个。

2、没有函数体。

含有纯虚函数的类叫做抽象类。

如果一个类里面只有纯虚函数，这个类就叫接口类。



纯虚函数是一种特殊的虚函数。

就是基类里赋值为=0 。不实现，要求子类必须实现。就这么回事。



虚函数，不是=0，而是有一个函数实现的。只是加了virtual进行修饰。

既然普通虚函数，也有函数实现，那么虚函数，跟普通的成员函数区别何在呢？



虚函数是c++的精髓。这句话怎么理解？

虚函数是c++实现多态的基础。

所谓多态，在代码上是这样的样子。

```
class Base {
    virtual void func1() {
        printf("base");
    }
}
class Derived : public Base {
    virtual void func1() {
        printf("derived");
    }
}
Base *p = new Derived();
p->func1();//得到的是derived。
```

而不是virtual的函数，p调用，则是调用的base里的。





# 参考资料

1、c++ 深入理解虚函数

https://www.cnblogs.com/jin521/p/5602190.html

2、在c++中，类的成员函数直接写成virtual bool good()=0；求大神解释一下后面

https://zhidao.baidu.com/question/1540827235101011667.html

3、虚函数和纯虚函数的区别

https://blog.csdn.net/Hackbuteer1/article/details/7558868

4、纯虚函数

https://baike.baidu.com/item/%E7%BA%AF%E8%99%9A%E5%87%BD%E6%95%B0

5、虚函数

https://baike.baidu.com/item/%E8%99%9A%E5%87%BD%E6%95%B0

6、虚函数与普通成员函数的区别

https://blog.csdn.net/zxc024000/article/details/78784297

7、C++虚函数表分析

https://www.cnblogs.com/hushpa/p/5707475.html