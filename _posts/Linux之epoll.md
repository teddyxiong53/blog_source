---
title: Linux之epoll
date: 2018-04-13 18:39:22
tags:
	- Linux

---



# 什么是epoll

当我们讨论linux的多路复用的时候，总是说select和poll有很多缺点，现在推荐使用epoll。

那么epoll到底是什么？

epoll就是为了处理大量handle而改进的poll。

从2.5.44版本内核就引入了。

现在是linux内核里公认最好的多路复用的机制。

# epoll改进了什么

说epoll好。

我们就的先看看select和poll有什么不好。

select的缺点：

1、数量有限，修改不方便。

select最多支持1024个文件的监听，这个是内核里的一个宏。

1024对于服务器来说，太小了。修改还得重新编译内核。

2、效率低。而且随着监听文件增加变得更慢。

它内部是用遍历的方式来看是否有文件就绪，监听的文件越多，就越慢。

而且每次调用select都要从用户态拷贝到内核态一次。

poll是对select的改进。它改进了什么？

select有一个很明显的问题，就是maxfd这个东西，从0到maxfd，select都要进行监听，实际是很多都是当前不关心的。但是select也得查询。

poll就是解决了这个问题。另外数量限制放宽了。

其实poll，我还不熟悉，我先把poll熟悉了。再继续往下写这篇。

但是poll的用户态和内核态之间的拷贝还是存在。而且效率也是随着fd的增加而降低的。



epoll有这些改进：

1、打开socket的数量受最大打开文件数的限制，这个数字是可以在proc文件系统里改的。

而且数字默认就很大。就突破了数量的限制了。

2、io效率不随着fd数量的增加而线性下降。

3、使用mmap来避免拷贝。

# epoll的接口

我们还是从musl这个c库里来看。

我们只需要了解这些就够了。

```
#define EPOLLIN 0x01
#define EPOLLPRI 0X02
#define EPOLLOUT 0X04
typedef union epoll_data {
  void *ptr;
  int fd;
  u32 u32;
  u64 u64;
} epoll_data_t;
struct epoll_event {
  u32 events;
  epoll_data_t data;
};
函数有3个：
int epoll_create(int);
int epoll_ctl(int, int, int, struct  epoll_event *);
int epoll_wait(int, struct epoll_event, int, int);
```





# 参考资料

1、I/O多路复用之poll

https://www.cnblogs.com/zengzy/p/5115679.html

2、Linux多路复用之select/poll/epoll实现原理及优缺点对比

https://blog.csdn.net/xiaofei0859/article/details/53202273