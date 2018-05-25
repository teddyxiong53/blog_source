---
title: cpp之lambda表达式
date: 2018-05-20 17:53:31
tags:
	- cpp

---



cpp的lambda表达式是从c++11开始引入的。

利用这个可以定义匿名函数。

语法格式是：

```
[capture list] (params list) mutable exception-> return type {function body}
```

解释如下：

````
capture list: 捕获外部变量列表。
params list : 形参列表。
mutable指示符：用来说明是否可以修改捕获的变量。
exception：异常设定。
return type： 返回类型。
function body：函数实现部分。
````

一般常用的是这3种组合。

```
[capture list](params list) -> return type {}
[capture list](params list) {}
[capture list] {}
```

直接看例子。

```
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

bool cmp(int a, int b)
{
	return a<b;
}

int main()
{
	vector<int> myvec{1,3,2};
	vector<int> yourvec(myvec);
	//普通方式。
	sort(myvec.begin(), myvec.end(), cmp);
	for(int i: myvec) {
		cout << i << ' ';
	}
	cout << endl;
	//lambda函数方式。
	sort(yourvec.begin(), yourvec.end(), [](int a, int b) -> bool {return a<b;});
	cout << "lambda:" << endl;
	for(int i: yourvec) {
		cout << i << ' ';
	}
	cout << endl;
}

```



# 参考资料

1、C++ 11 Lambda表达式

https://www.cnblogs.com/DswCnblog/p/5629165.html

