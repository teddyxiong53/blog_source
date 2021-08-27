---
title: npu之yolo
date: 2021-08-25 10:25:33
tags:
	- npu

---

--

YOLO（You Only Look Once: Unified, Real-Time Object Detection），

是Joseph Redmon和Ali Farhadi等人于2015年提出的**基于单个神经网络**的**目标检测系统**。

在2017年CVPR上，Joseph Redmon和Ali Farhadi又发表的YOLO 2，进一步提高了检测的精度和速度

论文在这里，并不长。

https://pjreddie.com/media/files/papers/yolo.pdf

目标检测发展过程

> 早期的目标检测方法:
>
> 通过提取图像的一些 robust 的特征（如 Haar、SIFT、HOG 等），
>
> 使用 DPM （Deformable Parts Model）模型，
>
> 用滑动窗口（silding window）的方式来预测具有较高 score 的 bounding box。
>
> 这种方式非常耗时，而且精度又不怎么高。



> 后来出现了object proposal方法（其中selective search为这类方法的典型代表）:
>
> 相比于sliding window这中穷举的方式，减少了大量的计算，同时在性能上也有很大的提高。
>
> 利用 selective search的结果，结合卷积神经网络的R-CNN出现后，
>
> Object detection 的性能有了一个质的飞越。
>
> 基于 R-CNN 发展出来的 SPPnet、Fast R-CNN、Faster R-CNN 等方法，
>
> 证明了 “Proposal + Classification” 的方法在 Objection Detection 上的有效性。



> 相比于 R-CNN 系列的方法，YOLO提供了另外一种思路：
>
> 将 Object Detection(目标检测) 的问题转化成一个 Regression 问题。
>
> 给定输入图像，直接在图像的多个位置上回归出目标的bounding box以及其分类类别。



YOLO是一个可以一次性预测多个Box位置和类别的卷积神经网络

能够实现端到端的目标检测和识别，

其最大的优势就是速度快。



**事实上，目标检测的本质就是回归，**

因此一个实现回归功能的CNN并不需要复杂的设计过程。

YOLO没有选择滑动窗口（silding window）或提取proposal的方式训练网络，

而是直接选用整图训练模型。

这样做的好处在于可以**更好的区分目标和背景区域**，

相比之下，采用proposal训练方式的Fast-R-CNN常常把背景区域误检为特定目标。



一体化的设计方案：

YOLO的设计理念遵循**端到端训练和实时检测**。

YOLO将输入图像划分为S*S个网格，如果一个物体的中心落在某网格(cell)内，则相应网格负责检测该物体。

在训练和测试时，每个网络预测B个bounding boxes，每个bounding box对应5个预测参数：

bounding box的中心点坐标(x,y)，宽高（w,h）
和置信度评分（confidence）



YOLO使用均方和误差作为loss函数来优化模型参数，

即网络输出的S*S*(B*5 + C)维向量与真实图像的对应S*S*(B*5 + C)维向量的均方和误差。





参考资料

1、

https://blog.csdn.net/wsp_1138886114/article/details/82048776