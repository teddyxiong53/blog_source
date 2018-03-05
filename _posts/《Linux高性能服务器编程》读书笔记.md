---
title: 《Linux高性能服务器编程》读书笔记
date: 2018-03-05 12:24:52
tags:
	- Linux
typora-root-url: ..\
---



全书结构：

```
第一篇 基础理论
	第一章 tcpip协议族介绍
	第二章 ip协议详解
	第三章 tcp协议详解
	第四章 tcpip通信案例
	
第二篇 相关接口
	第五章 linux网络编程基础api
	第六章 高级io函数。
	第七章 linux服务器程序规范
	第八章 高性能服务器程序框架（核心章节）
	第九章 io复用
	第十章 信号
	第十一章 定时器
	第十二章 高性能io框架库libevent
	第十三章 多进程编程
	第十四章 多线程编程
	第十五章 线程池和进程池
	
第三篇 优化与检测
	第十六章 调试
	第十七章 检测
```

# 第一章

![tcpip协议栈](/images/tcpip协议栈.png)

一个简单典型的层次情况是上图这样的。

ARP实现mac地址、令牌环地址、802.11地址到ip地址的转换。

ICMP是ip协议的补充。

OSPF是开放最短路径优先协议，是路由器上的动态路由更新协议。



# 第二章

##ip协议基本特点

ip协议为上层提供无状态、无连接、不可靠的服务。

无状态。

意味着所有的ip包之间没有上下文关系。所以没法处理乱序问题。乱序由传输层的来解决。

无状态带来的好处是：简单高效。

网络协议栈里无状态的还有http。连续两次http请求对于服务器来说没有区别。

无连接。

意味着通信双方都不会保持对方的任何信息。所以每次发送都要带上ip地址才行。

不可靠。

表示ip协议不能保证ip包可以准确达到对方。它只是尽最大努力。可靠性也是要靠传输层来做。

## ip分片

当ip包的长度超过MTU的时候，包会被分片。

分片可能在发生在服务器端，也可能在中间的路由器上。而且在传输过程中可能被多次分片。

分片只有到达最终目的地的时候，才会被组装起来。

组装的依据有哪些？

```
数据报标识。
标志
片offset
```

一个ip包被分片后，它的标识符是相同的。但是有不同的片偏移。

并且除了最后一个分片外，其他分片都有MF标志。

另外，每个分片的ip头部的总长度被设置为该分片的长度。

一般设置以太网的mtu是1500字节。

所以ip数据包里的内容最多是1480字节（20字节是ip头部）。

我们现在分析用ip数据包封装一个1481字节的ICMP包。这个包在传输的时候，会被分片。



![IP包分片](/images/IP包分片.png)

这个数据包的构造，可以这样：

```
ping 192.168.1.2 -s 1473
```

这就就可以了。

## 路由机制

不看。

## ip转发

默认都没有打开ip转发功能。

是对于有多个网卡的机器有用。

# 第三章

tcp就实现了ip不能保证的可靠和基于连接。

可靠性是通过应答机制。每次发送的报文必须得到对方的应答，才认为这个段发送成功了。

另外，还有超时重传机制。

```
重传默认5次。
时间间隔依次拉长。
1s、2s、4s、8s、16s。这样的拉长。
```



tcp是一对一的，所以多播和广播就只能用udp了。

发送端执行的写操作次数跟接受端执行的读操作的次数没有数量关系。这就是字节流的概念。

应用程序对数据的接收和发送是没有边界限制的。

udp就不能这样。这个是通过发送缓冲区和接受缓冲区来做到的。

##抓一个telnet的数据交互流

1、在树莓派上开一个shell窗口。输入：

```
tcpdump -nt -i loop port 23
```

这个会阻塞，输出内容是实现出来的。

2、另外开一个shell窗口。输入：

```
telnet 127.0.0.1
按照提示输入用户名密码。默认pi那个。
```

进去后，你会发现tcpdump那边已经出来一堆的内容了。把那个窗口内容清理掉。

在telnet这边，输入ls。你可以看到你输入“l”的时候，tcpdump那边出来了这个：

```
[1]：IP 127.0.0.1.44714 > 127.0.0.1.23: Flags [P.], seq 117:118, ack 966, win 350, options [nop,nop,TS val 42853654 ecr 42852210], length 1
[2]：IP 127.0.0.1.23 > 127.0.0.1.44714: Flags [P.], seq 966:967, ack 118, win 342, options [nop,nop,TS val 42853654 ecr 42853654], length 1
[3]：IP 127.0.0.1.44714 > 127.0.0.1.23: Flags [.], ack 967, win 350, options [nop,nop,TS val 42853654 ecr 42853654], length 0
[4]：IP 127.0.0.1.44714 > 127.0.0.1.23: Flags [P.], seq 118:119, ack 967, win 350, options [nop,nop,TS val 42853670 ecr 42853654], length 1
[5]：IP 127.0.0.1.23 > 127.0.0.1.44714: Flags [P.], seq 967:968, ack 119, win 342, options [nop,nop,TS val 42853670 ecr 42853670], length 1
[6]：IP 127.0.0.1.44714 > 127.0.0.1.23: Flags [.], ack 968, win 350, options [nop,nop,TS val 42853670 ecr 42853670], length 0
[7]：IP 127.0.0.1.44714 > 127.0.0.1.23: Flags [P.], seq 119:121, ack 968, win 350, options [nop,nop,TS val 42893634 ecr 42853670], length 2
[8]：IP 127.0.0.1.23 > 127.0.0.1.44714: Flags [P.], seq 968:970, ack 121, win 342, options [nop,nop,TS val 42893634 ecr 42893634], length 2
[9]：IP 127.0.0.1.44714 > 127.0.0.1.23: Flags [.], ack 970, win 350, options [nop,nop,TS val 42893634 ecr 42893634], length 0
[10]：IP 127.0.0.1.23 > 127.0.0.1.44714: Flags [P.], seq 970:1053, ack 121, win 342, options [nop,nop,TS val 42893634 ecr 42893634], length 83
[11]：IP 127.0.0.1.44714 > 127.0.0.1.23: Flags [.], ack 1053, win 350, options [nop,nop,TS val 42893634 ecr 42893634], length 0
[12]：IP 127.0.0.1.23 > 127.0.0.1.44714: Flags [P.], seq 1053:1071, ack 121, win 342, options [nop,nop,TS val 42893634 ecr 42893634], length 18
[13]：IP 127.0.0.1.44714 > 127.0.0.1.23: Flags [.], ack 1071, win 350, options [nop,nop,TS val 42893634 ecr 42893634], length 0
```

你的输入是一个个字节这样发送过来的。而不是“ls”2个字母一起发送的。

我们把上面的报文前面加上编号。总共13个报文。

报文1：发送字母“l“。

报文2：服务器对字母“l”的回显发送给客户端。

报文3：服务器对报文1的ack。

报文4/5/6：对字母“s”的处理。

报文7：是2个字节。是回车符和EOF 。

报文8和9：对报文7的回显。

报文10：服务器把处理结构发送给客户端。83字节。

报文11：客户端对报文10的ack。

报文12：服务器重新发送一个命令行提示符给客户端：`pi@raspberrypi:~$`18个字节。

报文13：对报文12的ack。



注意：这个例子是在本地测试的。在局域网内也可以得到基本类似的结果。但是在广域网上，就不一定了。

因为这就是著名的小包文件，一个字符就对应一个tcp包。效率太低了。解决方法就Nagle算法。

telnet可以开启本地回显就不依赖远程服务器发回来的了。



##tcp成块数据流

下面用ftp来传输一个大文件。



当传输大量大块数据的时候，发送方会连续发送多个tcp报文段。接收方可以一次性确认所有这些报文。

连续发送的报文段的个数，就窗口大小。



# 第四章

先构造一个场景。

![通过代理访问http场景](/images/通过代理访问http场景.png)

一个http请求可能被多个代理服务器转发。

代理服务器分类：

```
1、正向代理。
	要求客户端自己设置proxy的地址。
	局域网要屏蔽一些网站的时候，就是用这种方式。很常见。
	个人向外发出访问。
2、反向代理。
	服务端来设置。客户端不需要做任何的设置。
	用proxy来接收网络上来的请求，然后把请求转发给内部服务器去处理。
	公司从外面接收访问。
3、透明代理。
	只能用在网关上。可以看做正向代理的一种特殊情况。
```



整个通信过程：

1、代理服务器访问dns服务器以查询百度网址对应的ip地址。对应数据包8和9 。

2、代理服务器查询路由器mac地址的arp请求和应答，对应数据包6和9 。

3、运行curl的192.168.0.109和代理服务器192.168.0.108的http通信。包括数据包1-5,23-25,32-40,42和43 。

4、代理服务器和web服务器之间的http通信。包括数据包10-22,26-31和41



## http请求

GET/HEAD/PUT/DELETE连续多次执行和只发送一次，效果是一样，被认为的等幂的。

POST方法则不是等幂的。多次发送可能进一步影响服务器上的资源。



# 第五章

linux网络api分为3种：

```
1、socket地址api。
	sockaddr_in结构体。
	字节序转换函数。
	
2、socket基础api。
	定义在sys/socket.h里。
3、网络信息api。
	定义在netdb.h里。
	gethostbyname。
```



# 第六章

高级函数。没什么。



# 第七章

linux服务器程序规范。

服务器程序除了网络通信之外，还需要考虑很多的其他的细节，这些细节涉及广泛而有琐碎，而且基本上是模板式的。我们把这些细节叫做linux服务器程序规范。

一般包括这些内容：

```
1、设置为守护进程。
2、日志设置。
3、服务器程序一般以一个非root的用户身份运行，例如syslogd就以syslog这个名字来运行。
4、配置文件，一般放在/etc目录。
5、pid文件，放在/var/run目录下。
6、考虑最大的限制数。
```



## 日志

服务器的调试和维护都一个专业的日志系统。linux提供了一个守护进程syslogd来做这个事情。

syslogd的升级版本是rsyslogd。

rsyslogd既能接受用户进程输出的日志，也能接受内核的日志。

用户进程通过调用syslog函数来生成系统日志。

这个函数是把日志输出到unix类型的socket文件/dev/log，而rsyslogd则是一直在检测这个文件。

内核的日志是printk打印到内核的ring buffer里，而ring buffer的内容直接映射到/proc/kmsg文件中。rsyslogd是通过这个来获取内核日志。

rsyslogd拿到日志内容后，会输出到几个不同个的文件里。

内核日志放到/var/log/kern.log

调试信息放到/var/log/debug

普通信息放到/var/log/messages

这些可以在/etc/rsyslog.conf里配置。



## 用户信息

用户信息对于服务器的安全是很重要的。

很多的服务器就必须以root身份启动，但是不能以root身份运行。

一个进程有2个用户id：uid和euid。

euid存在的意义是方便资源访问。它使得运行程序的user拿到改程序的有效用户的权限。

例如su程序。普通用户启动su程序如何能访问/etc/passwd文件呢？

我们用ls查看一下su程序。

```
pi@raspberrypi:~$ ls /bin/su -l
-rwsr-xr-x 1 root root 34776 Jan 24  2016 /bin/su
```

而且，注意权限里的rws的s这字母。表示的是set-user-id。这个标志的含义是：普通用户运行su程序的时候，它的有效用户就是该程序的所有者root。

我们写一个简单的程序来看看。

```
#include <unistd.h>
#include <stdlib.h>

void main()
{
    uid_t uid = getuid();
    uid_t euid = geteuid();

    printf("uid is:%d, euid is:%d \n", uid, euid);
}
```

运行：

```
pi@raspberrypi:~/test/c-test$ ./test_uid 
uid is:1000, euid is:1000 
```

我们把这个程序的owner改为root。看看。

```
pi@raspberrypi:~/test/c-test$ sudo chown root:root test_uid
pi@raspberrypi:~/test/c-test$ ls -l
total 12
-rw-r--r-- 1 pi   pi    177 Mar  5 15:56 test.c
-rwxr-xr-x 1 root root 5920 Mar  5 15:56 test_uid
pi@raspberrypi:~/test/c-test$ ./test_uid 
uid is:1000, euid is:1000 
```

可以看到现在euid还是1000 。

再给test_uid加上set-user-id的标志。再看。

```
pi@raspberrypi:~/test/c-test$ sudo chmod +s test_uid 
pi@raspberrypi:~/test/c-test$ ./test_uid 
uid is:1000, euid is:0 
```

### 如何把以root身份启动的进程切换为普通用户身份运行？

```
static int switch_to_user(uid_t uid, gid_t gid)
{
    //1.确保目标用户不是root用户。
    if(uid == 0 && gid == 0)
    {
        return -1;
    }
    //2.确保当前用户是合法用户。
    //当前用户可以是root，或者目标用户。
    gid_t gid1 = getgid();
    uid_t uid1 = getuid();
    if(
        (gid !=0 || uid !=0 )
            && (gid1 != gid || uid1 != uid)
    )
    {
        return -1;
    }
    //如果不是root，则说明已经是模板用户了。
    //直接返回成功。
    if(uid1 != 0)
    {
        return 0;
    }
    //切换到目标用户。
    int ret |= setgid(gid);
    ret |= setuid(uid);
    if(ret)
    {
        return -1;
    }
    return 0;
}
```

## 会话

查看进程信息。

```
pi@raspberrypi:~/test/c-test$ ps -o pid,ppid,pgid,sid,comm | less
  PID  PPID  PGID   SID COMMAND
  420   418   420   420 bash
29184   420 29184   420 ps
29185   420 29184   420 less
```

这3个进程的关系是：

```
bash：这个group 420的首领，session 420的首领。
	-->fork得到ps，是group 29184的首领。
	-->fork得到less。
```



# 第八章

高性能服务器程序框架。

这个是本书的核心。也是后面章节的总览。

服务器程序可以分为3大块：

1、io处理器单元。

2、逻辑单元。

3、存储单元。

## 服务器模型

1、C/S模型。

最简单常用的模型。

![cs架构](/images/cs架构.png)



2、P2P模型。

P2P比C/S模型更加接近于网络通信的实际情况。

它抛弃了以服务器为中心的格局。

让网络上所有的主机重新回到对等的地位。

云计算群可以看做P2P模型的一个典范。



## io模型

socket在创建的时候，默认是阻塞的。

有2种方法改为非阻塞的：

1、传递SOCK_NONBLOCK表，在socket函数创建时。

2、用fcntl的F_SETFL命令。



socket的基本api里，可能阻塞的：

```
accept
connect 
send
recv
```



##两种高效的事件处理模式

服务器程序一般需要处理的事件有3种：

1、io事件。

2、信号。

3、定时事件。

在讨论具体的事件处理之前，我们先看看两种高效的事件处理模式。Reactor和Proactor。

这个是属于网络设计模式的范畴。

### Reactor模式

1、要求主线程只负责监听fd上是否有event发生。有的话，马上通知工作线程（就是逻辑单元）。

2、除此之外，main线程不做其他任何实质性的事情。

### Proactor模式

1、根Reactor模式不同，Proactor把所有的io操作都交给main线程和内核来处理。工作线程仅仅负责业务逻辑。



## 并发模式

1、多线程。

2、多进程。



##状态机

状态机是给逻辑单元内部用的。



## 提高服务器性能的其他建议



# 第九章

io复用的方法。

这些情况需要进行io复用处理。

```
1、client程序需要同时处理多个socket。
2、client程序要同时处理用户输入和网络连接
	比如说聊天室应用。
3、server同时处理监听socket和链接socket。这个是最常见的。
4、服务器要同时处理tcp请求和udp请求。
5、服务器要同时监听多个端口。
```

## select

可读的就绪条件：

1、socket的内核接收缓冲区里的字节数大于等于水线值SO_RCVLOWAT。

2、socket的对方关闭了。read返回0 。

3、listenfd上收到新的连接。

4、socket上有未处理的错误。这时候我们可以用getsockopt来读取和清除该错误。

可写的就绪条件：

1、socket的内核发送缓冲区里的字节数大于等于水线值SO_SNDLOWAT。

2、socket对端被关闭。进行写会触发EPIPE。

3、connect连接成功或者失败之后。

4、有未处理的错误。



对于网络程序，select能够处理的异常情况只有一种，socket上收到带外数据。

就是exception_fdset会被置位。

## poll



## epoll



## 用poll实现一个聊天室程序

代码我放在这里了。

客户端用poll同时监听用户输入和网络连接，并利用splice函数将用户的输入内容直接定向到网络连接上，这样就实现了零拷贝，提高了程序的执行效率。



## 超级服务xinetd

以太网服务进程xinetd，管理这多个子服务。也就是监听了多个端口。

配置文件在/etc/xinetd.d目录下。但是我看我的系统里都没有。连进程都没有。



# 第十章

信号。

不看了。



# 第十一章

定时器。

不看。



# 第十二章

libevent讲解。

前面我们讲到，服务器程序必须处理3类事件：io事件，信号、定时事件。

如何处理，有这几条原则：

1、统一事件源。io复用就是一种统一事件源的方法。

2、可移植性。

3、对并发的支持。

开源社区提供了很多的框架，libevent比较轻量的一种。

使用了libevent的著名案例有：分布式内存对象缓存软件memcached、chromium浏览器。

io框架库，封装了底层的系统调用，更加方便使用。而且高效合理，经过了大量的测试。

各种io框架库原理都是一样的。要么用Reactor模式，要么用Proactor模式，要么二者结合。

基于Reactor的框架库包含这么几个组件：

1、句柄Handle。

2、事件多路分发器EventDemultiplexer。

3、事件处理器EventHandler。

4、具体的事件处理器ConcreteEventHandler。

5、Reactor。这个是框架库的核心。

```
handle_events。
register_handler。
remove_handler。
```

工作时序是这样的：

![Reactor框架流程](/images/Reactor框架流程.png)



## libevent

特点：

```
1、跨平台。
2、统一事件源。
3、线程安全。用libevent_pthreads来提供线程安全支持。
4、基于Reactor模式实现。
```

树莓派上安装libevent。

```
1、从http://libevent.org/这里下载源代码。
2、配置编译。
./configure --prefix=/usr   
make
make install
```



先看一个简单的使用例子。

```
#include <sys/signal.h>
#include <event.h>

int signal_cb(int fd, short event, void *argc)
{
    struct event_base *base = (struct event_base *)argc;
    struct timeval delay = {2, 0};
    printf("catch a signal ,exit in two seconds \n");
    event_base_loopexit(base, &delay);
}

int timeout_event(int fd, short event, void *argc)
{
    printf("timeout \n");
}

int main()
{
    struct event_base *base = event_init();
    struct event *signal_event = evsignal_new(base, SIGINT, signal_cb, base);
    event_add(signal_event, NULL);
    
    struct timeval tv = {1, 0};
    struct event *timeout_event = evtimer_new(base, timeout_cb, NULL);
    event_add(timeout_event, &tv);
    
    event_base_dispatch(base);
    
    event_free(timeout_event);
    event_free(signal_event);
    event_base_free(base);
    
}
```





































