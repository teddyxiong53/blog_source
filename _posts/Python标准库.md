---
title: Python标准库
date: 2022-10-29 20:44:33
tags:
	- python

---

--

把python的常见api梳理一遍，便于记忆。

以3.11.0的为学习对象。

https://docs.python.org/zh-cn/3/library/functions.html

```
内置函数
	既然内置了，那么必然是高频使用的方法。
	a：6个。abs、aiter、all、any、anext、ascii。
		all和any的判断。
		aiter和anext是async的。
		abs和ascii是基础函数。
	b：5个。
		bin：返回二进制字符串。
		bool：返回布尔值。
		breakpoint：断点，不用。
		bytearray：是一个class。
		bytes。
		主要是二进制和bool相关的。
	c：5个。
		c的主要语义包括：调用、字符、类、编译，复数。
		5个函数，就分属于上面5个语义。
		callable
		chr
		classmethod
		compile
		complex
	d：4个。
		d的主要语义是：删除、字典、目录、除。
		4个函数分属于这4个语义。
		delattr
		dict
		dir
		divmod
	e：3个。e的语义有：枚举，计算、执行。
		enumerate
		eval
		exec
	f：4个。f的语义有：过滤、浮点、格式化、冻结。
		filter
		float
		format
		frozenset
	g：
		2个。g的语义有get、全局。
		getattr
		gloabals
	h：4个。h的语义有has、哈希、帮助、hex
		hasattr
		hash
		help
		hex
	i：6个。i的语义有：id、输入、int、is、iter
		id
		input
		int
		isinstance
		issubclass
		iter
	j：没有。
	l：3个。l的语义有：长度、list、locals
		len
		list
		locals
	m：4个。m的语义有：map、max、memory、min
		max/min
		map
		memoryview
	n：1个。就是next。
	o：4个。o的语义有：对象、八进制、打开、ord
		object
		oct
		open
		ord：把字符转成int。
	p：3个。p的语义有pow、打印、属性。
		pow
		print
		property
	q：没有。
	r：4个。r的语义有：范围、repr、反转、取整。
		range
		repr
		reversed
		round
	s：8个。这个是最多的。s的语义有：set、slice、static、sort、字符串、sum、super
		set
		setattr
		sorted
		staticmethod
		str
		sum
		super
	t：2个。语义是tuple和type。
	u：没有。
	v：1个。vars。返回属性。
	w：没有。
	x：没有。
	z：1个。zip。
	
	其中表示数据类型的：从简单到复杂依次是：
		数字类型：int、float、complex
		迭代类型：list、tuple、range
		文本序列：str
		二进制序列类型：bytes、bytearray
		集合类型：set、frozenset。
		映射类型：dict。
	总共70个。
	
```

```
内置常量
	False
	True
	None
	NotImplemented
	Ellipsis
	__debug__
	一共6个。常用是前面3个。
	
由site添加的常量。在repl中比较有用。脚本里不要用。
    quit()
    exit()
    copyright
    credits
    license
```

```
内置异常
	不一一看了。
	
```

```
文本处理
	string
	re
	这2个算是最常用的。掌握这2个就好了。
```

```
二进制垂柳
	struct
	掌握这一个就好了。
```

```
数据类型
	datetime
	collections
	collections.abc
	array
	weakref
	enum
```

```
函数式编程模块
	itertools
	functools
	
```

```
文件和目录访问
	os.path
	fileinput
	tempfile
	glob
	shutil
```

```
数据持久化
	pickle：对象序列化。
	sqlite3
	
```

```
文件格式
	csv
	
```

```
通用os服务
	os
	io
	time
	argparse
	logging
	getpass
	platform
	errno
	ctypes
```

```
并发执行
	threading
	multiprocessing
	subprocess
	queue
	
```

```
网络和进程通信
	asyncio
	socket
	ssl
	mmap
	signal
```

```
互联网数据处理
	json
	base64
```

```
html处理
	html
	html.parser
	html.entities
	
```

```
互联网协议处理
	urllib
	http
	http.server
	http.client
	uuid
	
```

```
多媒体
	wav
```

```
开发工具
	typing：类型注解支持
	unittest
```

```
unix特有服务
	posix
	pwd
	grp
	tty
	fcntl
```

