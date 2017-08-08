---
title: Linux命令之tcpdump
date: 2017-08-08 22:54:52
tags:

	- Linux命令

---

tcpdump是一个抓包工具。抓包的时候，最好把网卡设置为混杂模式，这就需要root权限。

# 1. 先抓一个包再说

```
teddy@teddy-ubuntu:~$ sudo tcpdump -i eth0 -nn -X 'port 22' -c 1  
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
22:58:40.174708 IP 192.168.190.128.22 > 192.168.190.1.9506: Flags [P.], seq 1388673925:1388674041, ack 3183231343, win 255, length 116
        0x0000:  4510 009c 1114 4000 4006 2b65 c0a8 be80  E.....@.@.+e....
        0x0010:  c0a8 be01 0016 2522 52c5 7b85 bdbc 416f  ......%"R.{...Ao
        0x0020:  5018 00ff 3484 0000 4f36 4a7e 21f1 5111  P...4...O6J~!.Q.
        0x0030:  acf0 5082 bfb9 8afb 8690 3cd6 02a5 d196  ..P.......<.....
        0x0040:  a240 e976 921b 2e56 bb91 b36b 104b 0d4b  .@.v...V...k.K.K
        0x0050:  4423 4393 f27d a46c 6a20 0a89 f558 1aeb  D#C..}.lj....X..
        0x0060:  52ab cbca cf63 01af 1dda 0639 3210 0fce  R....c.....92...
        0x0070:  116e dbe0 2ca9 edbb 7594 d241 a949 b6be  .n..,...u..A.I..
        0x0080:  af2a ecd7 42b2 586b e7d5 049f a2d7 28d7  .*..B.Xk......(.
        0x0090:  ae0a eead 82d3 b7d2 76c6 de0f            ........v...
1 packet captured
54 packets received by filter
47 packets dropped by kernel
```

我抓的是ssh的端口22的数据包。因为我现在用ssh连接着的，一定是有数据的。

选项说明：

i：指定接口。

nn：表示不要把22号显示为ssh这样的名字，保持数字原样，方便我们分析。

X：原样显示包的内容。

c：抓几个包。我们现在是抓一个。

一条更加基础的命令是：`tcpdump -i eth0 -c 1`。这就是随便抓一个包就行。

# 2. 基本选项

除了上面的4个，还有-e和-l这2个。

-e：显示以太网地址。

-l：把输出设置为行缓存，不要用默认的全缓冲。

# 3. 进阶选项

-t：不要打印时间戳。

-v：输出更加详细。

-F：把上面的port 22这种写到文件里（如果有很多端口，就很有用）。-F filter.txt这样用。

# 4. 包的保存和查看

-w：保存为文件。

-r：读取内容。

示例：

```
teddy@teddy-ubuntu:~$ sudo tcpdump -i eth0 -c 1 -w mypacket
tcpdump: listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
1 packet captured
7 packets received by filter
0 packets dropped by kernel
teddy@teddy-ubuntu:~$ ls mypacket -lh
-rw-r--r-- 1 root root 226  8月  8 23:09 mypacket
teddy@teddy-ubuntu:~$ sudo tcpdump -r mypacket 
reading from file mypacket, link-type EN10MB (Ethernet)
23:09:46.727838 IP 192.168.190.128.ssh > 192.168.190.1.9506: Flags [P.], seq 1388683949:1388684081, ack 3183235139, win 255, length 132
teddy@teddy-ubuntu:~$ 
```

# 5. 包的过滤



