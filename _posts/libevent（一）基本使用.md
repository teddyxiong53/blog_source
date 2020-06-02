---
title: libevent（一）基本使用
date: 2018-03-10 10:33:41
tags:
	- 网络
	- libevent

---



web服务器往往是需要处理海量连接的。

传统的处理海量连接的方法，往往会有各种问题，因为它们使用的内存或者CPU太多，或者达到了os的某个限制值。

传统方法主要有：

1、循环。最直观最古老的技术，效率低。

2、poll、epoll。对循环方法的改进。

3、select。限制1024 。

在其他的非linux平台上还有其他的实现，例如Solaris的/dev/poll、BSD上的kqueue。但是无法移植。

处理大量连接的另一个方法是，利用多线程来处理连接，但是对ram和cpu的开销较大。

许多内核不适于处理大量的活跃线程。

# libevent的著名应用

1、memcached。



# libevent做了什么

libevent实际上并没有更换select、poll这些基础机制，而是使用对于每个平台最高效的解决方法上进行了封装。

提供的事件系统，使得为一个连接添加一个处理函数，变得非常简单。

同时降低了底层io的复杂性。

这是libevent的核心。

libevent还提供了其他的实现：

1、缓冲的事件系统。

2、http、dns、rpc系统的核心实现。

创建一个libevent服务器的基本方法：

1、注册发送某个操作（例如连接）时的处理函数。

2、调用事件循环event_dispatch。

# echo服务器的例子

echo是网络编程里的HelloWorld。实现的功能就是把client发来的东西原样发回去。

我们看看用libevent如何实现。

```
#include <event.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <assert.h>
#include <errno.h>


#define SERVER_PORT 8082

int debug = 0;

struct client {
    int fd;
    struct bufferevent *buf_ev;
};

int setnonblock(int fd) 
{
    int flags;
    flags = fcntl(fd, F_GETFL);
    flags |= O_NONBLOCK;
    fcntl(fd, F_SETFL, flags);
    return 0;
}

void buf_read_callback(struct bufferevent *incoming, void *arg)
{
    struct evbuffer *evreturn;
    char *req;
    req = evbuffer_readline(incoming->input);
    assert(req != NULL);
    evreturn = evbuffer_new();
    evbuffer_add_printf(evreturn, "You said %s\n", req);
    bufferevent_write_buffer(incoming, evreturn);
    evbuffer_free(evreturn);
    free(req);
}

void buf_write_callback(struct bufferevent *bev, void *arg)
{
    
}
void buf_error_callback(struct bufferevent *bev, short what, void *arg)
{
    struct client *client = (struct client*)arg;
    bufferevent_free(client->buf_ev);
    close(client->fd);
    free(client);
}

void accept_callback(int fd, short ev, void *arg)
{
    int connfd ;
    struct sockaddr_in clientaddr = {0};
    struct client *client;
    errno = 0;
    int size = sizeof(clientaddr);
    connfd = accept(fd, (struct sockaddr *)&clientaddr, &size);
    printf("connfd :%d \n",connfd);
    if(connfd < 0)
    {
        perror("accept failed");
    }
    assert(connfd > 0);
    setnonblock(connfd);
    client = calloc(1, sizeof(*client));
    assert(client != NULL);
    client->fd = connfd;
    client->buf_ev = bufferevent_new(connfd, buf_read_callback, buf_write_callback, buf_error_callback, client);
    bufferevent_enable(client->buf_ev, EV_READ);
    
}

int main(int argc, char **argv)
{
    int listenfd ;
    struct sockaddr_in serveraddr = {0};
    struct event accept_event;
    
    event_init();
    listenfd = socket(AF_INET, SOCK_STREAM, 0);
    assert(listenfd>0);
    printf("listenfd:%d \n", listenfd);
    
    serveraddr.sin_family = AF_INET;
    serveraddr.sin_addr.s_addr = INADDR_ANY;
    serveraddr.sin_port = htons(SERVER_PORT);
    int ret;
    ret = bind(listenfd, (struct sockaddr *)&serveraddr, sizeof(serveraddr));
    printf("ret:%d \n", ret);
    assert(ret == 0);
    ret = listen(listenfd, 5);
    assert(ret == 0);
    int val = 1;
    setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, &val, sizeof(val));
    setnonblock(listenfd);

    event_set(&accept_event, listenfd, EV_READ|EV_PERSIST, accept_callback, NULL);
    event_add(&accept_event ,NULL);
    printf("before dispatch \n");
    event_dispatch();
    close(listenfd);
    
    return 0;
    
}
```

编译：

```
gcc test.c -levent
```

发现没有安装libevent，下载libevent源代码：

```
# 配置
./configure
# 编译
make 
# 安装
sudo make install 
```

测试：

```
pi@raspberrypi:~$ telnet 127.0.0.1 8082
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
xx
You said xx
fe
You said fe
fef
You said fef
```



# libevent内置的http服务器

libevent里的http实现，并不是Apache的替代品，而是适用于云和web环境的大规模动态内容的实用解决方案。

例如，可以在IBM Cloud或者其他解决方案中部署基于libevent的接口。

下面看最简单的例子。

```
#include <event.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <assert.h>
#include <errno.h>
#include <evhttp.h>


void generic_request_handler(struct evhttp_request *req, void *arg)
{
    struct evbuffer *returnbuffer = evbuffer_new();
    evbuffer_add_printf(returnbuffer, "thanks for the request");
    evhttp_send_reply(req, HTTP_OK, "Client", returnbuffer);
    evbuffer_free(returnbuffer);
    return;
}


int main(int argc, char **argv)
{
    short http_port = 8081;
    char *http_addr = "192.168.0.109";
    struct evhttp *http_server = NULL;
    event_init();
    http_server = evhttp_start(http_addr, http_port);
    evhttp_set_gencb(http_server, generic_request_handler,NULL  );
    event_dispatch();
    return 0;
}   
```

测试，在电脑上用浏览器访问：

```
http://192.168.0.109:8081/
```

得到一句：

```
thanks for the request
```



http包装器提供许多其他的功能。

例如，有一个请求解析器，它会从典型的请求中提取出查询参数。

还可以设置在不同的请求路径中要触发的处理函数。

例如，“/db”提供数据库相关接口这样。

另外一个重要特性就是支持通用定时器。

一个应用就是在新闻频发的时候，提供及时更新服务。下面是一个例子。

```
#include <event.h>
#include <sys/types.h>

#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <assert.h>
#include <errno.h>
#include <evhttp.h>

#define DEFAULT_FILE "sample.html"

#define RELOAD_TIMEOUT 5

char *filedata;
time_t lasttime = 0;
char filename[80];
int counter = 0;


void read_file()
{
    struct stat buf = {0};
    int size = 0;
    stat(filename, &buf);
    if(buf.st_mtime > lasttime) {
        fprintf(stderr, "reloading file:%d \n", filename);
    } else {
        fprintf(stderr, "loading file:%d \n", filename);
    }
    FILE *f = fopen(filename, "rb");
    if(f == NULL) {
        fprintf(stderr, "fopen %s failed \n", filename);
        exit(1);
    }
    fseek(f, 0, SEEK_END);
    size = ftell(f);
    fseek(f, 0, SEEK_SET);
    char *data = (char *)malloc(size+1);
    fread(data, sizeof(char), size, f);
    filedata = (char *)malloc(size+1);
    strcpy(filedata, data);
    free(data);
    fclose(f);
    lasttime = buf.st_mtime;

}
void load_file()
{
    struct event *loadfile_event;
    struct timeval tv;
    read_file();
    tv.tv_sec = RELOAD_TIMEOUT;
    tv.tv_usec = 0;
    loadfile_event = malloc(sizeof(struct event));
    evtimer_set(loadfile_event, load_file, loadfile_event);
    evtimer_add(loadfile_event, &tv);
    
}

void generic_request_handler(struct evhttp_request *req, void *arg)
{
    struct evbuffer *evb = evbuffer_new();
    evbuffer_add_printf(evb, "%s", filedata);
    evhttp_send_reply(req, HTTP_OK, "Client", evb);
    evbuffer_free(evb);
    
}
int main(int argc, char **argv)
{
    short http_port = 8081;
    char *http_addr = "192.168.0.109";
    struct evhttp *http_server = NULL;
    if(argc > 1) {
        strcpy(filename, argv[1]);
    } else {
        strcpy(filename, DEFAULT_FILE);
    }
    event_init();
    load_file();
    http_server = evhttp_start(http_addr, http_port);
    evhttp_set_gencb(http_server, generic_request_handler,NULL  );
    event_dispatch();
    return 0;
}   
```





# event和event_base关系

结构体event和event_base是libevent的两个核心数据结构，**前者代表一个事件对象，后者代表整个事件处理框架。**

Libevent通过**event对象将I/O事件、信号事件和定时器事件封装**，从而统一处理，这也是libevent的精妙所有。

```
(1) ev_events：event关注的事件类型，它可以是以下3种类型： 
I/O事件： EV_WRITE和EV_READ 
定时事件：EV_TIMEOUT 
信号：    EV_SIGNAL 
辅助选项：EV_PERSIST，表明是一个永久事件 
```



struct bufferevent 

写入数据的一般过程是：

1、现在应用要发送数据，把数据放入缓冲区里。

2、等待可以写入。

3、如果可以写了，写入尽量多的数据。

4、记住已经写入了多少数据，如果一次没有写完，则在再次可写时继续写入。

libevent为这个提供了一个通用的机制，就是bufferevent。

作用是在读取或者写入达到足够数量时，调用对应的回调函数。

bufferevent只能用于tcp这样基于流的协议。



bufferevent和evbuffer的关系

bufferevent包含了evbuffer。bufferevent里有2个evbuffer，一个输入的，一个输出的。



# 定时器例子

定时器的原理是这样：

Libevent **根据所有定时器事件的最小超时时间来设置系统 I/O 的 timeout 值**，当系统I/O 返回时，再激活就绪的定时器事件，如此 Timer 事件便可融合在系统 I/O 机制中。

定时器事件的实现基于一种经典的数据结构-小根堆，相关的数据结构定义和操作在*minheap-internal.h*中。

其处理与其他两种事件类似。 **不同之处在于定时器事件不依赖于文件描述符，在初始化该类型事件时，文件描述符处的参数为-1**，在注册定时器事件是，后面的时间参数不为 *NULL*。如下：



参考资料

1、libevent--学习使用struct bufferevent

https://blog.csdn.net/qq_36337149/article/details/89922974

2、

https://zhuanlan.zhihu.com/p/87562010

3、Libevent 编程- 定时器事件（timer event）

https://blog.csdn.net/u010090316/article/details/70833334

4、libevent学习笔记四——timer小根堆

https://blog.csdn.net/NMG_CJS/article/details/89602970