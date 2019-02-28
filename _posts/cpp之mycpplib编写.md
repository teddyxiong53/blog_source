---
title: cpp之mycpplib编写
date: 2019-02-25 14:38:17
tags:
	- cpp

---



这个是把陈硕的recipes这个代码库学习一遍。

学习到的技巧。

```
1、为了避免包含循环包含头文件，可以进行前向类型声明。
	例如声明：struct tm;然后就可以在头文件里使用了，不需要包含time.h了。

```

编码风格：

```
1、成员变量最后跟一个下划线。
2、常量用k做前缀。
```



自己写一遍。

```
hlxiong@hlxiong-VirtualBox ~/work/test/mycpplib $ tree         
.
├── datetime
│   ├── copyable.h
│   ├── TimeZone.cc
│   └── TimeZone.h
├── logging
└── thread
```

本来是打算先写logging的，但是发现logging下面用到了Timestamp。所以就先写datetime目录。

```
1、先写copyable.h。
	这个里面就是一个空类。表示保留拷贝构造函数。
2、写Date.h和Date.cc。
	因为TimeZone依赖了这个类。
	这里有儒略历，但是这个历法已经不用了啊。为什么要写这个呢？
	儒略历的只是中间值。不管。
3、TimeZone.cc里比较繁琐。没有什么价值，直接拷贝过来先。
4、看Timestamp.cc的。
5、写Date_test.cc和Date_unittest.cc这2个文件。
datetime部分就算写完了。
```

写logging部分：

```
1、先写LogStream。cc文件和h文件。然后写LogStream_test.c。可以单独运行测试。
2、然后写Logging文件。cc、h、test。
	但是Logging.cc里要用到Thread的东西。所以现在先写Thread的。
3、新建Thread.h。
	Thread.h里需要用到Atomic.h。Atomic只有头文件。
4、继续回到Logging.cc的编写。
	把Logging_test.cc写一下。
	发现要用到LogFile。把LogFile写一下。
	LogFile又用到Mutex了。所以先写Mutex。这个只有头文件。
5、接下来看异步logging的AsyncLoggingQueue.h。
	这个里面用到了thread目录下的几个类。所以现在又回到thread目录下去写。
	thread/BlockingQueue.h
		这个用到了Condition。所以先写Condition。
		这个只有头文件，很简单。
		把对应的测试文件也写一下。测试文件依赖了CountDownLatch.h。把这个先写一下。
	thread/BoundedBlockingQueue.h
		
	好了。可以开始写AsyncLoggingQueue.h了。
	算了。这个暂时不写了。因为没有用上。又比较复杂。
```



现在可以开始写reactor目录下的东西。这个是我的最终目的。

看看还缺什么，就加什么。

下面的目录，都是在前面一个的基础上拷贝修改。

s00

```
EventLoop.h和cc文件。
	只依赖了Thread。
```

s01

```
这个就有基本的形式了。
Channel和Looper都有了。
增加了test3.cc。测试了timerfd。
```

s02

```
增加了一个Callbacks.h文件。
	里面就定义了一个TimerCallback类型，typedef的。
增加了TimerId.h、Timer.h、TimerQueue.h这3个文件。

增加了test4.cc。测试定时器的行为。

```

s03

```
为EventLoop增加了几个接口。用起来更加方便。
增加了一个类：EventLoopThread。
	这个类就实现了这个理念：one loop per thread。
增加了test5 和test6 。

```



创建了EventLoop线程是IO线程。

IO线程的主要功能就是运行事件循环loop。

EventLoop对象的生命周期跟所属线程一样长，不必是heap对象。



muduo的接口设计会明确哪些成员函数是线程安全的，可以跨线程调用。

哪些线程只能在某个特定线程里调用（主要是io线程）。

所以需要检查当前的线程是哪个。



Reactor模式最核心的事件分发机制。

就是将io多路复用拿到的io事件分发给各个fd。



每个Channel对象之负责一个fd的io事件分发，但是它不拥有这个fd，也不会在析构的时候关闭这个fd。

Channel会把不同的事件分发给不同的回调，例如ReadCallback。

回调是用boost::function来做的。

用户无需继承Channel。Channel不是基类。

muduo的用户也一般不会直接使用Channel，而是使用更上层的封装。

例如TCPConnection。

Channel一般被包含在其他类里。

Channel的成员函数只能在io线程里调用。因此更新数据成员不用加锁（为什么？）



Poller是对io多路复用的封装。



EventLoop有一个非常实用的功能。

在它的io线程里执行某个用户回调。如果当前是在这个io线程里，是马上执行，否则是加入到队列。io线程会被唤醒来执行这个回调。

有了这个功能，我们就能轻易地在线程间调配任务，比如说把TimerQueue的成员函数调用放到io线程。这样就可以在不加锁的情况下保证线程安全性。

这个唤醒，是用eventfd。这个是跟timerfd类似的一个东西。是新的Linux特性。接口也类似。

用eventfd来做这个唤醒，效率很高，因为不用管理缓冲区。



io线程不一定是主线程。我们可以在任何一个线程创建并运行EventLoop。

一个程序有可以有不止一个io线程。

我们可以按优先级把不同的socket分给不同的io线程。避免优先级翻转。

为了方便使用，我们增加EventLoopThread这个类。



从一次poll到下一次poll，这个叫做一次事件循环。



继续写。

s04

```
增加了4个类。8个文件。
InetAddress。
Socket
SocketOps
Acceptor

```

我写的有问题，会导致出现errno为11的错误。资源不可用。

