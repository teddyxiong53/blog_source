---
title: npu之pytorch
date: 2021-09-09 19:57:33
tags:
	- npu

---

--

对于PyTorch，通过反向求导技术，可以让你零延迟地任意改变神经网络的行为，而且其实现速度 快。正是这一灵活性是PyTorch对比TensorFlow的最大优势。

另外，PyTorch的代码对比TensorFlow而言，更加简洁直观，底层代码也更容易看懂，这对于使用它的人来说理解底层肯定是一件令人激 动的事。



autograd 包是 PyTorch 中所有神经网络的核心。

首先让我们简要地介绍它，然后我们将会去训练我们的第一个神经网络。

该 autograd 软件包为 Tensors 上的所有操作提供自动微分。

它是一个由运行定义的框架，这意味着以代码运行方式定义你的后向传播，

并且每次迭代都可以不同。

我们从 tensor 和 gradients 来举一些例子。



参考资料

1、

https://pytorch123.com/FirstSection/PyTorchIntro/