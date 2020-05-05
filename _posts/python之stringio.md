---
title: python之stringio
date: 2020-05-05 17:06:51
tags:
	- python
---



StringIO，就类似C++里的stringstream。

就是用类似操作一个文件的方式，来操作一个字符串。

```
from io import StringIO
f = StringIO("hello\nworld\n")
while True:
	line = f.readline()
	line = line.strip()
	if line == '':
		break
		
```

BytesIO就是一个跟StringIO类似的东西，只是它里面是二进制的数据。

StringIO和BytesIO是在内存中操作str和bytes的方法，使得和读写文件具有一致的接口。

参考资料

1、python 的StringIO

<https://blog.csdn.net/lucyxu107/article/details/82728266>