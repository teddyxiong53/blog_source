---
title: npu之autokeras
date: 2021-09-06 15:10:33
tags:
	- npu

---

--

我们在构建自己的神经网络模型时，

往往会基于预编译模型上进行迁移学习。

但不同的训练数据、不同的场景下，各个模型表现不一，

需要投入大量的精力进行调参，耗费相当多的时间才能得到自己满意的模型。

而谷歌近期推出了AutoML，

可以帮助人们在给定数据下自动找寻最优网络模型，

可谓让不是专业的人也可以轻松构建合适自己的网络模型，

但唯一的问题是太贵了，每小时收费20美元啦。

幸好开源界也推出了autokeras，让我们一众屌丝也可以享受这免费的待遇，

AutoKeras: An AutoML system based on Keras. It is developed by [DATA Lab](http://faculty.cs.tamu.edu/xiahu/index.html) at Texas A&M University. The goal of AutoKeras is to make machine learning accessible to everyone.



autoKeras的作用就是省去你调参的过程。

帮你自动生成一个网络。



在给定的数据集中实现当前最佳模型性能

通常要求使用者认真选择合适的数据预处理任务，

挑选恰当的算法、模型和架构，

并将其与合适的参数集匹配。

这个端到端的过程通常被称为机器学习工作流（Machine Learning Pipeline）。

没有经验法则会告诉我们该往哪个方向前进，

随着越来越多的模型不断被开发出来，

即使是选择正确的模型这样的工作也变得越来越困难。

超参数调优通常需要遍历所有可能的值或对其进行抽样、尝试。

然而，这样做也不能保证一定能找到有用的东西。

在这种情况下，自动选择和优化机器学习工作流一直是机器学习研究社区的目标之一。

**这种任务通常被称为「元学习」，它指的是学习关于学习的知识。**



**AUTOKERAS**

- 开源与否：是
- 是否基于云平台：否
- 支持的模型类别：用于分类的卷积神经网路（CNN）、循环神经网络（RNN）、长短期记忆网络（LSTM）
- 使用的技术：高效神经架构搜索（参见《Efficient NeuralArchitecture Search via Parameter Sharing》）
- 训练框架：Keras



https://github.com/PacktPublishing/Automated-Machine-Learning-with-AutoKeras



参考资料

1、深度学习应用系列（三）| autokeras使用入门

https://www.cnblogs.com/hutao722/p/9553526.html

2、

https://www.sohu.com/a/274725104_129720

3、

https://zhuanlan.zhihu.com/p/41195489