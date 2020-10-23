---
title: 《深入理解cpp11》读书笔记
date: 2018-10-11 10:13:51
tags:
	- cpp

---



# 1、新标准的诞生

c++11实际上是c++的第二个事实标准。

为了这个标准，委员会工作了11年。

在之前，有c++98和c++03这2个标准。

c++11的目标就是完全取代之前的标准。

引入了140个新特性，修正了之前标准的600个缺陷。

之前c++11的代号是c++0x，因为之前委员会很乐观，认为会在21世纪的第一个10年内完成。

跟c++11同步的，还有C语言的c11标准。

模板使得c++近乎一种函数式编程语言。

在c++98/03里，有一些非常激进的特性，后面认为是不合适的。例如，动态异常处理、输出模板。所以在c++11里就抛弃了。

相比于c++98/03，c++11写的程序代码量会减少30%到80%。

有哪些很好的特性呢？

1、语言级别支持并行编程。多线程。

2、auto、decltype来加强泛型编程。

3、通过constexpr等更好地支持系统编程。

4、通过内联namespace、右值引用等，更好地帮助库编程。



对于新增的c++特性，可以分为这4类：

1、库作者需要的。

2、类作者需要的。

3、所有人需要的。

4、部分人需要的。



加入关键字的考虑，关键字对之前的代码有影响，因为你的关键字可能在之前的代码里当成变量名在用。

c++11引入关键字非常慎重。通过分析已有开源代码里，看看有没有被使用到。



开发能够改变人们思维方式的特性。

lambda表达式就是这样的一个特性。

# 2、保证稳定性和兼容性

在c++98里，`__cpluplus`定义为199711L。

而在c++11里，`__cplusplus`被定义为201103L。

这个可以在代码里使用来做判断。

## char和wchar_t的连接

## long long类型的引入

在1995年，就有人提议把long long加入到c++98标准。

但是被委员会拒绝了。

但是C99接纳了long long类型。c++11为了兼容C99，所以也引入了long long。

int和long long运算，会先把int提升为long long再进行运算。

## 静态断言

默认的断言都是在运行时起作用。

是否可以在编译时断言呢？

可以的。

c++11引入了static_assert来做这个事情。

## noexcept修饰符和noexcept操作符

```
void func() throw(int , double) {
    
}
```

这个就是动态异常处理，在c++11里被抛弃了。因为这个特性没什么用。

被noexcept修饰的，就不会抛出异常。

c++编译器会自动分配std::terminate()函数来处理这种情况。

具体用专门的文章来描述。

在C++98里，用throw()来声明不抛出异常的函数。

```
void func() throw() {
	
}
```

在C++11里，被替换为noexcept。

```
void func() noexcept {
	
}
```

noexcept主要用来保证应用程序的安全。

例如，一个析构函数，不应该抛出异常。

那么对于经常被析构函数调用的delete函数，C++11默认将delete设置为noexcept。这样就保证了安全。

```
void operator delete(void *) noexcept;
```

```
using namespace std;

struct A {
    ~A() {
        throw 1;
    }
};
struct B {
    ~B() noexcept(false) {
        throw 2;
    }
};
struct C {
    B b;
};

int funcA()
{
    A a;
}
int funcB()
{
    B b;
}
int funcC()
{
    C c;
}
int main()
{
    try {
        funcB();
    }catch(...) {
        cout << "catch funcB \n";
    }
    try {
        funcC();
    } catch(...) {
        cout << "catch funcC\n";
    }
    try {
        funcA();
    } catch(...) {
        cout << "catch funcA\n";
    }
    
    return 0;
}
```

运行结果：

```
hlxiong@hlxiong-VirtualBox:~/work/test/cpp/build$ ./test 
catch funcB 
catch funcC
terminate called after throwing an instance of 'int'
已放弃 (核心已转储)
```

A的析构函数，抛异常不行。这样是为了阻止异常的扩散。



## 快速初始化成员变量

在c++98里，**可以在类声明里，直接用等号对成员变量进行初始化。这个叫“就地初始化”。**

但是有很多要求。

c++11里的就宽松多了。



## 非静态成员的sizeof

在c++98里，sizeof不能对非静态成员使用，否则编译不过。

c++11，已经可以了。

## friend的改进

friend破坏了封装性。

感觉C++11的很多的改进，都是围绕了提高模板的作用而做的。



## final和override

override，是没有明确说明要重载父类的函数。就是把潜规则变成了明规则。

对非virtual函数进行override，会编译报错。



## 外部模板

为什么需要外部模板？

先说说外部的概念，C语言里的extern就是了。

外部模板，是为了让代码只有一份，避免冗余。



这一章主要就是讲了17个改动，这些改动都是为了保证兼容性和稳定性。

# 3、通用为本，专用为末

c++设计者总是希望从各种方案中抽象出更加通用的方法来构建新的特性。

## 继承构造函数

用using来透传构造函数。

## 委派构造函数

是指其他构造函数调用基准构造函数的这种行为。

```
class A {
	A() {
	
	}
	A(int i): A() {//这个就是委派构造函数。
	
	}
}
```

而高级用途，还是围绕着模板来的。



## 右值引用

std::move并没有移动任何东西，它实际上只是把一个左值强制转换为右值引用。

等价于：

```
static_cast<T&&>(lvalue);
```

