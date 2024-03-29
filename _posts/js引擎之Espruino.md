---
title: js引擎之Espruino
date: 2024-03-18 17:19:17
tags:
	- js

---

--

# 简介

Espruino 是一个非常轻量的 JavaScript 引擎，可以运行在 128KB Flash & 8KB RAM 的微控制器 (MCU) 上。

相比于其他 JavaScript 引擎，Espruino 具有以下特点：

- 轻量级 —— 可以运行在 128KB Flash & 8KB RAM 的微控制器 (MCU) 上；
- 事件驱动 —— 与 node.js 类似，Espruino 采用事件驱动机制，支持异步函数回调和异步 I/O；
- 简单易用 —— Espruino 提供丰富的外设库，对硬件层做了很好的抽象，只要会写 JavaScript 就能用它来控制硬件；
- 跨平台开发 —— Espruino 提供一个基于 Chrome 浏览的 Web IDE，可以进行跨平台开发；
- 无线调试 —— Espruino Web IDE 使用 Web Bluetooth API，可以提供无线下载调试 JavaScript 代码功能。



https://wiki.makerdiary.com/nrf52832-mdk/cn/espruino/



http://www.espruino.com/Reference#software

# espjs

一个espruino的命令行开发工具, 支持esp01,eps01s,esp8266开发版等

代码在这里：

https://github.com/zhaishuaigan/espjs

说明文档放在看云上：

https://www.kancloud.cn/shuai/espjs/2203723



https://juejin.cn/post/7204121228017532989

