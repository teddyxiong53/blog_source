---
title: Linux网络之tun和tap
date: 2018-04-10 23:17:08
tags:
	- Linux网络

---

--

我们现在处在云计算时代，到处都是虚拟机和容器。

支撑它们的网络管理都要靠虚拟网络设备。

所以了解虚拟网络设备，有利于我们更好的理解云时代的网络结构。



# 概念

## tun

是tunnel的缩写。

tun虚拟的是三层设备，处理的是ip包。相比之下，tap是二层设备，处理的是链路层，例如以太网包。

使用虚拟网络设备，可以实现隧道。例如openvpn就是这样实现的。

## tap

tap不是缩写，就是完整单词，表示水龙头的意思。

## 关系

1、tap是二层设备，tun是三层设备。

2、tap用来创建网桥，tun用来路由。



通过tun和tap发送的数据，是传送到用户空间程序。这个程序把自己跟设备进行了绑定。

用户程序也可以向tun和tap发送数据。



# 典型应用

## 虚拟私有网络

1、openvpn。

2、FreeLAN。

3、OpenSSH。

4、其他。

## 虚拟机网络

1、bochs。

2、coLinux。

3、UserMode Linux。

4、VirtualBox。

## NAT

1、tayga。



开源项目openvpn （http://openvpn.sourceforge.net）和Vtun(http://vtun.sourceforge.net)都是利用tun/tap驱动实现的隧道封装。

## 真实应用场景分析

我们的vpn应用，都是在本地起一个127.0.0.1:1080这样的一个端口监听。

我们发数据，就是发到这个地址。数据就被vpn应用收到了。

vpn应用再把数据往物理网卡上发送。

vpn就是tun/tap最最常用的情况了。



# 应用编写

我们还是通过一个应用来直观地认识tun和tap。

这里有一个简单的tun的例子。

https://github.com/gregnietsky/simpletun

这个包含了tun和tap的情况。写得比较完善，我们就重点分析它。

先看看用法：

```
./simpletun -i tun13 [-s|-c serverip] [-p port] [-u|-a] [-d] 
-s：server模式。
-c：client模式。
-p：端口。
-u：tun模式。
-a：tap模式。
-d：调试模式。
-h：帮助。
```

需要运行2个实例，一个做server，一个做client。

这个还是复杂了一点。不便于抓住问题的本质。

我找到一个简单的。

```
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <sys/types.h>
#include <linux/if_tun.h>
#include <stdlib.h>
#include <stdio.h>

int tun_alloc(int flags)
{
    struct ifreq ifr;
    int fd, err;
    char *clonedev = "/dev/net/tun";
    fd = open(clonedev, O_RDWR);
    if(fd <0) {
        
        printf("open failed");
        return fd;
    }
    memset(&ifr, 0, sizeof(ifr));
    ifr.ifr_flags = flags;
    err = ioctl(fd, TUNSETIFF, (void *)&ifr);
    if(err < 0) {
        close(fd);
        return err;
    }
    printf("open tun/tap device:%s for reading\n", ifr.ifr_name);
    return fd;
}

int main()
{
    int tun_fd, nread;
    char buffer[1500];
    tun_fd = tun_alloc(IFF_TUN|IFF_NO_PI);
    if(tun_fd < 0) {
        perror("alloc interface");
        exit(1);
    }
    while(1) {
        nread = read(tun_fd, buffer, sizeof(buffer));
        if(nread < 0) {
            perror("read from interface");
            close(tun_fd);
            exit(1);
        }
        printf("read %d bytes from tun/tap device\n", nread);
    }
    return 0;
}
```

这就是会产生一个tun0的网卡。

测试过程如下：

1、第一个shell窗口，编译代码，运行。

```
gcc test.c
teddy@teddy-ubuntu:~/work/test/c-test$ sudo ./a.out 
open tun/tap device:tun0 for reading
```

这样运行后，用ifconfig -a查看，可以看到。

```
tun0      Link encap:UNSPEC  HWaddr 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  
          POINTOPOINT NOARP MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:500 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
```

2、第二个shell窗口。tun0还不是up状态。所以我们需要配置ip和启动。

```
ifconfig tun0 192.168.3.2 netmask 255.255.255.0
sudo ifup tun0
```

3、还是在第二shell窗口，我们打开tcpdump监听。

```
sudo tcpdump -i tun0
```

4、打开第三个shell窗口。我们开始ping

```
ping 192.168.3.1 #注意这里是3.1，而不是我们配置的3.2 。
```

现在我们观察到的一个shell窗口，有打印输出：

```
teddy@teddy-ubuntu:~/work/test/c-test$ sudo ./a.out 
open tun/tap device:tun0 for reading
read 84 bytes from tun/tap device
read 84 bytes from tun/tap device
read 84 bytes from tun/tap device
read 84 bytes from tun/tap device
```

我们观察到第二shell窗口，也有打印输出。

```
teddy@teddy-ubuntu:~$ sudo tcpdump -i tun0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on tun0, link-type RAW (Raw IP), capture size 262144 bytes
10:13:16.640613 IP bogon > bogon: ICMP echo request, id 50407, seq 1, length 64
10:13:17.650239 IP bogon > bogon: ICMP echo request, id 50407, seq 2, length 64
10:13:18.658164 IP bogon > bogon: ICMP echo request, id 50407, seq 3, length 64
10:13:19.666327 IP bogon > bogon: ICMP echo request, id 50407, seq 4, length 64
```



# VTun代码分析

https://sourceforge.net/projects/vtun/files/vtun/3.0.3/vtun-3.0.3.tar.gz/download?use_mirror=jaist

下载地址在这里。

VTun是Virtual Tunnel over TCP/IP network。

```
 ./configure
```



```
gcc -g -O2  -I/usr/include/lzo -I/usr/include/openssl -I/usr/include/openssl -I/usr/include/openssl -I/usr/include/openssl -o vtund main.o cfg_file.tab.o cfg_file.lex.o server.o client.o lib.o llist.o auth.o tunnel.o lock.o netlib.o tun_dev.o tap_dev.o pty_dev.o pipe_dev.o tcp_proto.o udp_proto.o linkfd.o lfd_shaper.o lfd_zlib.o lfd_lzo.o lfd_encrypt.o lfd_legacy_encrypt.o  -lz -llzo2 -lcrypto
```

报了一个错误；

```
/home/teddy/work/tuntap/vtun-3.0.3/main.c:142: undefined reference to `clear_nat_hack_flags'
collect2: error: ld returned 1 exit status
Makefile:62: recipe for target 'vtund' failed
make: *** [vtund] Error 1
teddy@teddy-ubuntu:~/work/tuntap/vtun-3.0.3$ grep -nwr "clear_nat_hack_flags" .
./main.c:142:   clear_nat_hack_flags(svr);
./vtun.h:234:inline void clear_nat_hack_flags(int svr);
./cfg_file.tab.c:2396:inline void clear_nat_hack_flags(int svr)
./cfg_file.y:612:inline void clear_nat_hack_flags(int svr)
```

在C文件里有inline函数被外面用到。我们把inline去掉就好了。

install的时候，Makefile里也有个小错误。就是指定了strip的路径，跟我的系统的安装路径不匹配。

安装了这些东西。二进制的就是一个vtund。配置文件是vtund.conf文件。

```
/usr/bin/install -c -m 600 -o root -g 0 vtund.conf /usr/local/etc; 
/usr/bin/install -c -d -m 755 -o root -g 0 /usr/local/var/run
/usr/bin/install -c -d -m 755 -o root -g 0 /usr/local/var/log/vtund
/usr/bin/install -c -d -m 755 -o root -g 0 /usr/local/var/lock/vtund
/usr/bin/install -c -d -m 755 -o root -g 0 /usr/local/sbin
/usr/bin/install -c -m 755 -o root -g 0 vtund /usr/local/sbin
strip /usr/local/sbin/vtund
```

我们先看看vtund.conf文件。内容还比较多。

tun/tap在内核里添加了一个tun/tap的虚拟网络设备驱动程序，和对应的/dev/net/tun。

tun/tap还可以作为字符设备被访问（是一个misc设备）。这是不同于普通的物理网卡的一点。

# 操作

1、看看内核是否支持tun/tap

```
root@LEDE:/# modinfo tun
module:         /lib/modules/4.4.71/tun.ko
alias:          devname:net/tun
alias:          char-major-10-200
license:        GPL
depends:
```

如果没有，就modprobe tun。

2、看看有没有tunctl。没有的话，安装一下。

这个是添加一个叫tap0的网卡。

```
tunctl -t tap0 -u root
```

然后配置tap0网卡。

```
ifconfig tap0 192.168.1.1 netmask 255.255.255.0 promisc
```

promisc是promiscuous。混杂模式。



# 内核代码

驱动代码在drivers/net/tun.c里。

mylinuxlab默认没有编译，到menuconfig里的网络驱动里，打开。

运行，现在可以看到打印这个：

```
tun: Universal TUN/TAP device driver, 1.6
```

```
static struct miscdevice tun_miscdev = {
	.minor = TUN_MINOR,//200
	.name = "tun",
	.nodename = "net/tun",
	.fops = &tun_fops,
};
```



```
IFF_NO_PI - Do not provide packet information
```

if_tun.h



看看在协议栈里的实现。



# 再次尝试

1、确认host是支持tap和tun设备的。

```
ls /dev/net/tun 
存在这设备说明支持，默认都支持的。
```

2、编写qemu的tap初始化脚本。保存到/etc/qemu-ifup。增加可执行权限。

```
#!/bin/sh 
/sbin/ifconfig $1 192.168.0.11 
```

3、qemu命令启动时，增加tap网卡。

```
-net tap
```

注意：因为创建TAP网卡需要root权限，所以必须用root用户启动QEMU。

虚拟机启动后，用ifconfig命令设置网络，要求它的IP与host的tap网口的IP（即在上个步骤里qemu-ifup文件中设置的IP）处于同一网段。例如： 
ifconfig eth0 192.168.0.110 netmask 255.255.255.0 

**虚拟机通过host连接internet** 
现在实现了虚拟机和host的联网，如果需要虚拟机连接internet，则要在host设置NAT： 
echo 1 > /proc/sys/net/ipv4/ip_forward 
iptables -t nat -A POSTROUTING -o eth0 -s 192.168.0.0/24 -j MASQUERADE 

 

# 参考资料

1、Documentation/networking/tuntap.txt

2、维基百科

https://www.wikiwand.com/en/TUN/TAP

3、Linux下Tun/Tap设备通信原理

https://www.cnblogs.com/woshiweige/p/4532207.html

4、linux下TUN/TAP虚拟网卡的使用 - heidsoft

https://blog.csdn.net/hshl1214/article/details/52936091

5、What does ifconfig promisc mode do, or promiscuous mode in general?

https://serverfault.com/questions/106647/what-does-ifconfig-promisc-mode-do-or-promiscuous-mode-in-general

6、Tun/Tap interface tutorial

http://backreference.org/2010/03/26/tuntap-interface-tutorial/

7、Linux虚拟网络设备之tun/tap。这位作者的文章都值得一读。

https://segmentfault.com/a/1190000009249039

8、用TAP方式让QEMU虚拟机与host联网

https://blog.csdn.net/larryliuqing/article/details/27127843