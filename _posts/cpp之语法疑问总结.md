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



# 参考资料

1、C++类成员冒号初始化以及构造函数内赋值

https://blog.csdn.net/zj510/article/details/8135556

2、C++在函数声明时，后面跟个const是什么意思？

https://zhidao.baidu.com/question/510299233.html