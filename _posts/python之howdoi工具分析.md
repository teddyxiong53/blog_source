---
title: python之howdoi工具分析
date: 2023-01-16 21:12:31
tags:
	- Python

---

howdoi是一个python小的小工具。

先看一个简单用法：

```
$ howdoi write a simple Makefile
WARNING:root:no boto3 module found
HEADERS = program.h headers.h

default: program

program.o: program.c $(HEADERS)
    gcc -c program.c -o program.o

program: program.o
    gcc program.o -o program

clean:
    -rm -f program.o
    -rm -f program
```

可以看到是用比较自然的交互方式来获取一些信息。

本质上是从网上搜索信息并整理呈现。

还是有一定的价值的。

很多的搜索结果不如人意。

但是这个工具本身还是可以研究一下的。

代码不多，本质上就一个python文件。



参考资料

1、

https://zhuanlan.zhihu.com/p/419410973