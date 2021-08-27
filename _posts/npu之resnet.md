---
title: npu之resnet
date: 2021-08-25 19:19:33
tags:
	- npu

---

--

ResNet（Residual Neural Network）

由微软研究院的Kaiming He等四名华人提出，

通过使用ResNet Unit成功训练出了152层的神经网络，

并在ILSVRC2015比赛中取得冠军，

在top5上的错误率为3.57%，

同时参数量比VGGNet低，效果非常突出。

ResNet的结构可以**极快的加速神经网络的训练**，

模型的准确率也有比较大的提升。

同时ResNet的推广性非常好，甚至可以直接用到InceptionNet网络中。

ResNet的主要思想是在网络中增加了直连通道，

即Highway Network的思想。

此前的网络结构是性能输入做一个非线性变换，

而Highway Network则允许保留之前网络层的一定比例的输出。

ResNet的思想和Highway Network的思想也非常类似，

允许原始输入信息直接传到后面的层中，如下图所示。

![img](../images/random_name/20180710193536899)

这样的话这一层的神经网络可以不用学习整个的输出，而是学习上一个网络输出的残差，因此ResNet又叫做残差网络。



参考资料

1、ResNet介绍

https://blog.csdn.net/u013181595/article/details/80990930