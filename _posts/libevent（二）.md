---
title: libevent（二）
date: 2018-03-11 09:48:48
tags:
	- 网络

---



现在开始分析代码。

先把目录结构理一遍。下面把无关的文件都已经删掉了。

```
pi@raspberrypi:~/tmp/xx/libevent-2.1.8-stable$ tree
.
├── aclocal.m4
├── arc4random.c：一个产生随机数的算法。比random好，是真正的伪随机。
├── autogen.sh：
├── buffer.c：evbuffer_xxx函数的实现。
├── bufferevent_async.c
├── bufferevent.c
├── bufferevent_filter.c
├── bufferevent-internal.h
├── bufferevent_openssl.c
├── bufferevent_pair.c
├── bufferevent_ratelim.c
├── bufferevent_sock.c
├── buffer_iocp.c
├── compat
│   └── sys
│       └── queue.h
├── defer-internal.h
├── devpoll.c
├── epoll.c
├── epoll_sub.c
├── epolltable-internal.h
├── evbuffer-internal.h
├── evconfig-private.h
├── evconfig-private.h.in
├── evdns.c
├── event.c：核心文件。=====================
├── event-internal.h
├── event_iocp.c
├── event_rpcgen.py
├── event_tagging.c
├── evmap.c
├── evmap-internal.h
├── evport.c
├── evrpc.c
├── evrpc-internal.h
├── evsignal-internal.h
├── evthread.c
├── evthread-internal.h
├── evthread_pthread.c
├── evthread_win32.c
├── evutil.c
├── evutil_rand.c
├── evutil_time.c
├── ht-internal.h
├── http.c
├── http-internal.h
├── include
│   ├── evdns.h
│   ├── event2
│   │   ├── buffer_compat.h
│   │   ├── bufferevent_compat.h
│   │   ├── bufferevent.h
│   │   ├── bufferevent_ssl.h
│   │   ├── bufferevent_struct.h
│   │   ├── buffer.h
│   │   ├── dns_compat.h
│   │   ├── dns.h
│   │   ├── dns_struct.h
│   │   ├── event_compat.h
│   │   ├── event.h
│   │   ├── event_struct.h
│   │   ├── http_compat.h
│   │   ├── http.h
│   │   ├── http_struct.h
│   │   ├── keyvalq_struct.h
│   │   ├── listener.h
│   │   ├── rpc_compat.h
│   │   ├── rpc.h
│   │   ├── rpc_struct.h
│   │   ├── tag_compat.h
│   │   ├── tag.h
│   │   ├── thread.h
│   │   ├── util.h
│   │   └── visibility.h
│   ├── event.h
│   ├── evhttp.h
│   ├── evrpc.h
│   ├── evutil.h
│   └── include.am
├── install-sh
├── iocp-internal.h
├── ipv6-internal.h
├── kqueue.c
├── kqueue-internal.h
├── listener.c
├── log.c
├── log-internal.h
├── minheap-internal.h
├── mm-internal.h
├── openssl-compat.h
├── poll.c
├── ratelim-internal.h
├── sample
├── select.c
├── signal.c
├── strlcpy.c
├── strlcpy-internal.h
├── test
├── test-driver
├── time-internal.h
├── util-internal.h
├── whatsnew-2.0.txt
├── whatsnew-2.1.txt
├── WIN32-Code
│   ├── nmake
│   │   ├── evconfig-private.h
│   │   └── event2
│   │       └── event-config.h
│   └── tree.h
└── win32select.c
```



#例子代码深入

还是从libevent（一）那篇文章里的第一个例子开始看。

1、event_init。

```
参数：
	无。
返回值：
	struct event_base *
	用来判断分配是否成功。可以不管。
处理：
	1、内部新建了一个event_base，给到了内部的全局变量current_base。这个全局变量在起作用。
	2、event_base是Reactor模式里的Reactor。
	3、初始化了分配的结构体的一些成员，重点是选择poll、select这些机制。
```

2、event_set。

```
参数：
	1、struct event *event。要注册的事件，例如accept_event。
	2、fd。socket对应的fd。
	3、short event。EV_READ、EV_WRITE这些在event.h里定义的宏。
	4、void (*callback)(int fd, short event, void *arg) 一个回调函数。
	5、void *arg。可选的参数。
返回值：
	无。
```

3、event_add。

```
参数：
	1、struct event *event。要注册的事件，例如accept_event。
	2、struct timeval *tv。超时时间。可以给NULL。
返回：
	错误码。
```

4、event_dispatch。

```
参数：
	无。
返回值：
	int。
处理：
	event_dispatch
		event_loop
			event_base_loop		
```

接下来看回调函数里的实现。

```
void accept_callback(int fd, short ev, void *arg)
	1、accept。
	2、bufferevent_new，把read/write/error的处理函数注册进去。
	3、bufferevent_enable READ
```

```
void buf_read_callback(struct bufferevent *incoming, void *arg)
	1、evbuffer_readline(incoming->input);
	2、 struct evbuffer *evreturn = evbuffer_new;
	3、evbuffer_add_printf
	4、bufferevent_write_buffer。
	5、evbuffer_free。
```

# 看http的sample



