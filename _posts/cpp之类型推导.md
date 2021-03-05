---
title: cpp之类型推导
date: 2019-04-12 15:34:30
tags:
	- cpp

---



c++11引入了auto和decltype这2个关键字来实现类型推导。

通过这2个关键字，可以：

1、方便地获取复杂的类型。

2、简化书写，提高代码的可读性。

这个推导都是在编译时完成的，而不是运行时。



# auto

auto本来就是C语言里的关键字，但是很少用。

所以c++11就改变了这个关键字的内涵。

看例子：

```
int x = 0;
auto *a = &x; //auto == int
auto b = &x ;//auto == int *
auto &c = x; //auto == int
auto d = x; //auto == int
```

规则：

```
1、当不声明为指针或者引用时，auto的推导结果 跟 （初始化表达式抛弃 引用 和cv限定符 之后的）结果一样。
2、当声明为指针或引用时，auto的推导结构将保持初始化表达式的cv属性。
```

## auto的限制

1、不能用在函数参数里。

2、不能用在非static的成员变量。

3、不能定义数组。

## 什么时候用auto

一般是遍历容易的迭代器。

有时候不清楚数据类型的时候。



# decltype

为什么需要decltype？

可以在不定义变量的情况下，获得类型。

decltype是用来推导一个表达式的类型。

语法是这样：

```
decltype(expr)
```

decltype很像sizeof。

看例子：

```
int x = 0;
decltype(x) y = 1; // int y = 1;
decltype(x+y) z = 0; //int z = 0;

const int& i = x;
decltype(i) j = y; // const int& j = y;
```



## decltype应用

主要是用在泛型编程里。

我们先看没有decltype时，存在什么问题。

```
template<class T>
class Foo<const T>
{
	typename T::iterator it_;
public:
	void func(const T& t) {
		it_ = t.begin();
	}
};

int main()
{
	typedef const std::vector<int> container_t;
	container_t arr;
	
	Foo<container_t> foo;
	foo.func(arr);
	return 0;
}
```

这个编译会报错。

因为我们传递进去的是const的。

只能用const_iterator。

为了解决这种问题，c++98和c++03只能单独把const类型的容器单独声明一个。

这样代码就很冗余了。

而有了decltype，我们可以这么做。

```
template<class T>
class Foo<const T>
{
	decltype(T().begin()) it_;
public:
	void func(const T& t) {
		it_ = t.begin();
	}
};
```



decltype还经常用在变量表达式的类型抽取上。

如下：

```
vector<int> v;
decltype(v)::value_type i = 0;
```

很多标准库里，定义类型，现在都是用decltype来做的里了。

例如：

``` 
typedef decltype(sizeof(0)) size_t;
```



# auto和decltype综合运用

就是返回类型后置语法。

```
template <typename T, typename U>
auto add(T t, U u) -> decltype(t+u){
	return t+u;
}
```



参考资料

1、《深入应用c++11》

