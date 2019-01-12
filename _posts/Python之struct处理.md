---
title: Python之struct处理
date: 2018-07-05 22:28:09
tags:
	- Python

---



主要2个方法：struct.pack和struct.unpack。

原型是：

```
struct.pack(fmt, v1, v2, ...)
```

```
struct.unpack(fmt, string)
```

fmt是关键。

```
#coding: utf-8
import struct
#  本地字节序
buffer = struct.pack('ihb', 1,2,3)
print(buffer)
print( struct.unpack('ihb', buffer))

print("--------------")
# 网络字节序
data = [1,2,3]
buffer = struct.pack('!ihb', *data)
print(buffer)

```

i：int

h：short。

b： char。

!：网络字节序。

q：long long

Q：unsigned long long

```
>：大端
<：小端。
```



# 参考资料

1、Python中struct.pack()和struct.unpack()用法详细说明

http://www.php.cn/python-tutorials-356984.html