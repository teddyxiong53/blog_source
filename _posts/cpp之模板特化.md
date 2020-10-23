---
title: cpp之模板特化
date: 2020-10-14 10:14:30
tags:
	- cpp
---

1

# 函数模板的特化

使用模板时会遇到一些特殊的类型需要特殊处理，不能直接使用当前的模板函数，所以此时我们就需要对该类型特化出一个模板函数（就是写出一个模板函数专门给该类型使用）

```
template<class T>
bool IsEqual(T& p1, T& p2)
{
    return p1 == p2;
}
```

上面这个模板函数，对于字符串进行比较的情况，就不适用了。

所以我们需要特化出一个针对字符串的比较函数。

```
template<> //这里不添加类型模板
bool IsEqual<char*>(char *&p1, char *&p2)
{
    return strcmp(p1, p2)==0;
}
```

使用模板特化的时候，有这些需要注意的：

1、必须要先有一个基础的模板函数。

2、特化模板的格式：

```
1、template后面的尖括号里不写类型。
2、函数名后面填入类型。
```

在实际使用中，一般不这么干，有更加简单的办法。就是直接写同名函数，不做模板。

同名函数和模板，函数优先匹配。

```
bool IsEqual(char *&p1, char *&p2)
{
    return strcmp(p1, p2)==0;
}
```

# 类模板的特化

类的模板特化分为两种，一种是全特化，一种为偏特化

## 全特化

全特化就是把所有的模板类型都进行特化。

```
template<class T1, class T2>
class Test {

};
//全特化
template<>
class Test<int, char> {

};
```

## 偏特化

偏特化又可以分为两种：

1、部分特化。

2、类型限制。

### 部分特化

就是对部分模板类型进行特化。

```
//部分偏特化
template<class T1>
class Test<T1, char> {

};
```

### 类型限制

```
//类型限制
template<class T1, class T2>
class Test<T1*, T2*> {

};
```



参考资料

1、c++中模板的特化

https://blog.csdn.net/M_jianjianjiao/article/details/85220983