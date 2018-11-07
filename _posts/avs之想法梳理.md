---
title: avs之想法梳理
date: 2018-11-06 15:50:27
tags:
	- avs

---



归根结底，就是json生成和json解析。这个是主要工作。

只是cpp里，把这个操作搞得很复杂。



SpeakerManager。

就是调节音量的。



DirectiveRouter

这个相当于总开关，从这里分发消息到各个真正的处理者。



看看蓝牙的处理。

```
auto avrcpTarget = m_activeDevice->getAVRCPTarget();
```

```
BlueZBluetoothDevice
```

蓝牙是靠dbus来进行通信控制的。

DBusProxy