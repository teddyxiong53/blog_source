---
title: cpp之function和bind分析
date: 2019-02-23 14:34:17
tags:
	- cpp

---



关于std::function的用法，可以理解为函数指针。

bind函数用来把某些形式的参数跟已知的函数进行绑定。形成新的函数。

这种改变已有函数调用模式的做法，叫做函数绑定。

bind就是函数适配器。

什么是适配器？

就是把已有的东西稍微改一下，让它形成新的逻辑。

容器、迭代器、函数都有适配器。

bind就是一个函数适配器。

bind的一般形式是：

```
auto newfunc = bind(func, arg_list);
```



bind的常见用法：

```
1、减少传递的参数个数。这个是最常用的。
2、改变参数的顺序。
3、绑定类的成员函数。方便把this传递过去。
server_.setMessageCallback(
      std::bind(&EchoServer::onMessage, this, _1, _2, _3));
      callback的格式是只能接收3个参数的，所以这样把this传递过去。
```





保存自由函数。

```
void printA(int a) {
	std::cout << a << std::endl;
}


int main()
{
	std::function<void(int a)> func;
	func = printA;
	func(1);
}
```

保存lambda表达式。

```
std::function<void()> func = []() {std::cout << "save lambda func\n";};
func();
```

简单的写法，可以用auto来做。

```
auto func = []() {std::cout << "save lambda func\n";};
func();
```



参考资料

1、C++11 中std::function和std::bind的用法

https://blog.csdn.net/liukang325/article/details/53668046

2、应该用bind+function取代虚函数吗？

https://www.cnblogs.com/qicosmos/p/4527804.html

3、以boost::function和boost:bind取代虚函数

https://blog.csdn.net/Solstice/article/details/3066268

4、C++拾遗--bind函数绑定

https://blog.csdn.net/zhangxiangDavaid/article/details/43638747