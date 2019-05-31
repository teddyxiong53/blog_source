---
title: cpp之reinterpret_cast
date: 2018-11-19 15:31:28
tags:
	 - cpp

---



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