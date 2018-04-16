---
title: C++之双冒号作用
date: 2018-04-16 11:34:38
tags:
	- C++

---



1、作用域限定符。

在class内部直接定义函数的时候，不要在前面加上class名字。

但是在class外面定义函数的时候，就需要加上class名字和双冒号。

```
class Test {
  int func1() {
    
  }
};

Test::func2() {
  
}
```

2、static的成员变量，可以通过类名加双冒号来引用。

```
class Test {
  private:
  	static int a;
};
int main()
{
  int x = Test::a;
}
```

3、static的成员函数也是一样的方式。

4、在class里的typedef类型。

```
class Test {
  public:
  	typedef int INT;
};
int main()
{
  Test::INT x;
}
```



# 参考资料

1、C++中的::的作用

https://blog.csdn.net/zhanghuaichao/article/details/55676209