---
title: npu之armnn
date: 2021-09-24 11:19:33
tags:
	- npu

---

--

相对于其他竞品inference框架如NCNN、Tengine、Mace、MNN等等，ArmNN的知名度显得很小。

ArmNN基于Arm的另外一个开源计算引擎[ComputeLibrary](https://link.zhihu.com/?target=https%3A//github.com/ARM-software/ComputeLibrary)做后端的核心计算，

前端支持多种离线训练框架，

如TensorFlow、TFLITE、CAFFE以及ONNX。

从功能上来说，几乎实现了与市面上所有离线训练框架无缝对接。

**而且ArmNN在FP32、FP16及INT8上的加速非常可观，笔者在RK3399上做300x300的Mobilenet-SSD（depth_multiplier=1.0），效率可达90ms/ 帧，**

其余的框架大多在160ms左右徘徊。



在树莓派4b上编译运行。

```
git clone https://github.com/Arm-software/ComputeLibrary.git
git clone https://github.com/Arm-software/armnn
```

依赖了boost

```
wget https://dl.bintray.com/boostorg/release/1.64.0/source/boost_1_64_0.tar.bz2
```

```
$ git clone -b v3.5.0 https://github.com/google/protobuf.git
$ git clone https://github.com/google/flatbuffers.git
$ git clone https://github.com/tensorflow/tensorflow.git
$ cd tensorflow
$ git checkout 590d6eef7e91a6a7392c8ffffb7b58f2e0c8bc6b
```

ComputeLibrary是基于scons进行编译的。



参考资料

1、被低估的ArmNN（一）如何编译

https://zhuanlan.zhihu.com/p/71369040

2、

https://qengineering.eu/install-armnn-on-raspberry-pi-4.html

