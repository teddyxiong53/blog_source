---
title: Linux之poll
date: 2018-04-13 19:05:08
tags:
	- Linux
---



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



# 驱动里的poll

