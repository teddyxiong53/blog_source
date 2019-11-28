---
title: muduo之example分析
date: 2019-11-28 14:52:51
tags:
	- cpp
---

1

# asio chat

开一个shell窗口

```
./asio_chat_server 2020
```

另外开2个shell查看：

```
./asio_chat_client 127.0.0.1 2020
```

这2个client就可以聊天了。

client代码分析：

```
ChatClient
	包含了一个TcpClient成员变量。

main函数：
	1、使用了EventLoopThread。因为主线程需要用来接收命令行上的输入。
	
```



# asio chat loadtest

先启动server

```
./asio_chat_server 2020
```

执行loadtest

```
./asio_chat_loadtest 127.0.0.1 2020 100
```

这样是相当于100个client连上来。

我试了10000个，是报了这个错误了：

```
FATAL Too many open files (errno=24)
```



# asio timer

5个定时器的例子。都很简单。



# asynclogging_test

这个是测试日志的性能。



# balancer

这个代理的例子。

不看先。

# blockingqueue_bench



# exception_test

这个值得看看。

# fastcgi_test



# fileutil_test

# gzipfile_test

muduo还自己实现了gzip的算法。

# hub/pub/sub

可以参考mqtt的broker、pub、sub。

需要3个窗口。

```
./hub 2020
```

启动sub：

```
./sub 127.0.0.1 2020 topic hello
```

启动pub：

```
./pub 127.0.0.1 2020 topic hello
```



参考资料

1、

