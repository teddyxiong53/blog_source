---
title: 音频之audio patch是什么
date: 2021-12-20 15:02:11
tags:
	- 音频

---

--

amlogic的halaudio里用了audio patch的概念。

这个具体指什么？

是来自于Android音频的概念。

Android在5.0系统中引入了AudioPatch概念，用于表示音频中端到端的连接关系。

从目前看到的代码推测，

这个概念主要用于连接source与sink。

这里的source，既可以是实实在在的音频输入设备，如MIC，也可以是底层中混音后的音频流；

这里的sink则表示输出设备，如扬声器、耳机等。



引入这个概念以后，对音频来讲，显然抽象程度更高，更容易理解宏观上的概念，

如插拔耳机时，只要更换连接就可以，但更不易理解实现的细节，如音频数据在插拔耳机时如何运送到新设备上。

另外，虽然存在Java层的AudioPatch.java文件，但是并没有作为SDK开放给开发者使用，估计还是因为这个概念相对来说还是太底层。

参考资料

1、Android 5.0中AudioPatch概念简单探索

https://blog.csdn.net/heyjackdu/article/details/43957467

