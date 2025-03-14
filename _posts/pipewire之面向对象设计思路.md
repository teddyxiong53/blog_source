---
title: pipewire之面向对象设计思路
date: 2025-03-07 11:41:37
tags:
	- 音频
---

--

### 什么是虚函数表（VTable）？

- 定义

  ：

  - 虚函数表是面向对象语言（如 C++）中实现多态的核心机制。每个类有一个函数指针表，指向具体的实现函数，运行时通过对象的类型动态调用。

```
class Node {
public:
    virtual int process() = 0;
};
class AudioTestSrc : public Node {
    int process() override { return 42; }
};
Node* node = new AudioTestSrc();
node->process(); // 调用 AudioTestSrc::process
```

**C 中挑战**：

- C 没有类或虚函数，需要手动用结构体和函数指针模拟。

### PipeWire 如何模拟虚函数表？

PipeWire 通过 struct spa_interface 和方法表（如 struct spa_node_methods）实现类似功能。以下是逐步拆解：



### 模拟虚函数表的机制总结

- 关键元素

  ：

  1. **方法表**（struct spa_node_methods）：定义函数指针集合。
  2. **接口结构体**（struct spa_interface）：绑定方法表和数据。
  3. **调用宏**（SPA_INTERFACE_CALL）：实现动态跳转。

- C 语言实现

  ：

  - 用函数指针代替 C++ 的虚函数。
  - 用 void *data 代替 this 指针。

- 对比 C++

  ：

  - C++：编译器自动生成 VTable。
  - PipeWire：手动定义并绑定。
