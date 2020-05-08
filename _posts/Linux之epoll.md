---
title: Linux之epoll
date: 2018-04-13 18:39:22
tags:
	- Linux

---



# 什么是epoll

当我们讨论linux的多路复用的时候，总是说select和poll有很多缺点，现在推荐使用epoll。

那么epoll到底是什么？

**epoll就是为了处理大量handle而改进的poll。**

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

**select有一个很明显的问题，就是maxfd这个东西，从0到maxfd，select都要进行监听，实际是很多都是当前不关心的。但是select也得查询。**

**poll就是解决了这个问题。另外数量限制放宽了。**

其实poll，我还不熟悉，我先把poll熟悉了。再继续往下写这篇。

但是poll的用户态和内核态之间的拷贝还是存在。而且效率也是随着fd的增加而降低的。



epoll有这些改进：

1、打开socket的数量受最大打开文件数的限制，这个数字是可以在proc文件系统里改的。

而且数字默认就很大。就突破了数量的限制了。

2、io效率不随着fd数量的增加而线性下降。

**3、使用mmap来避免拷贝。**

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
int epoll_create(int size);//这个size参数实际上没有用了。
int epoll_ctl(int epfd, int op, int fd, struct  epoll_event * event);
	//epfd是epoll_create得到的。
	//op是EPOLL_CTL_ADD/DEL/MOD 3个之一。
	//fd是要监听的fd。例如listen_fd。
	//event，前面先定义一个struct epoll_event。把epfd注册过去，并且设置电平触发等方式先。
int epoll_wait(int epfd, struct epoll_event *events, int maxevents, int timeout);
	//events：是要监听的所有事件。
	返回值是就绪的事件个数。
```



# epoll的水平触发和边沿触发

简单来说，**水平触发，只要还有数据，就会一直触发事件给监听进程。**

而边沿触发，只有在数据的量**发生增加或者减少变化时**，才触发一次。

这个可以参考硬件中断的电平触发和边沿触发来理解。

```
#include <unistd.h>
#include <stdio.h>
#include <sys/epoll.h>

int main()
{
    int epfd, nfds;
    struct epoll_event event;
    struct epoll_event events[5];
    epfd = epoll_create(1);//这个参数是需要为1的，如果为0，则现象不符合预期。虽然musl库的实现，这个参数没有用。
    event.data.fd = STDIN_FILENO;
    event.events = EPOLLIN | EPOLLET;
    epoll_ctl(epfd, EPOLL_CTL_ADD, STDIN_FILENO, &event);
    while(1) {
        nfds = epoll_wait(epfd, events, 5, -1);
        int i;
        for(i=0; i<nfds; i++) {
            if(events[i].data.fd == STDIN_FILENO) {
                printf("hello world\n");
            }
        }
    }
}
```

这个例子的效果是：

输入字符，按下回车，会打印hello world。

监听了STDIN的情况。是边沿触发的。

我们如果把上面的代码这一行：

```
event.events = EPOLLIN | EPOLLET;
```

修改为：

```
event.events = EPOLLIN；
```

那么输入字符回车后，会一直打印hello world。这个是电平触发的。



**select和poll都只支持电平触发。**

**epoll默认也是电平触发。**

要用边沿触发，需要设置EPOLLET。



# 实际例子

实现一个echo服务器。测试就用nc来做客户端。

```
#include <unistd.h>
#include <stdio.h>
#include <sys/epoll.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <fcntl.h>

#define MAXEPOLL 100
#define MAXLINE 1024

int main()
{
    struct sockaddr_in server_addr = {0};
    struct sockaddr_in client_addr = {0};
    struct epoll_event ev = {0};
    struct epoll_event evs[MAXEPOLL] = {0};

    socklen_t len = sizeof(struct sockaddr_in);

    int listen_fd;
    int conn_fd;
    int epoll_fd;
    int nread;
    int cur_fds;
    int wait_fds;
    int i;
    char buf[MAXLINE];
    listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    if(listen_fd < 0) {
        perror("socket create fail");
        goto err1;
    }
    fcntl(listen_fd, F_SETFL, fcntl(listen_fd, F_GETFL, 0)|O_NONBLOCK);
    int ret;
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(8888);
    ret = bind(listen_fd, (struct sockaddr *)&server_addr, len);
    if(ret < 0) {
        perror("bind fail");
        goto err2;
    }
    ret = listen(listen_fd, 10);
    if(ret < 0) {
        perror("listen fail");
        goto err2;
    }
    epoll_fd = epoll_create(MAXEPOLL);
    if(epoll_fd < 0) {
        perror("epoll_create fail");
        goto err2;
    }
    ev.events = EPOLLIN | EPOLLET;
    ev.data.fd = listen_fd;
    ret = epoll_ctl(epoll_fd, EPOLL_CTL_ADD, listen_fd, &ev);
    if(ret < 0) {
        perror("epoll_ctl fail");
        goto err3;
    }
    cur_fds = 1;
    while(1) {
        wait_fds = epoll_wait(epoll_fd, evs, cur_fds, -1);
        if(wait_fds < 0) {
            perror("epoll_wait fail");
            goto err3;
        }
        for(i=0; i<wait_fds; i++) {
            if(evs[i].data.fd == listen_fd) {
                //new connection comes
                conn_fd = accept(listen_fd, (struct sockaddr *)&client_addr, &len);
                if(conn_fd < 0) {
                    perror("accept fail");
                    goto err3;
                }
                printf("get new connection from client\n");
                ev.data.fd = conn_fd;
                ev.events = EPOLLIN | EPOLLET;
                ret = epoll_ctl(epoll_fd, EPOLL_CTL_ADD, conn_fd, &ev);
                if(ret < 0) {
                    perror("epoll_ctl fail ");
                    goto err3;
                }
                cur_fds ++;
                continue;
            }
            nread = read(evs[i].data.fd, buf, MAXLINE);
            if(nread < 0) {
                perror("read fail" );
                epoll_ctl(epoll_fd, EPOLL_CTL_DEL, evs[i].data.fd, &ev);
                close(evs[i].data.fd);
                cur_fds --;
                continue; //这个不是严重错误，不需要退出。
            }
            write(evs[i].data.fd, buf, nread);
        }
    }
    close(listen_fd);
    close(epoll_fd);
    return 0;
err4:
    close(conn_fd);
err3:
    close(epoll_fd);
err2:
    close(listen_fd);
err1:
    printf("some error happens");
    return -1;
}
```



它能显著提高程序在大量并发连接中只有少量活跃的情况下的系统CPU利用率

epoll_create()创建一个epoll的事例，通知内核需要监听size个fd。size指的并不是最大的后备存储设备，而是衡量内核内部结构大小的一个提示。当创建成功后，会占用一个fd，所以记得在使用完之后调用close()，否则fd可能会被耗尽。

Note:自从[Linux](http://www.cppfans.org/tag/linux)2.6.8版本以后，size值其实是没什么用的，不过要大于0，因为内核可以动态的分配大小，所以不需要size这个提示了。

```
EPOLLIN:表示关联的fd可以进行读操作了。
EPOLLOUT:表示关联的fd可以进行写操作了。
EPOLLRDHUP(since Linux 2.6.17):表示套接字关闭了连接，或者关闭了正写一半的连接。
EPOLLPRI:表示关联的fd有紧急优先事件可以进行读操作了。
EPOLLERR:表示关联的fd发生了错误，epoll_wait会一直等待这个事件，所以一般没必要设置这个属性。
EPOLLHUP:表示关联的fd挂起了，epoll_wait会一直等待这个事件，所以一般没必要设置这个属性。
EPOLLET:设置关联的fd为ET的工作方式，epoll的默认工作方式是LT。
EPOLLONESHOT (since Linux 2.6.2):设置关联的fd为one-shot的工作方式。表示只监听一次事件，如果要再次监听，需要把socket放入到epoll队列中。
```



epoll支持水平触发和边缘触发，**理论上来说边缘触发性能更高，但是使用更加复杂，**因为任何意外的丢失事件都会造成请求处理错误。Nginx就使用了epoll的边缘触发模型。



这里提一下水平触发和边缘触发就绪通知的区别，这两个词来源于计算机硬件设计。

它们的区别是只要句柄满足某种状态，水平触发就会发出通知；而只有当句柄状态改变时，边缘触发才会发出通知。例如一个socket经过长时间等待后接收到一段100k的数据，两种触发方式都会向程序发出就绪通知。

假设程序从这个socket中读取了50k数据，并再次调用监听函数，水平触发依然会发出就绪通知，而边缘触发会因为socket“有数据可读”这个状态没有发生变化而不发出通知且陷入长时间的等待。

**因此在使用边缘触发的 api 时，要注意每次都要读到 socket返回 EWOULDBLOCK为止。 否则netstat 的recv-q会持续增加**

通常来说，et方式是比较危险的方式，如果要使用et方式，那么，应用程序应该 1、将socket设置为non-blocking方式 2、epoll_wait收到event后，read或write需要读到没有数据为止，write需要写到没有数据为止（对于non-blocking socket来说，**EAGAIN通常是无数据可读，无数据可写的返回状态**）；

我们最近遇到一个问题，就是由于在使用epoll的过程中，缓冲区的数据没有读完，造成后续的通信失败。

表现现象就是，使用netstat -an观察时，这个socket的recv-q值不为0.



电平触发方式

对于tcp连接，内核会维护2个buffer，读buffer和写buffer。

如果读buffer有内容可供读取，那就epoll_wait就会返回。

如果写buffer还有空间可以让你进行写入操作，那么epoll_wait也会返回。

对于电平触发方式，处理的时候，就要注意：

如果关注了事件，但是在事件发生后，不进行处理（例如把socket的数据读走），那么就会导致一直触发epoll_wait马上返回。

而对于边沿触发方式，则是在收到事件后，我们写的处理代码需要一直读到返回EWOULDBLOCK为止（就是把数据全部取走）。



# 参考资料

1、I/O多路复用之poll

https://www.cnblogs.com/zengzy/p/5115679.html

2、Linux多路复用之select/poll/epoll实现原理及优缺点对比

https://blog.csdn.net/xiaofei0859/article/details/53202273

3、epoll 水平触发与边缘触发

https://blog.csdn.net/lihao21/article/details/67631516

4、I/O多路复用之水平触发和边沿触发模式

https://blog.csdn.net/fengxinlinux/article/details/75331567

5、【Linux学习】epoll详解

https://blog.csdn.net/xiajun07061225/article/details/9250579

6、epoll 水平触发 边沿触发

https://www.cnblogs.com/my_life/articles/3968782.html