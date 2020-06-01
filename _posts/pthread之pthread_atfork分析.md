---
title: pthread之pthread_atfork分析
date: 2020-05-30 18:36:38
tags:
	 - C语言

---

1

pthread_atfork

```
原型：
	pthread_atfork(
		void (*prepare)(void),
		void (*parent)(void),
		void (*child)(void)
	);
可以看到参数是3个函数指针。都是不带参数，没有返回值的。

```

prepare函数是在fork之前调用，这样child进程可以获取parent进程的所有锁。

child函数则是child进程里调用，这样可以unlock从prepare那里得到的所有parent进程的锁。

parent函数，是在fork创建了child进程后，但是在fork返回之前，在parent进程的环境里调用的。一般在这里面对prepare获得的锁进行解锁。


使用场景





参考资料

1、pthread_atfork解读

https://blog.csdn.net/codinghonor/article/details/43737869