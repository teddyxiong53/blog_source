---
title: 网络之ifreq
date: 2018-04-13 08:37:59
tags:
	- 网络

---



struct ifreq，是interface request的缩写。

表示的是对接口的配置和信息获取。

定义在net/if.h里。是C库里的。但是我看到linux源代码里也有一个ifreq的定义。

我们还是以C库的为分析对象。

结构体的定义如下：

```
struct ifreq {
  union {
    char ifrn_name[16];
  }ifr_ifrn;
  union {
    struct sockaddr ifru_addr,
    	ifru_dstaddr,
    	ifru_broadaddr,
    	ifru_netmask,
    	ifru_hwaddr;
    short ifru_flags;
    int ifru_ivalue;
    int ifru_mtu;
    struct ifmap ifru_map;
    char ifru_slave[16];
    char ifru_newname[16];
    void *ifru_data;
  } ifr_ifru;
};
```

里面就两个union。

为了方便对结构体里的成员进行访问，定义一组宏。主要就是把union这一层隐藏掉。

```
#define ifr_name ifr_ifrn.ifrn_name
#define ifr_hwaddr ifr_ifru.ifru_hwaddr
...
```

里面涉及的ifmap结构体定义如下：

```
struct ifmap {
  ulong mem_start;
  ulong mem_end;
  ushort  base_addr;
  uchar irq;
  uchar dma;
  uchar port;
};
```

从ifreq里的内容，我们也可以推断出，这个结构体是用来设置和获取mtu、ip地址这些信息的。

都是在ioctl用的。所以还要配合一组宏来做。这些宏定义在bits/ioctl.h里。

```
#define SIOCGIFNAME 0x8910
...
```

ifconfig这个工具，就是基于ifreq来实现的。

另外还有一个struct ifconf结构体。这个相当于是ifreq的集合。

具体看下面的例子。

我们先看一个简单的例子。

```
#include <stdio.h>
#include <net/if.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/ioctl.h>


int main()
{
    int sock;
    struct ifreq ifr;
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    strcpy(ifr.ifr_name, "eth0");
    ioctl(sock, SIOCGIFADDR, &ifr);
    printf("%s\n", inet_ntoa(((struct sockaddr_in *)&(ifr.ifr_addr))->sin_addr));
    return 0;
}
```

从这个例子，我们也可以看出基于ifreq的程序的基本结构。

就是先要建立一个socket。然后对这个socket进行ioctl。

再看一个复杂一点的例子，自己实现ifconfig的部分功能。

```
#include <stdio.h>
#include <net/if.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/ioctl.h>

#define MAX_INTERFACE 16

void port_status(unsigned int flags)
{
    if(flags & IFF_UP) {
        printf("is up\n");
    }
    if(flags & IFF_BROADCAST) {
        printf("is broadcast\n");

    }
    if(flags & IFF_LOOPBACK) {
        printf("is loopback\n");
    }
    if(flags & IFF_POINTOPOINT) {
        printf("is point to point\n");
    }
    if(flags & IFF_RUNNING) {
        printf("is running\n");
    }
    if(flags & IFF_PROMISC) {
        printf("is promisc\n");
    }
}
int get_if_info(int fd)
{
    struct ifconf ifc;
    struct ifreq buf[MAX_INTERFACE];
    ifc.ifc_len = sizeof(buf);
    ifc.ifc_buf = (caddr_t) buf;
    int ret;
    ret = ioctl(fd, SIOCGIFCONF, (char *)&ifc);
    if(ret) {
        printf("get ifconfig failed \n");
        return -1;
    }
    int if_num = ifc.ifc_len/sizeof(struct ifreq);
    printf("interface num is :%d\n", if_num);

    while(if_num-- > 0) {
        printf("net device:%s\n", buf[if_num].ifr_name);
        ret = ioctl(fd, SIOCGIFFLAGS, (char *)&buf[if_num]);
        if (ret ) {
            continue;
        }
        port_status(buf[if_num].ifr_flags);
        ret = ioctl(fd, SIOCGIFADDR, (char *)&buf[if_num]);
        if(ret) {
            continue;
        }
        printf("ip addr is:%s\n", inet_ntoa(((struct sockaddr_in *)&(buf[if_num].ifr_addr))->sin_addr));

    }
}

int main()
{
    int sock;
    struct ifreq ifr;
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if(sock > 0) {
        get_if_info(sock);
        close(sock);
    }
    return 0;
}
```

```
teddy@teddy-ubuntu:~/work/test/c-test$ ./a.out 
interface num is :3
net device:docker0
is up
is broadcast
ip addr is:172.17.0.1
net device:eth0
is up
is broadcast
is running
ip addr is:192.168.190.137
net device:lo
is up
is loopback
is running
ip addr is:127.0.0.1
```



# lwip之ifreq

我看了一下，lwip里不支持这种方式。

ifconfig这种命令是直接访问netif_list链表的。



# 参考资料

1、struct ifreq学习和实例

https://blog.csdn.net/gujintong1110/article/details/45530911