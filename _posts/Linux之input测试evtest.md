---
title: Linux之input测试evtest
date: 2021-07-15 14:31:33
tags:
	- gui

---

--

evtest是测试input设备的简单工具。

使用也很简单：

```
evtest /dev/input/event1
```

这样进行按键等操作，就会看到按键值的打印情况。

代码就一个c文件。evtest.c

就是一个很简单的select和read操作。

丢事件的可能性很低。



参考资料

1、

