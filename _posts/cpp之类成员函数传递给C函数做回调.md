---
title: cpp之类成员函数传递给C函数做回调
date: 2020-05-08 14:29:08
tags:
	- cpp

---

1

在C和C++混合编程的时候，经常有C函数需要一个回调函数作为参数，但是我希望传递进去的是C++类的成员函数。

直接传递，肯定类型不匹配，编译不过。

但是还是有解决办法的。

我们下面以pthread_create为例来讲解。

方法一

用普通函数做回调，但是在回调里再调用类的成员函数。

相当于封装了一下。

```
pthread_create(&pid, NULL, thread_func_wrapper, this);
```

```
void *thread_func_wrapper(void *arg)
{
	MyClass *cls = (MyClass *)arg;
	cls->func();
}
```

这个的缺点是破坏了封装性。

所以有了改进的方法二

方法二

把thread_func_wrapper改成class里面的一个static成员函数。

方法三



参考资料

1、C++中类成员函数作为回调函数

https://www.cnblogs.com/findumars/p/5605563.html