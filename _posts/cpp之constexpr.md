---
title: cpp之constexpr
date: 2019-02-22 14:06:51
tags:
	- cpp
---





constexpr是constant express，常量表达式。

对于3+4这样的表达式，总是等于7 。

编译器一般会把这种进行优化掉。

在C++03里。下面的代码是非法的。

````
int GetFive(){
	return 5;
}
int some_value[GetFive() + 7];
````

c++11里，可以这样来保证合法。

```
constexpr int GetFive(){
	return 5;
}
int some_value[GetFive() + 7];
```



参考资料

1、

https://zh.wikipedia.org/wiki/C%2B%2B11