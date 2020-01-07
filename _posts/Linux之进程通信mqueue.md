---
title: Linux之进程通信mqueue
date: 2020-01-04 09:51:08
tags:
	- Linux

---

1

mqueue叫消息队列。

什么是消息队列？它相当于其他的进程间通信方式，有什么优点？

怎样进行使用？



先回答第一个问题：什么是消息队列？

是一种进程间通信机制。可以认为是一个链表，一个进程往里面放数据，不需要另外一个进程立刻读取使用。

这个是跟管道和fifo不同的（这两种都需要通信另外一段去读取通信内容，不然会阻塞）。

Linux上的消息队列有两种：

1、system V消息队列。

2、posix消息队列。

这两种消息队列的区别是：

```
1、读取返回不同。
	system V：返回指定优先级的消息。
	posix：总是返回最高优先级的的最早消息。
2、往一个空队列放消息的时候，行为不同。
	posix：允许产生一个信号或启动一个线程。
	system V：未提供类似机制。
```

结论：我们使用posix消息队列。

第二个问题：有什么优点？

上面已经有回答过，就是通信不是阻塞的，不会要求对端马上去读取。

发出的消息，在操作系统没有重启时，会一直存在。



下面看看如何进行使用。

posix消息队列的帮助信息，用man mq_overview可以查看。

只能放在根目录。名字里不能带“/”。

在fork后，子进程会继承父进程的消息队列fd。

消息的优先级从0到max。max值是`sysconf(_SC_MQ_PRIO_MAX) - 1`。

在Linux上，max值是32767。

posix标准要求是0到31就可以了。



在内核里的系统调用，名字跟posix标准的名字是类似的。如下：

```
Library interface    System call
mq_close(3)          close(2)
mq_getattr(3)        mq_getsetattr(2)
mq_notify(3)         mq_notify(2)
mq_open(3)           mq_open(2)
mq_receive(3)        mq_timedreceive(2)
mq_send(3)           mq_timedsend(2)
mq_setattr(3)        mq_getsetattr(2)
mq_timedreceive(3)   mq_timedreceive(2)
mq_timedsend(3)      mq_timedsend(2)
mq_unlink(3)         mq_unlink(2)
```

内核要支持posix消息队列，需要配置CONFIG_POSIX_MQUEUE。

在proc下面，有/proc/sys/fs/mqueue目录，可以看到相关的配置。



在Linux上，消息队列是在一个虚拟文件系统里。

```
mkdir /dev/mqueue
mount -t mqueue none /dev/mqueue # 这个需要内核打开了posix mqueue的选，否则会不识别mqueue类型。
```



基本数据结构：

```
#include <mqueue.h>
typedef int mqd_t;
```

操作类似于操作一个文件。

```
打开：
mqd_t mq_open(char *name, int oflag);
关闭：
int mq_close(mqd_t fd);
删除：
int mq_unlink(char *name);
发送：
int mq_send(mqd_t mqdes, char *msg_ptr, size_t msg_len, unsigned int msg_prio);
接收：
ssize_t mq_receive(mqd_t mqdes, char *msg_ptr, size_t msg_len, unsigned int *msg_prio);
mq_getattr
mq_setattr
mq_notify

```

链接时，需要链接librt.so。

简单的测试代码如下：

mq-send.c

```
#include <mqueue.h>
#include <stdio.h>
#include <fcntl.h>

int main()
{
    mqd_t mqid = mq_open("/mymq_test", O_RDWR|O_CREAT);
    if(mqid < 0) {
        perror("open mq fail");
        printf("open mq fail\n");
        return -1;
    }
    char *msg = "hello mq";
    mq_send(mqid, msg, strlen(msg), 1);
    mq_close(mqid);
    return 0;
}
```

mq-recv.c

```
#include <mqueue.h>
#include <stdio.h>
#include <fcntl.h>

int main()
{
    mqd_t mqid = mq_open("/mymq_test", O_RDWR|O_CREAT);
    if(mqid < 0) {
        perror("open mq fail");
        printf("open mq fail\n");
        return -1;
    }
    struct mq_attr attr;
    mq_getattr(mqid, &attr);//这个是必须的，不然收不到。
    char buf[1024] = {0};
    int prio = 0;
    mq_receive(mqid, buf, attr.mq_msgsize, &prio);
    printf("recv msg:%s, prio:%d\n", buf, prio);
    mq_close(mqid);
    return 0;
}
```

执行后，是在/dev/mqueue/目录下，生成一个mymq_test的节点。

mq_receive，在没有消息的时候，会阻塞。





参考资料

1、man手册

2、Linux进程通信之POSIX消息队列

https://blog.csdn.net/cp25807720/article/details/17260305

3、POSIX 消息队列函数(mq_open、mq_getattr、mq_send、mq_receive)示例

https://blog.csdn.net/mayue_web/article/details/92712163