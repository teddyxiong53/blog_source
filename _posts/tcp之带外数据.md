---
title: tcp之带外数据
date: 2020-05-09 13:19:08
tags:
	- socket

---

1

tcp带外数据，也叫紧急数据。

一般用于中断某些操作，例如中断ftp文件的传输。

tcp带外数据，可以理解为本地向对端发送一个signal。

收到带外数据时，系统会产生一个SIGURG信号。

tcp带外数据，就是一个普通的字节，只是tcp header里的flag置位了而已。

tcp带外数据，有严格的规定。

```
1、每个连接只有一个tcp带外数据。
2、每个连接只有一个带外标记。
3、每个连接只有一个单字节的带外缓冲区。
```

简单来说，就是在tcp接收缓冲区里，一次只能有一个带外数据存在，这个带外数据只有一个字节。

socket的send和recv函数，最后都有一个flag。平时一般我们都是填0，传输带外数据的时候，就有用了。

```
ssize_t send(int sockfd, const void *buf, size_t len, int flags);
ssize_t recv(int sockfd, void *buf, size_t len, int flags);
```

常用的flag有：

```
#define MSG_OOB       0x0001
#define MSG_FIN       0x0200
#define MSG_SYN       0x0400
#define MSG_RST       0x1000
```

下面看一个简单的例子。有2个文件，send.c和receive.c。

send.c

```
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <unistd.h>
#include <strings.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define SERV_PORT 5555

int tcp_connect(){
    struct sockaddr_in serv;
    int sockfd;

    sockfd=socket(AF_INET,SOCK_STREAM,0);
    assert(sockfd);
    bzero(&serv,sizeof(serv));
    serv.sin_family=AF_INET;
    serv.sin_port=htons(SERV_PORT);
    serv.sin_addr.s_addr=inet_addr("127.0.0.1");

    assert(connect(sockfd,(struct sockaddr *)&serv,sizeof(serv)) == 0);
    return sockfd;
}

int main(int argc, char *argv[]) {
    int sockfd=tcp_connect();
    write(sockfd,"123",3);
    printf("wrote 3 bytes of normal data\n");
    sleep(1);

    send(sockfd,"444",3,MSG_OOB);
    printf("wrote 3 byte of OOB data\n");
    sleep(1);

    write(sockfd,"56",2);
    printf("wrote 2 bytes of normal data\n");
    sleep(1);

    send(sockfd,"7",1,MSG_OOB);
    printf("wrote 1 byte of OOB data\n");
    sleep(1);

    write(sockfd,"89",2);
    printf("wrote 2 bytes of normal data\n");
    sleep(1);

    return 0;
    return 0;
}

```



receive.c

```
#include <stdio.h>
#include <fcntl.h>
#include <signal.h>
#include <assert.h>
#include <stdlib.h>
#include <unistd.h>
#include <strings.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define SERV_PORT 5555

int sockfd,connfd;

int tcp_listen(){
    struct sockaddr_in serv;
    int sockfd;

    sockfd=socket(AF_INET,SOCK_STREAM,0);
    assert(sockfd);
    bzero(&serv,sizeof(serv));
    serv.sin_family=AF_INET;
    serv.sin_port=htons(SERV_PORT);
    serv.sin_addr.s_addr=inet_addr("127.0.0.1");

    assert(bind(sockfd,(struct sockaddr *)&serv,sizeof(serv)) == 0);
    assert(listen(sockfd,10) == 0);
    return sockfd;
}

void sig_urg(int signo){
    int n;
    char buff[10];

    printf("SIGURG received\n");
    n=recv(connfd,buff,sizeof(buff)-1,MSG_OOB);
    buff[n]=0;
    printf("read %d OOB bytes: %s\n",n,buff);
}

int main(int argc, char *argv[]) {
    sockfd=tcp_listen();
    connfd=accept(sockfd,NULL,NULL);

    signal(SIGURG,sig_urg);
    fcntl(connfd,F_SETOWN,getpid());

    int n;
    char buff[100];
    for(;;){
        if((n=read(connfd,buff,sizeof(buff)-1)) == 0){
            printf("received EOF\n");
            exit(0);
        }
        buff[n]=0;
        printf("read %d bytes: %s\n",n,buff);
    }
    return 0;
}

```



从上面的例子可以看到，发送带外数据，如果超过1个字节，多的部分，在后续的接收操作里，当做正常数据去接收了。





参考资料

1、TCP带外数据

https://www.cnblogs.com/cfans1993/p/6598327.html

