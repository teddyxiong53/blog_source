---
title: libev之竞品ev项目分析
date: 2022-12-12 16:04:19
tags:
	- 网络

---

--

在搜索精简的mqtt broker的实现方案时，找到sol的作者的这个项目。

https://github.com/codepr/ev

这个项目的目标是以一个头文件的方式实现eventloop的功能。

先把提交历史记录看一下。

第一个的头文件860行代码。但是epoll、poll、select、kqueue都实现了。kqueue主要是为了支持apple。

然后添加了echo和pingpong这2个基础的例子。

然后添加了tcp server的接口。

还增加了signal的支持。

看作者有点意思，每次代码行数增加了，就改readme里的说明。

后面增加的udp支持。

增加了ssl支持，基于openssl。

后面单独把ev_tcp.h的内容从ev.h里拆分出来。

要编译ssl支持：

```
`-DHAVE_OPENSSL=1` to enable it.
```

开始没有加这个机制，导致只能在一个C文件里用。这样才算正常。

```
#define EV_SOURCE // add before ev.h
#include "../ev.h"
```

增加unix socket的支持。

ev.h和ev_tcp.h的关系

```
- `ev.h` a generic eventloop for I/O bound concurrency on a single-thread:
    - Based on the best multiplexing IO implementation available on the host,
      supporting epoll/poll/select on linux and kqueue on BSD
    - All IO operations are done in a non-blocking way
    - Support for time based repeated tasks
- `ev_tcp.h` exposes a set of APIs to simply create an event-driven TCP server
  using `ev.h` as the main engine:
    - TCP/UNIX socket connections
    - Basic TLS support through OpenSSL
    - Callback oriented design
```

把所有的提交日志都看完了。

项目写得比较完善了。

可以自己尝试使用。

既然这个项目可以，我觉得作者的代码质量可信赖。

那么mqtt broker就选用他的sol吧。

