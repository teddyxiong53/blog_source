---
title: cpp之语法疑问总结
date: 2018-04-16 18:52:33
tags:
	- cpp
---



#构造函数后面的冒号是什么意思？

看arduino的代码。看Print类。

```
class Print
{
  private:
    int write_error;
    size_t printNumber(unsigned long, uint8_t);
    size_t printFloat(double, uint8_t);
  protected:
    void setWriteError(int err = 1) { write_error = err; }
  public:
    Print() : write_error(0) {} //这里不太明白。
```

可以看到，Print构造函数后面跟了个冒号。这里代表了什么意思呢？

是用来初始化的。就是表示write_error这个成员变量值初始化为0 。



# 函数声明后面跟const是什么意思？

表示的是，class的这个成员函数，隐含传入的this指针为const指针。所以不能对this指向的内容进行修改。



# 命名空间

分为两种，有名的和无名的。

有名的：

```
namespace myns {
  
}
```

无名的。

```
namespace {
  
}
```

命名空间是开放的，可以随时把新的成员加入到已有的命名空间里去。

做法就是多次声明和定义同一个命名空间。

```
namespace A {
  int i;
  void func1();
}
namespace A {
  int i;
  void func2();
}
//现在A里面有i、j、func1、func2这4个成员了。
```

使用命名空间，就很类似Python里的module的概念。

using namespace xxx。就类似import xxx。

命名空间导致名字很长，为了方便，可以取别名。

```
namespace ns_with_long_name {
  int i;
}
namespace ns_short = ns_with_long_name;//这样就定义了别名了。
```

# std命名空间有什么内容

其实也没有多少，就是cin、cout、cerr这些。



# 双冒号

双冒号的名字是“作用域解析运算符”。



# 引用类型

引用就是别名。有引用的前提是已经有一个变量存在了。

可以这样理解：

一个小孩生下来了。给他起个名字，就是创建了一个引用。

## 引用和指针区别

1、没有空引用。一个不属于某个具体人的名字，没有意义。

2、引用不能修改指向的对象。可以理解为人的名字不能改。指针则是可以修改指向的位置的。

3、引用必须在创建的时候被初始化。

## 为什么用引用做形参？

引用在这个场景的作用就跟指针类型了。可以修改参数的值。

## 有没有引用的引用？

我看tinystl的代码。看到这种写法。

是什么意思？是表示二级引用吗？引用的引用？

```
vector(vector&& other);
```

https://www.zhihu.com/question/28023545

这里找到一些说明。

这里引入一个概念，引用折叠。

```
引用折叠规则：
X& &（引用的引用）、X& &&（右值引用的引用）、X&& &（引用的右值引用）均折叠为X &。
X&& &&（右值引用的右值引用）折叠为X &&。

上面的类型别名和函数模板均触发了引用折叠。
注意：引用折叠的前提必须是类型别名或者模板参数。标准禁止直接定义引用的引用。
```

## 如何理解引用折叠？

https://www.zhihu.com/question/40346748

一个简单说明是这样。

```
& && == && & == &
```

```
楼上几位把结果都说得很清楚了，根本原因是因为C++中禁止reference to reference，所以编译器需要对四种情况(也就是L2L,L2R,R2L,R2R)进行处理，将他们“折叠”(也可说是“坍缩”)成一种单一的reference。
```



# nullptr



# new和malloc区别

```
#include <iostream>
using namespace std;

class MyClass {
public:
	MyClass() {
		cout << "construct " << endl;
	}
	~MyClass() {
		cout << "destruct" << endl;
	}
	void show();
};
void MyClass::show()
{
	cout << "show" << endl;
}
int main(int argc, char const *argv[])
{
	MyClass c;
	c.show();
	return 0;
}
```

```
teddy@teddy-ubuntu:~/work/test/cpp$ ./a.out      
construct 
show
destruct
```

可以看到，new创建的对象会自动调用构造和析构函数。

# __cplusplus

```
cout << __cplusplus <<endl;
得到的结果是：201103
```



# 成员函数后面跟着const表示什么意思？

1、编译器会自动给每个成员函数加上this指针。在函数后面加上const，表示这个函数不能修改成员变量的值。

2、这个const其实是修饰到了this指针了。

看一个例子。

```
#include <iostream>

using namespace std;

class Test {
public:
	void show() const {
		cout << "const func" << endl;
	}
	void show() {
		cout << "normal func" << endl;
	}
};
int main(int argc, char const *argv[])
{
	Test a;
	a.show();
	const Test b;
	b.show();
	return 0;
}
```

```
teddy@teddy-ubuntu:~/work/test/cpp$ ./a.out 
normal func
const func
```

# 静态成员变量的初始化

我还是习惯C语言的编码方式。

定义一个类，里面的成员都是静态的。

初始化要这样：

```
int Test::a = 1;
```

不这样初始化，其他地方都不能引用的，会报找不到的错误。



# 判断string为空

https://blog.csdn.net/Xuebing_han/article/details/78143560?locationNum=9&fps=1



# syslog打印<<重写的枚举

```
#include <sstream>
std::ostringstream buf ;
buf << cmd;
syslog(LOG_INFO, "led state:%s", buf.str().c_str());
```



# 参考资料

1、C++类成员冒号初始化以及构造函数内赋值

https://blog.csdn.net/zj510/article/details/8135556

2、C++在函数声明时，后面跟个const是什么意思？

https://zhidao.baidu.com/question/510299233.html

3、malloc/free和new/delete的区别

https://blog.csdn.net/chance_wang/article/details/1609081

4、成员函数后面加const，没有const，以及使用的区别

https://blog.csdn.net/anye3000/article/details/6618615