---
title: avs之异步机制分析
date: 2018-11-27 14:05:24
tags:
	- avs

---



avs里到处都是网络收发处理，都进行了异步处理。

主要还是依靠Executor来做的。



