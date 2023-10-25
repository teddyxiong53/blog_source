---
title: wasm（1）
date: 2023-10-10 15:53:11
tags:
	- rtos
---

--

# 简介

`WebAssembly` 是基于[栈式虚拟机](https://www.zhihu.com/search?q=栈式虚拟机&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1961085507})的二进制指令集，可以作为编程语言的编译目标，能够部署在 `web` [客户端](https://www.zhihu.com/search?q=客户端&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1961085507})和服务端的应用中。

首先 `WebAssembly` 是由 `Web` 和 `Assembly` 两个词构成，其中 `Web` 表明它一定和前端有关。`Assembly` 的意思是汇编，汇编对应机器码，而机器码和 `CPU` 的指令集有关，接下来补一下相关的知识。



上边的格式属于 「[S- 表达式](https://www.zhihu.com/search?q=S- 表达式&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1961085507})」， `Lisp` 语言就是采用的这种表达式，每条语句都是先执行最里边括号的表达式然后依次展开。



由于当前 `Wasm` 标准下，`Wasm` 模块不能直接操纵 `dom` 元素，所以 `WebAssembly` 主要应用在了一些计算密集型的场景下，视频的解码编码、图像处理、涉及到复杂计算的算法、[加密算法](https://www.zhihu.com/search?q=加密算法&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1961085507})等等。



值得一提的是因为 wasm 有些底层，所以一般还是写高级语言来生成 wasm 比较合适，这样一来就可以把更多精力放在代码的逻辑上而不需要关注 wasm 怎么和宿主环境进行互相的函数调用，还有内存管理的各种细节之类的，





参考资料

1、

https://www.zhihu.com/question/304577684/answer/1961085507

# emscripten

简单说，就是把c/c++程序编译为js文件。



https://www.ruanyifeng.com/blog/2017/09/asmjs_emscripten.html

# wasm的典型用途

为了更明确的定义该术语，我们首先要解决关于WASM不是什么的说明：



1）WebAssembly不是一种编程语言；

2）WebAssembly不仅仅是“Web中的C++”;

3)  WebAssembly本身并不是一种Web技术，因此被称为Web Assembly。



## gpt回复

WebAssembly（简称 wasm）是一种开放标准的二进制指令集，旨在提供一种跨平台、高性能的执行环境，可以在现代 web 浏览器中运行。wasm 具有许多用途，包括但不限于以下典型用途：

1. **Web 应用程序的性能优化**：wasm 允许开发者将性能敏感的代码以高效的方式编译为二进制格式，以便在 web 浏览器中运行。这可以显著提高 web 应用程序的性能，特别是在处理大型数据集、复杂计算或图形渲染时。

2. **跨平台移动应用**：wasm 可以用于构建跨平台移动应用程序，使开发者能够在不同操作系统上共享代码。这可以减少开发和维护的工作量，并提供更一致的用户体验。

3. **在线游戏**：wasm 可以用于构建高性能的在线游戏，允许游戏开发者将复杂的游戏逻辑和图形渲染代码在 web 浏览器中运行，而无需插件或降低性能。

4. **多媒体应用**：wasm 可以用于创建音频和视频处理应用，以及图像编辑工具，这些应用可以在 web 浏览器中直接运行。

5. **科学计算和数据分析**：wasm 具有出色的性能，因此它适用于科学计算和数据分析任务。开发者可以将现有的数值计算库编译为 wasm 模块，并在浏览器中运行，或者使用 wasm 来加速数据处理。

6. **物联网设备**：wasm 可以用于在物联网设备中运行代码，使设备具有更强大的计算和处理能力，而无需大幅增加硬件成本或功耗。

7. **在线教育**：wasm 可以用于创建交互式的在线教育应用，包括模拟器、编程学习工具和虚拟实验室等。

8. **浏览器扩展和插件**：wasm 可以用于编写浏览器扩展和插件，以增强浏览器的功能，而无需依赖特定的浏览器扩展平台。

9. **自定义浏览器引擎**：一些项目使用 wasm 来构建自定义浏览器引擎或解释器，以实现特定的 web 浏览器功能或浏览器兼容性测试。

总的来说，WebAssembly 具有广泛的应用领域，可以用于改善 web 应用程序的性能、提供跨平台的解决方案、支持复杂的计算任务以及创建各种类型的交互性 web 内容。随着 wasm 生态系统的不断发展，它将在更多领域得到应用。

# wasm3

这个库，我看到txiki.js用到了。

https://github.com/wasm3/wasm3

先研究一下这个库的基本用法。

看看可以用来做什么。

快速的 WebAssembly 解释器和最通用的 WASM 运行时。

# pywasm3

https://github.com/wasm3/pywasm3



https://github.com/alvarowolfx/wasm-arduino-wifi



# 缓存wasm到本地



参考资料

1、将ffmpeg.wasm文件缓存到浏览器indexedDB，方便快速调用

https://zhuanlan.zhihu.com/p/431440059





但是随着 WasmEdge 等引擎支持 QuickJS 的解释器，

JavaScript 逐渐变成了 WebAssembly 平台之上的最流行的编程语言。

这里除了有 JavaScript 语言用户比较多的因素，

同时 JavaScript 的单线程模型也非常契合 WebAssembly 的单线程模型。

JavaScript 和 WebAssembly 无限套娃的事情真在切实发生，同时 JavaScript 也失去了浏览器中的霸主地位降级为普通公民。



https://zhuanlan.zhihu.com/p/635473856

# 参考资料

1、

https://blog.51cto.com/u_15127566/2665209