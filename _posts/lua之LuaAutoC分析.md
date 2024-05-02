---
title: lua之LuaAutoC分析
date: 2024-05-01 15:26:49
tags:
	- lua

---

--

https://github.com/orangeduck/LuaAutoC

自动将 C 函数和结构与 Lua API 结合使用

最基本的是，LuaAutoC 可用于从 Lua API 自动调用 C 函数。

Lua 堆栈参数会自动弹出并转换为 C 类型，执行函数，

然后将返回值转换回 Lua 类型并放置在堆栈顶部。

首先，该函数必须注册为 `luaA_function` ，然后以后的任何时候都可以用 调用 `luaA_call` 它。