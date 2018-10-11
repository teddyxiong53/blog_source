---
title: avs（3）
date: 2018-10-10 11:17:51
tags:
	- 智能音箱

---



# CertifiedSender

会把消息持久化，然后一直发送直到成功。

存储消息依赖的是MessageStorageInterface。

也是存到数据库里。

主要是这2个类用到。

AlertsCapabilityAgent

SettingsUpdatedEventSender



#播放控制

PlaybackRouterInterface

PlaybackRouter

播放暂停，都是发消息给云端的。

onContextAvailable里，取放入到队列里的按键事件。

在ContextManager::updateStatesLoop里调用。

contextManager被这些模块用到了。

1、PostConnectSynchronizer



# 分析跟avs服务端建立连接的过程

就在SampleApplication的最后。

```
    // Connect once configuration is all set.
    std::string endpoint;
    sampleAppConfig.getString(ENDPOINT_KEY, &endpoint);

    client->connect(m_capabilitiesDelegate, endpoint);

    // Send default settings set by the user to AVS.
    client->sendDefaultSettings();
```



HTTP2Transport::networkLoop



# CapabilitiesDelegate

CapabilitiesDelegate

这个主要的接口就是注册能力。





```
sqlite> select * from settings;
locale|en-US
```

```
sqlite> select * from messages
   ...> ;
1|{"event":{"header":{"namespace":"Settings","name":"SettingsUpdated","messageId":"ec23757f-aa80-4a73-9ac4-412c70785923"},"payload":{"settings":[{"key":"locale","value":"en-US"}]}}}
sqlite> 
```



AudioPlayer

这个的作用是什么？

