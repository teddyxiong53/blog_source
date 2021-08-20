---
title: npu之tflite-micro
date: 2021-08-20 10:39:33
tags:
	- npu

---

--

Tiny ML 的理念是在设备上用较少的资源（更小巧的外形、更少的能耗和更低成本的芯片）完成更多的工作。

若与传感器在同一块开发板上运行推理，

无论是对隐私还是电池续航时间都大有裨益，且意味着无需连网即可完成推理。

我们在电路板上安装了近接感应器，

这意味着我们可以即时读取开发板前方对象的深度，而无需使用摄像头，

也无需通过机器视觉来确定某个对象是否为目标对象。

在本教程中，当对象足够近时，我们可以对颜色进行采样，

此时的板载 RGB 传感器可以看作是一个 1 像素的彩色摄像头。

虽然此方法存在一定限制，但却让我们只需使用少量资源便可快速分类对象。

请注意，实际上您可以在设备端运行完整的[基于 CNN 的视觉模型](https://link.zhihu.com/?target=http%3A//cs231n.github.io/convolutional-networks/)。

这块特殊的 Arduino 开发板配有一个板载色度计，因此我们认为以此方式开始演示不仅有趣，还极具指导意义。

我们将展示一个简单但完整的端到端 TinyML 应用，无需深厚的 ML 或嵌入式背景就可以快速实现。此处所涉内容包括数据采集、训练和分类器部署。

我们介绍的是一个演示应用，您可连接一个外部摄像头，在此基础上进行改进和完善。

我们希望您能了解我们提供的工具能够实现什么，这里只是为您提供了一个起点。



我们所使用的 Arduino BLE 33 Nano Sense 开发板配备 Arm Cortex-M4 微控制器，

该控制器运行着 mbedOS，并具备多个板载传感器，

包括数字麦克风、加速度计、陀螺仪，以及温度、湿度、压力、光线、颜色和近接感应器。



虽然该微控制器按照云或移动标准来看非常微小，但其功能非常强大，

足以运行 TensorFlow Lite Micro 模型并对来自板载传感器的传感器数据进行分类。



现在，我们将采集用于在 TensorFlow 中训练模型所需的数据。

首先，选择几种颜色不同的对象。

在这里，我们将使用水果，但您可以使用任何您喜欢的其他对象。



操作步骤是：

1、运行程序，然后把一个苹果靠近传感器，串口会打印颜色数据。手动赋值数据，保存成一个csv文件。

2、一样的操作，把香蕉和橘子的数据也保存起来。

3、然后是打开教程提供的colab的链接，按照说明把cvs文件上传到google drive。

4、然后用keras用数据训练模型。把得到的模型下载下来。是转成了头文件数组的方式。

5、运行另外一个arduino程序，来使用模型进行判断。



先首先要把代码都梳理出来，自己编译一遍。

# 代码分析对象

以rt-thread集成的package的作为分析对象。

这个看起来经过整理和简化。

https://github.com/QingChuanWS/TensorflowLiteMicro



# rt-thread集成tflite-micro

ST Cube AI对TFLite Micro做了一层自己的封装，好用到爆。

你生成的模型无论是keras还是saved_model都支持，直接导入。

rt-thread里集成了这些AI框架。可以都看一下。

```
 [ ] libann: a light-weight ANN library, capable of training, saving and loading models.  ----   这个已经不再维护了。                             
 [ ] NNoM: A higher-level Neural Network framework on Microcontroller  ----                                                   
 [ ] onnx-backend: Open Neural Network Exchange backend on RT-Thread  ----                                                    
 [ ] onnx-parser: Open Neural Network Exchange model parser on RT-Thread  ----                                                
 [*] Tensorflow Lite Micro: a lightweight deep learning end-test inference framework for RT-Thread operating system.  --->    
 [ ] elapack: linear algebra library for embedded devices, compatible with matlab.  ----                                      
 [ ] ulapack: linear algebra library for embedded devices.  ----                                                              
 [ ] quest: A simulator of quantum computers on MCU. (RTC required) (NEW)  ----                                               
 [ ] A C++ Constraint Programming Library (NEW)  ----                                                                         
```

暂时先把tflite-micro的编译运行看看效果。

对应的仓库的代码是这里。

https://github.com/QingChuanWS/TensorflowLiteMicro

对饮的音频测试代码是这样

```
#include <rtthread.h>
#include <rtdevice.h>
#include <board.h>
#include "tflite/micro/examples/micro_speech/main_functions.h"

// This is the default main used on systems that have the standard C entry
// point. Other devices (for example FreeRTOS or ESP32) that have different
// requirements for entry code (like an app_main function) should specialize
// this main.cc file in a target-specific subfolder.
int main(int argc, char* argv[]) {
  setup();
  rt_kprintf("model load successfully!!\n");
   while (true) {
     loop();
   }

  return 0;
}
```

而在lite/micro/examples/helloworld/main_function.cc里，有setup和loop函数的实现。

这个实际是arduino的标准入口和循环函数。

就以arduino的为主来分析函数的调用流程。

所有的函数都在tflite这个namespace下面。

# HelloWorld

看下面的readme，这个例子用来演示怎么使用tflite-micro的。

包括了完整的端到端的流程，包括训练模型，转换到tflite-micro可用的模型，

# lite目录代码

```
c
	builtin_op_data.h  定义了一堆的结构体，复杂性不高的，但是概念很密集。
	c_api_types.h 状态枚举，数据类型枚举，就3个结构体。
	common.h 定义了一下重要的结构体。
	common.c
core
	下面就一个api目录。里面文件也不多。总共4对8个文件。
	error_reporter.h/cc
	flatbuffer_conversion.h/cc
	op_resolver.h/cc
	tensor_utils.h/cc
experimental
kernels
micro
schema
```

TF_LITE_STATIC_MEMORY 这个宏来控制是否使用动态malloc。

# tflite api

https://tensorflow.google.cn/lite/api_docs

c++的api就5个class。

| Classes                                                      |                                                              |
| :----------------------------------------------------------- | ------------------------------------------------------------ |
| [tflite::ErrorReporter](https://tensorflow.google.cn/lite/api_docs/cc/class/tflite/error-reporter) | A functor that reports error to supporting system.           |
| [tflite::FlatBufferModel](https://tensorflow.google.cn/lite/api_docs/cc/class/tflite/flat-buffer-model) | An RAII object that represents a read-only tflite model, copied from disk, or mmapped. |
| [tflite::Interpreter](https://tensorflow.google.cn/lite/api_docs/cc/class/tflite/interpreter) | An interpreter for a graph of nodes that input and output from tensors. |
| [tflite::InterpreterBuilder](https://tensorflow.google.cn/lite/api_docs/cc/class/tflite/interpreter-builder) | Build an interpreter capable of interpreting `model `.       |
| [tflite::OpResolver](https://tensorflow.google.cn/lite/api_docs/cc/class/tflite/op-resolver) | Abstract interface that returns TfLiteRegistrations given op codes or custom op names. |

# person detection例子

总体从流程上使用上还是比较简单的。

都是公式化的调用。

但是涉及的概念值得了解一下。



## 参考资料

tensorflow之神经网络层：AveragePooling2D、average_pooling2d、Conv2D和conv2d

https://blog.csdn.net/u013230189/article/details/82771622

# 参考资料

1、教程丨基于 TensorFlow Lite Micro 和 Arduino 的视觉分类和识别

https://zhuanlan.zhihu.com/p/337050133

2、太牛逼了，应用TinyML（嵌入式机器学习库）10分钟就可以在Arduino开发板上实现咳嗽检测

https://zhuanlan.zhihu.com/p/145846470

3、

https://zhuanlan.zhihu.com/p/74085789

4、

https://cloud.tencent.com/developer/article/1778813