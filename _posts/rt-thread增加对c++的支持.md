---
title: rt-thread增加对c++的支持
date: 2023-02-06 19:10:17
tags:
	- c++

---

看看rt-thread是如何增加对c++的支持的。



rtos增加对c++的支持，需要重载new和delete运算符。

例如在freertos里这样实现：

```
void * operator new( size_t size )
{
    return pvPortMalloc( size );
}

void * operator new[]( size_t size )
{
    return pvPortMalloc(size);
}

void operator delete( void * ptr )
{
    vPortFree ( ptr );
}

void operator delete[]( void * ptr )
{
    vPortFree ( ptr );
}
```



这个是c++实现的freertos

https://github.com/richard-damon/FreeRTOScpp

这个是对应的文档

https://codedocs.xyz/richard-damon/FreeRTOScpp/



rt-thread对c++的支持在这里

components\cplusplus

```

```

在嵌入式里，对c++有这些约束：

1、不用使用exception。

2、不要使用RTTI。就是运行时类型推断。

3、不建议使用模板，因为会导致代码膨胀。

4、static的class变量不建议使用。因为调用他们的构造函数的时机和位置不能精确控制，这对于多线程编程是个噩梦。

5、多继承不建议使用。

需要在连接脚本里加上调用构造函数的section。

```
    // in your .text section
    PROVIDE(__ctors_start__ = .);
    /* old GCC version uses .ctors */
    KEEP(*(SORT(.ctors.*)))
    KEEP(*(.ctors))
    /* new GCC version uses .init_array */
    KEEP (*(SORT(.init_array.*)))
    KEEP (*(.init_array))
    PROVIDE(__ctors_end__ = .);
```

还有需要加上析构函数的section。

cplusplus_system_init 这个函数里，依次遍历所有的构造函数并调用。

```
    typedef void(*pfunc)();
    extern pfunc __ctors_start__[];
    extern pfunc __ctors_end__[];
    pfunc *p;

    for (p = __ctors_start__; p < __ctors_end__; p++)
        (*p)();
```



# 参考资料

1、

https://www.freertos.org/FreeRTOS_Support_Forum_Archive/February_2017/freertos_FreeRTOSs_compatibility_with_C_2aa2a047j.html

