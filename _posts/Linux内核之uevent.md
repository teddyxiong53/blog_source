---
title: Linux内核之uevent
date: 2019-12-05 16:05:28
tags:
	- Linux
---

1

什么是uevent机制？

这个问题需要从设备的热插拔说起。

典型的就是U盘的热插拔。

当我们在设备上插入U盘时，系统的usb hub就会检测到U盘插入，并且完成设备枚举过程。

所谓枚举，就是从U盘上读取出对应的信息。

然后在内核里创建相应的结构体。

但是usb设备千奇百怪，内核不可能预先把所有usb设备驱动都load到内存里。

也就说，插入设备的时候，系统里对应该usb设备的驱动可能还没有被加载到内存。

驱动ko文件，是放在硬盘上 。

那么我们就需要从用户态来载入这个驱动。

当前你可以手动来加载驱动，但是这个无疑是很麻烦的。

为了解决这种问题，就推出了uevent机制。

uevent机制是指：

当有新的设备加入时，内核将设备的消息发送到用户态，用户态有一个udev进程一直在监听这一类消息。

udev检测到消息后，会做一些之前配置好的工作，包括加载驱动。



uevent是kobject的一部分。

用于在kobject状态发生变化时，通知用户空间。

通知的途径有两种：

1、kmod。

2、netlink。

```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <asm/types.h>
//该头文件需要放在netlink.h前面防止编译出现__kernel_sa_family未定义
#include <sys/socket.h>  
#include <linux/netlink.h>

void MonitorNetlinkUevent()
{
    int sockfd;
    struct sockaddr_nl sa;
    int len;
    char buf[4096];
    struct iovec iov;
    struct msghdr msg;
    int i;

    memset(&sa,0,sizeof(sa));
    sa.nl_family=AF_NETLINK;
    sa.nl_groups=NETLINK_KOBJECT_UEVENT;
    sa.nl_pid = 0;//getpid(); both is ok
    memset(&msg,0,sizeof(msg));
    iov.iov_base=(void *)buf;
    iov.iov_len=sizeof(buf);
    msg.msg_name=(void *)&sa;
    msg.msg_namelen=sizeof(sa);
    msg.msg_iov=&iov;
    msg.msg_iovlen=1;

    sockfd=socket(AF_NETLINK,SOCK_RAW,NETLINK_KOBJECT_UEVENT);
    if(sockfd==-1)
        printf("socket creating failed:%s\n",strerror(errno));
    if(bind(sockfd,(struct sockaddr *)&sa,sizeof(sa))==-1)
        printf("bind error:%s\n",strerror(errno));

    len=recvmsg(sockfd,&msg,0);
    if(len<0)
        printf("receive error\n");
    else if(len<32||len>sizeof(buf))
        printf("invalid message");
    for(i=0;i<len;i++)
        if(*(buf+i)=='\0')
            buf[i]='\n';
    printf("received %d bytes\n%s\n",len,buf);
}

int main(int argc,char **argv)
{
    MonitorNetlinkUevent();
    return 0;
}
```



参考资料

1、内核Uevent事件机制 与 Input子系统

https://www.cnblogs.com/sky-heaven/p/6394267.html

2、

http://www.wowotech.net/device_model/uevent.html

3、Netlink实现热拔插监控

https://blog.csdn.net/findaway123/article/details/53122437