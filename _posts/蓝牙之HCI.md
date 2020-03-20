---
title: 蓝牙之HCI
date: 2018-12-11 20:45:11
tags:
	- 蓝牙

---



蓝牙比较头疼的一点就是，上来就是一堆的缩写，把人都整懵了。

一个个缩写来啃。

还是按照协议栈从底层到上层的顺序来。



HCI是蓝牙协议栈最底层的一个协议。

根据蓝牙4.0的规范里写的，HCI的传输层主要有四种：

1、usb。优点是通用，缺点是复杂。

2、uart。跟RS232的串口类似。但是避开了232的缺点，速度可以达到跟usb接近的水平。更加简单。

3、三线串口。

4、sd接口。



命令是从协议栈到底层。

事件是底层到协议栈。

数据是双向的。



# HCI的命令

命令可以分为这些类：

1、link control。

2、link policy。

3、HCI control 和baseband 命令。

4、信息参数指令。

5、状态指令参数。

6、测试指令。

7、ble控制器命令。



# 帧结构

## 异步数据包ACL



## 同步数据包SCO



##命令包

发送的是cmd。

收到的是event。

cmd的结构是：

```
前面2个字节的opcode。
然后2个字节的长度。
后面就是内容。
```

event的结构：

```
前面1个字节的event code。
然后1个字节的长度。
后面是内容。
```



hci cmd的payload长度是32字节，或者64字节。

hci event的header的长度是2字节。event payload长度是255字节。

hci acl的payload长度是1695字节。

hci 的in buffer长度，就用1695这个。因为这个是可能的最长的包。

hci 的out buffer也是。





# 参考资料

1、HCI层数据包格式

https://blog.csdn.net/u010657219/article/details/42191039