---
title: directfb之C语言面向对象分析
date: 2021-07-20 14:59:33
tags:
	- gui

---

--

以wm.c和default.c为一个分析例子。

wm是窗口管理，default是一个实现。另外还有unique和sawman这2种实现。

相当于父类和子类的关系。

带2个void *指针，一个指向对外的数据，一个指向对内的数据。

```
static void
InitIDirectFB_Async( void *ctx,
                     void *ctx2 )
{
     DFBResult       ret;
     IDirectFB      *thiz = ctx;
     IDirectFB_data *data = ctx2;
```



# C和C++混合

ICore_Real 这种XX_Real的类。

这样来继承：

```
class ICore_Real : public ICore
class ICore : public Interface

class Interface {
protected:
     CoreDFB *core;

     Interface( CoreDFB *core )
          :
          core( core )
     {
     }
};
```

ICore 的函数有：

```
Initialize
Register
CreateSurface
CreatePalette
CreateState
CreateImageProvider
AllowSurface
GetSurface
```



CoreDFB_Initialize 只被dfb_core_arena_initialize调用。

dfb_core_arena_initialize只被dfb_core_create调用。

IDirectFB_Construct 





# 参考资料

1、DirectFB学习之面向对象设计

https://blog.csdn.net/jxgz_leo/article/details/69700237