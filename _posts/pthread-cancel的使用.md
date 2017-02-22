---
title: pthread_cancel的使用
date: 2017-02-19 20:33:12
tags:
	- pthread
---
pthread_cancel调用后，只是向目标线程发出取消申请，目标线程不会马上停止运行，而是要在运行到某个取消点的时候才会真正停止运行。
pthread标准指定了下面几种取消点：
1、你在目标线程里加上pthread_testcancle函数调用，这个点就是一个取消点。
2、目标线程里调用`pthread_cond_wait`的地方。
3、一些会导致进程挂起的系统调用。

pthread线程默认是允许被取消的，你可以通过`pthread_setcancelstate`来使能或者禁止这一特性。

目前，按照pthread_cancel手册的说明，由于LinuxThread库和c库结合得不好，目前C库函数不是取消点，但是取消信号会导致线程从阻塞的系统调用中退出，导致EINTR错误码。解决的办法是，在需要作为取消点的系统调用的前后加上`pthread_cancel`函数。
例如：
```
pthread_testcancel();
ret = read(fd, buff, size);
pthread_testcancel();
```

另外，如果线程处于死循环中，而且循环里没有执行到取消点的必然路径，则这个线程如果没有加上`pthread_testcancel`，则无法被取消掉。

线程的结束有两种，一种是主动调用`pthread_exit`或者return主动退出，这种可以预料，没有什么特别。
另外一种就是线程被其他线程干预，或者自己出错而退出，这种退出方式是不可预见的。

如果线程异常退出，那么如何保证释放掉自己所占用的资源，尤其是锁资源，这是个关键问题。
posix针对这个提供了2个函数：`pthread_cleanup_push`和`pthread_cleanup_pop`。
这2个函数实际上是以宏方式实现的。必须成对使用，否则大括号就无法配对了。

举例如下：
```
void cleanup(void *arg)
{
	pthread_mutex_unlock(&mutex);
}

void *thread_func(void *arg)
{
	pthread_cleanup_push(cleanup, NULL);
	pthread_mutex_lock(&mutex);
	pthread_cond_wait(&cond, &mutex);
	pthread_mutex_unlock(&mutex);
	pthread_cleanup_pop(0);
	pthread_exit(NULL);
}
```
