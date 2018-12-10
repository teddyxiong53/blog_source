---
title: freertos之命名规则
date: 2018-12-10 22:14:53
tags:
	- freertos

---



freertos的命名，初看之下，真的让人头疼。我现在要用esp32玩一点东西，所以需要把freertos的基本了解一下。

我看的是esp32 sdk里的，版本是8.2.0 。

变量命名规则：

```
u32的变量，前面都加上ul
u16的变量，前面都加上us
u8的变量，前面都加上uc
没有在stdint.h里定义的变量类型，在定义对应的变量的时候，都要加上x前缀。无符号的，加上ux前缀。
size_t定义的，前面也加上ux。
枚举类型，前面加上e。
指针类型，前面再加上p。例如u16的指针，前面就是pus。
```

函数

```
static的函数，前面都加上prv，表示private。
根据返回值类型，函数名加上对应的前缀，没有返回值，前面加上v。
把文件名也加入到函数名里。
```

宏定义

```
把文件名作为宏定义的前缀。
文件名小写。
configUSER_PREEMPTION
```

看起来还是感觉特别反人类。



# 参考资料

1、FreeRTOS学习记录1-熟悉FreeRTOS的命名规则

https://blog.csdn.net/liukais/article/details/78958850

