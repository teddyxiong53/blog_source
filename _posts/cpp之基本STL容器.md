---
title: cpp之基本STL容器
date: 2018-05-10 22:11:07
tags:
	- cpp

---



c++里的容器有两种类型：

1、顺序容器。包括vector、list、deque。

2、关联容器。包括map和set。



容器类自动申请和释放内存，不要new和delete。



可以参考的学习材料有：

https://github.com/zouxiaohang/TinySTL

其实github上有不少的tinystl实现。

上面这个是star最多的。

https://github.com/mendsley/tinystl

这个是更加简单的版本。我就用mendsley这个版本学习一下。

代码不多。

我们先看看如何编译。

根据readme.md内容，下载premake工具。这个工具是用来生成vs工程的。

我们把下载的premake.exe文件拷贝到tinystl目录下。

```
premake.exe vs2015
```

我们就得到一个vs2015的工程。打开。

编译，提示没有UnitTest++.h。

```
libunittest++-dev 
```

但是unittest跑起来有点麻烦。

我还是自己来做。

在include目录下，新建一个test.cpp。

里面写入：

```
#include "TINYSTL/vector.h"
using namespace tinystl;

int main()
{
    vector<int> v1;                  
}         
```

编译：

```
g++ test.cpp -I./
```

这样可以编译过。



# vector

```
#include "TINYSTL/vector.h"
#include <iostream>

using namespace tinystl;
using namespace std;

int main()
{
    tinystl::vector<int> v1;
    v1.push_back(1);
    int len = v1.size();
    cout << "len: " << len << endl;
    v1.insert(v1.end(), 2);//
    //遍历
    tinystl::vector<int>::iterator iter = v1.begin();
    for(; iter!=v1.end(); iter++) {
        cout << *iter << "   ";
    }
    cout << endl;
}
```



# list

list和vector对比：

1、list是双向链表。vector内部是数组实现。

2、list插入和删除的效率高。

3、list的随机访问比较慢。



# deque

deque和vector基本相同，但是deque可以push_front，就在前面插入。



# unsorted_map

## 改

insert。



## 查

[]操作符

at

find

contains



# set

看set里是否有某个元素。

```
std::set<int> myset;
myset.count(1);//查看这个set里1这个元素的个数，如果为0，说明不存在。
```



# 容器性能比较



# 参考资料

1、C++ STL基本容器使用

https://www.cnblogs.com/cxq0017/p/6555533.html

2、

http://www.cppblog.com/sailing/articles/161659.html