---
title: Linux之signal和多线程的配合问题
date: 2020-05-09 13:38:08
tags:
	- socket

---

1

看陈硕的那个Linux服务器编程的书里，提到说不要在多线程程序里使用signal。

具体是会导致什么样的问题？真的无法解决这种问题吗？

在Linux里，每个进程都有自己的signal mask。

这个mask指定哪些信号被屏蔽。

每个进程还有自己的signal action，表明了处理不同的信号的方法。

而引入多线程之后，就有这些问题：

1、信号发生的时候，哪个线程会收到？

2、是不是每个线程都有自己的mask及action？

3、每个线程能按照自己的方式处理信号吗？



我们先看第一个问题：信号发生的时候，哪个线程会收到？

这个要分几种情况。

1、异常信号，例如段错误、sigpipe这些，是产生这些异常的线程会收到并处理。

2、如果是主动调用pthread_kill产生的内部信号，则只有目标线程会收到这个信号。

3、如果是外部使用kill发来的信号，一般是SIGINT， SIGHUP这些job control信号。则会遍历所有的线程，直到找到一个不阻塞改信号的线程，然后调用它来处理。**注意：只有一个线程会收到。**



然后看第二个问题：是不是每个线程都有自己的mask及action？

答案是：mask是每个线程自己单独有的，但是action是共享一份的。

每个线程的mask设置是调用pthread_sigmask函数来做的。

所以第三个问题的答案也有了：所有线程处理的方式，就是action，在一个进程只有一份。

看一个例子：

```
/*threadsig.c*/
#include <signal.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sighandler(int signo);

void *
thr1_fn(void *arg)
{
    struct sigaction    action;
    action.sa_flags = 0;
    action.sa_handler = sighandler;

    sigaction(SIGINT, &action, NULL);

    pthread_t   tid = pthread_self();
    int     rc;

    printf("thread 1 with tid:%lu\n", tid);
    rc = sleep(60);
    if (rc != 0)
        printf("thread 1... interrupted at %d second\n", 60 - rc);
    printf("thread 1 ends\n");
    return NULL;
}

void *
thr2_fn(void *arg)
{
    struct sigaction    action;
    pthread_t       tid = pthread_self();
    int         rc, err;

    printf("thread 2 with tid:%lu\n", tid);

    action.sa_flags = 0;
    action.sa_handler = sighandler;

    err = sigaction(SIGALRM, &action, NULL);

    rc = sleep(60);
    if (rc != 0)
        printf("thread 2... interrupted at %d second\n", 60 - rc);
    printf("thread 2 ends\n");
    return NULL;
}

void *
thr3_fn(void *arg)
{
    pthread_t   tid = pthread_self();
    sigset_t    mask;
    int     rc, err;

    printf("thread 3 with tid%lu\n", tid);


    sigemptyset(&mask); /* 初始化mask信号集 */

    sigaddset(&mask, SIGALRM);
    err = pthread_sigmask(SIG_BLOCK, &mask, NULL);
    if (err != 0)
    {
        printf("%d, %s/n", rc, strerror(rc));
        return NULL;
    }

    rc = sleep(10);
    if (rc != 0)
        printf("thread 3... interrupted at %d second\n", 60 - rc);
    err = pthread_sigmask( SIG_UNBLOCK,&mask,NULL );
    if ( err != 0 )
    {
        printf("unblock %d, %s/n", rc, strerror(rc));
        return NULL;
    }

    rc = sleep(10);
    if (rc != 0)
        printf("thread 3... interrupted at %d second after unblock\n", 60 - rc);

    printf("thread 3 ends\n");
    return NULL;

    return NULL;
}

int
main(void)
{
    int     rc, err;
    pthread_t   thr1, thr2, thr3, thrm = pthread_self();

    printf("thread main with pid %lu\n",thrm);
    err = pthread_create(&thr1, NULL, thr1_fn, NULL);
    if (err != 0) {
        printf("error in creating pthread:%d\t%s\n",err, strerror(rc));
        exit(1);
    }


/*  pthread_kill(thr1, SIGALRM);    send a SIGARLM signal to thr1 before thr2 set the signal handler, then the whole process will be terminated*/
    err = pthread_create(&thr2, NULL, thr2_fn, NULL);
    if (err != 0) {
        printf("error in creating pthread:%d\t%s\n",err, strerror(rc));
        exit(1);
    }

    err = pthread_create(&thr3, NULL, thr3_fn, NULL);
    if (err != 0) {
        printf("error in creating pthread:%d\t%s\n",err, strerror(rc));
        exit(1);
    }

    sleep(10);
    //内部产生的信号，只有指定的线程能收到，因此要向所有线程发送
    pthread_kill(thr1, SIGALRM);
    pthread_kill(thr2, SIGALRM);
    pthread_kill(thr3, SIGALRM);
    pthread_kill(thr3, SIGALRM);
    pthread_kill(thr3, SIGALRM);
    sleep(5);
    pthread_join(thr1, NULL);   /*wait for the threads to complete.*/
    pthread_join(thr2, NULL);
    pthread_join(thr3, NULL);
    printf("main ends\n");
    return 0;
}

void
sighandler(int signo)
{
    pthread_t   tid = pthread_self();

    printf("thread with pid:%lu receive signo:%d\n", tid, signo);
    return;
}

```



运行效果，中间我按了4次ctrl+C试图结束进程。

```
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ ./thread_signal
thread main with pid 140442682369792
thread 2 with tid:140442665797376
thread 1 with tid:140442674190080
thread 3 with tid140442657404672
^Cthread with pid:140442682369792 receive signo:2
thread with pid:140442674190080 receive signo:14
thread 1... interrupted at 7 second
thread 1 ends
thread with pid:140442665797376 receive signo:14
thread 2... interrupted at 7 second
thread 2 ends

thread with pid:140442657404672 receive signo:14
^Cthread with pid:140442682369792 receive signo:2

^Cthread with pid:140442682369792 receive signo:2


^Cthread with pid:140442682369792 receive signo:2

thread 3 ends
main ends
```



参考资料

1、多线程中的信号处理

https://www.cnblogs.com/coding-my-life/p/4782529.html