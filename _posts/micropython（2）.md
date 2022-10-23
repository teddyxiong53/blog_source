---
title: micropython（2）
date: 2018-11-28 09:14:28
tags:
	- micropython

---



现在开始看代码细节。

从builtin的东西开始看。

```
typedef mp_obj_t (*mp_fun_0_t)(void);
typedef mp_obj_t (*mp_fun_1_t)(mp_obj_t);
typedef mp_obj_t (*mp_fun_2_t)(mp_obj_t, mp_obj_t);
typedef mp_obj_t (*mp_fun_3_t)(mp_obj_t, mp_obj_t, mp_obj_t);
typedef mp_obj_t (*mp_fun_var_t)(size_t n, const mp_obj_t *);
```



objtype.c是一切的基础。



分析一下mp_obj_type_t结构体。

注释写得已经很详细了。

```
1、mp_obj_type_t base。一个type也是一个对象，所以需要用这个开头，指向的是mp_type_type。
2、qstr name。qstr实际是一个数字。size_t类型。表示这种类型的名字。
3、mp_print_fun_t print。对应__repr__和__print__函数。
4、mp_make_new_fun_t make_new。对应__new__和__init__函数。
5、mp_call_fun_t call。对应__call__函数。
6、mp_unary_op_fun_t unary_op。一元操作符。
7、mp_binary_op_fuc_t binary_op。二元操作符。
8、mp_attr_fun_t attr。对属性进行load、save等操作。
9、mp_subscr_fun_t subscr。对下标进行load、save、delete等操作。
10、mp_getiter_func_t getiter。对应__iter__函数。
11、mp_fun_1_t iternext。对应__next__函数。
12、mp_buffer_p_t buffer_p 。实现buffer协议。
13、const void *protocol。解体协议。
14、const void *parent。指向父类。
15、struct _mp_obj_dict_t *locals_dict 。qstr到函数、变量的映射。
```



# 基础头文件内容分析

## misc.h

声明m_new和m_del函数。

定义vstr_t类型。声明相关函数。

## qstr.h

定义qstr和qstr_pool_t类型。

相关函数。

## mpprint.h

定义mp_print_t类型。相关函数。

## runtime0.h

定义3个主要枚举类型。

mp_unary_op_t

mp_binary_op_t

mp_fun_kind_t

## obj.h

定义了基础核心结构体。

_mp_obj_type_t

声明了一堆mp_obj_开头的函数。

## objtype.h

定义了一个实例结构体。

mp_obj_instance_t

相关函数。

## runtime.h

mp_init、mp_deinit这种系统层级的函数。

## mpstate.h



## lexer.h

这个单词什么意思？

```
/* lexer.h -- simple tokeniser for MicroPython
 *
 * Uses (byte) length instead of null termination.
 * Tokens are the same - UTF-8 with (byte) length.
 */
```

lexer是词法分析器的意思。

