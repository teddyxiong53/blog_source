---
title: npu之arm-nn-driver
date: 2021-08-20 17:08:33
tags:
	- npu

---

--

看看arm官方针对ML提供了哪些资源。

对象检测

语音识别

图像分类

关键词检测

pyarmnn

arm nn库针对arm硬件优化了神经网络。

pyarmnn是一个python包，包装了c++的api。

可以帮助你快速开发原型。

使用了parser来导入不同的外部矿机的模型。

支持的parser包括：

1、tflite

2、onnx

3、pytorch via onnx

parser把导入的模型转成armnn可以识别的样子。

物体检测是用来识别出视频或者静态图片里的人物、车辆、瓶子之类的。

可以把物体检测看成是图像分类的扩展应用。

在树莓派4b上可以安装测试。用apt来安装需要的软件，

```
git clone https://github.com/ARM-software/armnn.git
```

把你的测试视频拷贝到目录

```
cp example.mp4 armnn/python/pyarmnn/examples/object_detection
```

然后选择下载对应的模型。





参考资料

1、

https://github.com/ARM-software/ML-examples

2、

https://developer.arm.com/solutions/machine-learning-on-arm/developer-material/how-to-guides