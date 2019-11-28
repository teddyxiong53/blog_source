---
title: muduo之protobuf使用
date: 2019-11-27 15:01:06
tags:
	- 网络
---



1

我使用的muduo-cpp11的版本。

之前一直是把protobuf注释掉的。

现在把我本地的修改都放弃，跟github上的进行一次同步。

cpp11是在muduo代码里一个branch。不是单独的项目。

看muduo的readme里：

```
Requires:
  Linux kernel version >= 2.6.28.
  GCC >= 4.7 or Clang >= 3.5
  Boost (for boost::any only.)
```

用build.sh编译，还是报错。

在顶层的CMakeLists.txt里加上这个。

```
 -D_GLIBCXX_USE_CXX11_ABI=0
```

现在报错这个：

```
CMakeFiles/logstream_test.dir/LogStream_test.cc.o：在函数‘boost::unit_test::make_test_case(boost::unit_test::callback0<boost::unit_test::ut_detail::unused> const&, boost::unit_test::basic_cstring<char const>)’中：
/usr/include/boost/test/unit_test_suite_impl.hpp:255：对‘boost::unit_test::ut_detail::normalize_test_case_name(boost::unit_test::basic_cstring<char const>)’未定义的引用
```

我单独把这个文件里注释成空的，加上一个空的main函数。

但是还有其他的unittest的。

有没有开关可以统一把unittest的都关闭掉？

有的：

```
./CMakeLists.txt:62:find_library(BOOSTTEST_LIBRARY NAMES boost_unit_test_framework)
```

但是关闭这个了。前面protobuf的问题还是有。

算了，我暂时不弄这个了。

PROTOBUF_FOUND 这个代码里没有看到哪里赋值，但是通过message打印出来看，是TRUE。

我手动赋值为FALSE。编译。

但是有一堆的boost的错误了。

```
对‘boost::program_options::to_internal(std::string const&)’未定义的引用
```

把本地的改动全部放弃。

直接把find_package(protobuf)这一行注释掉，重新编译，这样可以正常编译过。





参考资料

1、在muduo编译阶段，报出大量protobuf未定义行为，网上找出两种解决方案，但是不理解怎么实现？

https://www.zhihu.com/question/264169902