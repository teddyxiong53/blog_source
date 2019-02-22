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



