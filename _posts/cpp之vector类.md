---
title: cpp之vector类
date: 2018-11-17 15:24:28
tags:
	 - cpp

---



#迭代vector

```
#include <iostream>

#include <string>
#include <vector>

std::vector<std::string> g_str_vector;
void func()
{
	for(int i=0; i<5; i++) {
		g_str_vector.push_back(std::to_string(i));
	}
}
int main()
{
	func();
	int size = g_str_vector.size();
	int i=0;
	std::vector<std::string>::iterator it;
	for(it=g_str_vector.begin(), i=0; it!=g_str_vector.end(); it++, i++) {
		if(i<size-1) {
			std::cout << *it << ", ";
		} else {
			std::cout << *it << "\n";
		}
	}
}

```



#索引

```
[]和at()的区别？
```

如果vector非空，那么这二者作用是一样的。

如果vector为空，at会抛异常。

而[]的方式，没有定义，是会内存越界的。

而c++标准不要求[]进行下标越界检查，因为检查会降低效率。



#如何判断2个vector是否相等





# 清空操作



# 在vector里搜索pair

这个需要使用find_if，而不是find。



参考资料

1、vector的下标索引与at的区别

https://blog.csdn.net/heroesjun/article/details/48415863

2、【C++】判断两个vector是否相等～直接用“==”呀～

https://blog.csdn.net/liuchuo/article/details/52486206

3、C++ vector清空元素的三种方法

https://blog.csdn.net/weixin_30897079/article/details/97119054

4、对vector中的pair进行多次find操作

https://blog.csdn.net/j_cou/article/details/83044739

5、

https://stackoverflow.com/questions/15499590/find-in-stdvectorstdpair