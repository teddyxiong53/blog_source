---
title: cpp之返回值和返回引用
date: 2020-10-17 15:55:30
tags:
	- cpp
---

--

1、返回值为引用型（int& ）的时候，返回的是地址，因为这里用的是 int& a=mymay.at(); ，所以a和m_data_指的是同一块地址（由寄存器eax传回的5879712）。

2、返回值不是引用型（int）的时候，返回的是一个数值。这个时候就很有意思了，编译器是先将这个数值放入一个内存中（上面例子中，该内存地址为ebp-24h)，再把这个地址付给a，此时的a代表的地址是ebp-24h，和m_data_代表的地址不一样（m_data_代表的地址是5879712）。

3、综上两点可以看出，当返回的值不是引用型时，编译器会专门给返回值分配出一块内存的（例子中为ebp-24h）



**函数返回时，如果不是返回一个变量的引用，则一定会生成一个临时变量。**



反正记住：引用就是变量的地址。要注意不用把局部变量作为引用返回出来了。

这样就是有问题的：

下面这样运行会段错误。因为x是局部变量。

```
int& fn()
{
    int x = 1;
    return x;
}

int main()
{
    int& a = fn();
    printf("a:%d\n", a);
    return 0;
}
```

改成下面这样，则会编译报错。

```
int fn()//就把这个返回值改了。
{
    int x = 1;
    return x;
}

int main()
{
    int& a = fn();
    printf("a:%d\n", a);
    return 0;
}
```

错误是：

```
error: invalid initialization of non-const reference of type ‘int&’ from an rvalue of type ‘int’
```

不过这样改一下就可以正常运行：

```
int fn()
{
    int x = 1;
    return x;
}

int main()
{
    const int& a = fn();//改成const的。
    printf("a:%d\n", a);
    return 0;
}
```



通过使用**引用来替代指针**，会使 C++ 程序**更容易阅读和维护**。

C++ 函数可以返回一个引用，方式与返回一个指针类似。

当函数返回一个引用时，则返回**一个指向返回值的隐式指针**。

这样，函数就可以放在赋值语句的左边。

当返回一个引用时，要注意被引用的对象**不能超出作用域**。

所以返回一个对局部变量的引用是不合法的，但是，可以返回一个对静态变量的引用。



# 参考资料

1、C++中返回引用和返回值的区别

https://www.cnblogs.com/qingergege/p/10486111.html

2、C++：引用作为返回值

https://blog.csdn.net/duhengqi/article/details/70198630

3、C++ 把引用作为返回值

https://www.runoob.com/cplusplus/returning-values-by-reference.html