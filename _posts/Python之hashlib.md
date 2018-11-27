---
title: Python之hashlib
date: 2018-11-27 21:11:16
tags:
	- Python

---



hashlib提供了常用的哈希算法。

```
>>> dir(hashlib)
['__all__', '__builtins__', '__doc__', '__file__', '__get_builtin_constructor', '__name__', '__package__', '_hashlib', 'algorithms', 'algorithms_available', 'algorithms_guaranteed', 'md5', 'new', 'pbkdf2_hmac', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']
```



先看看sha1函数。

SHA1是Secure Hash Algorithm。安全哈希算法。

```
import hashlib

sha1 = hashlib.sha1()
sha1.update("aaaaaaaaaaaaa")
sha1.update("bbbbbbbbbbbb")
print sha1.hexdigest()
```

```
teddy@teddy-ubuntu:~/work/test/python$ python test.py 
7de8c5dc905f4c306acd16c17f656c82210c5b3b
```

看看md5的。

```
import hashlib

md5 = hashlib.md5()
md5.update("aaaaaaaaaaaaa")
md5.update("bbbbbbbbbbbb")
print md5.hexdigest()
```

```
teddy@teddy-ubuntu:~/work/test/python$ python test.py 
89a306a28f6b2595f9493a07ae843582
```

md5的结果是32位的16进制数。

sha1的是40位的16进制数。



# 参考资料

1、python hashlib sha1和MD5哈希算法

https://blog.csdn.net/sinat_21302587/article/details/72639841

