---
title: Linux内核之用函数指针打印函数名
date: 2018-03-18 19:45:10
tags:
	- Linux

---



Linux内核里有一堆的函数是通过指针调用的，我想知道这些函数的调用顺序。

所以希望在调用的地方直接把函数的名字打印出来，这样就比较直观。

我直接用

```
printk("%s", ptr);
```

的方式，是乱码。

```
printk("%pF", ptr);
```

全是指针值。

先放着。在Stack Overflow上提了个问题。

https://stackoverflow.com/questions/49347664/how-to-print-function-name-with-function-pointer-in-linux-kernel#

有人解答了。