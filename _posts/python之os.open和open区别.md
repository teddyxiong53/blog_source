---
title: python之os.open和open区别
date: 2019-01-10 13:34:51
tags:
	- Python
---



其实有3个：

1、open。返回文件对象。这个对象有read、write方法。用起来也方便。

2、os.open。返回fd。相当于C语言的open系统调用。这种方式打开后，用os.read和os.write进行操作。

3、io.open。返回stream。相当于C语言里的fopen。



open的一些问题

```
在python2里，
open('1.txt', 'r+') #这样才能可以同时进行读写。rw是不行的。
```



参考资料

1、Python上的io.open()和os.open()有什么区别？

https://codeday.me/bug/20171121/98951.html