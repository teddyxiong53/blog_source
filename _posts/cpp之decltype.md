---
title: cpp之decltype
date: 2018-10-08 16:52:17
tags:
	- cpp

---



c++11引入的特性。

# decltype的意义

有时候我们希望从表达式的类型推断出要定义的变量类型。

但是不想用该表达式的值初始化变量。（如果要初始化，就用auto了）

为了满足这种要求，就引入了decltype类型说明符。

它的作用是选择并返回操作数的数据类型。

在这个过程中，编译器分析表达式并得到类型，但是不计算表达式的值。



# 基本用法

```
int getSize();//只是声明一个函数，不实现。

int main()
{
	int tempA = 1;
	decltype(tempA) dclTempA;
	decltype(getSize()) dclTempB;//只是分析类型，并不真的调用getSize函数。
	return 0;
}
```

2个变量都是int类型的。可以编译通过。



# 参考资料

1、C++11新标准：decltype关键字

https://www.cnblogs.com/cauchy007/p/4966485.html