---
title: python之EAFP和LBYL
date: 2019-10-10 17:27:48
tags:
	- python

---

1

EAFP和LBYL是两种编码风格的描述。

EAFP：Easy to Ask for Forgiveness than Permission。请求原谅比请求允许容易。

```
try:
	x = my_dict["key"]
except KeyError:
	# handle
```



LBYL：Look Before You Leap。跳之前先看一下。

```
if "key" in my_dict:
	x = my_dict["key"]
else:
	# handle 
```

python鼓励使用try的方式，也就是EAFP的方式。因为这种方式效率更高，而且可读性也好。



参考资料

1、LBYL与EAFP漫谈

http://ju.outofmemory.cn/entry/367391