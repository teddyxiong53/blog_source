---
title: npu之树莓派上基于Arm-Compute-Library运行AlexNet
date: 2021-08-26 11:01:33
tags:
	- npu

---

--

ARM Compute Library是ARM公司刚发布不久的开源工程，

旨在为图像/视频/多媒体/计算机视觉等领域的开发者提供arm平台的硬件加速库。

这个库中分别用OpenCL与NEON的方式实现了一些上述领域的基本算法，

OpenCL主要是arm的Mali GPU加速，

NEON是针对arm的A系列CPU。

我最近研究了一下它的源码，

主要看了针对CNN的卷积运算需要用到的convolution过程。

当然，其他的基本算法也都是同样的流程。

工程中是把图像按照列的方式分割成子块，

然后**分别启动几个线程去处理这些子块。**

对于convolution来说，

NEON方式实现了两种方法，

一种是GEMM的方法，

把输入图像先im2col，然后interleave操作，把weight进行transposed操作，之后进行矩阵乘法，

之所以有interleave与transposed两步

是为了矩阵乘法时NEON指令集load数据的连贯性与平顺性，

并且不需要重复load，

最大限度的发挥了neon指令集的能力。

还一种方法是标准的卷积运算。

当然其中也是运用了NEON的intrinsic函数调用方式。

OpenCL调用GPU加速的方式我还没有细看，

不过大体上看来主要流程与NEON的方式类似，

也是按照线程数分割图像，然后并行处理子块。

其中也是有shape，window，iterator的概念。

只是真正的计算中与NEON的指令集不一样。

这个lib发布之后，

开发者可以不用关心arm的cpu与gpu怎样通过NEON或OpenCL来实现硬件的加速，

直接调用这个库中的接口就可以，

对于开发计算机视觉类的应用但是不太了解硬件加速编程的工程师来说十分有利。

仓库地址

https://github.com/ARM-software/ComputeLibrary



https://docs.broadcom.com/doc/12358545

这篇文章非常好。

https://petewarden.com/2014/08/07/how-to-optimize-raspberry-pi-code-using-its-gpu/

https://github.com/jetpacapp/DeepBeliefSDK



基于arm-compute库实现的lenet。

https://github.com/ARM-software/ComputeLibrary/blob/master/examples/graph_lenet.cpp



arm-nn是在arm-compute的基础上进一步进行封装。



# 参考资料

1、

https://community.arm.com/developer/ip-products/processors/b/processors-ip-blog/posts/running-alexnet-on-raspberry-pi-with-compute-library

2、ARM Compute Library

https://blog.csdn.net/u010957054/article/details/73800217