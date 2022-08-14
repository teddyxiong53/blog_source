---
title: libev（1）
date: 2019-05-28 16:50:51
tags:
	- Linux

---

--

我决定用libev来做我的网络库。

看看怎么使用。

看了一下，没有太多资料。这个不是一个认真的项目。算了。还是换成libuv。



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

一类是产品类的，就比如Redis、Ngnix这一类本身是一个完整的可以运维的成熟产品；

另一类就是Libev这样的组件类的。

对于组件类的项目，我一般就是分成这样几步：

1. 有文档看文档，没有文档问相关人员（包括Google），这个组件主要提供什么服务
2. 结合上述信息使用组件的AIP写个示例程序，跑起来
3. 大致浏览下源码，分析一下代码的组织结构
4. 根据使用的API，进到源码中看看主干是怎么样实现的，从而了解整体思路
5. 再搜刮源码，把一些辅助的功能看下，并在例子中尝试
6. 之后将整个理解用文字记录下来。提炼两大块内容：实现思想和技巧tips

这里我对Libev的学习就是依照这样的一个逻辑一步一步走的。

参考资料

1、

这个系列文章非常好，思路清晰。

https://blog.csdn.net/guankeliang/article/details/82911856