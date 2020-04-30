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



参考资料

1、

