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
int epoll_create(int size);//这个size参数实际上没有用了。
int epoll_ctl(int epfd, int op, int fd, struct  epoll_event * event);
	//epfd是epoll_create得到的。
	//op是EPOLL_CTL_ADD/DEL/MOD 3个之一。
	//fd是要监听的fd。例如listen_fd。
	//event，前面先定义一个structepoll_event。把epfd注册过去，并且设置电平触发等方式先。
int epoll_wait(int epfd, struct epoll_event *events, int maxevents, int timeout);
	//events：是要监听的所有事件。
	返回值是就绪的事件个数。
```



# epoll的水平触发和边沿触发

简单来说，水平触发，只要还有数据，就会一直触发事件给监听进程。

而边沿触发，只有在数据的量发生增加或者减少变化时，才触发一次。

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
    epfd = epoll_create(1);
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



select和poll都只支持电平触发。

epoll默认也是电平触发。

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