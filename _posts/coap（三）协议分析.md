---
title: coap（三）协议分析
date: 2018-02-10 16:47:37
tags:
	- coap

---



coap协议是6lowpan协议栈里的应用层协议。

默认的端口号是5683 。



# 6LoWPAN

6lowpan是基于ipv6的低速、无线、个域网标准。



背景

将ip协议引入到无线通信网络一直被认为是不可能的。到目前为止，无线网只能采用专用协议。因为ip协议对带宽和内存的占用比较高。

6lowpan就是为了改变这种情况而出现的。

6lowpan具有低功耗的特点，aes-128又保证了它的安全性。

现在contiki、tinyos。都分别实现了完整的6lowpan协议栈。并且得到了广泛的应用。



# 消息分类

只有4种消息。

con、non、ack、rst。

con是comfirmable，可确认是消息，ack是用来响应con的。



# 返回消息码

跟http的200那一套基本对应。



开源实现有libcoap.a。还有很多的其他实现。因为这个协议不复杂。所以实现有很多。







