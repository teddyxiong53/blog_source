---
title: snapcast代码分析
date: 2020-04-30 16:24:08
tags:
	- 音频

---

1

stream的继承关系

```
PcmStream
	ProcessStream
		AirplayStream
			这个是对接AirPlay的。
		LibrespotStream
			这个是对接spotify的。
```



```
BaseMessage
WireChunk
PcmChunk
```



server端相关的类

```
ControlServer
	继承了ControlMessageReceiver，这个是一个接口。
		这个类又使用了ControlSession这个类。
		
StreamServer
	这个是最外层的
	实现了3个接口。public MessageReceiver, ControlMessageReceiver, PcmListener
	在main函数里：
	std::unique_ptr<StreamServer> streamServer(new StreamServer(io_context, settings));
    streamServer->start();
```



# snapclient

这个都是使用boost.asio的同步接口来做的。

snapserver则是使用的异步接口。

snapclient的整体逻辑还是很简单清晰的，采取同步方式，就更方便分析。

主要的cpp文件也就5个。

```
snapclient.cpp
	入口。main函数。
controller.cpp
	主要类。
client_connection.cpp
	处理连接相关。
stream.cpp
	处理媒体数据块。
time_provider.cpp
	统计时间差。
```

我想办法改造成用muduo来实现。

所以需要把通信细节理清楚。



参考资料

1、

