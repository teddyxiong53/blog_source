---
title: mqtt之paho.mqtt代码分析
date: 2017-10-17 23:21:42
tags:
	- mqtt
	- iot

---



从代码里的宏看，这套代码兼容了windows、osx、Linux。我们重点关注Linux版本的代码。

从sample目录下的paho_cs_pub.c代码作为分析入口。

