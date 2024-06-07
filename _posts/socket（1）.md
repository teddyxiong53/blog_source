---
title: socket（1）
date: 2024-03-39 14:11:17
tags:
	- socket

---

--

把socket相关的内容都汇总到这一篇里来，方便查阅。

# SOCK_STREAM  SOCK_DGRAM SOCK_RAW SOCK_SEQPACKET 区别

这些常量是用于在创建套接字时指定套接字类型的参数。它们定义了不同类型的套接字，每种类型都有不同的行为和适用场景。下面是它们的区别：

1. **SOCK_STREAM**：
   - 这种套接字类型是面向连接的，提供了可靠的、基于字节流的双向数据传输。
   - 它对应于 TCP 协议，通常用于需要可靠性和顺序性的数据传输场景，如 HTTP、FTP 等应用。
   - 在使用 `socket()` 函数创建套接字时，应指定 `SOCK_STREAM` 参数来创建一个流套接字。

2. **SOCK_DGRAM**：
   - 这种套接字类型是无连接的，提供了不可靠的、无连接的数据传输服务。
   - 它对应于 UDP 协议，通常用于无需可靠性保证的数据传输场景，如 DNS 查询、DHCP 等。
   - 在使用 `socket()` 函数创建套接字时，应指定 `SOCK_DGRAM` 参数来创建一个数据报套接字。

3. **SOCK_RAW**：
   - 这种套接字类型是原始套接字，提供了对底层网络协议的直接访问。
   - 它允许应用程序直接发送和接收 IP 数据包，对网络协议的封装和解析需要应用程序自行实现。
   - 通常用于实现特殊的网络工具或协议分析器，需要特权权限才能使用。
   - 在使用 `socket()` 函数创建套接字时，应指定 `SOCK_RAW` 参数来创建一个原始套接字。

4. **SOCK_SEQPACKET**：
   - 这种套接字类型提供了面向连接的、可靠的、基于数据包的数据传输服务。
   - 与 `SOCK_STREAM` 类似，但它保留了数据包的边界。
   - 通常用于需要保留消息边界的应用，如 RPC（远程过程调用）系统、网络消息传递等。
   - 在使用 `socket()` 函数创建套接字时，应指定 `SOCK_SEQPACKET` 参数来创建一个顺序数据包套接字。

总的来说，这些套接字类型提供了不同的数据传输方式和特性，应根据具体的应用需求选择适当的套接字类型。

# linux是怎么实现对多种不同的socket的统一处理的，使用了什么设计模式？

Linux实现对多种不同socket的统一处理，主要依靠以下设计模式和机制：

1. **抽象工厂模式 (Abstract Factory Pattern)**
   - 通过创建一系列相关或互相依赖的对象，不指定它们具体的类。对于socket编程，Linux内核提供了一个统一的接口，用户可以使用这些接口创建不同类型的socket（如TCP、UDP、Unix Domain Socket等）。

2. **策略模式 (Strategy Pattern)**
   - 定义一系列的算法，把它们一个个封装起来，并且使它们可以互换。对于不同的socket协议，Linux内核通过协议族（如AF_INET, AF_UNIX等）和类型（如SOCK_STREAM, SOCK_DGRAM等）来选择不同的策略进行处理。

3. **模板方法模式 (Template Method Pattern)**
   - 定义一个操作中的算法的框架，而将一些步骤延迟到子类中。Linux内核在处理socket操作（如发送、接收数据）时，提供了一个通用的框架，但具体的实现由不同的协议处理模块来完成。

4. **多态 (Polymorphism)**
   - 通过接口实现多态，允许不同的socket类型在需要时调用自己的具体实现。内核提供一组通用的socket操作接口，不同类型的socket通过实现这些接口来提供特定的功能。

以下是Linux内核处理多种不同socket的一个简化流程：

| 步骤      | 描述                                                         |
| --------- | ------------------------------------------------------------ |
| 1. 创建   | 用户通过`socket()`系统调用创建一个socket，指定协议族和类型。 |
| 2. 初始化 | 内核通过抽象工厂模式，选择合适的socket类型，并初始化socket结构。 |
| 3. 绑定   | 通过`bind()`系统调用，用户将socket绑定到地址。内核处理具体的绑定逻辑。 |
| 4. 连接   | 通过`connect()`或`listen()`系统调用，用户发起连接或监听。    |
| 5. 通信   | 通过`send()`, `recv()`, `read()`, `write()`等系统调用进行数据传输。 |
| 6. 关闭   | 通过`close()`系统调用关闭socket，内核释放资源。              |

这些设计模式和机制使得Linux能够灵活地处理不同类型的socket，实现统一接口和多样化功能的结合。

# socket创建函数的参数说明

在Linux中，`socket()`函数用于创建一个新的套接字。其函数原型如下：

```c
int socket(int domain, int type, int protocol);
```

以下是各参数的详细说明：

1. **domain**
   - 指定协议族。常见的协议族有：
     | 值          | 说明               |
     | ----------- | ------------------ |
     | `AF_INET`   | IPv4互联网协议     |
     | `AF_INET6`  | IPv6互联网协议     |
     | `AF_UNIX`   | 本地通信（UNIX域） |
     | `AF_PACKET` | 底层网络接口访问   |

2. **type**
   - 指定套接字类型。常见的类型有：
     | 值               | 说明                                |
     | ---------------- | ----------------------------------- |
     | `SOCK_STREAM`    | 提供面向连接的可靠字节流服务（TCP） |
     | `SOCK_DGRAM`     | 提供无连接的数据报服务（UDP）       |
     | `SOCK_RAW`       | 提供原始网络协议访问                |
     | `SOCK_SEQPACKET` | 提供面向连接的可靠数据报服务        |

3. **protocol**
   - 指定协议。通常设置为0，由系统根据前两个参数自动选择合适的协议。例如，`SOCK_STREAM`通常对应TCP协议，`SOCK_DGRAM`通常对应UDP协议。可以显式指定协议，如：
     | 协议          | 说明    |
     | ------------- | ------- |
     | `IPPROTO_TCP` | TCP协议 |
     | `IPPROTO_UDP` | UDP协议 |

示例代码

```c
#include <sys/types.h>
#include <sys/socket.h>

int main() {
    int sockfd;

    // 创建一个IPv4的TCP套接字
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        // 错误处理
    }

    // 使用sockfd进行其他操作

    return 0;
}
```

此示例中，`socket(AF_INET, SOCK_STREAM, 0)`创建了一个IPv4的TCP套接字。参数`0`表示协议由系统自动选择。

# 创建蓝牙socket的参数说明

在Linux中创建蓝牙套接字时，需要使用适当的参数来指定协议族、类型和协议。蓝牙套接字的创建也使用`socket()`函数，其参数如下：

```c
int socket(int domain, int type, int protocol);
```

### 参数说明

1. **domain**
   - 指定协议族。对于蓝牙套接字，使用以下值：
     | 值             | 说明       |
     | -------------- | ---------- |
     | `AF_BLUETOOTH` | 蓝牙协议族 |

2. **type**
   - 指定套接字类型。常见的蓝牙套接字类型有：
     | 值            | 说明                                        |
     | ------------- | ------------------------------------------- |
     | `SOCK_STREAM` | 提供面向连接的服务（类似于TCP，用于RFCOMM） |
     | `SOCK_DGRAM`  | 提供无连接的数据报服务（用于蓝牙的L2CAP）   |
     | `SOCK_RAW`    | 允许直接访问蓝牙协议层                      |
   
3. **protocol**
   - 指定协议。常见的蓝牙协议有：
     | 值               | 说明                    |
     | ---------------- | ----------------------- |
     | `BTPROTO_L2CAP`  | 蓝牙L2CAP协议           |
     | `BTPROTO_RFCOMM` | 蓝牙RFCOMM协议          |
     | `BTPROTO_SCO`    | 蓝牙SCO协议（同步连接） |
     | `BTPROTO_HCI`    | 蓝牙HCI协议（低级接口） |

### 示例代码

下面是创建一个蓝牙RFCOMM套接字的示例代码：

```c
#include <sys/types.h>
#include <sys/socket.h>
#include <bluetooth/bluetooth.h>
#include <bluetooth/rfcomm.h>

int main() {
    int sockfd;

    // 创建一个蓝牙RFCOMM套接字
    sockfd = socket(AF_BLUETOOTH, SOCK_STREAM, BTPROTO_RFCOMM);
    if (sockfd == -1) {
        // 错误处理
    }

    // 使用sockfd进行其他操作

    return 0;
}
```

在这个示例中，`socket(AF_BLUETOOTH, SOCK_STREAM, BTPROTO_RFCOMM)`创建了一个用于蓝牙RFCOMM通信的套接字。

### 蓝牙套接字类型和协议总结

| **协议族 (domain)** | **套接字类型 (type)** | **协议 (protocol)** | **说明**                      |
| ------------------- | --------------------- | ------------------- | ----------------------------- |
| `AF_BLUETOOTH`      | `SOCK_STREAM`         | `BTPROTO_RFCOMM`    | 面向连接的蓝牙RFCOMM协议      |
| `AF_BLUETOOTH`      | `SOCK_DGRAM`          | `BTPROTO_L2CAP`     | 无连接的蓝牙L2CAP协议         |
| `AF_BLUETOOTH`      | `SOCK_RAW`            | `BTPROTO_HCI`       | 直接访问蓝牙协议栈的HCI协议   |
| `AF_BLUETOOTH`      | `SOCK_SEQPACKET`      | `BTPROTO_SCO`       | 面向连接的蓝牙SCO协议（语音） |

根据应用需求，选择合适的套接字类型和协议即可。

# setsockopt有哪些可以设置的内容

`setsockopt()`函数用于设置套接字的各种选项，以便控制套接字的行为。它可以设置的内容非常广泛，涉及多种协议和功能。下面是一些常见的选项，按套接字层次分类：

### 通用选项（适用于所有套接字）

- **SO_REUSEADDR**
  - 允许重新绑定地址。
  - ```c
    int optval = 1;
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(optval));
    ```

- **SO_REUSEPORT**
  - 允许多个套接字绑定同一个端口。
  - ```c
    int optval = 1;
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEPORT, &optval, sizeof(optval));
    ```

- **SO_RCVBUF**
  - 设置接收缓冲区大小。
  - ```c
    int bufsize = 8192;
    setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &bufsize, sizeof(bufsize));
    ```

- **SO_SNDBUF**
  - 设置发送缓冲区大小。
  - ```c
    int bufsize = 8192;
    setsockopt(sockfd, SOL_SOCKET, SO_SNDBUF, &bufsize, sizeof(bufsize));
    ```

- **SO_KEEPALIVE**
  - 启用TCP保持连接检测。
  - ```c
    int optval = 1;
    setsockopt(sockfd, SOL_SOCKET, SO_KEEPALIVE, &optval, sizeof(optval));
    ```

### TCP 选项

- **TCP_NODELAY**
  - 禁用Nagle算法，降低延迟。
  - ```c
    int optval = 1;
    setsockopt(sockfd, IPPROTO_TCP, TCP_NODELAY, &optval, sizeof(optval));
    ```

- **TCP_MAXSEG**
  - 设置最大分段大小（MSS）。
  - ```c
    int mss = 512;
    setsockopt(sockfd, IPPROTO_TCP, TCP_MAXSEG, &mss, sizeof(mss));
    ```

- **TCP_KEEPIDLE**
  - 设置TCP保持连接空闲时间（以秒为单位）。
  - ```c
    int idle = 60;
    setsockopt(sockfd, IPPROTO_TCP, TCP_KEEPIDLE, &idle, sizeof(idle));
    ```

- **TCP_KEEPINTVL**
  - 设置TCP保持连接探测间隔时间（以秒为单位）。
  - ```c
    int interval = 10;
    setsockopt(sockfd, IPPROTO_TCP, TCP_KEEPINTVL, &interval, sizeof(interval));
    ```

- **TCP_KEEPCNT**
  - 设置TCP保持连接探测次数。
  - ```c
    int count = 5;
    setsockopt(sockfd, IPPROTO_TCP, TCP_KEEPCNT, &count, sizeof(count));
    ```

### UDP 选项

- **UDP_CORK**
  - 阻塞数据发送，直到取消该选项。
  - ```c
    int optval = 1;
    setsockopt(sockfd, IPPROTO_UDP, UDP_CORK, &optval, sizeof(optval));
    ```

### IPv4 选项

- **IP_TTL**
  - 设置IP报文的生存时间（TTL）。
  - ```c
    int ttl = 64;
    setsockopt(sockfd, IPPROTO_IP, IP_TTL, &ttl, sizeof(ttl));
    ```

- **IP_MULTICAST_TTL**
  - 设置多播数据包的TTL值。
  - ```c
    int ttl = 64;
    setsockopt(sockfd, IPPROTO_IP, IP_MULTICAST_TTL, &ttl, sizeof(ttl));
    ```

- **IP_MULTICAST_LOOP**
  - 设置多播回环。
  - ```c
    int loop = 0;
    setsockopt(sockfd, IPPROTO_IP, IP_MULTICAST_LOOP, &loop, sizeof(loop));
    ```

### IPv6 选项

- **IPV6_V6ONLY**
  - 限制套接字只使用IPv6。
  - ```c
    int optval = 1;
    setsockopt(sockfd, IPPROTO_IPV6, IPV6_V6ONLY, &optval, sizeof(optval));
    ```

- **IPV6_MULTICAST_HOPS**
  - 设置IPv6多播数据包的跳数。
  - ```c
    int hops = 64;
    setsockopt(sockfd, IPPROTO_IPV6, IPV6_MULTICAST_HOPS, &hops, sizeof(hops));
    ```

### 示例代码

以下是设置一些常见选项的示例代码：

```c
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>

int main() {
    int sockfd;
    int optval;
    socklen_t optlen;

    // 创建一个TCP套接字
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        perror("socket");
        return 1;
    }

    // 设置SO_REUSEADDR选项
    optval = 1;
    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(optval)) == -1) {
        perror("setsockopt SO_REUSEADDR");
        close(sockfd);
        return 1;
    }

    // 设置TCP_NODELAY选项
    optval = 1;
    if (setsockopt(sockfd, IPPROTO_TCP, TCP_NODELAY, &optval, sizeof(optval)) == -1) {
        perror("setsockopt TCP_NODELAY");
        close(sockfd);
        return 1;
    }

    // 获取和打印当前发送缓冲区大小
    optlen = sizeof(optval);
    if (getsockopt(sockfd, SOL_SOCKET, SO_SNDBUF, &optval, &optlen) == -1) {
        perror("getsockopt SO_SNDBUF");
        close(sockfd);
        return 1;
    }
    printf("发送缓冲区大小: %d\n", optval);

    // 关闭套接字
    close(sockfd);

    return 0;
}
```

通过使用`setsockopt()`函数，可以灵活地配置套接字的各种行为，以满足不同的网络编程需求。

# MSG_NOSIGNAL

```
static void ctl_thread_cmd_ping(const struct request *req, int fd) {
	(void)req;
	static const struct msg_status status = { STATUS_CODE_PONG };
	send(fd, &status, sizeof(status), MSG_NOSIGNAL);
}

```

**send()函数中的MSG_NOSIGNAL标志**

在Linux网络编程中，使用`send()`函数发送数据时可以设置一些标志（flags），`MSG_NOSIGNAL`就是其中之一。该标志的作用是防止在向已经关闭的套接字（socket）写入数据时，程序收到`SIGPIPE`信号，导致程序异常终止。

