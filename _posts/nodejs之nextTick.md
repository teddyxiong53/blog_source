---
title: nodejs之nextTick
date: 2022-08-21 08:22:08
tags:
	- nodejs

---

--

API要么100%同步要么100%异步时很重要的

API要么100%同步要么100%异步是很重要的，可以通过`process.nextTick()`去使得一个API完全异步化达到这种保证。

1、

https://segmentfault.com/a/1190000022317412