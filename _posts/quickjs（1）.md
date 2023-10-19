---
title: quickjs（1）
date: 2023-10-16 13:32:11
tags:
	- quickjs
---

--

# 代码分析

以qjs.c为切入口，结合quickjs-libc.c和examples/point.c来分析。

## 风格分析

数据结构，都是JS为前缀的大驼峰，没有下划线。例如：JSRuntime。

对外接口，都是JS_为前缀的大驼峰，就是`JS_`这里一个下划线。例如：`JS_NewRuntime`

结构体成员，都是小写加下划线的模式。

内部工具函数，都是小写加下划线的。

扩展的C模块的函数，都是js开头的小写下划线风格。这样就容易跟quickjs的核心接口区分开来。

同一个函数的不同版本，在后面加数字后缀，2/3等等这样，来区分不同的版本，做到版本向前兼容。



我觉得这些命名风格都挺好的，值得我去学习。

个人项目可以使用这种命名风格。

## 关于RT后缀

RT是runtime是意思。

很多接口的默认版本是针对context的，但是也有针对runtime的版本。所以在后面加上rt以示区别。

例如：

```
void JS_FreeAtom(JSContext *ctx, JSAtom v);
void JS_FreeAtomRT(JSRuntime *rt, JSAtom v);
```



## 常用顶层对外接口

### 创建阶段常用的接口

| 函数                   | 说明                                                         |
| ---------------------- | ------------------------------------------------------------ |
| JS_NewRuntime          | 新建一个Runtime，这个是需要最先被调用的。                    |
| JS_NewRuntime2         | 被JS_NewRuntime调用，也可以被用户调用，2个参数，定制malloc相关函数和传递一个void *的用户自定义指针进去。 |
| JS_SetMemoryLimit      | 设置Runtime的内存有多大。                                    |
| JS_SetMaxStackSize     | 设置Runtime的stack大小。                                     |
| JS_NewContext          | 新建一个Context。在Raw Context的基础上，增加了Date、String等內建对象的创建。 |
| JS_NewContextRaw       | 新建一个最基础的Context。                                    |
| JS_SetRuntimeOpaque    | 这个跟JS_NewRuntime2传递进去那个void*是一个东西。在quickjs-libc.c里，是传递了一个JSThreadState结构体指针进去了。 |
| JS_SetModuleLoaderFunc | 设置模块加载的2个函数。                                      |

### 运行阶段常用的接口

| 函数           | 说明                                      |
| -------------- | ----------------------------------------- |
| JS_Eval        | 这个是主要接口，就是把文件内容执行。      |
| JS_IsException | 这个用来判断JS_Eval运行的结果是不是异常。 |
| JS_FreeValue   | 释放JS_Eval运行的返回值                   |

### 调试相关接口

| 函数                  | 说明               |
| --------------------- | ------------------ |
| JS_ComputeMemoryUsage | 计算内存使用。     |
| JS_DumpMemoryUsage    | 打印内存占用情况。 |

销毁相关接口

| 函数           | 说明               |
| -------------- | ------------------ |
| JS_FreeContext | 计算内存使用。     |
| JS_FreeRuntime | 打印内存占用情况。 |

### Exception和Error相关

| 函数                     | 说明 |
| ------------------------ | ---- |
| JS_Throw                 |      |
| JS_GetException          |      |
| JS_IsError               |      |
| JS_ResetUncatchableError |      |
| JS_NewError              |      |
| JS_ThrowSyntaxError      |      |
| JS_ThrowTypeError        |      |
| JS_ThrowReferenceError   |      |
| JS_ThrowRangeError       |      |
| JS_ThrowInternalError    |      |
| JS_ThrowOutOfMemory      |      |

### job相关

| 函数                 | 说明 |
| -------------------- | ---- |
| JS_EnqueueJob        |      |
| JS_IsJobPending      |      |
| JS_ExecutePendingJob |      |

## 新建模块相关接口

这个就以examples/point.c的为例查看。

| 函数                       | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| js_init_module             | 这个是模块的入口函数。就用这个名字就好了。                   |
| JS_NewCModule              | 新建一个C模块。把js_point_init传递进去。这里的module_name是so文件的文件名，没有什么大的关系。 |
| JS_NewClassID              | 新建一个class对应的ID，是一个整数。                          |
| JS_NewClass                |                                                              |
| JS_NewObject               |                                                              |
| JS_SetPropertyFunctionList |                                                              |
| JS_NewCFunction2           |                                                              |
| JS_SetConstructor          |                                                              |
| JS_SetClassProto           |                                                              |
| JS_SetModuleExport         | 这里export的名字，才是对外的名字。                           |
| JS_AddModuleExportList     | Add和Set的关系：在js_init_module_std里Add，在js_std_init里Set。 |
| JS_AddModuleExport         |                                                              |

## 重要结构体



## 重要枚举和宏

### JSValue相关的

| 枚举/宏         | 说明                                      |
| --------------- | ----------------------------------------- |
| JS_TAG_XX       | 看起来是数据类型。用来标记JSValue的类型。 |
| JS_VALUE_XX     | 获取JSValue的值。JS_VALUE_GET_INT         |
| JS_MKVAL        |                                           |
| JS_VALUE_IS_NAN |                                           |
| JS_NULL         | JS_NULL    JS_MKVAL(JS_TAG_NULL, 0)       |

### PROP相关

### JS_Eval相关FLAG

```
#define JS_EVAL_TYPE_GLOBAL   (0 << 0) /* global code (default) */
#define JS_EVAL_TYPE_MODULE   (1 << 0) /* module code */
#define JS_EVAL_TYPE_DIRECT   (2 << 0) /* direct call (internal use) */
#define JS_EVAL_TYPE_INDIRECT (3 << 0) /* indirect call (internal use) */
#define JS_EVAL_TYPE_MASK     (3 << 0)
```

### 一些DEF枚举

| 枚举/宏              | 说明 |
| -------------------- | ---- |
| JS_CFUNC_DEF         |      |
| JS_CFUNC_MAGIC_DEF   |      |
| JS_CFUNC_SPECIAL_DEF |      |
| JS_ITERATOR_NEXT_DEF |      |
| JS_CGETSET_DEF       |      |
| JS_CGETSET_MAGIC_DEF |      |
| JS_PROP_STRING_DEF   |      |
| JS_PROP_INT64_DEF    |      |
| JS_OBJECT_DEF        |      |
| JS_ALIAS_DEF         |      |
| JS_ALIAS_BASE_DEF    |      |

## quickjs-libc.c的mainloop实现原理

是基于select实现的。为了各个平台都可以通用。

以setTimeout的流程为例进行分析。

js_std_loop，这个是一个死循环。

`js_os_setTimeout`

```
创建了一个Object后，
挂到了这个链表上
list_add_tail(&th->link, &ts->os_timers);
```

js_os_poll被js_std_loop调用。

这个函数是调用select的函数。

通过JS_Call来调用回调函数。

## cutils.c分析



# 使用qjs的项目



https://github.com/didi/Hummer

https://github.com/MarilynDafa/ijjs

ij在logo设计上看起来向一个U。所以这里表示的是micro的函数。这个名字可以理解为microjs。

https://github.com/zhuzilin/es