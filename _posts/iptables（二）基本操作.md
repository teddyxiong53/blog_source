---
title: iptables（二）基本操作
date: 2018-04-13 10:18:56
tags:
	- iptables

---



对于iptables，也是增删改查。

我们先看最简单的查。

#查

前面我们已经提到四张表：raw表、nat表、filter表、mangle表。

filter是最常用的，我们就先查询filter表。

为了全局掌控和安全起见，我在mylinuxlab里进行试验。

然后发现busybox默认没有带iptables。

下载源代码。教程编译。

```
git clone git://git.netfilter.org/iptables.git
```

配置，编译。

```
#生成configure文件。
./autogen.sh 
./configure -host=arm-linux-gnueabi CC=arm-linux-gnueabi-gcc
```

配置过程配到几个依赖库没有的文件，安装就好。

编译出错。

正确的配置应该是这样。

```
./configure --host=arm-linux-gnueabi --enable-static --disable-shared --with-ksource=/home/teddy/work/mylinuxlab/kernel/linux-stable
```

有报一个udata.h的头文件找不到的问题，我注释掉对应的行。

继续编译。报一些符号找不到的问题。

```
../extensions/libext4.a(initext4.o): In function `init_extensions4':
/home/teddy/work/iptables/iptables/extensions/initext4.c:20: undefined reference to `libipt_CLUSTERIP_init'
/home/teddy/work/iptables/iptables/extensions/initext4.c:21: undefined reference to `libipt_DNAT_init
```

这些符号在哪里定义呢？怎么都找不到这些的定义。

```
/usr/lib/gcc-cross/arm-linux-gnueabi/5/../../../../arm-linux-gnueabi/bin/ld: cannot find -lmnl
/usr/lib/gcc-cross/arm-linux-gnueabi/5/../../../../arm-linux-gnueabi/bin/ld: cannot find -lnftnl
```



算了，暂时不管了。我还是就在我的

这个打开，里面很多选项我也打开看看。

```
 [*] Network packet filtering framework (Netfilter)  ---> 
```

全部选择编译到内核里。

还是不行。我不管了。

我选择在我的一个alpine虚拟机上实验。保险起见，我先拍一个快照。

安装iptables。

```
m-alpine-0:~$ sudo apk add --update iptables
[sudo] password for teddy: 
fetch https://mirrors.aliyun.com/alpine/v3.7/main/x86/APKINDEX.tar.gz
fetch https://mirrors.aliyun.com/alpine/v3.7/community/x86/APKINDEX.tar.gz
(1/4) Installing libmnl (1.0.4-r0)
(2/4) Installing jansson (2.10-r0)
(3/4) Installing libnftnl-libs (1.0.8-r1)
(4/4) Installing iptables (1.6.1-r1)
Executing busybox-1.27.2-r7.trigger
OK: 1256 MiB in 459 packages
```

查询filter表。

```
vm-alpine-0:~$ sudo iptables -t filter -L 
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
```

可以看到当前都是空的。

当不带-t选项的时候，默认就是查询filter表。

我们还可以查询指定的链的情况。

```
vm-alpine-0:~# iptables -L INPUT
Chain INPUT (policy ACCEPT)
target     prot opt source               destination 
```

# 增

在进行操作之前，我们先清空input这个链的内容。

```
iptables -F INPUT
```

-F表示flush。不过我的默认也是没有任何规则的。

```
vm-alpine-0:~# iptables -nvL INPUT
Chain INPUT (policy ACCEPT 46 packets, 3608 bytes)
 pkts bytes target     prot opt in     out     source               destination         
vm-alpine-0:~# 
```

可以看到默认是accept的。

我现在的环境是这样的：

```
电脑win7:192.168.190.1
Ubuntu虚拟机：192.168.190.137
alpine虚拟机：192.168.190.131
```

是通过ssh2远程到alpine上的，所以在后续修改的时候，要保证win7跟alpine的连接不要断开。

默认3台机器，相互都可以ping通的。

现在增加一条规则，让Ubuntu无法访问alpine。

在alpine里执行

```
iptables -t filter -I INPUT -s 192.168.190.137 -j DROP
```

执行后，果然Ubuntu不能再ping通alpine了。

上面命令分析：

```
-I：插入到INPUT这个链里。
-s：源地址。
-j：jump的缩写。
```

现在再看统计。

```
vm-alpine-0:~# iptables -nvL INPUT
Chain INPUT (policy ACCEPT 82 packets, 6452 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    2   168 DROP       all  --  *      *       192.168.190.137      0.0.0.0/0  
```

我们再加一条接受Ubuntu的数据的规则，那最后的效果是接受还是拒绝呢？

```
iptables -t filter -A INPUT -s 192.168.190.137 -j ACCEPT
```

-A 表示追加。

实际是无法ping通的。

```
vm-alpine-0:~# iptables -nvL INPUT
Chain INPUT (policy ACCEPT 43 packets, 3280 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    4   336 DROP       all  --  *      *       192.168.190.137      0.0.0.0/0           
    0     0 ACCEPT     all  --  *      *       192.168.190.137      0.0.0.0/0 
```

没有匹配到ACCEPT的内容。

因为是从前面往后面走的。前面已经被拦截了。

我们在插入ACCEPT到前面看看。

```
iptables -t filter -I INPUT -s 192.168.190.137 -j ACCEPT
```

现在就是可用ping通的了。

```
vm-alpine-0:~# iptables -nvL INPUT
Chain INPUT (policy ACCEPT 15 packets, 964 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    2   168 ACCEPT     all  --  *      *       192.168.190.137      0.0.0.0/0           
    6   833 DROP       all  --  *      *       192.168.190.137      0.0.0.0/0           
    0     0 ACCEPT     all  --  *      *       192.168.190.137      0.0.0.0/0  
```

所以iptables的工作机制就是匹配到，就执行，后面的就不会继续去匹配了。

我们可以指定新的规则插入的位置。

```
iptables -t filter -I INPUT 2 -s 192.168.190.140 -j ACCEPT
```

查看。

```
vm-alpine-0:~# iptables -nvL INPUT --line-number
Chain INPUT (policy ACCEPT 92 packets, 7372 bytes)
num   pkts bytes target     prot opt in     out     source               destination         
1        2   168 ACCEPT     all  --  *      *       192.168.190.137      0.0.0.0/0           
2        0     0 ACCEPT     all  --  *      *       192.168.190.140      0.0.0.0/0           
3        6   833 DROP       all  --  *      *       192.168.190.137      0.0.0.0/0           
4        0     0 ACCEPT     all  --  *      *       192.168.190.137      0.0.0.0/0           
```

## 更加复杂的条件

在上面这些演示里，我们的调节都很简单。

加入我想过滤多个ip地址，怎么写？用逗号隔开。逗号两边都不能有空格。

```
iptables -t filter -I INPUT -s 192.168.190.131,192.168.190.141 -j DROP
```

指定某个网段。

```
-s 192.168.0.0/24
```

条件取反。

```
! -s 192.168.0.1 -j ACCEPT
```

这个表示除了192.168.0.1的，都接受。

## 扩展模块

-m选项就是扩展模块。可以通过插件的方式，增强iptables的功能。

常用的模块有：

1、iprange。

2、string。

3、time。

4、connlimit。

5、limit。

6、tcp、upd、icmp。

7、state





# 参考资料

1、iptables移植到arm 

http://www.360doc.com/content/15/0122/20/18578054_442918216.shtml

2、iptables系列教程。本文主要参考这个。

http://www.zsythink.net/archives/tag/iptables/page/2/