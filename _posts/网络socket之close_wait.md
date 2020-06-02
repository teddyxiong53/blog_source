---
title: 网络socket之close_wait
date: 2020-06-02 14:53:08
tags:
	- 网络

---

1

close wait这个是对方断开后，本地连接进入到这个状态。

也就是说，收到对方的FIN之后，本机进入到close wait状态。

如果你发现本机有连接处于close wait状态。

说明你自己的程序，也就是被动关闭的一方，没有及时发出FIN。



坏消息是 CLOSE_WAIT 没有类似的设置，如果不重启进程，那么 CLOSE_WAIT 状态很可能会永远持续下去；

好消息是**如果 socket 开启了 keepalive 机制，那么可以通过相应的设置来清理无效连接**，不过 keepalive 是治标不治本的方法，还是应该找到问题的症结才对。



1.代码需要判断socket，一旦read返回0，断开连接，read返回负，检查一下errno，如果不是AGAIN，也断开连接。(注:在UNP 7.5节的图7.6中，**可以看到使用select能够检测出对方发送了FIN**，再根据这条规则就可以处理CLOSE_WAIT的连接)
2.给每一个socket设置一个时间戳last_update，每接收或者是发送成功数据，就用当前时间更新这个时间戳。定期检查所有的时间戳，如果时间戳与当前时间差值超过一定的阈值，就关闭这个socket。
3.使用一个Heart-Beat线程，定期向socket发送指定格式的心跳数据包，如果接收到对方的RST报文，说明对方已经关闭了socket，那么我们也关闭这个socket。
4.设置SO_KEEPALIVE选项，并修改内核参数





我用mqtt来做测试。

把mqtt服务器关闭。则本机的read函数，返回值是0，错误码是EAGAIN。

这个时候，我主动关闭socket。再去重新连接就好了。



参考资料

1、浅谈CLOSE_WAIT

https://www.cnblogs.com/wanghui0412/p/10868636.html

2、

https://blog.csdn.net/libaineu2004/article/details/78886182