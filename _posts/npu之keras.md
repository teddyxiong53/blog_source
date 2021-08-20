---
title: npu之keras
date: 2021-08-18 19:56:33
tags:
	- npu

---

--

看tensorflow文档，看到Keras这个东西，先了解一下。

Keras 是一个用 Python 编写的高级神经网络 API，

它能够以 [TensorFlow](https://github.com/tensorflow/tensorflow), [CNTK](https://github.com/Microsoft/cntk), 或者 [Theano](https://github.com/Theano/Theano) 作为后端运行。

Keras 的开发重点是支持快速的实验。

能够以最小的时延把你的想法转换为实验结果，是做好研究的关键。

如果你在以下情况下需要深度学习库，请使用 Keras：

- 允许简单而快速的原型设计（由于用户友好，高度模块化，可扩展性）。
- 同时支持卷积神经网络和循环神经网络，以及两者的组合。
- 在 CPU 和 GPU 上无缝运行。

Keras 的核心数据结构是 **model**，一种组织网络层的方式。

最简单的模型是 [Sequential 顺序模型](https://keras.io/getting-started/sequential-model-guide)，它由多个网络层线性堆叠。对于更复杂的结构，你应该使用 [Keras 函数式 API](https://keras.io/getting-started/functional-api-guide)，它允许构建任意的神经网络图。



Sequential模型，也翻译为序贯模型。

是多个网络层的线性堆叠，也就是一条道走到黑。



# 参考资料

1、官方文档

https://keras.io/zh/

2、10行命令感受机器学习的神奇（0基础小白适用）

https://zhuanlan.zhihu.com/p/27303650