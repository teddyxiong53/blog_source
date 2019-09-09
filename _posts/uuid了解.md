---
title: uuid了解
date: 2019-09-06 14:55:48
tags:
	- uuid

---

1

uuid是128bit的全局唯一标识符。一般用32字节的字符串表示。

它可以保证时间和空间的唯一性。

包括这些方法：

```
1、mac地址。
2、时间戳。
3、命名空间。
4、随机数。
5、伪随机数。
```

```
uuid1：基于时间戳。
uuid2：基于分布式技术环境。python里没有实现这个。
uuid3：基于名字的md5散列。
uuid4：基于随机数。
	存在概率性重复，最好不用。
uuid5：基于sha1散列。
```

如果有唯一性要求，最好使用uuid3和uuid5 。



参考资料

1、Python使用UUID库生成唯一ID

https://www.cnblogs.com/dkblog/archive/2011/10/10/2205200.html

