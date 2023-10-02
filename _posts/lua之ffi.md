---
title: lua之ffi
date: 2023-09-29 16:42:11
tags:
	- lua
---

--

官方网站在这里：

http://luajit.org/ext_ffi.html

首先，这个是luajit才支持的特性，标准lua是不支持的。

# luajit vs lua

Lua和LuaJIT是两种不同的编程语言实现，它们在一些方面有所区别。

1. **执行速度：** LuaJIT是对Lua的即时编译（Just-In-Time Compilation，JIT）实现，相比纯解释执行的Lua，它可以提供更高的执行速度。LuaJIT通过将Lua字节码动态编译成本机机器码来实现这种性能提升。

2. **内存管理：** LuaJIT在内存管理方面也有一些优化。它采用了更高效的垃圾回收算法，并提供了一些额外的内存管理功能，例如显式的内存分配和释放接口。这使得LuaJIT在某些情况下可以更加灵活地控制内存使用。

3. **语言特性支持：** LuaJIT在语言特性上与Lua基本兼容，但在某些方面可能有所差异。一些Lua的扩展特性或语法糖可能在LuaJIT中不被支持或有不同的行为。因此，在使用LuaJIT时，需要注意与标准Lua的差异。

4. **跨平台支持：** Lua是一个跨平台的脚本语言，有广泛的移植性。LuaJIT在最初的设计中专注于x86体系结构，但后来也进行了其他平台的移植工作，例如ARM和PowerPC。然而，与Lua相比，LuaJIT的跨平台支持可能相对较少或存在一些限制。

luajit的官网：

https://luajit.org/

现在还在继续维护的。

当前最新的版本是2.1。

luajit只是兼容了lua语法，它自己的实现是完全重写的。自己的函数都是以lj为前缀的。

https://github.com/LuaJIT/LuaJIT

但是它使用的lua的版本是5.1的。

# luajit怎么用

Just-in-time 即时编译技术，在 LuaJIT 里的具体使用是：将 Lua byte code 即时编译为机器指令，也就是不再需要解释执行 Lua bytecode，直接执行即时编译产生的机器指令。
也就是说，解释模式，和 JIT 模式的输入源是一样的，都是 Lua byte code。相同的字节码输入，两种模式却可以有跑出明显的性能区别（一个数量级的区别，也是比较常见的），这个还是很需要功力的。

JIT 可以分为这么几个步骤：

1. 计数，统计有哪些热代码
2. 录制，录制热代码路径，生成 SSA IR code
3. 生成，SSA IR code 优化生成机器指令
4. 执行新生成的机器指令



```
luajit -b test.lua test.out
```



参考资料

1、LuaJIT 是如何工作的 - 解释模式

https://segmentfault.com/a/1190000040170791

# 参考资料

1、

https://lua.ren/topic/tweyseo-WalkOnLuaJIT-1/