---
title: cpp之nullptr
date: 2018-05-09 19:25:51
tags:
	- cpp

---



nullptr是c++11引入的新的关键字。

为什么要引入nullptr这个关键字呢？

我们先看看之前是怎么用的。

之前c++跟c一样，都用NULL表示空指针。

定义上这样：

```
/* Define NULL pointer value */
#ifndef NULL
    #ifdef __cplusplus
        #define NULL    0 //cpp里明确定义为整数0 。
    #else  /* __cplusplus */
        #define NULL    ((void *)0)
    #endif  /* __cplusplus */
#endif  /* NULL */
```

c++之所以把NULL定义为整数0 。是为了重载机制。





# 参考资料

1、C++ 11 nullptr关键字

https://www.cnblogs.com/DswCnblog/p/5629073.html