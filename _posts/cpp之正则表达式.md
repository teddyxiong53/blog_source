---
title: cpp之正则表达式
date: 2019-07-04 16:47:37
tags:
	- cpp
---

1

c++提供了对正则表达式的支持。

```
void test()
{
    std::cout << std::regex_match("123", std::regex("\d+")) << std::endl;//不能匹配。
    std::cout << std::regex_match("123", std::regex("\\d+")) << std::endl;//可以匹配。
}
```

需要对反斜杠进行转移，不然不支持。

regex_match函数是对整个字符串进行匹配。

怎么获得匹配的结果？

有两种方式：

```
1、std::match_results<std::string::const_iterator> result;
2、std::smatch result;//
```

推荐使用第二种，简洁多了。



参考资料

1、C++ 使用正则表达式

https://blog.csdn.net/tojohnonly/article/details/78326633

