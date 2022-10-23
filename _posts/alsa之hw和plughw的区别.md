---
title: alsa之hw和plughw的区别
date: 2022-04-22 16:29:11
tags:
	- alsa

---

--

hw：直接使用硬件。

plughw：会自己根据需要自行使用rate等插件。

而且plughw不会增加latency。不同于dmix。

看/usr/share/alsa/alsa.conf里的hint内容：

```
plughw的是这样：
Hardware device with all software conversions

hw的是这样：
Direct hardware device without any conversions
```



# 参考资料

1、

https://raspberrypi.stackexchange.com/questions/69058/difference-between-hwplug-and-hw

2、

https://stackoverflow.com/questions/49970117/low-latency-and-plughw-vs-hw-devices