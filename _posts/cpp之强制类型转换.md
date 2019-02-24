---
title: cpp之强制类型转换
date: 2018-05-10 21:10:32
tags:
	- cpp

---



强制类型转换，简称强转。有4种：

1、static_cast。编译时类型检查。

2、dynamic_cast。运行时检查。

3、const_cast。

4、reinterpert_cast。

格式都是：

```
xx_cast<type>(expression)
```



c++里层次类型转换，无非两种，向上转换和向下转换。

对于向上转换，就是子类转父类，static_cast和dynamic_cast是一样的，都是安全的。

对于向下转换，就是把父类指针转成子类指针。那么就可能访问不存在的成员，static_cast会返回，但是可能会越界访问内存。

而dynamic_cast就安全些。会判断转换是否可以进行，在不能进行的时候，返回NULL。



# 参考资料

1、C++强制类型转换操作符 static_cast

https://www.cnblogs.com/QG-whz/p/4509710.html

2、C++中static_cast和dynamic_cast强制类型转换

https://blog.csdn.net/qq_26849233/article/details/62218385