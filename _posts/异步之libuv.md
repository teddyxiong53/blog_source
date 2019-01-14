---
title: 异步之libuv
date: 2019-01-14 09:48:59
tags:
	- 异步
---



libuv是一个高性能的、事件驱动的io库。

提供了跨平台的api。

libuv是封装了iocp和libev。

nodejs的底层就用了libuv。

libuv的核心工作就是提供一个eventloop。



系统编程里最经常处理的是输入和输出，而不是数据处理（这个一般是应用编程的工作）。

现在的os都提供了事件通知机制。

```
#include <stdio.h>
#include <uv.h>
#include <stdlib.h>

int main(int argc, char const *argv[])
{
    uv_loop_t *loop = malloc(sizeof(uv_loop_t));
    uv_loop_init(loop);
    uv_run(loop, UV_RUN_DEFAULT);
    uv_loop_close(loop);
    free(loop);
    return 0;
}
```



参考资料

1、Basics of libuv

http://luohaha.github.io/Chinese-uvbook/source/basics_of_libuv.html