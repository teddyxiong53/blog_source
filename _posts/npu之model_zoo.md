---
title: npu之model_zoo
date: 2021-08-31 16:45:33
tags:
	- npu

---

--

提供了一组预先培训过的检测模型，

包括Coco数据集、Kitti数据集、开放图像数据集、AVA V2.1数据集和不自然物种检测数据集。

如果您对那些数据集中已经存在的类别感兴趣，

那么这些模型对于开箱即用的推断很有用。

在新数据集的培训中，它们对于初始化模型也很有用。

比如用于图像分类的Slim，深度文字OCR，

以及用于NLP任务的句法分析模型syntaxnet，Seq2Seq with Attention等等。

这次公布的Object Detection API同样是放在了tensorflow/models里。 

- COCO 数据集（微软开源的数据集）
- Kitti数据集（自动驾驶场景）
- Open Images数据集（谷歌开源的数据集）
- AVA v2.1数据集（人类动作识别数据集）
- iNaturalist Species Detection数据集



首先，对于目标检测这个任务来说，

前面必须有一个像样的ImageNet图像分类模型

来充当所谓的特征提取（Feature Extraction）层，

比如VGG16、ResNet等网络结构。

TensorFlow官方实现这些网络结构的项目是TensorFlow Slim，

而这次公布的Object Detection API正是基于Slim的。

Slim这个库公布的时间较早，

不仅收录了AlexNet、VGG16、VGG19、Inception、ResNet

这些比较经典的耳熟能详的卷积网络模型，

还有Google自己搞的Inception-Resnet，MobileNet等。




参考资料

1、tensorflow models zoo简介

https://blog.csdn.net/qq_30460949/article/details/88924412