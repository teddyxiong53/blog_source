---
title: micropython之qstr
date: 2018-11-29 15:57:28
tags:
	- micropython

---



qstr是quick string的缩写。

为什么可以称为quick？

qstr是一种机制，大概意思是用一个数字来替代一个字符串。

优点有：

1、节省flash空间。

2、节省ram空间。

3、加快了比较速度。



模块被编译的时候，出现多次的字符串只存储一次。这个过程称为字符串驻留。

驻留字符串就叫qstr。

MP_QSTR_NULL这些，实际上是枚举值，从0开始。

```
QDEF(MP_QSTR_NULL, (const byte*)"\x00\x00" "")
QDEF(MP_QSTR_, (const byte*)"\x05\x00" "")
QDEF(MP_QSTR___abs__, (const byte*)"\x95\x07" "__abs__")
QDEF(MP_QSTR___add__, (const byte*)"\xc4\x07" "__add__")
```

以这一条为例，进入分析。

```
QDEF(MP_QSTR___abs__, (const byte*)"\x95\x07" "__abs__")
```

95和07 这2个分别代表了什么？

95是hash值，07表示后面的字符串的长度。

代码注释里写了的。

```
// A qstr is an index into the qstr pool.
// The data for a qstr contains (hash, length, data):
//  - hash (configurable number of bytes)
//  - length (configurable number of bytes)
//  - data ("length" number of bytes)
//  - \0 terminated (so they can be printed using printf)
```





参考资料

1、what the advantages of QSTR

https://forum.micropython.org/viewtopic.php?t=3211