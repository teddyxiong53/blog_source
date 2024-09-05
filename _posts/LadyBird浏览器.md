---
title: LadyBird浏览器
date: 2024-09-04 11:10:17
tags:
	- 浏览器

---

--

# 基本信息

Ladybird 浏览器基于 SerenityOS 的 LibWeb 和 LibJS 引擎，LibWeb 始于 2019 年开发，其 JavaScript 引擎 LibJS 则于 2020 年开发。

Ladybird 浏览器诞生于 7 月 4 日，最初是作为 LibWeb 浏览器引擎调试工具，随后 Andreas 决定继续推进并为它构建一个简单的 GUI 。然而两个月后，Andreas 发现自己使用 Ladybird 完成了一个 Web 浏览器的大部分开发工作，这也让他意识到可以将 SerenityOS 的浏览器引擎”调整为“跨平台浏览器引擎”。

当前浏览器主要组件：

- Ladybird : 选项卡式浏览器 GUI 应用程序
- LibWeb：Web 引擎，多种标准：HTML、DOM、CSS、SVG，……
- LibJS：ECMAScript 语言、运行时库、垃圾收集器
- LibGfx：2D 图形、文本渲染、图像格式（PNG、JPG、GIF，...）
- LibRegex：正则表达式引擎
- LibXML : XML 解析器
- LibWasm：WebAssembly 解析器和解释器
- LibUnicode：Unicode 支持库
- LibTextCodec : 文本编码转换库
- LibMarkdown : Markdown 解析器
- LibCore：其他支持功能（I/O、日期时间、MIME 数据……）
- Qt：跨平台 GUI 和网络

https://www.infoq.cn/article/bbh2olmjoyofsda15i6b

# 代码

https://github.com/LadybirdBrowser/ladybird

依赖的库都是在serenity\Userland\Libraries\下面。

