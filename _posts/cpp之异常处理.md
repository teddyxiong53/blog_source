---
title: cpp之异常处理
date: 2019-12-09 10:29:38
tags:
	 - cpp

---

1

关键字有：

```
try catch
	这2个是捕获异常。
throw
	这个是抛出异常。
	
因为异常其实很少使用，所以c++11增加了noexcept关键字。

```

通过throw关键字抛出异常。

throw之后的语句不会再被执行。

程序的控制器从throw转移到对应的catch代码块。

throw有点类似return的作用。



throw之后，如果当前函数里没有找到匹配的catch块，就向上抛出，一直到最外层，如果都没有找到匹配的catch。

就调用std::terminate来退出程序。



标准异常有：

```

```



除零异常演示

```
using namespace std;

double divide(double a, double b)
{
    if(b == 0) {
        throw "b is not valid";
    }
    return a/b;
}
int main()
{
    double a = 1.0;
    double b = 0;
    try {
        double c = divide(a,b);
    } catch(const char *msg) {
        printf("catch exception\n");
        printf("message is:%s\n", msg);
    }
    printf("end of code\n");
    return 0;
}
```

抛出的是一个const char *类型的异常。



自定义一个异常

```
class MyException : public std::exception
{
public:
    const char* what() const throw() {
        return "MyException throws";
    }
};

int main()
{
    try {
        throw MyException();
    } catch(MyException& e) {
        printf("e.what:%s\n", e.what());
    }
}

```



参考资料

1、C++11异常处理

https://blog.csdn.net/qq_35976351/article/details/82981927

2、c++11 异常处理

https://www.cnblogs.com/reboost/p/11072902.html