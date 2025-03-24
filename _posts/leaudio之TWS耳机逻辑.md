---
title: leaudio之TWS耳机逻辑
date: 2025-03-20 15:30:37
tags:
	- 蓝牙
---

--

# 一些概念

### RSI 与 SIRK 和 CSIS 的关系

- SIRK（Set Identity Resolving Key）

  ：

  - SIRK 是协调集的“根密钥”，由制造商预置或动态分配。
  - RSI 是 SIRK 的派生结果，客户端需要知道 SIRK 才能解析 RSI。

- CSIS（Coordinated Set Identification Service）

  ：

  - CSIS 是 GATT 服务，定义了如何存储和访问 SIRK（如通过 Set Identity Resolving Key 特性）。
  - RSI 通常不直接存储在 CSIS 中，而是通过广播数据对外暴露，客户端通过 CSIS 获取 SIRK 来验证 RSI。
