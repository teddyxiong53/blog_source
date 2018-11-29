---
title: micropython之nlr
date: 2018-11-29 15:57:28
tags:
	- micropython

---



我发现如果不把rtos的task切换时的栈的切换情况这个点弄清楚，很多地方都会碰到理解问题。

现在的nlr也是一个类似的东西。现在我决定把这个知识点搞懂。

这个跟setjmp和longjmp也是关联的。

没有用setjmp。

是直接保存寄存器的。

```
#elif defined(__thumb2__) || defined(__thumb__) || defined(__arm__)
    #define MICROPY_NLR_THUMB (1)
    #define MICROPY_NLR_NUM_REGS (10)
```

```
    #if MICROPY_NLR_SETJMP//这个没有定义。
    jmp_buf jmpbuf;
    #else
    void *regs[MICROPY_NLR_NUM_REGS];
    #endif
```



头文件的注释写着：

```
// non-local return
// exception handling, basically a stack of setjmp/longjmp buffers
```



nlr_push的实现。

```
unsigned int nlr_push(nlr_buf_t *nlr) {
    (void)nlr;//这个变量没有用
    __asm volatile ("jmp    nlr_push_tail       \n" )
}
```

