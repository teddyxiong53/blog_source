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



参考资料

1、

