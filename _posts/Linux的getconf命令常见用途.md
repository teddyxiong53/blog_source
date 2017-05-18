---
title: Linux的getconf命令常见用途
date: 2017-05-18 19:29:04
tags:

	- Linux

	- getconf

---

## 1. 查询页大小

```
getconf PAGESIZE
```

## 2. 查询long的字节数

这个可以用来判断机器是64位还是32位的。

```
getconf LONG_BIT
```

