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



在内存里读写数据。但是接口上接近读写文件的操作方式。

还是有点类似unix的一切皆文件的思路。

统一接口的用法。

而StringIO和BytesIO的区别。

就跟str跟bytes的区别类似。

StringIO，就是编码后的。

BytesIO的，就是二进制层面的。



简单用法。

```
from io import StringIO, BytesIO
f = StringIO()
f.write('hello')
f.write(' ')
f.write('world')
print(f.getvalue()) # yong f.read为什么不行？
```



参考资料

1、python 的StringIO

<https://blog.csdn.net/lucyxu107/article/details/82728266>

2、Python中StringIO和BytesIO

https://www.cnblogs.com/yqpy/p/8556090.html