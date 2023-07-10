---
title: pthread_cancel的使用
date: 2017-02-19 20:33:12
tags:
	- pthread
---
--

pthread_cancel调用后，只是向目标线程发出取消申请，目标线程不会马上停止运行，

而是要在运行到某个取消点的时候才会真正停止运行。

pthread标准指定了下面几种取消点：

1、你在目标线程里加上pthread_testcancle函数调用，这个点就是一个取消点。
2、目标线程里调用`pthread_cond_wait`的地方。
3、一些会导致进程挂起的系统调用。



pthread线程默认是允许被取消的，你可以通过`pthread_setcancelstate`来使能或者禁止这一特性。

目前，按照pthread_cancel手册的说明，

由于LinuxThread库和c库结合得不好，目前C库函数不是取消点，但是取消信号会导致线程从阻塞的系统调用中退出，导致EINTR错误码。

解决的办法是，在需要作为取消点的系统调用的前后加上`pthread_cancel`函数。

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

# pthread_cancel机制

`pthread_cancel` 是 POSIX 线程库中的一个函数，用于向目标线程发送取消请求，以请求目标线程终止。

`pthread_cancel` 函数的原型如下：

```c
#include <pthread.h>

int pthread_cancel(pthread_t thread);
```

其中，`thread` 参数是目标线程的标识符，它是一个 `pthread_t` 类型的变量。

调用 `pthread_cancel` 函数会发送取消请求给目标线程。目标线程会在合适的时机进行取消处理，例如在取消点（cancellation point）处检查取消请求，或者在线程调用可取消的线程安全函数时。

值得注意的是，`pthread_cancel` 并不保证目标线程会立即终止。取消请求的实际处理取决于目标线程的取消状态、取消类型以及线程的取消点等因素。

另外，目标线程可以选择是否响应取消请求。可以通过以下几种方式来管理线程的取消状态和处理取消请求：

- 设置取消状态：通过调用 `pthread_setcancelstate` 函数来设置线程的取消状态，可以将线程的取消状态设置为 `PTHREAD_CANCEL_ENABLE`（响应取消请求）或 `PTHREAD_CANCEL_DISABLE`（忽略取消请求）。

- 设置取消类型：通过调用 `pthread_setcanceltype` 函数来设置线程的取消类型，可以将线程的取消类型设置为 `PTHREAD_CANCEL_DEFERRED`（在线程取消点处检查取消请求）或 `PTHREAD_CANCEL_ASYNCHRONOUS`（立即执行取消请求）。

- 注册清理处理程序：可以使用 `pthread_cleanup_push` 和 `pthread_cleanup_pop` 函数在线程中注册清理处理程序，当线程接收到取消请求时，会执行这些清理处理程序。

需要注意的是，`pthread_cancel` 应该谨慎使用，并且在使用时需要仔细考虑线程安全和资源管理等问题。对于需要终止线程的情况，建议使用线程间通信或其他更可控的机制来请求线程退出。

另外，目标线程本身也可以通过调用 `pthread_testcancel` 函数主动检查是否有取消请求，以便在适当的时机处理取消请求。

总结而言，`pthread_cancel` 提供了一种向线程发送取消请求的机制，但具体的取消行为和响应取决于目标线程的取消状态和类型，以及线程中的取消点和清理处理程序。