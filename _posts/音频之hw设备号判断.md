---
title: 音频之hw设备号判断
date: 2018-10-25 10:42:08
tags:
	- 音频

---



hw:x,y

x代表声卡，y代表device。

```
// 设备名称，这里采用默认，还可以选取"hw:0,0","plughw:0,0"等 
const char *device = "default";
```



# 参考资料

1、What is 0 and 0 in hw:0,0 mean? and how can I get those value?

https://askubuntu.com/questions/606770/what-is-0-and-0-in-hw0-0-mean-and-how-can-i-get-those-value

2、5.ALSA录放音

https://www.jianshu.com/p/8d2cc3733782

3、Configuring Sound on Linux/HW Address

https://en.wikibooks.org/wiki/Configuring_Sound_on_Linux/HW_Address

4、Difference between “hwplug” and “hw”

https://raspberrypi.stackexchange.com/questions/69058/difference-between-hwplug-and-hw



