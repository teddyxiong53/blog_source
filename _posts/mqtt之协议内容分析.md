---
title: mqtt之协议内容分析
date: 2017-10-09 20:33:56
tags:
	- mqtt

---



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

00：最多一次。

01：最少一次。

10：刚好一次。

11：保留。

###bit0：保持标志。retain。

## 第二个字节

第二个字节表示剩余长度Remaining Length。

这个字节的bit7有特殊含义，剩下的才用来表示长度值。

bit7位1，表示后续还有字节存在。

mqtt协议最多允许用4个字节来表示剩余长度。那么最大长度是：

0xFF，0xFF， 0xFF，0x7F。注意最后的一个是0x7F。表示后面没有字节用来表示长度值了。

这个数字的值大概是256M。





