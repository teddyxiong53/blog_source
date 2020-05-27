---
title: cpp之map和pair关系
date: 2020-05-26 14:19:08
tags:
	- cpp

---

1

pair一般是作为元素，放入到一个map里。也可以放入到其他容器里，例如set、vector。



```
map<string, int>::key_type v1; //string
map<string, int>::mapped_type v2; //int
map<string, int>::value_type v3; //pair<const string, int>
```

map 是以 pair形式插入的。

在<map>的源代码里。

````
public:
	using key_type = _Kty;
	using value_type = pair<const _Kty, _Ty>;
	using key_compare = _Pr;
````



参考资料

1、c++如何理解map对象的value_type是pair类型

https://zhidao.baidu.com/question/468116809.html