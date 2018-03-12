---
title: lwip（四）架构分析
date: 2018-03-12 11:02:16
tags:
	- lwip
typora-root-url: ..\
---



lwip的调用层次图。

![lwip架构](/images/lwip架构.png)



#通信机制

采用的是主线程加消息的设计方式。这个跟Android上的ui线程是一样的。

其他线程不能执行操作，而是要发消息给主线程来操作。

整个机制不复杂。

其他线程跟主线程的通信是用mbox来做的。



#消息设计

```
enum tcpip_msg_type {
  TCPIP_MSG_API,
  TCPIP_MSG_API_CALL,
  TCPIP_MSG_INPKT,
```

主要就是API和INPKT这2个。CALL这个很少用。

INPKT只在收包的时候用。其余的都是API消息。

然后设计的tcpip_msg结构体。就是tcpip_msg_type。然后加上各种类型的struct得到的 一个union。



# 结构体设计

![lwip结构体设计](/images/lwip结构体设计.png)



所谓bind过程，就是把ip地址和端口跟tcp的pcb结构体里的成员进行赋值。

而这个pcb对应netconn，也就是对应lwip_socket，也就是对应sockfd了。

再看listen。



accept。

```
里面其实就是在等一个acceptmbox。邮箱的内容就是一个netconn指针。
那么这个指针的内容谁来分配的呢？
有accept的前提，是有tcp连接进来，那就是有tcp包进来嘛。
所以是tcp_input，然后一路调用到对应的回调accept_function
	netconn_alloc
	sys_mbox_trypost(&conn->acceptmbox,
```



recv

```
recv
	lwip_recv
		lwip_recvfrom
			netconn_recv_tcp_pbuf
				netconn_recv_data
					发消息，do_recv。
```



















现在看看tcp协议的内容。

思路的话，我觉得以tcp的状态机为核心，根据状态变迁的过程来看。

首先是LISTEN状态。

好像这样看不下去。还是从代码的入口来看。

主要c文件是3个：tcp.c、tcp_in.c、tcp_out.c。

# tcp.c

1、tcp_init。空的。

2、tcp_tmr。

```
1、250ms调用一次。
2、
	tcp_fasttmr
		处理tcp_active_pcbs的。
	tcp_slowtmr
		除了处理tcp_active_pcbs。
		还处理tcp_tw_pcbs。
```



