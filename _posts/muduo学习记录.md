---
title: muduo学习记录
date: 2019-03-22 10:38:32
tags:
	- muduo

---





决定用写的方式来进行学习。

参考c++11的版本。

先把目录结构建好。

```
hlxiong@hlxiong-VirtualBox ~/work/test/mymuduo/muduo $ tree
.
├── build.sh
├── CMakeLists.txt
├── compile_commands.json -> ../build/release-cpp11/compile_commands.json
└── muduo
    ├── base
    │   ├── CMakeLists.txt
    │   ├── date.cc
    │   └── Types.h
    └── net
        ├── CMakeLists.txt
        └── Poller.cc
```

开始写c++代码，从base目录里写起。

第一个文件是Types.h。

这个文件里没有什么优先的内容的，包含了几个其他头文件。

然后写CurrentThread.h。这个因为比较底层，不依赖其他的头文件。

然后写CurrentThread.h和cc文件。

然后noncopyable文件。

然后Mutex.h。这里发现一个知识点，MutexLockGuard的成员变量是引用类型的。

然后Singleton.h。用pthread_once来实现单例的。另外了解到sfinae的概念。







