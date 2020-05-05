---
title: cpp之function和bind分析
date: 2019-02-23 14:34:17
tags:
	- cpp

---

1

# 理解

bind就类似python里的偏函数，要求的回调参数个数是固定的。我们需要传递的参数比这个多。

用bind，就是把多出来的参数，跟函数绑定，形成一个新的函数传递给参数。



关于std::function的用法，可以理解为函数指针。

bind函数用来把某些形式的参数跟已知的函数进行绑定。形成新的函数。

**这种改变已有函数调用模式的做法，叫做函数绑定。**

bind就是函数适配器。

什么是适配器？

就是把已有的东西稍微改一下，让它形成新的逻辑。

容器、迭代器、函数都有适配器。





bind就是一个函数适配器。

bind的一般形式是：

```
auto newfunc = bind(func, arg_list);
```



bind的常见用法：

```
1、减少传递的参数个数。这个是最常用的。
2、改变参数的顺序。
3、绑定类的成员函数。方便把this传递过去。
server_.setMessageCallback(
      std::bind(&EchoServer::onMessage, this, _1, _2, _3));
      callback的格式是只能接收3个参数的，所以这样把this传递过去。
```



**在传统的c++程序里，事件回调是通过虚函数进行的。**

虚函数实现方式：

```
struct Button {
	Button();
	~Button();
	virtual void OnClick() = 0;
};

struct MyButton: pulic Button {
	virtual void OnClick() {
		printf("click\n");
	}
};

```

function方式实现：

```
struct Button {
	Button();
	~Button();
	void OnClick() {
		m_func();
	}
	function<void()> m_func = []() {};
};

int main() {
	Button a;
	a.m_func = []() {
		printf("click\n");
	};
	
}
```

**用function和bind的方式，一个明显优势，就是不用担心对象的生命周期了。**



bind作用：

```
1、把函数、成员函数、闭包转成function对象。
2、将多元(N>1)函数转成一元函数或者(N-1)元函数。
```



#回调

**使用callback可以改善软件结构，提高软件的复用性。**

callback，主要用在框架上，把需要给客户自定义的，通过回调来调用，客户具体实现。

先看C语言的版本，很简单。

```
#include <stdio.h>


void callback(int a) {
	printf("callback called with param:%d\n", a);
}

typedef void (*pfunc)(int a);

void caller(pfunc p) {
	(*p)(1);
}

int main()
{
	caller(&callback);
}
```

但是引入面向对象后，事情就变得复杂了。

如果回调函数是类的成员函数，怎么办？

static的成员函数，跟C语言的还是一样，没有问题。

但是非static的成员函数。就不同了。

```
#include <stdio.h>

class CCallback {
public:
	void Func(int a) {
		printf("member callback function\n");
	}
	
};

typedef void (CCallback::*pMemberFunc)(int);

void Caller(pMemberFunc p) {
	(*p)(1);
} 

int main()
{
	CCallback obj;
	//Caller()
}
```

这个编译是不能通过的。

因为非static的成员函数，必须通过对象来访问。

那我们就改进一下。

```
#include <stdio.h>

class CCallback {
public:
	void Func(int a) {
		printf("member callback function\n");
	}
	
};

typedef void (CCallback::*pMemberFunc)(int);

void Caller(CCallback *pObj, pMemberFunc p) {
	(pObj->*p)(1);
} 

int main()
{
	CCallback obj;
	Caller(&obj, &CCallback::Func);
}
```

这样可以编译运行了。



# function可以保存的内容

可以保存这些，把这些都封装成一个function对象。

```
1、普通函数。
2、lambda表达式。
3、函数指针。
4、仿函数。重载()运算符。
5、类成员函数。
6、静态成员函数。
```



##普通函数

```
void printA(int a) {
	std::cout << a << std::endl;
}


int main()
{
	std::function<void(int a)> func;
	func = printA;
	func(1);
}
```





##lambda表达式

```
std::function<void()> func = []() {std::cout << "save lambda func\n";};
func();
```

简单的写法，可以用auto来做。

```
auto func = []() {std::cout << "save lambda func\n";};
func();
```

## 仿函数

```
class compare_class {
public:
	bool operator()(int a, int b) {
        return a>b;
	}
};
int main() 
{
    func = compare_class();
    bool result = func(1,2);
}
```

## 静态成员函数

这个跟普通函数没有本质区别。



## 成员函数

这个需要借助bind函数，需要实例化对象。



参考资料

1、C++11 中std::function和std::bind的用法

https://blog.csdn.net/liukang325/article/details/53668046

2、应该用bind+function取代虚函数吗？

https://www.cnblogs.com/qicosmos/p/4527804.html

3、以boost::function和boost:bind取代虚函数

https://blog.csdn.net/Solstice/article/details/3066268

4、C++拾遗--bind函数绑定

https://blog.csdn.net/zhangxiangDavaid/article/details/43638747

5、std::function与std::bind 函数指针

https://blog.csdn.net/QQ575787460/article/details/8531397

6、虚函数和 std::function 如何取舍？

https://www.zhihu.com/question/27952064

7、我写C++喜欢用继承有问题么？

https://www.zhihu.com/question/264755585

8、C++回调机制实现(转)

https://www.cnblogs.com/qq78292959/archive/2012/10/10/2719155.html

9、std::function和std::bind详解

https://blog.csdn.net/xiaoyink/article/details/79348806