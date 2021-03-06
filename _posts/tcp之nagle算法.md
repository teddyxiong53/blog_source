---
title: tcp之nagle算法
date: 2017-11-02 20:57:19
tags:
	- tcp

---



Nagle算法是John Nagle发明的。

# 发明的背景

1984年，福特航空公司为了减少自己的专用的TCP/IP网络的拥塞情况，发明了这种方法。

为了解决的问题，就是小包问题。如果一个应用里，它一次只产生一个字节的数据，这一个字节被封包之后，有效数据率就很低。这样就会导致网络上都是这种小包。键盘输入1个字节，产生的网络包是41个字节。Nagle算法，就是会积累一些数据量，到了一定程度了再一起往外发。这个算法得到了广泛应用，而且现在是默认打开的。

我们可以通过设置TCP_NODELAY来关闭。



# Nagle算法的规则

1、如果包长度达到MSS，就允许发送。

2、如果包里有FIN，就允许发送。

3、如果设置了TCP_NODELAY，允许发送。

4、未设置TCP_CORK（cork是塞子的意思）选项时，如果所有发出去的小数据包都被确认，允许发送。

5、上述条件都不满足，但是发生了超时（一般是200ms），则立即发送。



对应到C代码里，就是一个判断条件。

```
#define tcp_do_output_nagle(tpcb) ((((tpcb)->unacked == NULL) || \
                            ((tpcb)->flags & (TF_NODELAY | TF_INFR)) || \
                            (((tpcb)->unsent != NULL) && (((tpcb)->unsent->next != NULL) || \
                              ((tpcb)->unsent->len >= (tpcb)->mss))) || \
                            ((tcp_sndbuf(tpcb) == 0) || (tcp_sndqueuelen(tpcb) >= TCP_SND_QUEUELEN)) \
                            ) ? 1 : 0)
```

