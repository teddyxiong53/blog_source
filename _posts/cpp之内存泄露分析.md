---
title: cpp之内存泄露分析
date: 2018-11-15 14:45:17
tags:
	- cpp

---


就用valgrind来测试一下。

```
std::string g_str;
void main()
{
    g_str = std::string(100, 'a');
}
```

这样并不会内存泄露。因为g_str不是一个指针。

而且我没有用new。所以也就不需要delete，也无法delete。

