---
title: cpp之muduo代码学习
date: 2018-10-09 17:28:51
tags:
	- cpp

---



muduo是c++写的多线程网络库。

作者是陈硕。他的博客在这里：https://blog.csdn.net/solstice/



这个是基于boost库写的，而不是标准STL。

但是作者也写了cpp11的分支。其实有不少的分支。

```
git clone https://github.com/chenshuo/muduo 
切换分支
git checkout -b cpp11 origin/cpp11
```

编译：

```
./build.sh -j4
```

把examples目录下的PROTOBUF_FOUND分支里的都注释掉。不知道为什么当前编译不过。

编译生成的文件都在build/release-cpp11/bin目录下。

simple_echo。对应simple目录下的echo程序。

对比一下master版本和cpp11分支的改动点。

| boost::bind                | std::bind       |
| -------------------------- | --------------- |
| boost::ptr_container::move | std::move       |
| boost::nocopyable          | 自己实现        |
| BOOST_STATIC_ASSERT        | static_assert   |
| boost::function            | std::function   |
| boost::scoped_ptr          | std::unique_ptr |
| boost::shared_ptr          | std::shared_ptr |

区别不是很大。





muduo的设计目标用途是公司内部的分布式系统。



muduo里的大部分类都是noncopyable。



我通过对recipes代码的编写。对muduo的基本类都有一些了解了。

现在看examples里的例子。

看看muduo可以怎样实际应用。



