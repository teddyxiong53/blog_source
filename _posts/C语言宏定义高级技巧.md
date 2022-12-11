---
title: C语言宏定义高级技巧
date: 2022-12-10 12:40:19
tags:
	- C语言

---

--

现在看很多比较复杂的代码，宏技巧都用得比较多。

所以有必要系统研究一下。

# 怎么调试复杂宏定义

使用-g3的编译选项，这个是比-g更多调试信息的。

-g3 -gdwarf-2

可以用gdb进行展开。

```
macro expand MACRO3(a)
```



参考资料

1、

https://blog.csdn.net/dearwind153/article/details/47360763

# 编译时把宏的情况打印出来

用这个技巧来打印宏定义：

```
#define    PRINT_MACRO_HELPER(x)  #x
#define    PRINT_MACRO(x)         #x"="PRINT_MACRO_HELPER(x)

#pragma message(PRINT_MACRO(YOUR_MACRO))
```

如果YOUR_MACRO是没有定义的，则打印是：

```
note: #pragma message: YOUR_MACRO=YOUR_MACRO
```

否则打印：

```
note: #pragma message: YOUR_MACRO=xxx
```



https://www.cnblogs.com/suiyek/p/14164160.html

