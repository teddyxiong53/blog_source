---
title: npu之GX8010上的NPU使用
date: 2021-08-25 17:00:33
tags:
	- npu

---

--

# NPU

搜索TF跟NPU对接的，找到了GX8010这个国芯的资料。

NPU处理器专门为物联网人工智能而设计，用于加速神经网络的运算，

解决传统芯片在神经网络运算时效率低下的问题。

在GX8010中，CPU和MCU各有一个NPU，MCU中的NPU相对较小，习惯上称为SNPU。

NPU处理器包括了乘加、激活函数、二维数据运算、解压缩等模块。

**乘加模块用于计算矩阵乘加、卷积、点乘等功能**，NPU内部有64个MAC，SNPU有32个。

激活函数模块采用最高12阶参数拟合的方式实现神经网络中的激活函数，

NPU内部有6个MAC，SNPU有3个。

二维数据运算模块用于实现对一个平面的运算，

如降采样、平面数据拷贝等，NPU内部有1个MAC，SNPU有1个。

解压缩模块用于对权重数据的解压。

为了解决物联网设备中内存带宽小的特点，

在NPU编译器中会对神经网络中的权重进行压缩，

在几乎不影响精度的情况下，可以实现6-10倍的压缩效果。



为了能将基于TensorFlow的模型用NPU运行，需要使用gxDNN工具。

**gxDNN用于**将用户生成的Tensorflow**模型编译**成可以被NPU硬件模块执行的指令，

并提供了一套API让用户方便地运行TensorFlow模型。

# VSP

这个文档写得不错。可以学习一下。

# skylarkos

SkylarkOS是基于NationalChip AI芯片构建的嵌入式Linux系统，集成了语音信号处理，神经网络运算，WIFI，蓝牙，播放器，GUI等丰富的功能组件，内置灵活高效的JS APP框架，帮助用户快捷地打造自己的AI应用方案



https://gitlab.com/nationalchip/skylarkos-getstarted

# 参考资料

1、GX8010上NPU的使用

http://ai.nationalchip.com/docs/gx8010/npukai-fa-zhi-nan/npujian-jie.html

2、

http://139.196.170.32/docs/pdf/GX8010_VSP_SDK_DG.pdf