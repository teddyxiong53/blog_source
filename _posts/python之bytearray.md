---
title: python之bytearray
date: 2020-10-30 17:50:30
tags:
	- python
---

1

python3引入了两种新的数据类型：bytes和bytearray。

bytes：表示在内存里连续不可变的字节序列。

bytearray：表示字节数组，可变。



字符串跟bytes关系：

字符串编码后，得到bytes。

bytes解码后，可以打印出来。

```
a = '啊'.encode(encoding='gbk')
b = a.decode(encoding='gbk')
print(a)
print(b)
print(type(a))
print(type(b))
```

输出：

```
b'\xb0\xa1'
啊
<class 'bytes'>
<class 'str'>
```



# bytes基本用法

## 定义一个bytes对象

```
b1 = bytes() # 
# 等价于
b2 = b''
```

可以带一个整数参数。

```
b1 = bytes(3)
```

得到长度为3的的bytes。里面填满了0

可以带一个可迭代的int组合。

```
b1 = bytes([61,62])
print(b1)
b2 = bytes((61,62))
print(b2) #都是得到=>这个
```

可以传递字符串和编码。

```
bytes(string, encoding)
等价于
string.encode()
```

## 操作方法

跟str很多类似，只是输入和输出是bytes类型。

# bytearray

构造方法跟bytes的类似。

操作也类似。



参考资料

1、python——bytes、bytearray

https://www.cnblogs.com/zyybky/p/12559706.html