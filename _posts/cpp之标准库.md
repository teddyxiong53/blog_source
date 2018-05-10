---
title: cpp之标准库
date: 2018-05-09 15:49:54
tags:
	- cpp

---



cpp的标准库可以分为两部分：

1、标准函数库。不属于任何类。继承自C语言。

2、面向对象类库。



标准函数库包括：

```
1、输入输出。
2、字符串。
3、数学。
4、时间。
5、动态分配。
6、其他。
7、宽字符。
```

面向对象类库：

```
1、标准C++ io库。
2、string类。
3、数值类。
4、STL容器。
5、STL算法。
6、STL函数对象。
7、STL迭代器。
8、STL分配器。
9、本地化库。
10、异常处理库。
11、其他。
```

我们下面重点关注面向对象类库。

#标准io库

iostream的内容就是这样。/usr/include/c++/5/iostream

```
namespace std 
{
  extern istream cin;       /// Linked to standard input
  extern ostream cout;      /// Linked to standard output
  extern ostream cerr;      /// Linked to standard error (unbuffered)
  extern ostream clog;      /// Linked to standard error (buffered)
} // namespace
```





# 算法

非改变类的：

```
all_of：
any_of：
none_of：
for_each：
find_if：
...
```

改变类的：

```
copy
move
transform

```

排序相关的：

```
sort
stable_sort

```

# 数值类的



# 容器相关





# vector用法

vector是cpp里的一种数据结构。相当于一个动态数组。

用法：

```
#include <vector>
using namespace std;
```

简单例子。

```
#include <string>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;

int main()
{
	vector<int> v = {1,2,3};//这种要c++11语法才支持。
	v.push_back(4);
	v.push_back(5);

	for (int n: v) {
		cout << n << endl;
	}
}
```



# 参考资料

1、C++ 标准库

http://www.runoob.com/cplusplus/cpp-standard-library.html

2、C++ 标准库

https://blog.csdn.net/wancongconghao/article/details/77624003

3、cpp参考手册

http://zh.cppreference.com/w/cpp/container/vector


