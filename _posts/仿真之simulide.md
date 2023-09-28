---
title: 仿真之simulide
date: 2023-09-21 17:29:11
tags:
	- 仿真
---

--

打算通过这个项目来加速对电子、仿真、qt、c++的理解和掌握。

src\simulator\e-element.h

从这里开始看。

eElement代表了一个最基础的抽象的电子元件。

```
一个eElement，有一个vector，里面是ePin的指针。
```

所以更基础的ePin。

ePin的

```

```

ePin又涉及到eNode这个概念。eNode就是图形里的节点。

ePin有自己所属于的eNode，又有一个连接的eNode。

一个eNode有一组的ePin。

