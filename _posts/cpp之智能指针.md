---
title: cpp之智能指针
date: 2018-05-09 17:52:35
tags:
	- cpp

---





智能指针是面试官爱问的，也是实际开发中很实用的东西。



为什么要引入智能指针呢？

我们先看一段示例代码。

```
void func(string &str) 
{
  string *ps = new string(str);
  if(xxx) {
    throw exception();
  }
  str = *ps;
  delete ps;
}
```

上面这段代码有问题，就是在xxx满足的情况下，没有释放ps的内存。这就导致了内存泄漏。

而在开发过程中，这种情况难以完全避免。

如果有一种机制，在func退出的时候，可以帮我们自动释放分配的内存，该有多好。

正是出于这样的需求，c++引入了智能指针的概念。

我们用auto_ptr来改造上面的代码。

```
void func(string &str)
{
  std::auto_ptr<string> ps (new string(str));
  if(xxx) {
    throw exception();
  }
  str = *ps;
  
}
```

这样，我们就不需要去关心内存的释放问题了。



有了智能指针，我们就可以认为c++也有了内存回收了。不用再担心内存泄露问题。

delete这个关键字可以不再去用了。



用java的写法来写智能指针的就对了。

不用考虑释放内存的事情了。



# 智能指针分类

STL给我们提供了四种智能指针：

1、auto_ptr。C++98提供的方案，c++11已经抛弃了。但是还是很多地方用到。

2、unique_ptr。

3、shared_ptr。引用计数型的智能指针。当引用计数变为0的时候才销毁。

4、weak_ptr。也是引用计数型的，但是不增加对象的引用次数。



为什么要抛弃auto_ptr。

我们还是先看一段代码。

```
auto_ptr<string> ps (new string("hello"));
auto_ptr<string> ps2;
ps2 = ps;
```

上面的语句将会完成上面工作呢？

如果ps和ps2是常规指针。则2个指针指向了同一个string对象。

这个是不能接受的。因为程序将会试图释放两次。

要避免这种情况出现，有这些手段：

1、定义赋值运算符。使得赋值时进行深拷贝。这样的缺点是浪费空间。智能指针没有采用这种方式。

2、建立所有权（ownership）概念。对于特定的对象，只能有一个智能指针可以拥有。这就是auto_ptr和unique_ptr使用的策略。

3、创建更加智能的指针。跟踪对象的引用计数。这就是shared_ptr采用的策略。

要抛弃auto_ptr，是因为存在潜在的内存崩溃的问题。



所以，常用的智能指针就剩下unique_ptr和shared_ptr了。



unique_ptr为什么优于auto_ptr呢？



如何选择智能指针呢？

有这些原则可以参考。

1、如果程序要使用多个指向同一个对象的指针，用shared_ptr。

```
常见的场景是这些：
1、有一个指针数组。另外有一些辅助指针来标定特定的元素，例如最大元素和最小元素。
2、2个对象都包含指向第三个对象的指针。
3、STL容器包含指针。
```



# 例子学习

下面是我自己写的例子。

```
#include <iostream>
#include <memory>

class Test {
public:
	Test(int a) {
		m_a = a;
		std::cout << "Test Construct\n";
	}
	virtual ~Test() = default;
	Test(const Test& t) {
		m_a = t.m_a;
		std::cout << "Test Copy Construct\n";
	}
	Test& operator=(Test&) = default;
	int m_a;
};

class TestChild : public Test {
	
};

int main()
{
	std::shared_ptr<Test> t1(new Test(1));//这种是对的。
	//std::shared_ptr<Test> t1 = new Test(1);//这种会编译错误。
	std::cout << "m_a: " << t1->m_a << std::endl;
	
}
```



```
auto t1 = std::make_shared<Test>(1);
或者
auto t1 = std::shared_ptr<Test>(new Test(1));
```



# weak_ptr和shared_ptr区别

weak_ptr是为了解决shared_ptr在某些场景下存在的问题而出现的。

2个类之间，指针进行互相引用。

```
#include <iostream>
#include <memory>

class B;
class A {
public:
	~A() {
		std::cout << "A destruct\n";
	}
	std::shared_ptr<B> m_pB;
};

class B {
public:
	~B() {
		std::cout << "B destruct\n";

	}
	std::shared_ptr<A> m_pA;
};

int main()
{
	std::shared_ptr<A> pA(new A);
	std::shared_ptr<B> pB(new B);
	std::cout << "pA use count: " << pA.use_count() << std::endl;
	std::cout << "pB use count: " << pB.use_count() << std::endl;
}
```

上面的的例子，可以正常调用到析构函数。

我们把测试程序改一下。

```
int main()
{
	std::shared_ptr<A> pA(new A);
	std::shared_ptr<B> pB(new B);
	std::cout << "pA use count: " << pA.use_count() << std::endl;
	std::cout << "pB use count: " << pB.use_count() << std::endl;
	pA->m_pB = pB;
	std::cout << "pA use count: " << pA.use_count() << std::endl;
	std::cout << "pB use count: " << pB.use_count() << std::endl;
	pB->m_pA = pA;
	std::cout << "pA use count: " << pA.use_count() << std::endl;
	std::cout << "pB use count: " << pB.use_count() << std::endl;
}
```

```
pA use count: 1
pB use count: 1
pA use count: 1
pB use count: 2
pA use count: 2
pB use count: 2
```

如果用weak_ptr，就可以解决这种问题。

只需把class B的改成weak_ptr的就可以打破这种循环。

```
class B {
public:
	~B() {
		std::cout << "B destruct\n";

	}
	std::weak_ptr<A> m_pA;//改这一行就可以了。
};
```



```
pA use count: 1
pB use count: 1
pA use count: 1
pB use count: 2
pA use count: 1
pB use count: 2
A destruct
B destruct
```



# 智能指针跟裸指针相互转化

普通指针转化成智能智能：

```
int *iPtr = new int(42);
shared_ptr<int> p(iPtr);
```

智能指针转普通指针。

```
int *pI = p.get();
```



# make_shared和shared_ptr区别

```
class A;
std::shared_ptr<A> p1 = std::make_shared<A>();
std::shared_ptr<A> p2 = std::shared_ptr(new A);
```

p1和p2的这2种定义方式，区别何在？

make_shared只有一次内存分配，而shared_ptr有2次。

所谓2次，一次是对象的内存，一次是控制块的内存。

make_shared把这2个内存一次性分配了。



# 参考资料

1、C++智能指针简单剖析

https://www.cnblogs.com/lanxuezaipiao/p/4132096.html

2、智能指针shared_ptr与unique_ptr详解

https://blog.csdn.net/weixin_36888577/article/details/80188414

3、

https://blog.csdn.net/game_fengzi/article/details/21528185

4、普通指针到智能指针的转换

https://blog.csdn.net/seamanj/article/details/50507470

5、使用 C++11 智能指针时要避开的 10 大错误

http://blog.jobbole.com/104666/

6、make_shared和shared_ptr的区别

https://blog.csdn.net/u013349653/article/details/51155675