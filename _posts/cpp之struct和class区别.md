---
title: cpp之struct和class区别
date: 2018-09-30 09:25:51
tags:
	- cpp

---



c++对struct关键字进行了大量扩展。

struct可以包含成员函数，可以继承，可以实现多态，看起来跟类一样了。

那么跟class还有什么区别？

最重要的一点就是继承时的权限不一样。

看例子。

struct的可以编译过，正常运行。class的不能编译通过。

```
#if 0  
struct A {
    char a;
};
struct B : A {//注意这里没有写明public继承
	char b;
};

int main()
{
	A var_a;
	B var_b;
	var_b.a = 1;
	
}
#else
class A {
    char a;
};
class B : A {//注意这里没有写明public继承
	char b;
};

int main()
{
	A var_a;
	B var_b;
	var_b.a = 1;
	
}
#endif
```

```
/home/hlxiong/work/test/cpp/main.cpp:36:10: error: ‘char A::a’ is private
     char a;
          ^
/home/hlxiong/work/test/cpp/main.cpp:46:8: error: within this context
  var_b.a = 1;
```





参考资料

1、C++中结构体与类的区别（struct与class的区别）

https://www.cnblogs.com/starfire86/p/5367740.html