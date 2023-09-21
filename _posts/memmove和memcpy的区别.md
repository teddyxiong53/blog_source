---
title: memmove和memcpy的区别
date: 2023-09-13 11:43:11
tags:
	- C语言
---

--

`memmove` 和 `memcpy` 都是C语言中用于内存复制的函数，它们的主要区别在于如何处理内存重叠。

1. **memcpy**（Memory Copy）：

    - `memcpy`函数用于从一个内存区域复制数据到另一个内存区域，通常用于非重叠内存的复制。
    - `memcpy`不会检查源内存区域和目标内存区域是否重叠，它只会简单地按字节复制数据。
    - 如果源内存区域与目标内存区域重叠，`memcpy`的行为是未定义的，可能会导致意外的结果。

    示例：
    ```c
    #include <string.h>

    char source[] = "Hello, World!";
    char destination[20];
    memcpy(destination, source, strlen(source) + 1);
    ```

2. **memmove**（Memory Move）：

    - `memmove`函数也用于从一个内存区域复制数据到另一个内存区域，但它能够处理源内存区域和目标内存区域重叠的情况。
    - `memmove`会进行额外的检查以确保复制操作不会损坏数据。
    - 当源内存区域和目标内存区域重叠时，`memmove`会以一种安全的方式进行复制，避免数据的损坏。

    示例：
    ```c
    #include <string.h>

    char text[] = "Hello, World!";
    memmove(text + 7, text, strlen(text) + 1);
    ```

总结：如果你知道内存区域不会重叠，可以使用`memcpy`，因为它可能比`memmove`更快。但是，如果你不确定内存区域是否重叠，或者确实知道它们重叠，请使用`memmove`以确保安全性。在大多数情况下，建议使用`memmove`，因为它可以处理所有情况，并且不会导致未定义行为。