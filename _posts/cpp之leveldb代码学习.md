---
title: cpp之leveldb代码学习
date: 2018-10-12 14:37:51
tags:
	- cpp
---



leveldb是谷歌的一个开源key-value数据库。

可以支持billion级别的数据量了。

设计非常好，性能很高。

是单进程服务。

我觉得这个程序，对我的意义，就是可以认真学习非c++11风格的c++代码的写法。

leveldb的主要使用场景是什么呢？

到github上下载代码，编译。

```
mkdir -p build && cd build
cmake -DCMAKE_BUILD_TYPE=Release .. && cmake --build .
```

编译完了，得到一堆的测试程序。

我们看看db_test这个做了什么。

测试花了不少的时间。

最后的打印是：

```
==== PASSED 54 tests
```

把db_test.cc的代码走读一遍。



代码风格的谷歌的风格，用xx_这种后面带下划线的方式来表示成员变量。

```
Env：被leveldb用来访问os的文件系统等内容。
	EnvWrapper：对Env的简单包装。
		SpecialEnv
```

```
SequentialFile
RandomAccessFile
WritableFile

FileLock
```



Status

这个类封装了操作的返回结果。

```
 private:
  // OK status has a null state_.  Otherwise, state_ is a new[] array
  // of the following form:
  //    state_[0..3] == length of message
  //    state_[4]    == code
  //    state_[5..]  == message
  const char* state_;
```

Slice类

简单类，包含一个指针和size，



```
Options
ReadOptions
WriteOptions
```



# 参考资料

1、LevelDB（适用于写多读少场景）

https://blog.csdn.net/qq_26222859/article/details/79645203