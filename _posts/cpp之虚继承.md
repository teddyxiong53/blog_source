---
title: cpp之虚继承
date: 2019-02-22 09:45:51
tags:
	- cpp

---



什么是虚继承？

虚继承是为了解决多继承而存在的。

假如存在如下的继承关系：

```
       A
   B1     B2
   	   D
```

这就是一个菱形继承。

如果没有虚继承，D里面就会有2套A的成员变量。

怎么处理呢？

让B1和B2虚继承A就好了。

```
class B1 : public virtual A {
    
}
```

但是这个实际上很少用。因为不推荐多重继承。



参考资料

1、关于C++中的虚拟继承的一些总结

https://www.cnblogs.com/BeyondAnyTime/archive/2012/06/05/2537451.html