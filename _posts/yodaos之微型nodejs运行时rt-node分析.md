---
title: yodaos之微型nodejs运行时rt-node分析
date: 2024-08-18 10:46:11
tags:
	- yodaos

---

--

这个nodejs运行时非常小巧，而且可以正常运行。代码不是很多。

代码写得很清晰，值得研究一下。

而且是可以在单片机上运行的。

# struct napi_value__找不到定义

```
typedef struct napi_value__* napi_value;
```

有个这样的typedef，但是搜索不到napi_value__ 的定义。

网上找了一下，原则这个C语言是支持这样的定义的。

其实等价于

```
typedef void * napi_value;
```

那这个定义是什么意思呢？c语言中，允许定义一个没有定义的结构体的指针。所以napi_value其实就是一个一级指针。他不需要类型信息，因为Node.js不会对他进行解引用。

https://cloud.tencent.com/developer/article/1822419

# napi_env的作用是什么

`napi_env` 是 N-API 中的一个重要类型，它代表了一个上下文环境。其主要作用包括：

1. **资源管理**：
   - `napi_env` 提供了一个上下文，在该上下文中可以创建和管理 JavaScript 对象、函数和其他资源。

2. **线程安全**：
   - N-API 设计为线程安全，`napi_env` 允许在多个线程中安全地访问和操作 Node.js 运行时环境。

3. **错误处理**：
   - 在 `napi_env` 中，可以使用 N-API 提供的函数来处理错误和异常。

4. **数据传递**：
   - 它允许在 C/C++ 层和 JavaScript 层之间传递数据。

使用示例

在初始化模块时，你通常会看到 `napi_env` 作为参数传递给你的初始化函数。

```c
napi_value Init(napi_env env, napi_value exports) {
    // 在这个环境中创建和管理对象
    return exports;
}
```

总结

`napi_env` 是 N-API 的核心组成部分，使得开发者能够在原生模块中安全且高效地与 Node.js 的 JavaScript 运行时进行交互。