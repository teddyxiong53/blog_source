---
title: 《Linux多线程服务端编程》读书笔记
date: 2019-02-22 14:5-:51
tags:
	- cpp
---





# 1.线程安全的对象生命周期

一个线程安全的class应该满足下面3个条件：

```
1、多个线程同时访问时，行为要正确。
2、无论os如何调度这些thread，都要正确。
3、调用者的代码无需额外的同步。
```

根据这个定义，c++标准库里的大多数class都不是线程安全的。

包括：string/vector/map这些。

因为这class需要额外加锁才能保证安全。

为了后面的讨论，需要先实现2个类：MutexLock和MutexLockGuard。

我们要讨论的大部分类，都要求是不可复制的，所以几乎所有类都继承这个类。

```
class nocopyable {
public:
	nocopyable(const nocopyable&) = delete;
	virtual operator=(const nocopyable &) = delete;
protected:
	nocopyable() = default;
	~nocopyable() = default;
};
```

```
#include <pthread.h>

class MutexLock : nocopyable {
public:
	MutexLock(): holder_(0) {
		pthead_mutex_init(&mutex_, NULL);
	}
	~MutexLock() {
		pthread_mutex_destroy(&mutex_);
	}
	void lock() {
		pthread_mutex_lock(&mutex_);
		//assignHolder();
	}
	void unlock() {
		pthread_mutex_unlock(&mutex_);
		//unassignHolder();
	}
private:
	friend class Condition;
private:
	pthread_mutex_t mutex_;
	pid_t holder_;
};

class MutexLockGuard: nocopyable {
public:
	MutexLockGuard(MutexLock& mutex): mutex_(mutex) {
		mutex_.lock();
	}
	~MutexLockGuard() {//注意这里是在析构函数里进行解锁的。这个技巧很好。
		mutex_unlock();
	}
private:
	MutexLock& mutex_;
};
```

编写单个的线程安全的class并不难。只需要用同步原语来保护它的内部状态就可以了。

class本身是安全的，但是如果class是动态创建并且通过指针来访问的，对象销毁时的竞争状态可能还是存在的。



对象构造要做到线程安全，唯一的要求就是不要在构造期间泄露this指针。

具体操作上，是需要做到；

```
1、不要在构造函数里注册任何回调。
2、不要在构造函数里把this传递给跨线程的对象。
```

注册回调，这个对于observer模式是很常见的。

解决方法就是单独用一个函数来注册。在构造函数之外。

相比于构造的安全性，析构的安全性问题更加验证。

作为成员变量的mutex，不能保护析构。



在面向对象的设计里，对象之间的关系主要有3种：组合、聚合、关联。



解决这个问题，要使用智能指针。



shared_ptr<T>是一个类模板。

实现上是原子操作，性能很好。



c++里的内存问题有下面几种：

```
1、缓冲器溢出。
2、空指针、野指针。用shared_ptr。
3、重复释放。用unique_ptr。
4、内存泄露。用unique_ptr。
5、不配对的new[]/delete。用vector替代数组。
6、内存碎片。
```

正确使用智能指针，可以很好地解决前面5个问题。



java是支持并发编程最好的主流语言，c++11就从java借鉴了不少的东西。



# 2.线程同步精要

并发编程有两种基本模型：

```
1、message passing。
2、share memory。
```

对于分布式系统，只能用message passing。

对于单击的，也可以用message passing来统一实现。

这样分布式的扩容就比较方便。



线程同步的四项原则：

```
1、尽量减少共享的对象。
2、优先使用高级的并发编程构件，如TaskQueue、CountDownLatch。
3、不得已要使用底层同步原语时，只使用mutex。
4、不自己编写lock-free的代码。
```

## mutex

使用原则：

```
1、用RAII手法封装create、destroy、lock、unlock这4个操作。用RAII手法，就不存在会忘记解锁的情况。
2、只使用非递归的mutex。
3、不要手动调用lock和unlock。
```

次要原则：

```
1、不使用跨进程的mutex。进程间通信只用tcp socket。
2、加锁解锁在同一个线程。
3、必要时，可以用PTHREAD_MUTEX_ERRORCHECK来查错。
```

使用非递归的mutex，是为了让问题暴露地更加明显。

递归的mutex，可能会暂时隐藏问题。



为了避免死锁问题，可以把函数分解为2个版本：

1、Xxx。

2、XXXWithLock。

## condition

condition只有一种正确的使用方式，几乎不可能用错。

对于wait端：

```
1、必须与mutex一起使用。
2、在mutex上已上锁的时候，才能调用wait。
3、把判断调节和wait放到while循环里。
```

写成代码就是：

```
muduo::MutexLock mutex;
muduo::Condition cond(mutex);
std::deque<int> queue;

int deque() {
	MutexLockGuard lock(mutex);
	while(queue.empty()) {
		cond.wait();//这一步会自动unlock mutex并进入等待。

	}
	int top = queue.front();
	queue.pop_front();
	return top;
}
```

对于notify端：

```
void enqueue(int x) {
    MutexLockGuard lock(mutex);
    queue.push_back(x);
    cond.notify();
}
```

condition也是底层同步原语，很少直接使用。

一般用它来实现高级同步措施。例如BlockingQueue或CountDownLatch。



## 线程安全的singleton的实现

以前大家认为double checked locking(DCL)是最合适的做法。兼顾了效率和正确性。

后来有人发现由于乱序执行的影响，DCL靠不住。

java5修改了内存模型，并给volatile赋予了acquire/release语义，使得java里的DCL又变得安全了。

但是c++里还没有好。

其实可以通过pthread_once来做单例。靠pthread库来保证安全性。



# 3.多线程服务器的适用场合与编程模型

网络应用程序的功能可以归纳为：

1、收到数据。

2、算一算。

3、发出去。

## 进程与线程

可以把进程比喻为人，进程间通信是交谈。

在同一个机器是进程，相当于面对面的2个人。

不同机器上的进程通信，相当于电话会议。需要问一下，某某在吗，才能顺利交谈。

线程的概念，在1993年才开始流行起来的。

unix出现已经很久了。线程的出现，给unix带来了不少的麻烦。

很多的C库函数，例如ctime、strtok都不是线程安全的。需要重新定义。

signal的语义也复杂化了。

1995年，pthread标准确立。

线程的特点是共享地址空间，从而可以更加高效地共享数据。

## 单线程服务器的常用编程模型

非阻塞io + io多路复用 = reactor模式。

这个是最常用的。

lighttpd和libevent就是用的这种模型。

Reactor模型的优点很明显：

```
1、编程不难。
2、效率也不错。
```



## 多线程服务器的常用编程模型

非阻塞io + one loop per thread模型。

在这种模型下，程序里每个io线程有一个event loop（也叫Reactor），用于处理读写和定时事件。



## 进程间通信只用tcp

通信方式有很多，我们只选择最通用的tcp socket方式。

好处是：

```
1、可以跨主机。
2、有伸缩性。
```

tcp方式和pipe方式比较：

```
相同点：
1、都是操作文件描述符。
2、都是收发字节流。
3、都可以用read、write、fcntl、select、poll。

不同点：
1、pipe是单向的。要双向通信还得开2个文件描述符，不方便。
2、pipe还要求进程为父子关系。

```

tcp的优点：

```
1、tcp port由一个进程独占，且os会自动回收。即使进程意外退出，也不会给系统留下垃圾。
2、两个进程通过tcp通信，如果一个挂了，另外一个很快就可以感知到。
3、tcp的天生好处就是“可记录、可重现”。可以用tcpdump进行分析，用tcpcopy进行压力测试。
4、tcp还能跨语言，客户端和服务端可以不用同一种语言。
5、tcp的local吞吐量也很高。
```



多线程不是银弹，有些场景必须使用单线程。

```
1、程序可能会fork。
2、需要限制程序的cpu占用率。
```



单线程程序的优点：

```
简单。
io多路复用的event loop。
```



适用多线程的场景：

```

```



一个多线程的服务端程序里的线程可以分为3类：

```
1、io线程。这个线程的主循环的io多路复用。阻塞在select上。
2、计算线程。
3、第三方库用的线程。
```

服务器程序不会频繁创建和销毁线程。



# 4.c++多线程系统编程精要

## 基本线程原语的选用

pthread的函数有110个左右。

但是常用的不过10个左右。

最常用的11个pthread函数是：

```
pthread的create和join。
mutex的创建、销毁、加锁、解锁。
condition的创建、销毁、等待、通知、广播。
```

## 系统库的线程安全性

unix系统库的接口风格是在70年代确立的。

线程则是在90年代才出现的。

线程的出现给系统库带来了冲击。破坏了20年来的一贯的编程传统和假定。

不过经过这些年的改进，现在glibc的函数大部分都是线程安全的了。





# 5.高效的多线程日志

在服务器端编程时，要做到log everything all the time。

对于关键进程，需要记录：

```
1、收到的每条内部消息的id。
2、每条外面消息的全文。
3、发出的每条消息的全文。
4、关键内部状态的变更。
```

关键要有时间戳。

诊断日志不仅是给程序员看的，还是给运维人员看的。

一个日志库可以分为前端和后端2部分。

前端是供应用程序使用的api。

后端负责把日志写到目的地。

关键在于多个前端同时跟后端通信。

这是一个典型的多个生产者单个消费者的问题。

对于前端，要做到：

```
低延迟
低cpu开销。
无阻塞。
```

对于后端，要做到：

```
足够大的吞吐量。
较少的资源占用。
```

c++的日志库，整体上前端有2种风格的接口：

```
1、类似printf的风格。
log_info("xxx")
2、c++的<<风格。
LOG_INFO << "xxx";
```

我们选择后面这种。

muduo自己实现了LogStream类，而没有使用iostream，主要是考虑性能。

对于log4j这种日志库，考虑非常全面，

```
1、日志多个级别。
2、日志目的地可以是多个，文件、socket等。
3、格式可配置。
4、运行时过滤器。
```

只有第一项是必须的。其余都可以不要。

对于分布式系统，最安全的是写到本地文件。

既然是写到本地文件，那么日志文件的rotate就是必须的。

rotate的条件一般是2个：文件大小、时间。



# 8.muduo网络库设计与实现

给EventLoop加锁定时器功能。

传统的Reactor通过控制select或者poll的等待时间来实现定时。

而现在的Linux有了timerfd，我们可以用和处理io事件相同的方式来处理定时。代码的一致性更好。

```
s00
	这个只有EventLoop这个文件。
	直接在loop函数里调用poll函数。
s01
	增加了Channel和Looper这2个文件。
	这2个类被EventLoop包含使用。
	EventLoop的loop函数，调用Looper的loop函数，Looper的loop函数里才调用poll函数。
	Channel被EventLoop和Looper都使用了。
	Poller是对io多路复用机制的封装。
	到这里，Reactor模式的基本类都有了。
s02
	这个加入了定时器的。
	在Linux没有加入timerfd之前，一般是通过设置select和poll的超时时间来做定时处理的。
	
```

