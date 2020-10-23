---
title: stl之enable_if
date: 2020-10-14 13:45:30
tags:
	- cpp
---

1

`std::enable_if` 顾名思义，满足条件时类型有效。作为选择类型的小工具，其广泛的应用在 C++ 的模板元编程（meta programming）中。它的定义也异常的简单：

```
template <bool, typename T=void>
struct enable_if {
};
 
template <typename T>
struct enable_if<true, T> {
  using type = T;
};
```

由上可知，**只有当第一个模板参数为 `true` 时，`type` 才有定义，否则使用 `type` 会产生编译错误，**并且默认模板参数可以让你不必指定类型。

# 用法一：类型偏特化

在使用模板编程时，经常会用到根据模板参数的某些特性进行不同类型的选择，或者在编译时校验模板参数的某些特性。

```
template<typename T, typename Enable=void>
struct check;

template<typename T>
struct check<T, typename std::enable_if<T::value>::type> {
    static constexpr bool value= T::value;
};
```

上述的 `check` 只希望选择 `value==true` 的 `T`，**否则就报编译时错误**。**如果想给用户更友好的提示，可以提供结构体的原型定义，并在其中进行 `static_assert` 的静态检查，给出更明确的字符串说明。**

# 用法二：控制函数返回类型

# 用法三：校验函数模板参数类型

在jsonhpp里，就大量做了这种用途。

限制你你传递给模板的类型。

有时定义的模板函数，只希望特定的类型可以调用

这个一般跟std::is_pointer/ std::is_object等配合使用。

```
template<bool B, typename T = void>
using enable_if_t = typename std::enable_if<B, T>::type;

template <typename T>
struct iterator_traits < T, enable_if_t < !std::is_pointer<T>::value >>
            : iterator_types<T>
{
};
```



参考资料

1、std::enable_if 的几种用法

https://blog.csdn.net/jeffasd/article/details/84667090

