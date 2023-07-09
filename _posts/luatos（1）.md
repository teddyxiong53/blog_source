---
title: luatos（1）
date: 2023-07-09 17:30:51
tags:
	- lua

---

--

luatos是基于lua的单片机开发框架。

使用了xmake做编译系统。

所以对我比较有研究价值。

# 入口代码流程研究

入口文件是：

bsp\linux\src\main.c

分配了1M的内存：

```
#define LUAT_HEAP_SIZE (1024*1024)
uint8_t luavm_heap[LUAT_HEAP_SIZE] = {0};
```

```
bpool(luavm_heap, LUAT_HEAP_SIZE);
```

