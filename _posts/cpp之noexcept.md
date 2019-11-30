---
title: cpp之noexcept
date: 2018-10-10 20:20:51
tags:
	- cpp

---



用来防止异常的扩散和传播。

关键字告诉编译器，函数中不会发生异常,这有利于编译器对程序做更多的优化。

C++中的异常处理是在运行时而不是编译时检测的。为了实现运行时检测，编译器创建额外的代码，然而这会妨碍程序优化。

# 参考资料

1、noexcept修饰符与noexcept操作符

https://book.2cto.com/201306/25351.html

2、c++ noexcept

https://blog.csdn.net/liufengl138/article/details/101797756