---
title: cpp之右值引用
date: 2019-04-12 16:31:30
tags:
	- cpp

---



c++11引入了右值引用和move语义。

可以避免不必要的复制，提高了程序性能。

相应的，c++11容器增加了一些右值版本的插入函数。

讨论之前，我们先看看，什么是左值和右值。

```
左值
表达式结束后，依然存在的持久对象。

右值
表达式结束后，就不存在了的临时对象。
```

一个简单的区分方法就是，看看能不能对表达式取地址，如果能，就是左值，如果不能，就是右值。

在c++11里，右值由2个概念组成；

```
1、将亡值。
	xvalue。
	expiring value
	c++11新增的，与右值引用相关的表达式。
	将要被move的对象。
	T&&函数返回值。
	std::move返回值
2、纯右值。
	prvalue
	PureRight Value
	非引用返回的临时变量。
	运算表达式产生的临时变量。
	原始字面量。
	lambda表达式。
```



右值不具名，所以我们只能通过引用的方式找到它。



```
#include <iostream>
using namespace std;

int g_constructCount = 0;
int g_copyConstructCount = 0;
int g_destructCount = 0;

struct A {
    A() {
        cout << "construct: " << ++g_constructCount << endl;
    }
    ~A() {
        cout << "destruct: " << ++g_destructCount << endl;
    }
    A(const A& a) {
        cout << "copy construct: " << ++g_copyConstructCount << endl;
    }

};
A getA() {
    return A();
}
int main()
{
    A a = getA();
    return 0;
}
```

编译的时候，加上这个选项：

```
-fno-elide-constructors
```

运行效果：

```
construct: 1 这个是getA()里面的构造函数。
copy construct: 1 
destruct: 1
copy construct: 2 
destruct: 2
destruct: 3
```

可以看到，拷贝构造函数执行了2次。

一次是：getA函数内部创建的对象返回后，构造一个临时对象产生的。

一次是：main函数里构造a对象时产生的。

如果我们使用右值引用，则效果是这样：

```
A&& a = getA();
```

```
construct: 1
copy construct: 1
destruct: 1
destruct: 2
```

只执行了一次拷贝构造。

原因在于右值引用绑定了右值，让临时右值的生命周期延长了。

我们可以利用这个特性做一些性能优化。



实际上，T&&并不一定是右值，它绑定的类型的未定的。也叫通用引用。

```
template <typename T>
void f(T&& param) ;

f(10);//传递右值
int x = 10;
f(x);//传递左值
```

只有在发送自动类型推导时，&&才是一个通用引用。



std::move可以把一个左值转化成右值。



用移动构造避免深拷贝。



move和forward都是用来把左值转成右值。

C++中所有的值都必然属于左值、右值二者之一。



左值是指表达式结束后依然存在的持久化对象，右值是指表达式结束时就不再存在的临时对象。所有的具名变量或者对象都是左值，而右值不具名。很难得到左值和右值的真正定义，但是有一个可以区分左值和右值的便捷方法：看能不能对表达式取地址，如果能，则为左值，否则为右值。

书上又将右值分为将亡值和纯右值。
纯右值就是c++98标准中右值的概念，
如非引用返回的函数返回的临时变量值；
一些运算表达式，如1+2产生的临时变量；
不跟对象关联的字面量值，如2，'c'，true，"hello"；这些值都不能够被取地址。

而将亡值则是c++11新增的和右值引用相关的表达式，这样的表达式通常时将要移动的对象、T&&函数返回值、std::move()函数的返回值等，

不懂将亡值和纯右值的区别其实没关系，统一看作右值即可，不影响使用。

c++98中的引用很常见了，就是给变量取了个别名，
在c++11中，因为增加了右值引用(rvalue reference)的概念，
所以c++98中的引用都称为了左值引用(lvalue reference)。

关于左值引用：

```
int a = 10;
int& refA = a; //refA是a的别名。修改refA就是修改a。

printf("a:%p, refA:%p\n", &a, &refA);
这2个值是相同的，是同一块内存地址。
```

```
int& b = 1;//这个会编译错误的，因为常量1没有内存地址。
```

编译报错是：

```
invalid initialization of non-const reference of type ‘int&’ from an rvalue of type ‘int’
```

```
const int& b = 1;//这个是可以编译通过的。
```



右值引用使用的符号 是&& 。

```
cannot bind ‘int’ lvalue to ‘int&&’
```

匿名的临时变量就是右值。

匿名临时变量本来在表达式语句结束后，它的生命周期也就结束了。

但是通过右值引用，这个右值又重获新生。它的生命周期变得跟右值引用变量一样长了。

实际上就是给临时变量取了个名字。

```
class A {
public:
	int a;
};
A getTemp()
{
	return A();
}
A&& a = getTemp();//getTemp返回的是一个右值（匿名临时变量）。
```



左值引用只能绑定左值，右值引用只能绑定右值。

如果绑定不对，编译就会失败。

但是有个特例，就是const左值引用，是个万能的引用类型。

它可以绑定左值、const左值、右值。

而且在绑定右值的时候，const左值引用可以像右值引用一样延长右值的生命周期。

缺点是，只能读不能写。

```
const int &a = 1;//const左值引用绑定右值。不报错。
const A& a = getTemp();//也不报错。
```



现在很多的c++编译器，都进行了返回值优化。

可以避免很多不必要的拷贝构造。

但是不是所有的都能被优化。

我们需要自己代码可控的方式来做到这一点，这个方式就是右值引用和移动语义。



下面我们通过自己实现一个MyString类来说明。

```
#include <iostream>
#include <cstring>
#include <vector>
using namespace std;

class MyString
{
public:
    static size_t CCtor; //统计调用拷贝构造函数的次数
//    static size_t CCtor; //统计调用拷贝构造函数的次数
public:
    // 构造函数
   MyString(const char* cstr=0){
       if (cstr) {
          m_data = new char[strlen(cstr)+1];
          strcpy(m_data, cstr);
       }
       else {
          m_data = new char[1];
          *m_data = '\0';
       }
   }

   // 拷贝构造函数
   MyString(const MyString& str) {
       CCtor ++;
       m_data = new char[ strlen(str.m_data) + 1 ];
       strcpy(m_data, str.m_data);
   }
   // 拷贝赋值函数 =号重载
   MyString& operator=(const MyString& str){
       if (this == &str) // 避免自我赋值!!
          return *this;

       delete[] m_data;
       m_data = new char[ strlen(str.m_data) + 1 ];
       strcpy(m_data, str.m_data);
       return *this;
   }

   ~MyString() {
       delete[] m_data;
   }

   char* get_c_str() const { return m_data; }
private:
   char* m_data;
};
size_t MyString::CCtor = 0;

int main()
{
    vector<MyString> vecStr;
    vecStr.reserve(1000); //先分配好1000个空间，不这么做，调用的次数可能远大于1000
    for(int i=0;i<1000;i++){
        vecStr.push_back(MyString("hello"));
    }
    cout << MyString::CCtor << endl;
}
```

可以看到，这个一共执行了1000次拷贝构造。是没有必要的。

我们要实现移动语义，就需要增加2个函数：

1、移动构造函数。

2、移动赋值。

```
#include <iostream>
#include <cstring>
#include <vector>
using namespace std;

class MyString
{
public:
    static size_t CCtor; //统计调用拷贝构造函数的次数
    static size_t MCtor; //统计调用移动构造函数的次数
    static size_t CAsgn; //统计调用拷贝赋值函数的次数
    static size_t MAsgn; //统计调用移动赋值函数的次数

public:
    // 构造函数
   MyString(const char* cstr=0){
       if (cstr) {
          m_data = new char[strlen(cstr)+1];
          strcpy(m_data, cstr);
       }
       else {
          m_data = new char[1];
          *m_data = '\0';
       }
   }

   // 拷贝构造函数
   MyString(const MyString& str) {
       CCtor ++;
       m_data = new char[ strlen(str.m_data) + 1 ];
       strcpy(m_data, str.m_data);
   }
   // 移动构造函数
   MyString(MyString&& str) noexcept
       :m_data(str.m_data) {
       MCtor ++;
       str.m_data = nullptr; //不再指向之前的资源了
   }

   // 拷贝赋值函数 =号重载
   MyString& operator=(const MyString& str){
       CAsgn ++;
       if (this == &str) // 避免自我赋值!!
          return *this;

       delete[] m_data;
       m_data = new char[ strlen(str.m_data) + 1 ];
       strcpy(m_data, str.m_data);
       return *this;
   }

   // 移动赋值函数 =号重载
   MyString& operator=(MyString&& str) noexcept{
       MAsgn ++;
       if (this == &str) // 避免自我赋值!!
          return *this;

       delete[] m_data;
       m_data = str.m_data;
       str.m_data = nullptr; //不再指向之前的资源了
       return *this;
   }

   ~MyString() {
       delete[] m_data;
   }

   char* get_c_str() const { return m_data; }
private:
   char* m_data;
};
size_t MyString::CCtor = 0;
size_t MyString::MCtor = 0;
size_t MyString::CAsgn = 0;
size_t MyString::MAsgn = 0;
int main()
{
    vector<MyString> vecStr;
    vecStr.reserve(1000); //先分配好1000个空间
    for(int i=0;i<1000;i++){
        vecStr.push_back(MyString("hello"));
    }
    cout << "CCtor = " << MyString::CCtor << endl;
    cout << "MCtor = " << MyString::MCtor << endl;
    cout << "CAsgn = " << MyString::CAsgn << endl;
    cout << "MAsgn = " << MyString::MAsgn << endl;
}

/* 结果
CCtor = 0
MCtor = 1000
CAsgn = 0
MAsgn = 0
*/
```

分析：

vecStr.push_back(MyString("hello"));

这里MyString的匿名对象是一个右值，所以是进入到移动构造函数。



对于一个左值，肯定是调用拷贝构造函数了。

但是有些左值是局部变量，生命周期也很短，能不能使用移动而不是拷贝构造呢？

可以，就是std::move。用来把左值转成右值。

它就是告诉编译器，虽然我是一个左值，但是我就喜欢用移动构造函数。



如果我们没有提供移动构造函数，只提供了拷贝构造函数。

这个时候，move会失效，但是不会出错，它会去调用拷贝构造。

这也就是为什么拷贝构造函数是const T&类型的原因。



c++11里所有的容器都实现了移动语义。

move只是转移了资源的控制权，本质上是把左值强制转化为右值使用。

避免无谓的拷贝。

对应基本类型，move没有意义。



当右值引用和模板结合的时候，情况就更加复杂了。

T&&不一定表示右值引用。

它可能是左值。

&&表示的实际上是未定义的引用类型。

它必须被初始化，它的类型取决于你传递给的引用的类型。

（注意：只要在发生自动类型推导的时候，例如模板、auto关键字，&&才是通用引用类型）。



完美转发

什么是转发？

就是通过一个函数，把参数交给另外一个函数进行处理。

之前的参数可能是右值，也可能是左值。

如果在转发后，参数还是保持之前的属性，那么这个转发就是完美的。

```
#include <iostream>
#include <cstring>
#include <vector>
using namespace std;

void process(int& i){
    cout << "process(int&):" << i << endl;
}
void process(int&& i){
    cout << "process(int&&):" << i << endl;
}

void myforward(int&& i){
    cout << "myforward(int&&):" << i << endl;
    process(i);
}

int main()
{
    int a = 0;
    process(a); //a被视为左值 process(int&):0
    process(1); //1被视为右值 process(int&&):1
    process(move(a)); //强制将a由左值改为右值 process(int&&):0
    myforward(2);  //右值经过forward函数转交给process函数，却称为了一个左值，
    //原因是该右值有了名字  所以是 process(int&):2
    myforward(move(a));  // 同上，在转发的时候右值变成了左值  process(int&):0
    // forward(a) // 错误用法，右值引用不接受左值
}
```

输出是这样：

```
process(int&):0
process(int&&):1
process(int&&):0
myforward(int&&):2
process(int&):2
myforward(int&&):0
process(int&):0
```

我们自己转发后，右值引用变成了左值引用了。

这个就是不完美的。

我们修改一下。

```
void myforward(int&& i){
    cout << "myforward(int&&):" << i << endl;
    process(std::forward<int>(i));//这里加上
}
```

这样就对了。

但是还不是完美转发。

现在myforward还只能转发右值，不能转发左值。

需要借助模板和通用引用来做。

```
#include <iostream>
#include <cstring>
#include <vector>
using namespace std;

void RunCode(int &&m) {
    cout << "rvalue ref" << endl;
}
void RunCode(int &m) {
    cout << "lvalue ref" << endl;
}
void RunCode(const int &&m) {
    cout << "const rvalue ref" << endl;
}
void RunCode(const int &m) {
    cout << "const lvalue ref" << endl;
}

// 这里利用了universal references，如果写T&,就不支持传入右值，而写T&&，既能支持左值，又能支持右值
template<typename T>
void perfectForward(T && t) {
    RunCode(forward<T> (t));
}

template<typename T>
void notPerfectForward(T && t) {
    RunCode(t);
}

int main()
{
    int a = 0;
    int b = 0;
    const int c = 0;
    const int d = 0;

    notPerfectForward(a); // lvalue ref
    notPerfectForward(move(b)); // lvalue ref
    notPerfectForward(c); // const lvalue ref
    notPerfectForward(move(d)); // const lvalue ref

    cout << endl;
    perfectForward(a); // lvalue ref
    perfectForward(move(b)); // rvalue ref
    perfectForward(c); // const lvalue ref
    perfectForward(move(d)); // const rvalue ref
}
```

现在可以完美转发这四种类型了。



用emplace_back减少内存拷贝和移动

我们之前对vector都是用push_back。这个是会有内存拷贝的。

我们可以自己定义移动构造和赋值。

但是实际上也可以不定义。

容器给我们提供了更方便的处理方式。

就是emplace_back。

```
#include <iostream>
#include <cstring>
#include <vector>
using namespace std;

class A {
public:
    A(int i){
//        cout << "A()" << endl;
        str = to_string(i);
    }
    ~A(){}
    A(const A& other): str(other.str){
        cout << "A&" << endl;
    }

public:
    string str;
};

int main()
{
    vector<A> vec;
    vec.reserve(10);
    for(int i=0;i<10;i++){
        vec.push_back(A(i)); //调用了10次拷贝构造函数
//        vec.emplace_back(i);  //一次拷贝构造函数都没有调用过
    }
    for(int i=0;i<10;i++)
        cout << vec[i].str << endl;
}
```

移动语义对于swap影响也很大。

现在可以很高效地进行swap了。

```
template <typename T>
void swap(T& a, T& b)
{
    T tmp(std::move(a));
    a = std::move(b);
    b = std::move(tmp);
}
```



参考资料

1、《深入应用c++11》

2、C++11新特性之右值引用(&&)、移动语义(move)、完美转换(forward)

https://www.cnblogs.com/xiaobingqianrui/p/9064260.html

3、[c++11]我理解的右值引用、移动语义和完美转发

这篇文章挺好的。

https://www.jianshu.com/p/d19fc8447eaa

