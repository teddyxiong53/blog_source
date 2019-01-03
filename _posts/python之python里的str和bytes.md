---
title: python之python里的str和bytes
date: 2019-01-03 10:25:59
tags:
	- python

---



python3最重要的特性，可以说是对文本和二进制数据做了更为清晰的区分。

文本总是Unicode的，用str类型表示。

二进制数据，则用bytes类型表示。

python3不会隐式混用str和bytes。

str通过encode得到bytes。bytes通过decode得到str。

```
>>> "abc".encode("utf-8")
b'abc'
>>> "你好".encode("utf-8")
b'\xe4\xbd\xa0\xe5\xa5\xbd'
```

在python2里：

```\
bytes == str 是True
```

在python3里是False。

