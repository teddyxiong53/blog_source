---
title: awtk之脚本引擎fscript分析
date: 2023-04-26 11:11:11
tags:
	- awtk
---



入口是在awtk\src\tkc\fscript.c。

--

核心是在代码awtk\src\tkc\fscript.c。

示例文件在这里：

tests\fscripts

入口是tests\fscript_run.cpp

得到二进制runFScript这个文件。来解析执行脚本文件。



```
fscript_t
```



参考资料

1、官网文档

https://awtk.zlg.cn/api/awtk/fscript_t.html