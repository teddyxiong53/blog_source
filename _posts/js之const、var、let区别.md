---
title: js之const、var、let区别
date: 2018-12-19 11:11:17
tags:
	- js

---



js里定义变量有3种方式：

1、const。定义变量不能改，必现定义时初始化。

2、var。可以不初始化（会给warning的）。

3、let。作用域在函数内部。



const的内涵是：

指向的内存地址不能再变了。所以定义的时候就指定。

但是内存里的对象可以变。所以就是属性可以增减、可以修改。

用const完全可以的。尽量用const。



参考资料

1、js中const,var,let区别

https://www.cnblogs.com/ksl666/p/5944718.html

2、const定义的对象属性是否可以改变

https://blog.csdn.net/qq_25643011/article/details/79426015