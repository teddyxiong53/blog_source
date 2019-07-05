---
title: Linux之coredump文件远超文件系统容量
date: 2019-07-01 16:19:37
tags:
	- Linux
---



我的板子的ram和flash都是128M。我设置core文件限制为unlimited。

让core文件生成在/tmp路径下。

生成的core文件有600M。居然可以放下。

有点难以理解。

我觉得可能是这个core的大小跟普通文件的大小不能一样理解。

先不管，至少我可以放心调试了。不用担心core文件放不下的问题。





