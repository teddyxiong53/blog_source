---
title: Python之with
date: 2018-02-27 11:11:55
tags:
	- Python

---



with是从Python2.5开始引入的一种与异常处理相关的概念。

# 什么时候用with

1、在对资源进行访问的场景。with机制会把你进行资源的清理操作。



讨论with之前，先要看几个概念。

1、上下文管理器。Context Manager。

2、上下文管理协议。包括`__enter__()`和`__exit__()`这2个函数。

3、运行时上下文。runtime context。



基本语法：

```
with context_expression [as target]:
	with-body
```

当然我们也可以用try finally的方式来进行操作。代码是等价的。

```
f = open('test.txt')
try:
	for line in f:
		print line
		#...
finally:
	f.close()
```

等价于

```
with open('test.txt') as f:
	for line in f:
		print line
		#...
```

