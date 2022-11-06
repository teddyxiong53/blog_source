---
title: Linux之posix之semaphore
date: 2022-11-01 16:08:32
tags:
	- Linux

---

--

看musl这个库里的实现。

semaphore.h里：

```
typedef struct {
	volatile int __val[4*sizeof(long)/sizeof(int)];
} sem_t;

int    sem_close(sem_t *);
int    sem_destroy(sem_t *);
int    sem_getvalue(sem_t *__restrict, int *__restrict);
int    sem_init(sem_t *, int, unsigned);
sem_t *sem_open(const char *, int, ...);
int    sem_post(sem_t *);
int    sem_timedwait(sem_t *__restrict, const struct timespec *__restrict);
int    sem_trywait(sem_t *);
int    sem_unlink(const char *);
int    sem_wait(sem_t *);
```

# sem_close和sem_destroy是什么关系

**Posix的有名信号量一般用于进程同步, 有名信号量是内核持续的. 有名信号量的api为**

**sem_open**

**sem_close**

**sem_unlink**

**Posix的无名信号量一般用于线程同步, 无名信号量是进程持续的, 无名信号量的api为**

**sem_init**

**sem_destroy**



参考资料

https://www.cnblogs.com/my_life/articles/4532873.html

# 参考资料

1、

http://www.csc.villanova.edu/~mdamian/threads/posixsem.html

2、POSIX多线程笔记（7）：信号量（Semaphore）

https://blog.csdn.net/yunlong654/article/details/87775044