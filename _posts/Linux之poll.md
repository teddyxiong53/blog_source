---
title: Linux之poll
date: 2018-04-13 19:05:08
tags:
	- Linux
---

--

# 简介

关于poll，需要关注的代码，都在这里了。（从musl的poll.h里摘录出来）

```
#define POLLIN 0X01
#define POLLPRI 0X02
#define POLLOUT 0X4
typdef unsigned long nfds_t;

struct pollfd {
    int fd;
    short events;//注册事件。
    short revents;//收到的事件。
};

int poll(struct pollfd *, nfds_t , int);
```



我们写一个echo server。来进行测试。

```
teddy@teddy-ubuntu:~/work/test/poll$ ls
client.c  Makefile  server.c
```

Makefile

```
.PHONY: all clean
all:
	gcc server.c -o server
	gcc client.c -o client
clean:
	rm server client
```



server.c

```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <poll.h>
#include <unistd.h>
#include <sys/types.h>
#include <assert.h>
#include <fcntl.h>
#include <arpa/inet.h>

#define OPEN_MAX 1000

static void handle_connection(struct pollfd *connfds, int num)
{
    int i = 1;
    for(i=1; i<=num; i++) {
        if(connfds[i].fd < 0) {
            continue;
        }
        if(connfds[i].revents & POLLIN) {
            char buf[1024] = {0};
            int n = read(connfds[i].fd, buf, 1024);
            if(n == 0) {
                close(connfds[i].fd);
                connfds[i].fd = -1;
                continue;
            }
            printf("recv:");
            write(STDOUT_FILENO, buf, n);
            write(connfds[i].fd, buf, n);
        }
    }
}
static void do_poll(int listenfd)
{
    struct pollfd clientfds[OPEN_MAX];
    clientfds[0].fd = listenfd;
    clientfds[0].events = POLLIN;
    int i = 0;
    for(i=1; i<OPEN_MAX; i++) {
        clientfds[i].fd = -1;
    }
    int maxi = 0;
    int nready = 0;
    struct sockaddr_in client_addr = {0};
    socklen_t addr_len = sizeof(client_addr);
    int connfd;
    while(1) {
        nready = poll(clientfds, maxi+1, -1);
        if(nready == -1) {
            perror("poll error");
            exit(-1);
        }
        if(clientfds[0].revents & POLLIN) {
            addr_len = sizeof(client_addr);
            connfd = accept(listenfd, (struct sockaddr *)&client_addr, &addr_len);
            printf("get connection from %s:%d\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
            if(connfd < 0) {
                if(errno == EINTR) {
                    continue;
                } else {
                    perror("accept error");
                    exit(-1);
                }
            }
            for(i=1; i<OPEN_MAX; i++) {
                if(clientfds[i].fd == -1) {
                    clientfds[i].fd = connfd;
                    break;
                }
            }
            if(i == OPEN_MAX) {
                printf("too many connection\n");
                exit(-1);
            }
            clientfds[i].events = POLLIN;
            if(i > maxi) {
                maxi = i;
            }
            if(--nready <= 0) {
                continue;
            }
        }
        handle_connection(clientfds, maxi);
    }
}
int main()
{
    struct sockaddr_in serveraddr = {0};
    int listenfd ;
    listenfd = socket(AF_INET, SOCK_STREAM, 0);
    assert(listenfd > 0);
    serveraddr.sin_family = AF_INET;
    serveraddr.sin_addr.s_addr = INADDR_ANY;
    serveraddr.sin_port = htons(8000);
    int val = 1;
    setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, &val, sizeof(val));
    int flags = fcntl(listenfd, F_GETFL);
    flags |= O_NONBLOCK;
    fcntl(listenfd, F_SETFL, flags);
    
    int ret;
    ret = bind(listenfd, (struct sockaddr*)&serveraddr, sizeof(serveraddr));
    if(ret < 0) {
        perror("bind fail");
    }
    assert(ret == 0);
    ret = listen(listenfd, 5);
    do_poll(listenfd);
}
```

client.c

```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <poll.h>
#include <unistd.h>
#include <sys/types.h>


#define IPADDR "127.0.0.1"
#define PORT 8080

#define MAXLINE 1024

void handle_connection(int  sockfd)
{
    char sendline[MAXLINE];
    char recvline[MAXLINE];
    struct pollfd pfds[2];
    pfds[0].fd = sockfd;
    pfds[0].events = POLLIN;
    pfds[1].fd = STDIN_FILENO;
    pfds[1].events = POLLIN;
    int n;
    while(1) {
        poll(pfds, 2, -1);
        if(pfds[0].revents & POLLIN) {
            n = read(pfds[0].fd, recvline, MAXLINE);
            if(n == 0) {
                printf("server is closed\n");

                close(sockfd);
                exit(1);
            }
            write(STDOUT_FILENO, recvline, n);
        }
        if(pfds[1].fd & POLLIN) {
            n = read(STDIN_FILENO, sendline, MAXLINE);
            if(n == 0) {
                shutdown(sockfd, SHUT_WR);
                continue;
            }
            write(sockfd, sendline, n);
        }
    }
}
int main(int argc, char **argv)
{
    int sockfd;
    struct sockaddr_in server_addr;
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if(sockfd < 0) {
        perror("socket error");
        exit(1);
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    inet_aton(IPADDR, &server_addr.sin_addr);
    server_addr.sin_port = htons(PORT);
    connect(sockfd, (struct sockadrr *)&server_addr, sizeof(server_addr));
    handle_connection(sockfd);
    return 0;
}
```

# POLLHUP什么时候会发生

`POLLHUP` 事件在 Linux 中发生时通常表示以下情况之一：

1. **挂断事件**：`POLLHUP` 通常与挂断事件相关。当在终端或串口通信中，远程设备或连接方关闭连接时，将会发生挂断事件。这通常会导致读取 `POLLIN` 事件和挂断事件 `POLLHUP`。

2. **套接字关闭**：在网络编程中，当另一端的套接字关闭时，将触发 `POLLHUP` 事件。这表明连接已经终止，不再可用于数据传输。

3. **管道关闭**：当管道的写端关闭，但读端仍然存在时，将触发 `POLLHUP` 事件。

4. **FIFO关闭**：在 FIFO（命名管道）通信中，当写入端关闭，但读取端仍然存在时，将触发 `POLLHUP` 事件。

5. **其他文件描述符关闭**：在一般文件描述符的情况下，当文件被关闭时，将触发 `POLLHUP` 事件。

`POLLHUP` 事件通常用于通知应用程序连接已经关闭或者文件描述符不再可用于读取或写入数据。

应用程序可以使用 `revents` 字段中的事件掩码来检测 `POLLHUP` 事件是否已经发生。

==一旦 `POLLHUP` 事件发生，应用程序通常应该执行相应的清理操作==，关闭文件描述符或进行其他必要的处理。

需要注意的是，不是每种文件描述符类型都会在关闭时触发 `POLLHUP` 事件。

在使用 `poll` 或其他多路复用机制时，要小心处理各种事件，以确保及时处理关闭连接或文件的情况。

# POLLHUP和POLLERR什么区别

`POLLHUP` 和 `POLLERR` 是 `poll` 系统调用中的两种不同的事件标志，它们表示了不同的事件：

1. **POLLHUP（Hang Up）**：`POLLHUP` 事件通常表示文件描述符的挂断事件。它发生在以下情况：

   - 当在终端或串口通信中，远程设备或连接方关闭连接时，将会发生挂断事件。
   - 在网络编程中，当另一端的套接字关闭时，将触发 `POLLHUP` 事件。这表明连接已经终止，不再可用于数据传输。
   - 当管道的写端关闭，但读端仍然存在时，将触发 `POLLHUP` 事件。
   - 在 FIFO（命名管道）通信中，当写入端关闭，但读取端仍然存在时，将触发 `POLLHUP` 事件。
   - 当一般文件描述符关闭时，将触发 `POLLHUP` 事件。

   `POLLHUP` 通常用于通知应用程序连接已经关闭或文件描述符不再可用于读取或写入数据。

2. **POLLERR（Error）**：`POLLERR` 事件表示文件描述符上发生了错误事件。它发生在以下情况：

   - 当文件描述符处于错误状态时，例如套接字发生错误。
   - 当连接套接字的远程端口发生错误或连接失败。
   - 当文件描述符不处于合法状态或出现了某种错误条件时。

   `POLLERR` 通常用于通知应用程序文件描述符上发生了错误，可能需要进行错误处理和故障排除。

要注意的是，`POLLHUP` 和 `POLLERR` 是独立的事件标志，可以同时设置。在使用 `poll` 系统调用时，应用程序可以使用 `revents` 字段中的事件掩码来检测这两种事件是否已经发生。处理 `POLLHUP` 和 `POLLERR` 事件的方式通常取决于具体的应用和使用情况，但通常它们都需要进行相应的错误处理和资源清理。



# 驱动里的poll

