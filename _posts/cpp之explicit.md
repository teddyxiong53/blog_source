---
title: C++之explicit
date: 2018-04-16 08:59:06
tags:
	- CPP

---



鉴于c++这个词，在hexo的文件名字里，会被替换为c-，我在文件名字里，统一把c++写成cpp。

一直没有去深入学习c++，现在看arduino的底层库，发现是用c++写的，所以是一个不错的学习切入口。

我不再采取系统学习语法的方式了，之前语法也大概看过。现在就看到一个疑问，解决一个问题，通过这种方式来进行学习。

在cores/esp8266/WString.h里。看到explicit这个关键字，了解一下。

# 作用

explicit用来防止构造函数被隐式替换。



# 举例

```
#include <string>

class things {
    public:
        things(const std::string&name=""):
            m_name(name),height(0),weight(10){}
        int CompareTo(const things & other);
        std::string m_name;
        int height;
        int weight;
        
};

int main()
{
    things a;
    std::string nm = "book_1";
    int result = a.CompareTo(nm);//本来CompareTo要求的参数是things类型的，现在只是给了一个string，也是可以的，因为默认会给你构造。
}
```

如果你不希望这样的默认构造，就这样改。

```
class things {
    public:
        explicit things(const std::string&name="")://这里加上explicit。
            m_name(name),height(0),weight(10){}
```



这个知识点还是有必要深入一下。

这种主要是针对只有一个参数的构造函数而言的。

下面这两种情况会调用单参数构造函数：

```
1、同类型对象的拷贝构造。
2、不同类型对象的隐式转化。
例如A a = 1;就是隐式转化。
正常的写法应该是A a(1);
```



这种隐式转化是不安全的。

解决办法就是加上explicit声明。对于无参构造和多参数构造，不存在这种问题。

简单例子是这样。如果不加explicit，那么编译可以通过，也可以正常运行。

加上explicit，则编译就报错。

```
class A
{
public:
    /*explicit*/ A(int x) {
        printf("x:%d\n", x);
    }
};
int main()
{
    A a = 1;
}
```



# 参考资料

1、

https://www.cnblogs.com/winnersun/archive/2011/07/16/2108440.html

2、C++ explicit禁止单参构造函数隐式调用

https://blog.csdn.net/K346K346/article/details/82779248