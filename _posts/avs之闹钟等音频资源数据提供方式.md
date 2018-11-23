---
title: avs之闹钟等音频资源数据提供方式
date: 2018-11-22 16:47:19
tags:
	- avs
---



感觉c++把不少的问题复杂话了。闹钟音频资源，放在C语言了，就是一个数组就好了。简单易懂，但是在avs系统里，我觉得需要花力气来梳理一下才能懂。

最底层的数据，同样是另一个数组。

```
med_system_alerts_melodic_01__TTH__mp3
```

借助这个函数，把buffer内容转成一个istream指针。

```
std::unique_ptr<std::istream> streamFromData(const unsigned char* data, size_t length);
```

```
    AudioFactory
    	AlertsAudioFactory
    		alarmDefault函数，返回istream
```

