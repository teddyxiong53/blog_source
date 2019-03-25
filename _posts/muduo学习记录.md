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

然后打算写Thread.h。发现里面依赖了Atomic.h。所以先写Atomic.h。这里面的知识点是gcc的原子操作。

然后发现Thread.h依赖了CountDownLatch.h。CountDownLatch.h依赖了Condition.h。

所以先写Condition.h.

这里涉及到的知识点：friend友元。UnassignGuard 这个是为了方便借助RAII来进行持有者id的清零和置位。为什么需要这么做呢？只有Condition这里这么用了。

Condition.h有一个函数放在了Condition.cc里实现，所以新建Condition.cc文件。

然后就是CountDownLatch.h。这个里面3个成员变量：mutex、cond、count。

2个主要函数：wait和countDown。

现在可以开始写Thread.h了。

发现Thread.cc还依赖了Exception.h。这个倒不复杂。涉及到的知识点是是std::exception。

还依赖Timestamp.h。

```
Timestamp里的知识点：
1、继承copyable类。这个类很简单，就是定义要求默认的无参构造和析构函数。
2、boost的equality_comparable和less_than_comparable。
```

Thread.cc写完了。

上传一个版本。

在base目录下，新建tests目录，修改CMakeLists.txt文件，写一些测试代码。











