---
title: npu之imagenet
date: 2021-08-23 13:21:33
tags:
	- npu

---

--

ImageNet项目是一个用于视觉对象识别软件研究的大型可视化数据库。

超过1400万的图像URL被ImageNet手动注释，以指示图片中的对象;

在至少一百万个图像中，还提供了边界框。

ImageNet包含2万多个类别; 

一个典型的类别，如“气球”或“草莓”，包含数百个图像。

第三方图像URL的注释数据库可以直接从ImageNet免费获得;

**但是，实际的图像不属于ImageNet。**

自2010年以来，ImageNet项目每年举办一次软件比赛，

即ImageNet大规模视觉识别挑战赛（ILSVRC），

软件程序竞相正确分类检测物体和场景。 

ImageNet挑战使用了一个“修剪”的1000个非重叠类的列表。

**2012年在解决ImageNet挑战方面取得了巨大的突破，被广泛认为是2010年的深度学习革命的开始。**

ImageNet就像一个网络一样，拥有多个Node（节点）。

每一个node相当于一个item或者subcategory。

据官网消息，一个node含有至少500个对应物体的可供训练的图片/图像。

**它实际上就是一个巨大的可供图像/视觉训练的图片库。**

ImageNet的结构基本上是金字塔型：目录->子目录->图片集。



参考资料

1、

https://baike.baidu.com/item/ImageNet/17752829?fr=aladdin