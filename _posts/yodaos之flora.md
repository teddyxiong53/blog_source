---
title: yodaos之flora
date: 2022-10-17 11:35:33
tags:
	- yodaos

---

--

```
├── examples
│   ├── all-demos.cc
│   ├── all-demos.h
│   └── main.cc
├── include
│   ├── flora-agent.h
│   ├── flora-cli.h
│   └── flora-svc.h
├── src
│   ├── adap.h
│   ├── cli.cc
│   ├── cli.h
│   ├── conn.h
│   ├── defs.h
│   ├── disp.cc
│   ├── disp.h
│   ├── flora-agent.cc
│   ├── poll.cc
│   ├── ser-helper.cc
│   ├── ser-helper.h
│   ├── sock-adap.cc
│   ├── sock-adap.h
│   ├── sock-conn.cc
│   ├── sock-conn.h
│   ├── sock-poll.cc
│   └── sock-poll.h
```

include目录是对外的接口。

主要关注flora-svc.h、flora-agent.h这2个头文件。

一个是服务端，一个是客户端。

flora-svc.h

```
Dispatcher
	static方法：new_instance。参数是msg buf size。
	2个方法：run和close。
	
Poll
	static方法：new_instance。参数是uri字符串。
	2个方法：start和stop。
	
```

对应的c接口是：

```
flora_dispatcher_new
flora_dispatcher_run
flora_dispatcher_close
```



参考资料

1、

