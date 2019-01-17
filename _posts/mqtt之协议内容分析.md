---
title: mqtt之协议内容分析
date: 2017-10-09 20:33:56
tags:
	- mqtt
typora-root-url: ..\
---



一个mqtt包的内容，3个部分：固定头部+可变头部+载荷。

![mqtt协议报文内容](/images/mqtt协议报文内容.png)

固定头部2个字节。

可变头部，就举一个例子看。

byte1: 0x00

byte2：0x06 和byte1一起表示可变头部的长度。

byte3：'M'

byte4：'Q'

byte5：'I'

byte6：'s'

byte7：'d'

byte8：'p'

byte9:0x3。表示版本号。

byte10:0xXX。这个各个bit表示不同的标志。例如username、password有没有。

byte11：keep alive时间高字节。

byte12：keep alive时间低字节。



# 1. 固定头部

2个字节。

## 第一个字节

###bit7到bit4：表示消息类型，总共16种。

0：保留

1：CONNECT消息。

2：CONNACK消息。

3：publish消息。

4：puback消息。

5：pubrec消息。receive。

6：pubrel消息，rel代表release。

7：pubcomp消息。complete。

8：subscribe消息。

9：suback。

10：unsubscribe。

11：unsuback。

12：pingreq。ping request。

13：pingresp。

14：disconnect。

15：保留。

### bit3：dup标志。重复标志位。



### bit2和bit1：Qos标志。

00：最多一次。记忆为>

01：最少一次。记忆为<

10：刚好一次。记忆为=

11：保留。

###bit0：保持标志。retain。

## 第二个字节

第二个字节表示剩余长度Remaining Length。

这个字节的bit7有特殊含义，剩下的才用来表示长度值。

bit7位1，表示后续还有字节存在。（不参与计算，只是标记）。

mqtt协议最多允许用4个字节来表示剩余长度。那么最大长度是：

0xFF，0xFF， 0xFF，0x7F。注意最后的一个是0x7F。表示后面没有字节用来表示长度值了。

这个数字的值大概是256M。





# 具体消息分析

消息内容，按字节排布：

```
0x10 表示connect消息 

```

