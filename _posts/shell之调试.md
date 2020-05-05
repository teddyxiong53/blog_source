---
title: shell之调试
date: 2018-01-19 17:57:35
tags:
	- shell

---



有时候看到一些复杂的脚本，难以看懂，还是希望可以通过调试的方式来阅读。

#bashdb

有个工具叫bashdb。可以用来调试bash脚本。使用方法类似gdb。

# -x选项

1、bash -x test.sh

2、在脚本前面加上#!/bin/sh -x

3、用set -x来启用，用set +x来禁用。



参考资料

1、如何在 Linux 或者 UNIX 下调试 Bash Shell 脚本

<https://linux.cn/article-9302-1.html>