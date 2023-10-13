---
title: ama协议分析
date: 2019-03-27 10:46:32
tags:
	- ama

---



这个不是按章节分析的。是根据我碰到的疑问点来分析。

# override assistant具体内涵

意思是让Alexa覆盖手机的默认语音助手。

当前是给0的，给1试一下看看。

```
stDeviceConfig->needs_assistant_override = 0;
```



## update and switch transport

这个是什么意思？

是手机这边要求切换蓝牙传输方式，例如ble切到spp。



## state

这部分内容不少。

get、set、sync。

sync如何工作呢？

应该是板端状态变化时，主动上报给手机端。

都是bool的或者枚举值。

