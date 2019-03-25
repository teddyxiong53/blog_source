---
title: gcc提供的原子操作
date: 2019-03-22 15:59:32
tags:
	- cpp

---



gcc从4.1.2版本开始，提供了`__sync_*`系列的内置函数。

用来提供加减和逻辑运算的原子操作。

自增操作为什么不是原子性的？

声明如下，分为两组，每组6个。

```
type __sync_fetch_and_xxx(type *ptr, type value, ...);
xxx可以是：
add
sub
or
and
xor
nand
```

```
type __sync_xxx_and_fetch(type *ptr, type value, ...);
xxx可以是：
add
sub
or
and
xor
nand
```

区别就是fetch的位置，前面一组是，是先取值再修改。

后面一组是，先修改再取值。

type可以是1到8个字节的。

另外还有：

```
bool __sync_bool_compare_and_swap(type *ptr, type oldval, type newval, ...);
type __sync_val_compare_and_swap(type *ptr, type oldval, type newval, ...);
```

这2个函数提供原子的比较和交换。

如果`*ptr==oldval`，就把newval写到到*ptr。

bool返回值的那个，在相等并写入的情况下返回true。

type返回值的那个，在相等并写入的情况下返回oldval。







因为目前gcc实现的是full barrier。





参考资料

1、GCC 提供的原子操作

https://www.cnblogs.com/FrankTan/archive/2010/12/11/1903377.html

2、对int变量赋值的操作是原子的吗？

https://www.zhihu.com/question/27026846