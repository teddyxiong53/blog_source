---
title: cpp之类型萃取
date: 2019-04-12 17:17:30
tags:
	- cpp

---





什么是类型萃取？做什么用的？

在编译时计算、查询、判断、转换、选择，增强了泛型编程能力。

举例：

```
#include <iostream>
#include <type_traits>

int main() {
    std::cout << "is_const:" <<std::endl;
    std::cout << "int:" << std::is_const<int>::value << std::endl;
    std::cout << "const int:" << std::is_const<const int>::value << std::endl;
}
```





参考资料

1、C++类型萃取之type_traits和type_info

https://blog.csdn.net/wf19930209/article/details/79312006