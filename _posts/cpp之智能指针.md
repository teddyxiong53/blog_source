---
title: cpp之智能指针
date: 2018-05-09 17:52:35
tags:
	- cpp

---





智能指针是面试官爱问的，也是实际开发中很实用的东西。



为什么要引入智能指针呢？

我们先看一段示例代码。

```
void func(string &str) 
{
  string *ps = new string(str);
  if(xxx) {
    throw exception();
  }
  str = *ps;
  delete ps;
}
```

上面这段代码有问题，就是在xxx满足的情况下，没有释放ps的内存。这就导致了内存泄漏。

而在开发过程中，这种情况难以完全避免。

如果有一种机制，在func退出的时候，可以帮我们自动释放分配的内存，该有多好。

正是出于这样的需求，c++引入了智能指针的概念。

我们用auto_ptr来改造上面的代码。

```
void func(string &str)
{
  std::auto_ptr<string> ps (new string(str));
  if(xxx) {
    throw exception();
  }
  str = *ps;
  
}
```

这样，我们就不需要去关系内存的释放问题了。



# 智能指针分类

STL给我们提供了四种智能指针：

1、auto_ptr。C++98提供的方案，c++11已经抛弃了。但是还是很多地方用到。

2、unique_ptr。

3、shared_ptr。

4、weak_ptr。



为什么要抛弃auto_ptr。

我们还是先看一段代码。

```
auto_ptr<string> ps (new string("hello"));
auto_ptr<string> ps2;
ps2 = ps;
```

上面的语句将会完成上面工作呢？

如果ps和ps2是常规指针。则2个指针指向了同一个string对象。

这个是不能接受的。因为程序将会试图释放两次。

要避免这种情况出现，有这些手段：

1、定义赋值运算符。使得赋值时进行深拷贝。这样的缺点是浪费空间。智能指针没有采用这种方式。

2、建立所有权（ownership）概念。对于特定的对象，只能有一个智能指针可以拥有。这就是auto_ptr和unique_ptr使用的策略。

3、创建更加智能的指针。跟踪对象的引用计数。这就是shared_ptr采用的策略。

要抛弃auto_ptr，是因为存在潜在的内存崩溃的问题。



所以，常用的智能指针就剩下unique_ptr和shared_ptr了。



unique_ptr为什么优于auto_ptr呢？



如何选择至智能指针呢？

有这些原则可以参考。

1、如果程序要使用多个指向同一个对象的指针，用shared_ptr。

```
常见的场景是这些：
1、有一个指针数组。另外有一些辅助指针来标定特定的元素，例如最大元素和最小元素。
2、2个对象都包含指向第三个对象的指针。
3、STL容器包含指针。
```



# 参考资料

1、C++智能指针简单剖析

https://www.cnblogs.com/lanxuezaipiao/p/4132096.html