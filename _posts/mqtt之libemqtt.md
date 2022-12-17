---
title: mqtt之libemqtt
date: 2018-07-30 09:28:29
tags:
	- 物联网

---

--

总的来说，这个库实用价值不高。



libemqtt是一个简单小巧的库。只有一个头文件和一个C文件。

默认提供了一个sub和一个pub的例子。



emqtt怎么知道连上来的client是同一个呢？

连接的时候，需要设置一个clientid，这个id可以不设置，如果不设置，在emqtt服务端会自动产生一个唯一的id，如果你要用到session，必须有一个唯一个id，你可以用imei。如果你一定要收到离线消息的话，就必须使用确定的id了。



自己写一遍。

先简单实现pub功能。系统里安装了mosquitto。

启动mosquitto。

```
sudo mosquitto -v
```

启动mosquitto订阅。

```
mosquitto -t "hello"
```

执行./client/pub。发现失败了。

```
1547703060: New connection from 127.0.0.1 on port 1883.
1547703060: Invalid protocol "" in CONNECT from 127.0.0.1.
1547703060: Socket error on client <unknown>, disconnecting.
```

是我写得有问题，用原始的libemqtt的pub是可以的。

是我的connect函数里写得有问题。

https://github.com/teddyxiong53/c_code/tree/master/mymqtt

另外，libemqtt的select用得不太对。我改了。

现在pub一个消息可以正常了。

pub的写完了。正常。

现在开始写sub的。



#参考资料

