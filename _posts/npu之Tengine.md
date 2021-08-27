---
title: npu之Tengine
date: 2021-08-18 17:27:33
tags:
	- npu

---

--

就从Tengine来入门npu的使用。

https://github.com/OAID/Tengine

根据这个readme的内容来编译，先在ubuntu的笔记本上跑起来先。

新建一个tengine-test目录，都在这个目录下存在。

先下载TIM-VX的代码

```
git clone https://github.com/VeriSilicon/TIM-VX.git
```



下载tengine的代码

```
git clone https://github.com/OAID/Tengine.git  tengine-lite
```

Tengine-Lite 支持三种 TIM-VX 的集成编译方法，具体如下：

> 第一种是将 TIM-VX 代码主要部分包含在 Tengine-Lite 的代码里，一并编译，最后得到单一 libtengine-lite.so，该 so 依赖 libCLC.so 等一系列 so；

我们就用这种方法。

TIM-VX 提供了在 x86_64 宿主系统上的预编译依赖库，

此部分依赖库可以在没有 NPU 的情况下，

在 PC 上进行算法的开发和验证，

其功能和板卡中是一致的，

精度因计算路径区别略有影响但不影响验证。

然后我们就把TIM-VX的代码拷贝到tengine的指定目录下。

```
cd tengine-lite
cp -rf ../TIM-VX/include  ./source/device/tim-vx/
cp -rf ../TIM-VX/src      ./source/device/tim-vx/
```

还有一些第三方的代码也要拷贝进来编译

```
cd tengine-lite
mkdir -p ./3rdparty/tim-vx/include
mkdir -p ./3rdparty/tim-vx/lib/x86_64
cp -rf ../TIM-VX/prebuilt-sdk/x86_64_linux/include/* ./3rdparty/tim-vx/include/
cp -rf ../TIM-VX/prebuilt-sdk/x86_64_linux/lib/*     ./3rdparty/tim-vx/lib/x86_64/
```

执行编译

```
cd tengine-lite
mkdir build && cd build
cmake -DTENGINE_ENABLE_TIM_VX=ON ..
make -j`nproc` && make install
```

编译后install的目录如下：

```
hanliang.xiong@walle01-sz:~/work/test/tengine-test/tengine-lite/build/install$ tree
.
├── bin
│   ├── tm_classification
│   ├── tm_classification_int8
│   ├── tm_classification_timvx
│   ├── tm_classification_uint8
│   ├── tm_efficientdet
│   ├── tm_efficientdet_uint8
│   ├── tm_landmark
│   ├── tm_landmark_timvx
│   ├── tm_landmark_uint8
│   ├── tm_mobilefacenet
│   ├── tm_mobilefacenet_uint8
│   ├── tm_mobilenet_ssd
│   ├── tm_mobilenet_ssd_uint8
│   ├── tm_retinaface
│   ├── tm_ultraface
│   ├── tm_yolofastest
│   └── tm_yolov5
├── include
│   └── tengine
│       ├── c_api.h
│       ├── defines.h
│       └── timvx_device.h
└── lib
    ├── libtengine-lite.so
    └── libtengine-lite-static.a
```

运行一下bin下面的测试程序看看。

```
export LD_LIBRARY_PATH=./3rdparty/tim-vx/lib/x86_64:./build/install/lib
```

执行一下

```
hanliang.xiong@walle01-sz:~/work/test/tengine-test/tengine-lite$ ./build/install/bin/tm_landmark
Error: Tengine model file not specified!
[Usage]:  [-h]
    [-m model_file] [-i image_file] [-r repeat_count] [-t thread_count]
```

不知道tm_landmark是要做什么。

需要指定一个model文件。

在benchmark/models目录下，默认放了一些模型文件。

```
googlenet_benchmark.tmfile
inception_v3_benchmark.tmfile
mobilefacenets_benchmark.tmfile
mobilenet_benchmark.tmfile
mobilenet_v2_benchmark.tmfile
mobilenet_v3_benchmark.tmfile
mssd_benchmark.tmfile
resnet18_benchmark.tmfile
resnet50_benchmark.tmfile
retinaface_benchmark.tmfile
shufflenet_v2_benchmark.tmfile
squeezenet_v1.1_benchmark.tmfile
vgg16_benchmark.tmfile
yolov3_tiny_benchmark.tmfile
```

执行：

```
./build/benchmark/tm_benchmark -r 5 -t 1 -p 0
```

提示模型找不到，就把模型拷贝到当前目录下。

```
cp benchmark/models ./ -rf
```

执行打印

```
Tengine benchmark:
  loops:    5
  threads:  1
  cluster:  0
  affinity: 0xFFFFFFFF
Tengine-lite library version: 1.5-dev
     squeezenet_v1.1  min =   19.67 ms   max =   35.14 ms   avg =   27.04 ms
         mobilenetv1  min =   27.85 ms   max =   45.32 ms   avg =   33.53 ms
         mobilenetv2  min =   28.49 ms   max =   29.93 ms   avg =   28.79 ms
         mobilenetv3  min =   30.02 ms   max =   30.12 ms   avg =   30.06 ms
        shufflenetv2  min =    9.24 ms   max =   11.70 ms   avg =    9.97 ms
            resnet18  min =   66.35 ms   max =   79.15 ms   avg =   69.42 ms
            resnet50  min =  134.31 ms   max =  134.90 ms   avg =  134.68 ms
           googlenet  min =  104.89 ms   max =  105.67 ms   avg =  105.16 ms
         inceptionv3  min =  237.00 ms   max =  387.32 ms   avg =  268.05 ms
               vgg16  min =  446.27 ms   max =  529.17 ms   avg =  473.46 ms
                mssd  min =   53.20 ms   max =   53.41 ms   avg =   53.28 ms
          retinaface  min =   12.00 ms   max =   12.27 ms   avg =   12.09 ms
         yolov3_tiny  min =  113.66 ms   max =  144.74 ms   avg =  123.09 ms
      mobilefacenets  min =   13.05 ms   max =   13.07 ms   avg =   13.06 ms
ALL TEST DONE.
```

examples有多个实用的例子。

都是用图片作为输入的，进行标定等操作输出。对硬件没有依赖。

不过对应的模型和图片素材要从百度网盘上下载下来。

tengine的模型格式是tmfile，TensorFlow、pytorch等的模型格式需要经过转换才能使用。

当前用的是tim-vx（跟TensorFlow是并列关系）作为后端的。

tim-vx是针对npu的，但是可以用CPU来模拟运行。



重新设计的设计目标之一是，采用纯 `C` 设计 **Tengine** 的 **Lite** 分支(以下简称 **Tengine**，不再强调 **Lite** 分支)最小 `Runtime`，复杂的功能和逻辑可以使用 `C++` 开发。这样保持纯 `C Runtime` 在局限场景下优势的同时，使用 `C++` 开发复杂模块，使注意力集中在开发算法本身上。



# TensorFlow怎么对接到Tengine

Tengine是一个推理引擎，

可以适应TensorFlow的model来进行推理。

那跟直接使用TensorFlow在板端进行推理，有哪些不同？Tengine的价值体现在哪里？

提供了多种model的对接，比TensorFlow通用性更好一点？

提供了对NPU的支持。



# 参考资料

1、Tengine的TIM-VX后端试用以及踩坑

https://zhuanlan.zhihu.com/p/386386554

2、Amlogic T962芯片简介

http://www.scensmart.com/general-description-of-soc/amlogic-t962/

3、Tengine Lite with VeriSilicon TIM-VX User Manual

参考这个来进行编译模拟。

https://github.com/OAID/Tengine/blob/tengine-lite/doc/npu_tim-vx_user_manual_zh.md

4、官方文档

https://tengine-docs.readthedocs.io/zh_CN/latest/