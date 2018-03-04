---
title: 树莓派之bcm2835之mailbox
date: 2018-03-04 16:47:36
tags:
	- 树莓派

---



看树莓派的uboot，看到mailbox这个东西，不太明白是干啥用的。

网上找到这篇文章，学习总结一下。

http://magicsmoke.co.za/?p=284



树莓派的soc，其实主要是gpu，cpu反而是个打杂的。

mailbox是gpu和cpu之间的通信机制。

这个在2835的手册里，是没有什么介绍的。

mailbox就是一系列的寄存器。这组寄存器可以被GPU和CPU访问。

我们往内存里放一个消息，然后把消息的地址通过mailbox告诉GPU。（我们是在CPU上编程）。

寄存器是这些：

```
base
poll
sender
status
Configuration
write
```

发送的处理过程是这样的：

```
while 1
	read status
	if not busy
		break
要放入邮箱的地址，需要左移4位，这样我们的地址空间只有28位了。
低4位，放mailbox的channel
把组装的地址写入到write寄存器。
```

接收的处理过程是：

```
while 1
	read status
	if not busy
		break
读取base寄存器。
```



mailbox的channel有10个。

```
1、power管理。
2、fb。
3、virtual uart
4、VCHIQ
5、led
6、button
7、触摸屏。
8、na
9、mailbox属性接口，arm to gpu。
10、mailbox属性接口，gpu to arm。
```

虽然chn1被标记为fb的通道，但是我们可以用chn8来做。



