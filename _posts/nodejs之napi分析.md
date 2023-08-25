---
title: nodejs之napi分析
date: 2023-08-21 16:10:33
tags:
	- nodejs

---

--

以shadownode的代码的src/napi目录为分析对象。

```
node_api_async.c
node_api.c
node_api_env.c
node_api_function.c
node_api_lifetime.c
node_api_module.c
node_api_object_wrap.c
node_api_property.c
node_api_tsfn.c
node_api_value.c
```

# 头文件

头文件就2个：

```
node_api_types.h
node_api.h
```

## node_api_types.h

主要的结构体有：

```
napi_env
napi_value
napi_ref
napi_handle_scope
napi_escapable_handle_scope
napi_callback_scope
napi_callback_info
napi_async_context
napi_async_work
napi_deferred

napi_property_descriptor
napi_extended_error_info
napi_node_version
```

重要的枚举：

```
napi_property_attributes
napi_valuetype
napi_typedarray_type
napi_status

```

## node_api.h

重要结构体：

```
node_module

```

工具宏：

```
NAPI_MODULE(modname, regfunc) 
```

典型的api函数的组成：

```
NAPI_EXTERN napi_status napi_get_undefined(napi_env env, napi_value* result);
NAPI_EXTERN napi_status napi_create_object(napi_env env, napi_value* result);
NAPI_EXTERN napi_status napi_create_double(napi_env env,
                                           double value,
                                           napi_value* result);
NAPI_EXTERN napi_status napi_get_value_double(napi_env env,
                                              napi_value value,
                                              double* result);
NAPI_EXTERN napi_status napi_get_value_string_utf8(napi_env env,
                                                   napi_value value,
                                                   char* buf,
                                                   size_t bufsize,
                                                   size_t* result);
```

可以看到：

1、返回值都是napi_status枚举。

2、参数至少有2个，一个env，一个result。



# 文件分析

## node_api_async.c

```
napi_create_async_work
napi_delete_async_work
napi_queue_async_work
napi_cancel_async_work
napi_async_init
napi_async_destroy
napi_make_callback
```

