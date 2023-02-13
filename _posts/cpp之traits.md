---
title: cpp之traits
date: 2023-02-09 15:31:17
tags:
	- cpp

---



C++ 的 traits 技术，是一种约定俗称的技术方案，

用来为同一类数据（包括自定义数据类型和内置数据类型）提供统一的操作函数，

例如 advance(), swap(), encode()/decode() 等。



首先来看 traits 技术可以解决什么问题，我们拥有自定义类型 Foo, Bar，以及编译器自带类型 int, double, string，我们想要为这些不同的类型提供统一的编码函数 decode() ，该怎样实现呢？

# 方案一

首先想到的方案，就是进行函数重载。

```
// 内置类型 int, double
void decode(const int data, char* buf);
void decode(const unsigned int data, char* buf);
void decode(const double data, char* buf);
// 自定义类型 Foo, Bar
void decode(const Foo& data, char* buf);
void decode(const Bar& data, char* buf);
```

这种方案当然可行，但我们不满足于此，因为每增加一种数据类型就需要重新实现一个函数，而同一类数据（int, unsinged int）可以使用同样的编码方法。我们想要的是针对同一种数据类型，只编写一个函数，这样有可能实现吗？

# 方案二

下面我们尝试使用模板函数来实现，自定义数据类型中定义类型字段，然后在函数中进行判断。

```text
// 自定义类型
enum Type {
  TYPE_1,
  TYPE_2
};
class Foo {
  Type type = Type::TYPE_1;
};
class Bar {
public:
  Type type = Type::TYPE_2;
};
// 模板函数
template<typename T>
void decode(const T& data, char* buf) {
  if(T::type == Type::TYPE_1) {
    ...
  }
  else if(T::type == Type::TYPE_2) {
    ..
  }
  ...
}
```

这样一来，对于同一种自定义类型，我们只需要写一遍 decode 函数就可以了，但是对于系统自定义变量 int, double 而言，是无法在其内部定义 type 的，这时候我们该怎么办呢？这时候就需要用到 traits 技术了。

# 方案三

traits 技术的关键在于，使用另外的模板类 type_traits 来保存不同数据类型的 type，这样就可以兼容自定义数据类型和内置数据类型，代码如下：

```text
// 定义数据 type 类
enum Type {
  TYPE_1,
  TYPE_2,
  TYPE_3
}
```

对于自定义类型，与方案二中类似，我们在类内部定义了数据类型 type，然后在 traits 类中定义同样的 type

```text
// 自定义数据类型
class Foo {
public:
  Type type = TYPE_1; 
};
class Bar {
public:
  Type type = TYPE_2; 
};
template<typename T>
struct type_traits {
  Type type = T::type;
}
```

对于内置数据类型，使用模板类的特化为自定义类型生成独有的 type_traits

```text
// 内置数据类型
template<typename int>
struct type_traits {
  Type type = Type::TYPE_1;
}
template<typename double>
struct type_traits {
  Type type = Type::TYPE_3;
}
```

这样就可以为不同数据类型生成统一的模板函数

```text
// 统一的编码函数
template<typename T>
void decode<const T& data, char* buf) {
  if(type_traits<T>::type == Type::TYPE_1) {
    ...
  }
  else if(type_traits<T>::type == Type::TYPE_2) {
    ...
  }
}
```



# **总结**

- traits 技术的关键在于使用第三方模板类 traits，利用模板特化的功能，实现对自定义数据和编译器内置数据的统一
- tratis 技术常见于标准库的实现中，但对日常开发中降低代码冗余也有很好的借鉴意义
- C++20 提供了 Concept 的特性，使用 Concept 可以使得实现类似的功能更加方便
- 本文所举的例子使用了枚举变量来表示数据类型(type)，而实际操作中通常使用不同的类来表示不同的类型，这样可以在编写模板函数时更好的优化，这里就不做展开，感兴趣的可以参考《Effective C++》的第47条





# 参考资料

1、C++ 的 traits 技术到底是什么？

https://zhuanlan.zhihu.com/p/413864991