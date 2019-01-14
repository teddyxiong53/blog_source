---
title: shadowsocks之lightsocks分析
date: 2019-01-14 10:53:59
tags:
	- shadowsocks
	- 异步
---



lightsocks是用asyncio实现的简化版本的shadowsocks。

不是很实用，但是适合用来学习。

里面用了asyncio。也可以作为学习asyncio的材料。



加密

就是简单的把0到255 的，都加1处理。

0变成1，

1变成2，

255变成0

