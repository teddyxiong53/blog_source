---
title: srs之state-thread协程
date: 2020-11-06 11:12:30
tags:
	- 直播
---

1

协程是一种程序组件，也叫微线程。

一般我们把协程理解为自己实现调度，用于提高程序运行效率，降低开发复杂度的微线程。

协程在用户态实现调度。

而普通的线程的调度，需要切换到内核态。

协程这样就减少了换页操作，提高了效率。

开发者可以用同步的方式去进行代码开发。不需要考虑多线程开发的资源保护问题。



协程在处理异步等待事件的时候，有很大的优势。

例如io读写一般比较耗时，cpu在遇到io读写的时候，需要切换线程。

使用协程就可以直接在用户切换微线程。





state threads

协程库state threads library(以下简称st)是一个基于setjmp/longjmp实现的C语言版用户线程库或协程库（user level thread）。

是一个应用程序库，用来编写快速和可扩展的网络程序，基于类unix平台。

它结合了多线程编程范式的简易性（一个thread来处理一个连接）和io多路复用的高性能和扩展性。

也就是说，用多线程的方式来编程，从模型上看，比较直观，便于理解，但是效率不高。

而使用原生的io多路复用，效率高了，但是代码不直观。

st就是结合了二者的优点。

让代码又直观又高效。





基于setjmp和longjmp实现协程库基本步骤（下述线程指用户线程）：

1.需要用jmpbuf变量保存每一个线程的运行时环境，称为线程上下文context。

2.为每个线程分配（malloc/mmap）一个stack，用于该线程运行时栈，该stack完全等效于普通系统线程的函数调用栈。**该stack地址是在线程初始化时设置，所以不需要考虑setjmp时保存线程的栈上frames数据的问题。**

3.通过调用setjmp初始化线程运行时上下文，将context数据存放到jmpbuf结构中。然后修改其中的栈指针sp指向上一步分配的stack。根据当前系统栈的增长方向，将sp设置为stack的最低或最高地址。

4.线程退出时，需要返回到一个安全的系统位置。即，需要有一个主线程main thread或idle thread来作为其他线程最终的退出跳转地址。需要为主线程保存一个jmpbuf。

5.设置过main thread的jmpbuf后，需要跳转到其他线程开始执行业务线程。

6.实现一个context交换函数，在多个线程之间进行跳转：保存自己的jmpbuf，longjmp到另一个线程的jmpbuf。





每一个并发session的状态包括了它的stack状态。

跟通用的线程库不同，st是完全确定的。

st的线程切换只会在一组确定函数调用后才会发生。

在io函数、显式的同步点等等。

因此，大多数情况下，进程相关的全局数据，就不需要用mutex来进行保护。

这样就降低了编写难度，也提供了效率。

所有的st线程，具有相同的优先级。

调度是非抢占性的。

因为是数据驱动，也没有时间片轮转。

只有两种外部事件被st库的调度器处理。

因为底层是依赖select和poll机制。

两种外部事件是：io事件和定时器事件。

但是signal事件，也可以通过转化为io事件来得到处理。



st库是非常轻量级的用户态程序。





对外接口分析

头文件，就一个st.h。

数据类型

```
st_thread_t  ：void *类型
st_cond_t ：void *类型
st_mutex_t ：void *类型
st_utime_t  ：u64 
st_netfd_t  ：void *类型
st_switch_cb_t： void (*)(void)
```

错误处理

很简单，靠errno。

返回值：非负数，或者指针来表示成功。

-1或者NULL，表示失败。



库的初始化

```
int st_init();
	//这个应该最先被调用。st_set_eventsys 这个可以在前面。
int st_getfdlimit(void);
	//这个是获取最大的fd数量。看一下就好。
int st_set_eventsys(int eventsys);
	这个是设置io多路复用的模型。
	有这些取值：
	ST_EVENTSYS_DEFAULT
	ST_EVENTSYS_SELECT
	ST_EVENTSYS_POLL
	ST_EVENTSYS_ALT //我们用这个就好了。就是尽量使用更好的方式，例如在Linux上，就是尝试去使用epoll。如果没有，那么就是使用了ST_EVENTSYS_DEFAULT
	
int st_get_eventsys(void);
	这个是读取，看看设置是否成功了。
const char *st_get_eventsys_name(void);
	这个是打印名字。上面一个函数是打印数字，不直观。
	
st_set_switch_in_cb()
st_set_switch_out_cb()
	设置回调函数。
	
```

线程控制

```
//创建
st_thread_t st_thread_create(
	void *(*start)(void *arg), 
	void *arg,
	int joinable,
	int stack_size
);
//退出
void st_thread_exit(void *retval);
//等待
int st_thread_join(st_thread_t thread, void **retvalp);
//获取id
st_thread_t st_thread_self();
//打断
void st_thread_interrupt(st_thread_t thread);
//休眠
int st_sleep(int secs);
int st_sleep(st_utime_t usecs);

//一个提示性能的方式。把栈机制随机化。我不用这个。
int st_randomize_stacks(int on);
```



线程私有数据

```
int st_key_create(int *keyp, void (*destructor)(void *));
	创建一个key，非负数，可以被所有线程使用。
	key可以被st_thread_setspecific来操作。
int st_key_getlimit();
	获取最多可以创建的key的个数。看看就好了。
int st_thread_setspecific(int key, void *value);
void *st_thread_getspecific(int key);
```



同步

```
就mutex和cond的操作。
创建，销毁。
int st_cond_wait(st_cond_t cvar);
int st_cond_timedwait(st_cond_t cvar, st_utime_t timeout);
int st_cond_signal(st_cond_t cvar);
int st_cond_broadcast(st_cond_t cvar);
mutex的就lock和unlock。
```

时间

```
st_utime_t st_utime(void);
	获取us为单位的时间。跟时间戳没有关系。
	
int st_set_utime_function(st_utime_t (*func)(void));
	取代默认的st_utime函数。
	
int st_timecache_set(int on);
	
time_t st_time(void);
	这个获取就是时间戳的秒数了。
	
```



io函数

这些函数，跟默认的socket操作函数，有两点不同：

1、文件描述符，是st_netfd_t类型

2、多了一个st_utime_t的超时参数。

```
st_netfd_t st_netfd_open(int osfd);
	需要一个fd做为输入参数。
	会设置为non-blocking。这个是必须的，因为这个库的基础就是非阻塞io多路复用。
	后面不用再直接用fd去进行其他操作。一切操作都通过st_netfd_t来做。
	
st_netfd_t st_netfd_open_socket(int osfd);
	这个跟上面一个函数的不同在于，这个fd是socket。
	效率会比上面一个函数高一点。
	
void st_netfd_free(st_netfd_t fd);
	释放内存，不会关闭真的fd。
	
int st_netfd_close(st_netfd_t fd);
	这个会关闭fd。
	
int st_netfd_fileno(st_netfd_t fd);
	这个是获取真实的fd。
	
void st_netfd_setspecific(st_netfd_t fd, void *value,
                          void (*destructor)(void *));
	fd的私有数据。
	value会在st_netfd_free和st_netfd_close的时候被释放。
	
void *st_netfd_getspecific(st_netfd_t fd);
	获取私有数据。
	
int st_netfd_serialize_accept(st_netfd_t fd);
	
int st_netfd_poll(st_netfd_t fd, int how, st_utime_t timeout);
	等待数据。
	
st_netfd_t st_accept(st_netfd_t fd, struct sockaddr *addr, int *addrlen,
                     st_utime_t timeout);
	和上面的st_netfd_serialize_accept区别是什么？
	
int st_connect(st_netfd_t fd, struct sockaddr *addr, int addrlen,
               st_utime_t timeout);
ssize_t st_read(st_netfd_t fd, void *buf, size_t nbyte, st_utime_t timeout);
ssize_t st_read_fully(st_netfd_t fd, void *buf, size_t nbyte,
                      st_utime_t timeout);
                      
int st_read_resid(st_netfd_t fd, void *buf, size_t *resid,
		  st_utime_t timeout);
		  
ssize_t st_readv(st_netfd_t fd, const struct iovec *iov, int iov_size,
		 st_utime_t timeout);
		 
int st_readv_resid(st_netfd_t fd, struct iovec **iov, int *iov_size,
		   st_utime_t timeout);
		   
ssize_t st_write(st_netfd_t fd, const void *buf, size_t nbyte,
                 st_utime_t timeout);
                 
int st_write_resid(st_netfd_t fd, const void *buf, size_t *resid,
                   st_utime_t timeout);
```



参考资料

1、srs之state thread库接口分析

https://segmentfault.com/a/1190000019539131

2、协程库st(state threads library)原理解析

https://www.cnblogs.com/NerdWill/p/6166220.html

3、使用State Threads实现简单的服务器

https://blog.csdn.net/caoshangpa/article/details/79582873

4、官方文档

https://github.com/ossrs/state-threads/tree/srs/docs

5、这里翻译了官方文档

https://github.com/zfengzhen/Blog/blob/master/article/%E4%B8%BA%E4%BA%92%E8%81%94%E7%BD%91%E5%BA%94%E7%94%A8%E7%A8%8B%E5%BA%8F%E8%80%8C%E7%94%9F%E7%9A%84State%20Threads%5B%E5%B8%B8%E8%A7%81%E5%90%8E%E5%8F%B0%E6%9E%B6%E6%9E%84%E6%B5%85%E6%9E%90%5D.md