---
title: gcc之__wrap
date: 2020-06-27 15:06:51
tags:
	- gcc

---

1

看XR872的代码，看到了一个__wrap_main函数，但是没有找到调用的地方。

就搜索了一个`__warp_main`函数，才发现这个是gcc的一个`__wrap`特性。

在使用gcc编译器的时候，如果不想使用标准库函数。

例如，出于调试目的，想要统计malloc和free的字节数。

那么 就是需要改变标准的malloc和free的行为。怎样做才是最简单的呢？

有两种方法：

1、指定链接路径。自己实现一个malloc。然后先链接自己的库路径。这个不是太好。

2、使用gcc的--wrap=symbol选项。来指定函数。

例如替换malloc和free额。

```
-Wl,--wrap,malloc,--wrap,free 
```

然后我们只是像要在malloc前面加一个统计，最后还是要调用一下标准的malloc。

C代码里要这样写：

```
#include <stdio.h>
#include <stdlib.h>
void* __real_malloc(size_t size); // 只声明不定义__real_malloc
void __real_free(void *p);

void* __wrap_malloc(size_t size) // 定义__wrap_malloc
{
    printf("__wrap_malloc called, size:%zd\n", size); // log输出
    return __real_malloc(size); // 通过__real_malloc调用真正的malloc
}
void *__wrap_free(void *p)
{
    printf("__wrap_free called, ptr:0x%p\n", p);
}

int main(int argc, char const *argv[])
{
    char *p = malloc(100);
    free(p);
    return 0;
}
```







参考资料

1、GCC中通过--wrap选项使用包装函数

https://blog.csdn.net/fengbingchun/article/details/82947673

2、【Linux】使用__wrap_malloc查看内存使用

https://blog.csdn.net/iEearth/article/details/49737577