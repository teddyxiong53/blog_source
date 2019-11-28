---
title: cpp之各种cast
date: 2018-11-19 15:31:28
tags:
	 - cpp

---

1

c++的cast函数有这些：

```
1、static_cast。
	最常用。相当于C语言的强制类型转化。但是多了一些检查。
2、const_cast。
	添加或者去掉const属性。
3、dynamic_cast。
	被转化类型必须包含虚函数（多态）。
	只要代码设计合理，都可以用static_cast替换。而且static_cast的效率更高。
4、interpret_cast。
	二进制重新解释。
```



muduo里的自己另外定义了2种转化

从注释看，是从Google的代码里扒出来的。

```
1、implicit_cast
	在类层次里，向上cast的时候，应该用implicit_cast代替static_cast。
	这个更加安全一点。
2、down_cast
	类层次里，向下cast。
```



reinterpret cast和static cast不同，但是和const cast类似。

是一个编译时指令。



#static_cast

c++ primer在第五章里说了，编译器隐式执行的任何类型转化，都可以通过static_cast来显式完成。

可以这么理解，static_cast，可以不写，不写的效果是一样的。

注意，static_cast不能转换掉const、volatile或者__unaligned属性。



# reinterrupt_cast

reinterrupt，字面意思就是重新解释。

这个可以理解为c++里的强制类型转化。

只能在指针直接进行转换时用。

谨慎使用。

一般是用来把void *转成某个确定的类型时用。

用来把2个毫不相干的类型进行转化。



# 参考资料

1、reinterpret_cast 转换

https://zh.cppreference.com/w/cpp/language/reinterpret_cast

2、static_cast 与reinterpret_cast

http://www.cnblogs.com/chengxin1982/archive/2010/01/13/1646311.html

3、c++小技巧(三)更好的类型转换implicit_cast和down_cast

https://blog.csdn.net/xiaoc_fantasy/article/details/79570788