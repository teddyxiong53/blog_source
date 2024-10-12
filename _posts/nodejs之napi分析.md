---
title: nodejs之napi分析
date: 2023-08-21 16:10:33
tags:
	- nodejs

---

--

# 介绍

N-API（Node.js API）是Node.js提供的一种稳定的、跨版本的编写本地插件（native addon）的API。它的设计目标是提供一个稳定的、可靠的接口，使得开发者可以编写C/C++模块，并且这些模块不会受到Node.js版本的影响。

N-API的主要特点和优势包括：

1. **稳定性和跨版本兼容性**：N-API提供了一组稳定的API，使得开发者可以编写的本地插件不会受到Node.js版本变化的影响。这意味着插件可以在不同版本的Node.js上运行，而不需要重新编译。

2. **简化插件开发流程**：N-API简化了本地插件的开发流程，开发者不再需要关注Node.js的内部实现细节和不同版本之间的差异，从而提高了开发效率。

3. **更好的性能和安全性**：由于N-API采用了Node.js提供的稳定的、官方支持的API，因此插件可以更好地利用Node.js的性能优势，并且更安全地集成到应用程序中。

4. **支持跨平台**：N-API设计为跨平台的API，可以在不同的操作系统上运行，包括Windows、Linux和macOS等。

5. **社区支持和活跃度**：N-API得到了Node.js社区的广泛支持和积极参与，正在不断地发展和完善，为开发者提供更好的插件开发体验。

总的来说，N-API是Node.js生态系统中的一个重要组成部分，它为开发者提供了一种稳定的、跨版本的编写本地插件的API，使得开发者可以更轻松地编写高性能、可靠的Node.js插件。

# helloworld

```
#include <node_api.h>

// 实现一个简单的函数，返回一个字符串
static napi_value SayHello(napi_env env, napi_callback_info info) {
  napi_status status;

  // 创建一个N-API的字符串
  napi_value str;
  status = napi_create_string_utf8(env, "Hello, World!", NAPI_AUTO_LENGTH, &str);
  if (status != napi_ok) {
    napi_throw_error(env, NULL, "Failed to create string");
    return NULL;
  }

  // 返回字符串
  return str;
}

// 导出初始化函数，用于注册模块
static napi_value Init(napi_env env, napi_value exports) {
  napi_status status;
  napi_value fn;

  // 创建一个函数对象
  status = napi_create_function(env, NULL, 0, SayHello, NULL, &fn);
  if (status != napi_ok) {
    napi_throw_error(env, NULL, "Failed to create function");
    return NULL;
  }

  // 将函数对象导出为模块的属性
  status = napi_set_named_property(env, exports, "sayHello", fn);
  if (status != napi_ok) {
    napi_throw_error(env, NULL, "Failed to set property");
    return NULL;
  }

  return exports;
}

// 导出模块初始化函数
NAPI_MODULE(NODE_GYP_MODULE_NAME, Init)

```

示例中的`NODE_GYP_MODULE_NAME`是一个宏，通常会被预处理器替换为实际的模块名称。

# 代码

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

# c++ api

https://github.com/nodejs/node-addon-api/blob/main/doc/hierarchy.md
