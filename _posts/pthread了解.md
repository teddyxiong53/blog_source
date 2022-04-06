---
title: pthread了解
date: 2018-02-06 10:43:30
tags:
	- pthread

---



# 基本情况

pthread是posix标准里定义的线程规范。

包括了这些内容：

1、类型。

2、函数。

3、常量。



包含的文件是：

1、pthread.h头文件。

2、libpthread.a。



大约100个API函数。都以pthread_开头。

分两大类：

1、线程管理。create、detach、join、set、get等。

2、线程通信。Mutex、cond、r/w lock、sem、消息队列mq。

前缀如下：

```
pthread_
pthread_attr_

pthread_mutex_
pthread_mutexattr_

pthread_cond_
pthread_condattr_
pthread_rwlock_
pthread_rwlockattr_
pthread_spin_
pthread_barrier_
pthread_barriesattr_
sem_
mq_

```

返回值：

成功返回0，错误码在errno.h里定义。

