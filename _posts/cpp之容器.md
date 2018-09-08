---
title: cpp之容器
date: 2018-09-01 14:36:31
tags:
	- cpp

---



顺序容器

array：静态数组。

vector：动态数组。

deque：双端队列。

forward_list：单链表。

list：双链表。



关联容器：

set

map：

multiset：

multimap：



无序关联容器：

unsorted_set：

unsorted_map：

unsorted_multiset：

unsorted_multiset：



# 顺序容器

## array

隐式成员函数：

```
构造函数
析构函数
operator=
```

元素访问：

```
at
operator[]
front
back
data
```

迭代器：

```
begin
end
```

容量：

```
empty
size
max_size
```

操作：

```
fill
swap
```



```
#include <iostream>
#include <string>
#include <iterator>
#include <algorithm>
#include <array>

int main()
{
	std::array<int,3> a1 {{1,2,3}};//c++11里要求双大括号，c++14不要求。
	std::array<int, 3> a2 = {1,2,3};//如果有=号，则都不需要双大括号
	std::array<std::string, 2> a3 = {std::string("aa"), "bb"};
	
	std::sort(a1.begin(), a1.end());
	std::reverse_copy(a2.begin(), a2.end(), std::ostream_iterator<int>(std::cout, " "));
	
	std::cout << '\n';
	for(const auto& s: a3) {
		std::cout << s<< ' ';
	}
	std::cout << '\n';
}
```

## vector





# 参考资料

1、容器库

https://zh.cppreference.com/w/cpp/container