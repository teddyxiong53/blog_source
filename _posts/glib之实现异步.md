---
title: glib之实现异步
date: 2019-08-07 17:47:19
tags:
	- glib

---

1

我在使用c++的时候，感觉非常方便的一点就是可以实现函数对象的异步。

创建一个任务，直接扔出去运行就可以了。

glib是否可以完成类似的功能呢？

先看GTask。

GTask最主要的用途就是作为一个GAsyncResult。

用来管理异步操作的数据。



线程池

有时候，你希望可以异步分出一部分工作，并且在当前线程继续你自己的操作。

如果你经常有这种需求，创建和销毁线程的开销就是需要考虑的问题。

在这种情况下，重用已经启动的线程似乎是一个不错的选择。

但是这个过程很乏味，而且容易出错。

所以为了解决这种问题，glib就提供了线程池。

```
#include <glib.h>
#include <sys/syscall.h>

void thread_execute(gpointer data, gpointer user_data)
{
    g_printf("in, thread id is:%d, data is:%d\n", syscall(__NR_gettid), *((gint*)data));
    g_usleep(1000*1000);
    g_printf("out, thread id is:%d\n", syscall(__NR_gettid));
}
gint data[10];
int main()
{
    GError *gerr = NULL;
    GThreadPool *gpool = NULL;
    gpool = g_thread_pool_new(thread_execute, NULL, 2, FALSE, NULL);
    g_printf("max num:%d\n", g_thread_pool_get_max_threads(gpool));
    g_printf("cur num:%d\n", g_thread_pool_get_num_threads(gpool));

    //set max num to 3
    if(!g_thread_pool_set_max_threads(gpool, 3, &gerr)) {
        g_printf("set max num fail, reason:%s\n", gerr->message);
    }
    g_printf("after modify, max num:%d\n", g_thread_pool_get_max_threads(gpool));
    int count;
    for(count=0; count < 10; count++) {
        data[count] = count;
        g_thread_pool_push(gpool, (gpointer)(&(data[count])), &gerr);
        if(gerr != NULL) {
            g_printf("push fail, reason:%s\n", gerr->message);
        }
    }
    g_usleep(100*1000);
    g_printf("cur num:%d\n", g_thread_pool_get_num_threads(gpool));
    g_printf("unprocessed num:%d\n", g_thread_pool_unprocessed(gpool));
    g_printf("unused num:%d\n", g_thread_pool_get_num_unused_threads());

    if(g_thread_pool_move_to_front(gpool ,(gpointer)(&data[9]))) {
        g_printf("move to front is 9\n");
    }
    //这个是等待所有的线程执行完成。
    g_thread_pool_free(gpool, FALSE, TRUE);

}
```



参考资料

1、Glib学习（12） 线程池 Thread Pools

https://blog.csdn.net/andylauren/article/details/79244658