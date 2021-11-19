---
title: iotjs研究
date: 2021-11-19 19:16:33
tags:
	- nodejs

---

--

jerryscript + iotjs 等价于v8引擎 + nodejs。

就是这样的对应关系。

iotjs代码量相对不大，而且是纯C语言写的，所以我感觉可以研究一下。

用 C 语言来扩展 iotjs 不是太难的事情，

但是将 GUI 集成到 iotjs 却是有些麻烦的。

主要原因在于 iotjs 有个主循环 (main loop)，

GUI 自己也有个主循环 (main loop)，

两者不同并存，只能选一个。

这里 AWTK 为例，介绍一下如何将 GUI 集成到 iotjs 中，这对将 GUI 集成到 nodejs 也是有参考价值。



在集成 AWTK 到 iotjs 时，我选择了以 iotjs 的主循环为主。这并不是唯一的正确方案，做这个选择的主要原因有：

让 AWTK 作为 iotjs 的模块，保持 iotjs 本身的开发方式。

避免修改 iotjs。iotjs 对我来说是第三方模块，修改第三方模块，会增加后期的维护成本。



我们把 AWTK 主循环的一次循环提取成一个 step，然后把它放到 iotjs 的定时器中，每隔 16 毫秒（最大 60FPS) 调用一次，这样可以模拟 GUI 的主循环了。



要将 GUI 集成到 iotjs，GUI 必须要把对外提供的API全部绑定到 jerryscript。

这个对 AWTK 来说只是举手之劳的事情，

AWTK 通过提取注释来生成 IDL，

再根据 IDL 来生成各种语言的绑定，这让绑定工作变得轻松，同时也降低了后期的维护成本。



AWTK-JS 这个项目提供了对 jerryscript 的绑定，我们把它编译成一个库，即可在 AWTK-iotjs 中使用了。



zlg官方的集成iotjs和awtk

https://github.com/zlgopen/awtk-iotjs





# iotjs内部

## 设计

iotjs基于jerryscript和libtuv。

JerryScript 是一个轻量级的 Javascript 引擎，

旨在运行在物联网的小型设备上，

而 libuv 是一个支持异步 I/O 的库。

有一个层将 JerryScript 和 libuv 绑定到 IoT.js。

我们将在本文档的 Javascript Binding 和 libuv Binding 部分进行介绍。



IoT.js 核心层位于这些绑定层之上。

这个核心层在这个项目中扮演着核心角色，

为上层提供运行主事件循环、与 Javascript 引擎交互、通过 libuv 管理 I/O 资源、管理对象的生命周期、提供内置模块等基本功能。

## JavaScript binding

许多现代 Javascript 引擎都带有嵌入的 API，

以提供用于编译和执行 Javascript 程序、访问 Javascript 对象及其值、处理错误、管理对象生命周期等的功能。

您可以将 Javascript 绑定层视为上层（IoT.js 核心）和底层 Javascript 引擎之间的接口。

虽然 IoT.js 目前只支持 JerryScript，

但未来我们有机会扩展支持 Javascript 引擎（如 Duktape 或 V8）。

出于这个原因，我们希望保持层独立于特定的 Javascript 引擎。

在iotjs_binding.h中可以看到该层的接口。



### jerry_value_t

这个结构体代表了一个JavaScript object。

上层会通过这个结构体来访问JavaScript object。

这个结构体提供了这些工具函数

```
创建一个js obj，通过iotjs_jval_create_xx函数。
创建一个js obj，通过一个value
创建一个js obj，它的实现是在C里面实现的。
创建一个js Error对象
增加ref cnt
减少ref cnt
检查obj 类型
调用一个js函数
eval一个js 脚本
set和get native数据给js obj
```

### native handler

有些操作，例如io、network、device control、多任务等等，

不能通过纯js来实现。

iotjs通过native handler的机制来执行这些操作。

你可以理解成js函数实现在C代码里。

### embedding api

现在很多的js引擎，都提供embedding api。

iotjs使用这些api来创建内置模块和native handler。

## libuv binding

iotjs使用libuv来执行异步io和线程。

### iotjs_handlewrap_t

这个结构体是用来binding一个js obj和一个libuv handler。

iotjs_handlewrap_t继承了iotjs_jobjectwrap_t结构体。因为它跟一个js obj关联了。

### iotjs_reqwrap_t

这个结构体是包装了libuv请求数据和js callback函数。

并确保js callback在io操作期间是alive状态的。

异步io操作在iotjs里是这样做的

1、js module调用builtin函数来执行io操作。

2、builtin创建iotjs_reqwrap_t来包装uv_req_s和js callback函数。

3、builtin调用libuv来执行io操作。

4、在io操作完成后，libuv调用builtin after handler（内置的后处理函数？韩国人的英文有点难懂）

5、内置的后处理函数 拿到iotjs_reqwrap_t（里面包含了io处理的结果和callback函数）

6、内置的后处理函数调用js callback。

7、内置的后处理函数释放iotjs_reqwrap_t。

## iotjs core

### life cycle

iotjs的处理过程如下

1、初始化jerryscript引擎。

2、执行空的脚本，创建一个初始化的js context。

3、初始化builtin module。包括process这个

4、执行iotjs.js，创建入口函数。

5、运行入口函数。

6、初始化process模块。

7、load用户的脚本。

8、运行用户脚本。

9、run eventloop，直到没有事件。

10、clean up

### builtin module

使用embedding api，在C语言里实现的js obj。

或者使用js实现的，包括src/js目录下的这些文件。

### eventloop





# jerryscript api文档

https://jerryscript.net/api-reference/

# libuv设计文档

http://docs.libuv.org/en/v1.x/design.html



# 参考资料

1、集成 AWTK 到 iotjs

这个是李先静的文章

https://blog.csdn.net/chongdingxi9493/article/details/101005502

2、官方文档

https://github.com/jerryscript-project/iotjs/blob/master/docs/devs/Developer-Tutorial.md

高级话题

https://github.com/jerryscript-project/iotjs/blob/master/docs/devs/Advanced-Development.md