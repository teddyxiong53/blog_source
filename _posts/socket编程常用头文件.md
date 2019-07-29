---
title: socket编程常用头文件
date: 2018-08-01 10:28:29
tags:
	- 网络
---





#arpa目录

```
hlxiong@hlxiong-VirtualBox:/usr/include/arpa$ tree
.
├── ftp.h：很少用。
├── inet.h：包含了netinet/in.h（需要sockaddr_in定义），定义了inet_ntop等函数。
	这个必须要用。
├── nameser_compat.h：
├── nameser.h
├── telnet.h
└── tftp.h
```

只有inet.h经常用。其余都不管。

# netinet目录

netxx目录有这些：

```
hlxiong@hlxiong-VirtualBox:/usr/include$ cd net
net/       netash/    netatalk/  netax25/   neteconet/ netinet/   netipx/    netiucv/   netpacket/ netrom/    netrose/   nettle/   
```

只有inet杀出了重围，得到了广泛应用。

```
hlxiong@hlxiong-VirtualBox:/usr/include/netinet$ tree
.
├── ether.h
	定义了ether_ntoa和ether_aton。
├── icmp6.h
	这个不用。
├── if_ether.h
	定义了2个结构体。
	ethhdr
	ether_arp
├── if_fddi.h
	不用。
├── if_tr.h
├── igmp.h
├── in.h：
	这个重要，600行左右。定义了各种宏，和sockaddr_in。
├── in_systm.h
├── ip6.h
├── ip.h：定义了ip包头。
├── ip_icmp.h
├── tcp.h
	定义tcphdr。
└── udp.h
	定义udphdr。
```

主要就用in.h这个就够了。

# sys目录

这个就是跟系统相关的了。所以都是软连接。

```
hlxiong@hlxiong-VirtualBox:/usr/include/sys$ tree
.
├── acct.h -> ../x86_64-linux-gnu/sys/acct.h
├── asoundlib.h
├── auxv.h -> ../x86_64-linux-gnu/sys/auxv.h
```

重要的就是socket.h。定义了send等函数。

还有types.h。定义了基础类型。



# net目录

这个下面就4个头文件。偏硬件底层。

```
ethernet.h
	定义了一个以太网帧头结构体。
	包含了netinet/if_ether.h头文件。
if.h
	1、网卡名字长度最长16字符。
	2、定义了if_nameindex结构体。2个成员：索引、名字。
		配套4个函数。
	3、包含sys/socket.h头文件。
	4、定义IFF_XX这些标志。
	5、ifaddr。网卡地址结构体。
	6、ifmap。
		被ifreq包含，不会单独使用。
	7、ifreq。
		这个一般用来在C语言里用ioctl获取ip地址、mac地址的。
	8、ifconf。
		保存所有接口信息。
if_arp.h
	1、arphdr。
	2、arpreq。
	3、arpd_request。
route.h
	这个很少用。
```



看musl目录下的头文件。

发现这些特点：

1、netinet/if_ether.h。

这个里面定义了一个ethhdr的头文件。而在net/ethernet.h里。定义了一个ether_header的头文件。

本质是一样的。这个说明这些头文件定义有功能重叠的部分。

更加坑的是，这个2个头文件还相互进行了包含。



总的来说，包含3个就够了。分别在3个目录下。

```
#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>
```



#参考资料

1、ioctl和struct ifreq

https://wenku.baidu.com/view/59f4508d680203d8ce2f2412.html