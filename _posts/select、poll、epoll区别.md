---
title: select、poll、epoll区别
date: 2017-05-14 17:37:21
tags:

	- select

---

select、poll、epoll都是IO多路复用的机制。它们从本质上来说，都是同步IO，因为在监听到可以读写后，就需要自己来进行读写操作，读写过程是阻塞的。



select的缺点：

1、每次调用select，都需要把fd集合从用户态拷贝到内核态，这个开销在fd很多的时候会比较大。

2、同时每次调用select的时候，都需要再内核遍历所有传递进来的fd，fd很多时，开销也很大。

3、select支持的文件描述符太小了，只有1024个。

poll和select差不多，只是描述fd集合的方式不一样，select是用fd_set，而poll是用pollfd。

poll就没有了链接数量的限制了。但是内核态和用户态之间的复制还是存在的。

epoll则是对select和poll的改进。没有了上面的缺点。





select，相对于把一张bit表跟一个fd绑定起来。就看bit表里哪个bit置位了没有。









