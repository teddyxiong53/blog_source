---
title: gcc之malloc调试
date: 2022-07-29 14:23:07
tags:
	- gcc

---

--

我现在是有个问题，在malloc要么是出现段错误，要么是失败。

其实内存是有非常多的。

为什么会出现这种问题，怎么进行调试？

对malloc和free进行wrap操作就可以了。

我另外有篇文章说了这个问题了。



```
#include <stdlib.h>
#include <stdio.h>

void* __real_malloc(size_t size); // 只声明不定义
 
void* __wrap_malloc(size_t size) 
{
    printf("__wrap_malloc called\n");
 
    return __real_malloc(size); //调用真正的malloc
}

int main(int argc, char const *argv[])
{
    extern void func1();
    func1();
    char *p1 = malloc(10);
    printf("p1:%p\n", p1);
    free(p1);
    return 0;
}
```

这个只对main这个有用。

对于func1里的函数没有用。即使重新编译func1的so文件。

其实可以的，只需要在编译func1的命令里，也加上`-Wl,--wrap,malloc`。



参考资料

1、

https://www.cnblogs.com/arnoldlu/p/10827884.html

2、

https://www.cnblogs.com/arnoldlu/p/9649229.html#valgrind

3、

https://blog.csdn.net/q2519008/article/details/88661486