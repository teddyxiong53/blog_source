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
├── icmp6.h
├── if_ether.h
├── if_fddi.h
├── if_tr.h
├── igmp.h
├── in.h：这个重要，600行左右。定义了各种宏，和sockaddr_in。
├── in_systm.h
├── ip6.h
├── ip.h：定义了ip包头。
├── ip_icmp.h
├── tcp.h
└── udp.h
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

#参考资料

