---
title: npu之深度学习和神经网络关系
date: 2021-10-08 13:51:33
tags:
	- npu

---

--

 **浅层学习是机器学习的第一次浪潮。**

20世纪80年代末期，用于人工神经网络的反向传播[算法](http://lib.csdn.net/base/datastructure)（也叫Back Propagation算法或者BP算法）的发明，

给机器学习带来了希望，掀起了**基于统计模型**的机器学习热潮。

这个热潮一直持续到今天。

人们发现，利用BP算法可以让一个人工神经网络模型从大量训练样本中学习统计规律，从而对未知事件做预测。

这种基于统计的机器学习方法比起过去基于人工规则的系统，在很多方面显出优越性。

这个时候的人工神经网络，虽也被称作多层感知机（Multi-layer Perceptron），但实际是种只含有一层隐层节点的浅层模型。

这些模型无论是在理论分析还是应用中都获得了巨大的成功。相比之下，由于理论分析的难度大，训练方法又需要很多经验和技巧，这个时期浅层人工神经网络反而相对沉寂。



深度学习是机器学习研究中的一个新的领域，其动机在于建立、模拟人脑进行分析学习的神经网络，它模仿人脑的机制来解释数据，例如图像，声音和文本。



Deep learning与传统的神经网络之间有相同的地方也有很多不同。

二者的相同在于deep learning采用了神经网络相似的分层结构，

系统由包括输入层、隐层（多层）、输出层组成的多层网络，

只有相邻层节点之间有连接，同一层以及跨层节点之间相互无连接，

每一层可以看作是一个logistic regression模型；

这种分层结构，是比较接近人类大脑的结构的。



深度学习是为了让层数较多的多层神经网络可以训练，能够work而演化出来的一系列的 新的结构和新的方法。

新的网络结构中应用最广泛的的就是CNN，大量应用在计算机视觉领域，它解决了传统较深的网络参数太多，很难训练的问题，使用了“局部感受野”和“权植共享”的概念，大大减少了网络参数的数量。一些研究表明，这种对信息的层次化抽取与提练很符合视觉类任务在人脑上的工作原理。CNN这个方向上结构经过几年的发展，出来了很多的经典网络结构，如VGG、Inception、ResNet等。除了CNN之外，在序列数据的处理上，RNN被广泛应用，RNN方向上也有很多创新的网络结构被提出，比如LSTM。







参考资料

1、

https://blog.csdn.net/a493823882/article/details/83548447

