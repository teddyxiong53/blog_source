---
title: Lex和Yacc分析
date: 2023-02-07 19:49:17
tags:
	- 编译器

---



Lex和Yacc是进行词法分析和语法分析的工具。

是Unix下的工具。

Linux下面的是GNU实现的版本，Flex和Bison。

对于这一类程序，我们统一成为Lex和Yacc。



Lex和yacc可以为你做什么？

可以帮助你解析复杂的语言。

当你需要读取一个配置文件时，或者你需要编写一个你自己的编译器的时候。



Lex会生成一个叫做词法分析器的程序。

这个程序是一个函数，它有一个字符流的参数。

函数的处理就是去分析这个字符流。

一个非常简单的例子如下：

```
%{
#include <stdio.h>
%}
%%
stop printf("Stop command received\n");
start printf("Start command received\n");
%%
```



# 参考资料

1、Lex与YACC详解

https://zhuanlan.zhihu.com/p/143867739

