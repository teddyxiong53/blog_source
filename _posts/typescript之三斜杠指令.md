---
title: typescript之三斜杠指令
date: 2018-12-30 09:35:25
tags:
	- typescript

---





什么是三斜杠指令？

```
/// <reference path="..." />
```

构成：

1、3个斜杠开头。

2、后面是一个xml标签。

实质还是一个单行注释，但是编译器会处理这个，而不是直接过滤掉。



注意：

1、只能放在文件的最前面。

2、如果出现在语句之后，只会被当成普通注释。



最常见的就是reference这条指令。

它的作用是声明文件之间的依赖。告诉编译器在编译过程中要引入的文件。



其他指令

```
/// <reference no-default-lib="true" />
这句的含义是把一个文件标记为默认库。
告诉编译器在编译过程不用包含这默认哭。
```



参考资料

1、

https://m.runoob.com/manual/gitbook/TypeScript/_book/doc/handbook/Triple-Slash%20Directives.html

