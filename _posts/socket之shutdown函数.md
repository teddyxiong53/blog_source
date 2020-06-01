---
title: socket之shutdown函数
date: 2020-05-31 11:17:20
tags:
	- socket

---

1

close一个socket，是完全关闭了socket。

有时候存在只需要关闭socket的一个方向的，例如只关闭读或者只关闭写。

这个时候，就需要使用shutdown函数。

```
原型：
	int shutdown(int sock, int howto);
参数2：
	howto，有3个取值。SHUT_RD/SHUT_WR/SHUT_RDWR
```

close是关闭socket。执行后，socket对应的内存结构从内存里完全清除掉了。

而shutdown是关闭连接，socket在内存里继续存在。

默认情况下，close调用时，系统马上向对方发出FIN包，不管socket的缓冲区里是否还有数据没有发送。

而shutdown则会等output buffer里的发出去之后，再发送FIN包。

所以shutdown要更加安全一些。



参考资料

1、socket--shutdown()函数

https://blog.csdn.net/cs1462155255/article/details/77991006