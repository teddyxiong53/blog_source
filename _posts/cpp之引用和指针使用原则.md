---
title: cpp之引用和指针使用原则
date: 2018-05-13 19:16:13
tags:
	- cpp

---



# 为什么要使用引用？

1、可以修改对象的成员。

2、传递引用比传递整个对象的效率高。可以避免不必要的构造和析构。



在C语言里，使用指针传递参数，因为指针比传递值的效率高，而且可以修改参数的值。

c++再引入引用类型，主要是为了更加直观地进行使用。本质还是指针。



传递参数，有两种情况，一种是修改值，一种是不修改值。



不修改的情况：

1、如果是数组，只能传递指针。但是要把指针声明为const。

2、对于类对象，传递引用是标准做法。



修改的情况：

1、如果是内置数据类型，用指针。

2、如果是数组类型，用指针。

3、结构体，指针和引用都可以。

4、类，用引用。



##连续2个&号

我看到有连续2个&符号的用法，不知道具体代表了什么内涵？二级引用吗？

&&是右值引用。&是普通的左值引用。

所谓右值，就是永远不能放在=的左边。

常见的应用情况是：

例如string类内部，都有一个char *指针pstr指向实际存放字符串的内存。

对于这条语句：

```
str3 = str1.concat(str2);
```

实际是执行了2次构造函数，第一次是concat构造一个新的string对象。

第二次是赋值的时候执行了一次拷贝构造函数，把concat的临时值复制给了str3的内存。

然后concat的临时值在之后立即被销毁了。显然第二次拷贝构造很多余。

有了&&之后，可以给string增加一个参数是&&的拷贝构造函数来解决这个问题。

实现是这样：

```
string(string&& other) {
  pstr = other.pstr;
  other.pstr = nullptr;
}
```



# 类的成员变量是引用类型

看muduo的代码，看到MutexLockGuard的定义里：

```
 private:

  MutexLock& mutex_;
```

为什么这个类的成员变量，是引用类型？

如果有类的成员变量是引用类型，那么有这些需要注意的：

```
1、必须明确提供构造函数，不能用默认的构造函数。
2、构造函数的参数类型要是引用类型。
3、初始化必须在初始化列表里完成。
```

这种使用方式，在UML里，就是对应聚合方式。（普通成员变量的方式，就是组合了）

还可以有指针的方式来做聚合。



使用聚合的主要原因是：

外层对象不拥有内层对象。它们的生命周期不应该被绑定到一起。



# 存在引用的引用吗？

c++ primer里写着，因为引用不是一种数据类型，所以不存在引用的引用。

你如果直接定义引用的引用，编译会报错。



# 引用的折叠



# 参考资料

1、什么时候使用引用、什么时候使用指针

https://blog.csdn.net/hao5335156/article/details/53893714

2、c++中&和&&引用工作原理的区别？

https://zhidao.baidu.com/question/426629663273398972.html

3、C/C++ - 类中成员变量是引用

https://blog.csdn.net/lazyq7/article/details/48186291

4、Reference member variables as class members

https://stackoverflow.com/questions/12387239/reference-member-variables-as-class-members/25845843

5、为什么 C++ 有指针了还要引用？

https://blog.csdn.net/a3192048/article/details/84621775

6、C++ 是否能够定义引用的引用？

https://www.zhihu.com/question/28023545

7、Effective Modern C++ 条款28 理解引用折叠

https://blog.csdn.net/big_yellow_duck/article/details/52433305

8、C++中函数返回引用

https://blog.csdn.net/tlxxm/article/details/8860760