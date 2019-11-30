---
title: cpp之智能指针
date: 2018-05-09 17:52:35
tags:
	- cpp

---





智能指针是面试官爱问的，也是实际开发中很实用的东西。

不是所有的指针都需要用智能指针，如果一直不需要释放的指针，例如EventLoop，就可以用裸指针。

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

# 原理

智能指针的原理是：

```
接受一个内存地址，构造一个在栈上的智能指针对象。
这样当程序退出栈的作用范围后，智能指针对象自动被销毁。
而智能指针对象里保存的内存也就被释放了（除非把智能指针保存起来）。
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

## weak_ptr其他

weak_ptr是为了配合shared_ptr而引入的。

之所以叫weak，是因为它并不具备普通指针的行为：

```
1、没有重载*和->
2、主要是为了协助shared_ptr工作，获得资源的观测权，像旁观者那样观测资源的变化。
3、当观测的shared_ptr失效后，weak_ptr也就失效了。
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

按照大家以往的编程经验，都是要求new和delete成对出现。

而现在智能指针是不需要手动delete的了。所以new最好也别出现了。

这也是make_shared出现的原因之一。



# 使用中的疑问

我现在使用中，需要把一个智能指针转成普通指针传递下去用。

就是protobuf的接口。这些接口为了通用性，是普通指针的。

我的疑问就是，转成普通指针了，还能正常被回收吗？

注意原始指针的获取，应该是

```
p.get();//注意是点
而不是
p->get();//这样会从包含的类里面去找get函数，当然一般是找不到的。
```

```
#include <memory>
#include <iostream>
#include <unistd.h>

class A {
public:
  A() {
    std::cout << "A construct" << std::endl;
  }
  ~A() {
    std::cout << "A destruct" << std::endl;
  }
  void print(const std::string& str) {
    std::cout << str << std::endl;
  }
};
std::shared_ptr<A> p1;

void func1()
{
  p1 = std::shared_ptr<A>(new A());
  p1->print("func1");
}
void func2(A *a)
{
  a->print("func2");
}
int main()
{
  func1();
  //func2(p1.get());
  sleep(2);
}
```

最后退出的时候，当然是调用了析构。

我这样改造了后，把p1变成jub在sleep之前，就调用了析构。所以传递原始指针的方式，不影响。

```
#include <memory>
#include <iostream>
#include <unistd.h>

class A {
public:
  A() {
    std::cout << "A construct" << std::endl;
  }
  ~A() {
    std::cout << "A destruct" << std::endl;
  }
  void print(const std::string& str) {
    std::cout << str << std::endl;
  }
};
//std::shared_ptr<A> p1;
void func2(A *a)
{
  a->print("func2");
}
void func1()
{
  std::shared_ptr<A> p1 = std::shared_ptr<A>(new A());
  p1->print("func1");
  func2(p1.get());
}

int main()
{
  func1();
  //func2(p1.get());
  sleep(2);
}
```





```
[2019-06-01 16:36:58][DEBUG][DossOS.cpp][connectToHttpServer][106]: 1122
terminate called after throwing an instance of 'std::bad_weak_ptr'
  what():  bad_weak_ptr
已放弃
```



互相持有对方的智能指针，导致析构函数没有被调用。

```
using namespace std;
class B;
class A
{
public:
    A(){cout<<"A()"<<endl;}
    ~A(){cout<<"~A()"<<endl;}
    shared_ptr<B> _ptrb;//解决办法是把这个改成weak_ptr。
};

class B
{
public:
    B(){cout<<"B()"<<endl;}
    ~B(){cout<<"~B()"<<endl;}
    shared_ptr<A> _ptra;//解决办法是把这个改成weak_ptr。跟上面都要改。
};
int main(int argc, char* argv[])
{
    shared_ptr<A> ptra(new A());
    shared_ptr<B> ptrb(new B());

    ptra->_ptrb = ptrb;
    ptrb->_ptra = ptra;

    return 0;
}
```



# 一种常见的用法

我看avs里都是类似这种用法。我也大量模仿了这种用法。

```
class A {
public:
  static std::unique_ptr<A> create();
  A() {
    std::cout << "a construct\n";
  }
  ~A() {
    std::cout << "a destruct\n";
  }
};
std::unique_ptr<A> A::create()
{
  auto tmp = std::unique_ptr<A>(new A);
  return tmp;
}
int main()
{
  std::shared_ptr<A> a1 = A::create();
  std::shared_ptr<A> a2 = a1;
  printf("a1:%p, a2:%p\n", a1.get(), a2.get());
}
```



用智能指针来做异步消息。

```
std::mutex mtx;
std::condition_variable cond;

class Msg {
public:
  Msg(int i) {
    m_i = i;
    std::cout << "Msg construct\n";
  }
  ~Msg() {
    std::cout << "Msg destruct\n";
  }
  int m_i;
};
std::queue<std::shared_ptr<Msg>> msgQueue;

void threadProc()
{
  sleep(1);
  {
    std::unique_lock<std::mutex> lock(mtx);
    cond.wait(lock, []() {
      if(!msgQueue.empty()) {
        return true;
      }
    });
  }
  std::shared_ptr<Msg> msgGet;
  {
    std::unique_lock<std::mutex> lock(mtx);
    msgGet = msgQueue.front();
    msgQueue.pop();
  }
  std::cout << "get msg\n";
  std::cout << msgGet->m_i << std::endl;
}

void sendMsg()
{
  std::shared_ptr<Msg> msg1 = std::shared_ptr<Msg>(new Msg(1));
  {
    std::unique_lock<std::mutex> lock(mtx);
    msgQueue.push(msg1);
  }
  cond.notify_one();
}
int main()
{
  std::thread t1(threadProc);
  sendMsg();
  std::cout <<"out of sendMsg\n";
  t1.join();
  std::cout << "end\n";
}
```

# lock

智能指针可以进行lock操作。这样就很像java的对象的锁了。

并不是，而是weak_ptr的一个操作。



# 常见错误

智能指针从创建方式有三种：

```
1、用malloc的一段内存地址，跟shared_ptr做构造函数的参数。
2、用make_shared函数。
3、用另外一个shared_ptr来做，就是拷贝构造。
```

对应的代码如下：

```
int main()
{
    int *raw_ptr = (int *)malloc(sizeof(int));
    std::shared_ptr<int> p1(raw_ptr);//方式1
    std::shared_ptr<int> p2 = std::make_shared<int>(11);//方式2
    std::shared_ptr<int> p3(p1);//方式3
}
```



错误用法

1、把同一个内存地址，给多个指针用了。导致重复释放。





weak_ptr和shared_ptr配合使用，是为了解决重复释放的野指针问题。

不考虑拷贝构造的话，shared_ptr的基本构造方式有4种。

```
1、1个参数。就是一个指针。
2、2个参数。一个指针，一个删除器。
3、3个参数。指针、删除器、allocator。
4、无参构造。
```

shared_ptr<void>类似于void *，可以容易任意类型。



常用方法

```
use_count()
	拿到指针的引用计数次数。
get()
	拿到裸指针。
reset()
	把引用计数清除到1 。
swap()
	交互2个智能指针的内容。
=
	赋值，会导致引用计数加1 。
```



# 使用shared_ptr可能会遇到的问题

## 生命周期的问题

使用shared_ptr就是为了管理对象的生命周期。

你不再是自己手动进行管理了。但是对象内存的释放时间也就没有那么精确了。





## 多次引用同一块内存

这个会导致对同一块内存的重复释放。

看例子。

```
void test()
{
    A * a1 = new A();
    std::shared_ptr<A> p1(a1);
    std::shared_ptr<A> p2(a1);
    std::cout << p1.get() << "  " << p2.get() << std::endl;
}
int main()
{
    test();
}
```

运行：

```
hlxiong@hlxiong-VirtualBox:~/work/test/cpp/build$ ./test 
A construct
0x142dc20  0x142dc20
A destruct
A destruct
```

可以看到被调用了2次析构函数。而只有一次构造函数。

## this指针的问题

对于传统方式，返回当前对象指针。

```
class A {
public:
    A() {
        std::cout <<"A construct\n";
    }
    ~A() {
        std::cout << "A destruct\n";
    }
    A * getThis() {//返回当前对象指针。
        return this;
    }
};
```

这个代码改成shared_ptr方式，不好改。

如果直接这么改。

```
std::shared_ptr<A> getThis() {
        return std::shared_ptr<A>(this);
    }
```

是有问题的。因为返回后，就被析构了。this就成了野指针了。

看例子。

```
class A {
public:
    A() {
        std::cout <<"A construct\n";
    }
    ~A() {
        std::cout << "A destruct\n";
    }
    std::shared_ptr<A> getThis() {
        return std::shared_ptr<A>(this);
    }
    int m_i;
};

void test()
{
    std::shared_ptr<A> a1 = std::make_shared<A>();
    a1->m_i = 11;
    std::shared_ptr<A> a2 = a1->getThis();
    std::cout << a2->m_i << std::endl;
}
int main()
{
    test();
}
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/cpp/build$ ./test 
A construct
11
A destruct
*** Error in `./test': double free or corruption (out): 0x000000000256ac30 ***
======= Backtrace: =========
```



为了解决这个问题，标准库提供了一个模板类，enable_shared_from_this<T>。

你继承这个类就好了。

在需要使用this的时候，用shared_from_this就好了。

```
class A : public std::enable_shared_from_this<A>{
public:
    A() {
        std::cout <<"A construct\n";
    }
    ~A() {
        std::cout << "A destruct\n";
    }
    std::shared_ptr<A> getThis() {
        return shared_from_this();
    }
    int m_i;
};
```

这样运行就不会出错了。

有一点要注意的，shared_from_this不能在构造函数里被调用。



## 多线程问题

根据boost文档，shared_ptr的线程安全定义如下：

```
1、一个shared_ptr，可以被多个线程同时read。
2、2个shared_ptr，指向同一个raw指针。2个线程同时write这2个shared_ptr，是线程安全的。包括析构。
3、多个线程，对同一个shared_ptr进行读写，是线程不安全的。

简而言之，就是说：
唯一需要注意的，就是多个线程对同一个shared_ptr对象读写的时候，需要加锁。
```

这个加锁，也有一个常用的技巧。

是这样的：

```
thread lock();
std::shared_ptr<T> tmp = globalSharedPtr;
thread unlock();
//对tmp进行操作。
```

## 环形引用

这个就是A和B这2个类，分别持有一个对方的shared_ptr。

导致无法释放。因为引用计数永远不会等于0。相当于死锁了。

要打破这个死锁，就要靠weak_ptr。



weak_ptr本身不具有指针的行为。

例如，你不能使用*和->操作。

它一般是用来配合shared_ptr进行工作的。



weak_ptr作为shared_ptr的观察者。可以获知shared_ptr的引用计数。还可以获知一个shared_ptr是否被析构了。



怎样构造一个weak_ptr呢？

```
1、用一个shared_ptr来构造。
	这个不会导致shared_ptr的引用计数增加。但是会增加另外一个计数增加。
2、从另一个weak_ptr拷贝。
```

从上面的说法来看，可以得到一个结论：

weak_ptr不可能脱离shared_ptr而存在。

```
void test()
{
    std::shared_ptr<A> a1 = std::make_shared<A>();
    std::weak_ptr<A> a2 = a1;
    a1.reset();
    std::cout << "a1.use_count():" << a1.use_count() << std::endl;
    std::cout << "a2.expire:" << a2.expired() << std::endl;
}
int main()
{
    test();
}
```

运行打印：

```
hlxiong@hlxiong-VirtualBox:~/work/test/cpp/build$ ./test 
A construct
A destruct
a1.use_count():0
a2.expire:1
```



weak_ptr的常用函数

```
expired()
	如果关联的shared_ptr的引用计数减到了0，这个就返回true。
lock()
	从当前的weak_ptr创建一个新的shared_ptr。
use_count()
	返回的是关联的weak_ptr的引用计数值。
	
```



如上面所说的，weak_ptr的最关键特性就是不会增加shared_ptr的引用计数。



```
class A {
public:
    A() {
        std::cout <<"A construct\n";
    }
    ~A() {
        std::cout << "A destruct\n";
    }
    int m_i;
};

void test()
{
    std::shared_ptr<A> a1 = std::make_shared<A>();
    a1->m_i = 11;
    std::weak_ptr<A> a2 = a1;
    auto a3 = a2.lock();
    std::cout << a3->m_i << std::endl;
}
int main()
{
    test();
}
```

运行：

```
hlxiong@hlxiong-VirtualBox:~/work/test/cpp/build$ ./test 
A construct
11
A destruct
```



# 异步执行时的问题

我写了下面的测试代码。异步是用的avs里的Executor来做的。

```
#include "Executor.h"

class  A {
public:
    A() {
        printf("a constructor\n");
    }
    ~A() {
        printf("a destruct\n");
    }
    int m_i;
};


void test1(std::shared_ptr<A> a1) {

    a1->m_i = 1;
}
void test2(A *a) {
    sleep(2);
    a->m_i = 2;
    printf("hhhhhhhhh\n");
}
void test()
{
    std::shared_ptr<A> a1 = std::make_shared<A>();
    std::shared_ptr<Executor> executor = std::make_shared<Executor>();
    test1(a1);
    executor->submit([a1]() {
        test2(a1.get());
    });
    //sleep(5);//这里sleep，就可以保证test2可以正常执行。
}
int main()
{
    test();

    while(1) {
        sleep(1);
    }
}
```

执行结果是这样：

```
hlxiong@hlxiong-VirtualBox:~/work/test/cpp/build$ ./test 
a constructor
a destruct
```

test2函数根本就执行不进去了。

这样虽然避免了死机问题，但是还是没有符合预期的行为。

哦，是因为executor也被销毁了而导致的无法执行。

如果executor还在，应该还是会死机的。

把executor提升为全局变量。

再测试。可以正常运行，销毁的时间自动被退后了。

ok，那就没有问题。跟我希望的是一致的。



# 自己实现SmartPointer

智能本质，本质上也是靠RAII机制来实现资源的释放的。

```
#include <iostream>
#include <memory>
#include <stdio.h>

template <typename T>
class SmartPointer {
private:
    T* _ptr;
    size_t *_count;
public:
    SmartPointer(T *ptr = nullptr):
        _ptr(ptr)
    {
        if(_ptr) {
            _count = new size_t(1);
        } else {
            _count = new size_t(0);
        }
    }
    SmartPointer(const SmartPointer& ptr) {
        if(this != &ptr) {
            this->_ptr = ptr._ptr;
            this->_count = ptr._count;
            (*this->_count)++;
        }
    }
    SmartPointer& operator=(const SmartPointer& ptr) {
        if (this->_ptr == ptr._ptr) {
            return *this;
        }
        if(this->_ptr) {
            (*this->_count)--;
            if(this->_count == 0) {
                delete this->_ptr;
                delete this->_count;
            }
        }
        this->_ptr = ptr._ptr;
        this->_count = ptr._count;
        (*this->_count)++;
        return *this;
    }
    T& operator*() {
        return *(this->_ptr);
    }
    T* operator->() {
        return this->_ptr;
    }
    ~SmartPointer() {
        (*this->_count)--;
        if(*this->_count == 0) {
            delete this->_ptr;
            delete this->_count;
        }
    }
    size_t use_count() {
        return *this->_count;
    }
};

int main()
{
    SmartPointer<int> sp(new int(10));
    SmartPointer<int> sp2(sp);
    SmartPointer<int> sp3(new int(20));
    sp2 = sp3;
    printf("sp use count:%d\n", sp.use_count());
    printf("sp3 use count:%d\n", sp3.use_count());
}

```







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

7、C++11里的智能指针

https://www.cnblogs.com/xiaouisme/p/7498782.html

8、bad_weak_ptr的原因

https://blog.csdn.net/yockie/article/details/40213331

9、C++11智能指针（五）：shared_ptr的循环引用的问题及weak_ptr

https://blog.csdn.net/lijinqi1987/article/details/79005738

10、c++ shared_ptr使用的几点注意

https://blog.csdn.net/man_sion/article/details/77196766

11、shared_ptr 简介以及常见问题

这篇文章总结得很好

https://blog.csdn.net/stelalala/article/details/19993425

12、

https://wenku.baidu.com/view/99517ee4ba1aa8114531d968.html

13、智能指针在多线程情况下的问题

https://blog.csdn.net/hopingwhite/article/details/6896211

14、智能指针shared_ptr的用法

https://www.cnblogs.com/jiayayao/archive/2016/12/03/6128877.html

15、智能指针（三）：weak_ptr浅析

https://blog.csdn.net/albertsh/article/details/82286999

16、C++11中智能指针的原理、使用、实现

https://www.cnblogs.com/wxquare/p/4759020.html

17、比起直接使用new，更偏爱使用std::make_unique和std::make_shared

https://blog.csdn.net/f110300641/article/details/83409804