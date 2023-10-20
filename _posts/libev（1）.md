---
title: libev（1）
date: 2019-05-28 16:50:51
tags:
	- Linux

---

--

# 资源收集

这个系列文章不错。

https://segmentfault.com/a/1190000006173864



# 背景

我决定用libev来做我的网络库。

看看怎么使用。

实际上，libev是对libevent的改进。

nodejs最开始用的也是libev。只是为了更好的通用性，自己开发了libuv。

所以值得对libev进行深入学习掌握的。虽然代码写得不是很好懂。但是我先只从接口使用上进行掌握。

用到熟练之后，再看源代码。尽量多看网上的文章。



现在看jsonrpc-c的实现，这个是基于libev的。所以还是有必要看一下libev的代码。

Libev通过一个 ·struct ev_loop· 结结构表示一个事件驱动的框架。

在这个框架里面通过ev_xxx结构，ev_init、ev_xxx_set、ev_xxx_start接口

向这个事件驱动的框架里面注册事件监控器，

当相应的事件监控器的事件出现时，便会触发该事件监控器的处理逻辑，去处理该事件。

处理完之后，这些监控器进入到下一轮的监控中。符合一个标准的事件驱动状态的模型。

Libev 除了提供了基本的三大类事件（IO事件、定时器事件、信号事件）外

还提供了周期事件、子进程事件、文件状态改变事件等多个事件，

这里我们用三大基本事件写一个例子，

```
#include <ev.h>
#include <stdio.h>
#include <signal.h>
#include <sys/unistd.h>

ev_io io_w;
ev_timer timer_w;
ev_signal signal_w;

void io_action(struct ev_loop *main_loop, ev_io *io_w, int e)
{
    int ret;
    char buf[1024] = {0};
    puts("in io cb\n");
    read(STDIN_FILENO, buf, sizeof(buf));
    buf[1023] = '\0';
    printf("read a string:%s\n", buf);
    ev_io_stop(main_loop, io_w);
}
void timer_action(struct ev_loop *main_loop, ev_timer *timer_w, int e)
{
    puts("in timer cb\n");
    ev_timer_stop(main_loop, timer_w);
}
void signal_action(struct ev_loop *main_loop, ev_signal *signal_w, int e)
{
    puts("in signal cb\n");
    ev_signal_stop(main_loop, signal_w);
    ev_break(main_loop, EVBREAK_ALL);
}

int main(int argc, char const *argv[])
{
    struct ev_loop *main_loop = ev_default_loop(0);
    ev_init(&io_w, io_action);
    ev_io_set(&io_w, STDIN_FILENO, EV_READ);
    ev_init(&timer_w, timer_action);
    ev_timer_set(&timer_w, 2,0);
    ev_init(&signal_w, signal_action);
    ev_signal_set(&signal_w, SIGINT);

    ev_io_start(main_loop, &io_w);
    ev_timer_start(main_loop, &timer_w);
    ev_signal_start(main_loop, &signal_w);
    ev_run(main_loop, 0);
    return 0;
}
```

编译：

```
gcc test.c -lev
```

拿到一份源码，怎么去熟悉它是首要解决的问题。

我一般把会把源码进行分类：

**一类是产品类的，就比如Redis、Ngnix这一类本身是一个完整的可以运维的成熟产品；**

**另一类就是Libev这样的组件类的。**

对于组件类的项目，我一般就是分成这样几步：

1. 有文档看文档，没有文档问相关人员（包括Google），这个组件主要提供什么服务
2. 结合上述信息使用组件的API写个示例程序，跑起来
3. 大致浏览下源码，分析一下代码的组织结构
4. 根据使用的API，进到源码中看看主干是怎么样实现的，从而了解整体思路
5. 再搜刮源码，把一些辅助的功能看下，并在例子中尝试
6. 之后将整个理解用文字记录下来。提炼两大块内容：实现思想和技巧tips

这里我对Libev的学习就是依照这样的一个逻辑一步一步走的。

# 对外接口

```
时间相关
ev_tstamp ev_time();//获取当前的时间戳
void ev_sleep(ev_tstamp t);// 睡眠

错误处理相关
void ev_set_syserr_cb(void (*cb)(char *msg));//设置发生严重错误时的行为。默认是abort。

signal相关
void ev_feed_signal(int sig);//模拟一个信号触发

eventloop相关
struct ev_loop *ev_default_loop(unsigned int flags);//创建或者返回默认的loop。
	//默认的这个loop最特殊，只有它可以处理ev_child事件。
struct ev_loop *ev_loop_new(unsigned int flags);//
	这里flag常用的有：
	EVFLAG_AUTO :这个是默认值，
	EVFLAG_NOENV
	EVBACKEND_EPOLL
void ev_loop_destroy(struct ev_loop *loop);
int ev_is_default_loop(struct ev_loop *loop);
void ev_suspend (struct ev_loop *loop);//暂停loop
void ev_resume (struct ev_loop *loop);
bool ev_run (struct ev_loop *loop, int flags);
void ev_break (struct ev_loop *loop, how);
void ev_ref (struct ev_loop *loop);
void ev_unref (struct ev_loop *loop);
	只要 reference count 不为0，ev_run 函数就不会返回。
	
```

## ev_loop_destroy 

销毁`ev_loop`。注意这里要将所有的 IO 清除光之后再调用，因为这个函数并不中止所有活跃（active）的 IO。部分 IO 不会被清除，比如 signal。这些需要手动清除。这个函数一般和`ev_loop_new`一起出现在同一个线程中。

# EVFLAG_AUTO

EVFLAG_AUTO 是 libev 库中用于设置 watcher 的标志之一。设置 EVFLAG_AUTO 标志后，libev 库会自动选择最合适的 I/O 多路复用机制，从而提高程序的效率和可移植性。

EVFLAG_AUTO 标志的使用非常简单，只需要在创建 watcher 时将 EVFLAG_AUTO 标志作为第二个参数传递给对应的初始化函数即可。例如：

```c
ev_io_init(&io_watcher, io_cb, fd, EVFLAG_AUTO); // 创建一个 EVFLAG_AUTO 的 ev_io watcher
```

EVFLAG_AUTO 标志的主要作用有以下几点：

1. 自动选择最合适的 I/O 多路复用机制

在不同的操作系统上，I/O 多路复用机制的实现方式可能不同，如在 Linux 上可以使用 epoll、在 macOS 上可以使用 kqueue。EVFLAG_AUTO 标志会自动选择最合适的 I/O 多路复用机制，从而提高程序的效率和可移植性。

2. 隐藏 I/O 多路复用机制的差异

不同的 I/O 多路复用机制在使用方式和实现细节上可能存在差异，这可能会给程序员带来一定的麻烦。EVFLAG_AUTO 标志会隐藏 I/O 多路复用机制的差异，使得程序员可以更加专注于业务逻辑的实现，而不用过多关注系统底层的实现细节。

3. 提高程序的可移植性

由于 EVFLAG_AUTO 标志会自动选择最合适的 I/O 多路复用机制，因此可以使得程序更加具有可移植性。这使得程序可以在不同的操作系统和硬件平台上运行，而不需要对代码进行过多的修改和调整。

需要注意的是，虽然 EVFLAG_AUTO 标志可以自动选择最合适的 I/O 多路复用机制，但是在一些特殊情况下，手动选择 I/O 多路复用机制可能会更加有效和合适。因此，在实际应用中，应该根据具体情况选择合适的方式进行设置。

# Libev 支持：

- ev_io：用于文件描述符事件，支持：
  - select，poll
  - Linux 特有的 aio 和 epoll 接口
  - BSD 特有的 kqueue
  - Solaris 特有事件端口机制
- ev_stat：Linux inotify 接口，
- **Linux eventfd/signalfd （用于更快和更清晰的线程间唤醒（ev_async）/信号处理（ev_signal））**
- ev_timer：相对定时器
- ev_periodic：具有定制重新调度的绝对定时器，
- ev_signal：同步信号，
- ev_child：进程状态改变事件
- ev_idle，ev_embed，ev_prepare 和 ev_check：和事件观察器处理事件循环机制本身。
- ev_stat：文件观察者
- ev_fork：fork 事件的有限支持。

### 时间显示

Libev 使用一个`ev_tstamp`数据类型来表示1970年以来的秒数，实际类型是 C 里面的`double`类型。



### 错误事件

Libev 使用三种层级的错误：

1. **操作系统错误**：调用`ev_set_syserr_cb`所设置的回调。默认行为是调用`abort()`
2. **参数错误**：调用`assert`
3. **内部错误（bug）**：内部调用`assert`

# ev_async用法

ev_async的主要应用场景是什么？

ev_async(异步调用观察器)

ev_async当ev_async_send通过watcher调用时调用，触发EV_ASYNC

主要在于跨线程进行触发。

一个线程调用：ev_async_send进行触发。

另一个线程调用

```
ev_async_init(&async_watcher, async_cb);
ev_async_start(loop, &async_watcher);
```

ev_io的这些行为，都是发生在一个线程内部。



ev_async可以在多种event loop，而不是默认的loop。

参考资料

1、这个例子可以正常运行，就以这个来学习

https://blog.csdn.net/yahstudio/article/details/48681481

2、Socket网络编程--Libev库学习(3)

这个有分析

https://www.cnblogs.com/wunaozai/p/3955156.html

# ev_prepare和ev_check

**ev_prepare** (每次event loop之前事件)

**ev_check** (每次event loop之后事件)

那就相当于是hook回调的作用。

# ev_idle

每次evloop idle的时候会触发。

我们的idle是可以控制开始和结束的。

而这个idle的作用是但event_loop处于空闲的时候，

与其在ev_run阻塞等待，

不如利用这时的cpu时间来做其他事。

应用的话，就是如果服务器繁忙的话就主要处理请求等，

如果服务器请求不多时，可以利用cpu时间来处理备份什么的，

这样就可以最大限度的利用cpu了。





# ev_timer

接口函数：

```
设置
ev_timer_set(ev, after_, repeat_)
启动
ev_timer_start
停止
ev_timer_stop
```



参考资料

1、这篇文章分析还比较深入。

https://blog.csdn.net/gqtcgq/article/details/49402041

# ev_stat一般的用途

ev_stat 是 libev 库中用于监视文件状态变化的一个 watcher 类型。它可以监视文件或目录的状态变化，如文件的修改、删除、重命名等，从而在状态变化时触发对应的回调函数进行处理。

ev_stat 的一般用途包括以下几个方面：

1. 监视文件状态变化

ev_stat 可以监视文件或目录的状态变化，如文件的修改、删除、重命名等。当文件状态发生变化时，会触发对应的回调函数进行处理。这在需要及时处理文件状态变化的应用中非常有用，如实时监控文件系统、自动备份文件等。

2. 实现文件系统监控

通过使用 ev_stat 监视文件或目录的状态变化，可以实现文件系统监控功能。例如，可以监视某个目录下的文件，当有新文件添加或者文件被删除时，可以及时进行处理，如发送邮件通知、备份文件等。

3. 实现文件同步

通过使用 ev_stat 监视文件或目录的状态变化，可以实现文件同步功能。例如，可以监视某个目录下的文件，当文件被修改时，可以自动将修改的内容同步到其他机器上，从而实现文件同步。

以下是一个使用 ev_stat 监视文件状态变化的示例：

```c
#include <ev.h>
#include <stdio.h>
#include <sys/stat.h>

void stat_cb(EV_P_ ev_stat *w, int revents) {
    if (revents & EV_STAT) {
        printf("file %s changed\n", w->path);
    }
}

int main() {
    struct ev_loop *loop = EV_DEFAULT;
    ev_stat stat_watcher;
    ev_stat_init(&stat_watcher, stat_cb, "test.txt", 0); // 初始化 ev_stat watcher
    ev_stat_start(loop, &stat_watcher); // 开始监听文件状态变化

    ev_run(loop, 0); // 进入事件循环

    return 0;
}
```

在上面的代码中，我们创建了一个 ev_stat watcher，并在回调函数中输出一条日志。在主函数中，我们初始化了 ev_stat watcher 并开始监听文件状态变化。当文件状态发生变化时，会触发对应的回调函数输出日志。

需要注意的是，在实际应用中，使用 ev_stat 监视文件状态变化时需要考虑文件系统的性能和安全性，避免对文件系统造成过大的负载和安全风险。

# 系列文章

把这个系列文章学习一遍

https://www.cnblogs.com/wunaozai/p/3950249.html

Libev 除了提供了**基本的三大类事件（IO事件、定时器事件、信号事件）外**

还提供了周期事件、子进程事件、文件状态改变事件等多个事件，

这里我们用三大基本事件写一个例子。

## 三大基础事件：io、timer、signal

写libev的例子代码，都用这种风格来写吧：

```
ev_io io_w
//就是ev_xx xx_w 这样来定义全局的watcher。

然后对应的回调都写成：
xx_action

这样写起来风格比较统一。没有必要每个例子换一种命名。
```



void ev_run (EV_P_ int flags);

void ev_break (EV_P_ int how);

同样我们这里比较关注flags和how这两个参数。flags有下面这几个：

0:默认值。一直循环进行处理，直到外部引用计数==0或者是显示退出。
EVRUN_NOWAIT:运行一次，poll时候不会等待。如果有pending事件进行处理，否则立即返回。
EVRUN_ONCE:运行一次，poll时候会等待至少一个event发生，处理完成之后返回。
而how有下面这几个：

EVBREAK_ONE:只是退出一次ev_run这个调用。通常来说使用这个就可以了。
EVBREAK_ALL:退出所有的ev_run调用。这种情况存在于ev_run在pengding处理时候会递归调用。



使用libev的核心是事件循环，可以用 ev_default_loop 或 ev_loop_new 函数创建循环，

或者直接使用 EV_DEFAULT 宏，

区别是 **ev_default_loop 创建的事件循环不是线程安全的，**

**而 ev_loop_new 创建的事件循环不能捕捉信号和子进程的观察器。**

大多数情况下，可以像下面这样使用：



在**创建子进程后**，且想要使用事件循环时，

需要先在子进程中调用 ev_default_fork 或 ev_loop_fork 来重新初始化后端的内核状态，

它们分别对应 ev_default_loop 和 ev_loop_new 来使用。



ev_suspend 和 ev_resume 用来暂停和重启事件循环，比如在程序挂起的时候。



libev中将观察器分为4种状态：初始化、启动/活动、等待、停止。libev中的观察器还支持优先级。

### 用ev_timer创建一个每10s执行一次的watcher

```
ev_timer timer_w;
ev_timer_init(&timer_w, timer_action, 0.0, 10.0);
```

这个ev_timer居然不能重复，是不是没有解决办法呢？不是还有个ev_periodic这个可以实现周期性观察器。

### 用ev_periodic创建周期性执行的

```
ev_periodic periodic_w;
ev_periodic_init(&periodic_w, periodic_action, 0, 10, 0);
```

最后一个参数一个callback。

可以用来自定义周期。

例如这样：

```
ev_tstamp my_schedule_cb(ev_periodic *w, ev_tstamp now)
{
	return now + 10;
}

ev_periodic_init(&periodic_w, periodic_action, 0, 0, my_schedule_cb);
```

## ev_child

主要用途是：fork一个新的进程，给它install 一个child处理器等待进程结束。

举例：

```
#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <sys/unistd.h>
#include <ev.h>
#include "mylog.h"

ev_child child_w;

void child_action(struct ev_loop *loop, ev_child *w, int e)
{
    ev_child_stop(loop, w);
    mylogd("child process %d exit status:%d", w->rpid, w->rstatus);
}
int main(int argc, char const *argv[])
{
    struct ev_loop *loop = ev_default_loop(0);
    pid_t pid = fork();
    if (pid < 0) {
        myloge("fork fail");
        return -1;
    } else if (pid == 0) {
        mylogd("child process here ");
        //子进程直接退出
        exit(1);
    } else {
        mylogd("child process id:%d", pid);
        //父进程里，监听子进程的状态。
        ev_child_init(&child_w, child_action, pid, 0);
        ev_child_start(loop, &child_w);
        ev_run(loop, 0);
    }
    return 0;
}

```

## ev_stat

这个就相当于inotify，监视文件的变化。

这个其实是比较有用的功能。

## watcher的状态

wacther的状态有下面这么几种：

　　(1) initialiased.调用init函数初始化
　　(2) active.调用start进行注册
　　(3) pending.已经触发事件但是没有处理
　　(4) inactive.调用stop注销。这个状态等同于initialised这个状态。

## ev_cleanup

这个相当于ev_loop在退出的hook。



# ev_run

ev_run怎么不是预期的一直阻塞？有时候是一次就退出了。

在没有break的情况下。就自己退出了。

看有的示例代码，可以多次运行`ev_run(loop, 0)`

所以ev_run具体的用法是怎样的？



# libev ipc

看看有没有用libev做ipc方案的。

或者说找找基于libev的各种技术方案。



这个是基于libev的http server实现。

https://github.com/Yellow-Camper/libevhtp/



这个是在线markdown书籍，将libevent的。

https://github.com/aceld/libevent

这个算是libev的ipc例子。但是好像不是很好。

https://github.com/coolaj86/libev-examples/blob/master/ipc/unix-socket-ipc-remote-control.c

# ev_loop_fork

这个函数的用途是什么？

The libev manual does not say that after a fork an event loop will be stopped. All it says is that to be sure that the event loop will **properly** work in the child, you need to call ev_loop_fork(). What's actually happening depends on the backend.

就是fork之后，在子进程里，需要调用一下ev_loop_fork，子进程里才能正常使用ev_loop。

这个是epoll等底层决定的。

https://stackoverflow.com/questions/35604292/what-happend-if-i-didnt-call-ev-loop-fork-in-the-child

# ANFD 

ANFD 是一个结构体类型的名称，它代表着 "Active Node for File Descriptor"，

这个是问gpt得到的。我觉得解释合理。

# 参考资料

1、

这个系列文章非常好，思路清晰。

https://blog.csdn.net/guankeliang/article/details/82911856

2、libev 手册

https://phenix3443.github.io/notebook/c/3rd-libs/libev-manual.html