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

# examples在pc上运行测试

https://github.com/OAID/Tengine/tree/tengine-lite/examples

## 分类任务

运行 MobileNet v1 分类网络模型

输入是一张图片，输出是标签。

需要准备的东西：模型，图片。

可执行程序是tm_classification，模型是mobilenet_ssd.tmfile。

运行：

```
./build/install/bin/tm_classification -m models/mobilenet.tmfile -i cat.jpg
```

这个运行看不出效果。

参考资料

https://blog.csdn.net/mzpmzk/article/details/82976871

## 人脸关键点检测

landmark

需要模型文件和图片。

运行：

```
./build/install/bin/tm_landmark -m models/landmark.tmfile -i images/mobileface02.jpg 
```

这个可以看到效果。

输出landmark_out.jpg



## ssd目标检测

```
./build/install/bin/tm_mobilenet_ssd -m ./models/mobilenet_ssd.tmfile -i ./images/ssd_dog.jpg 
```

是把图片里的物体用矩形框起来。

输出mobilenet_ssd_out.jpg

## 人脸检测

运行：

```
./build/install/bin/tm_retinaface -m ./models/retinaface.tmfile -i ./images/mtcnn_face4.jpg 
```

输出retinaface_out.jpg

是所有的人脸被矩形框柱。

## yolact实体分割

这个模型很大。为了加快下载速度，我们使用量化过的版本。

没有量化的，140M。量化后的，35M。

## unet图像分割

这个也使用量化后的版本。

## yolov3

还是用狗和自行车的那张图片。区别在于还把百分比给画到图片上了。

模型也是特别大。还是用量化后的版本。

```

```

## yolov4-tiny

## yolov5s

## nanodet

## efficientdet

这些都是狗和自行车的图片。

## openpose

人体姿态检测。

## hrnet

人体姿态。

## 汉字识别





# 实际例子



https://tengine-docs.readthedocs.io/zh_CN/latest/source_compile/deploy_SuperEdge.html

案例基于开源AI推理框架Tengine 实现

**容器调用边缘硬件NPU资源，**

完成高效物体检测的推理任务，

并通过开源边缘容器方案 SuperEdge 轻松将应用调度到边缘计算节点，

实现一条指令部署边缘计算跨平台AI应用案例。

[SuperEdge](https://github.com/superedge/superedge) 是基于原生 Kubernetes 的**边缘容器**管理系统。

该系统把云原生能力扩展到**边缘侧**，

很好的实现了云端对边缘端的**管理**和控制，

极大**简化**了应用从云端部署到边缘端的过程。

SuperEdge 为应用实现**边缘原生化**提供了**强有力**的支持。

SuperEdge项目由以下公司共同发起：腾讯、Intel、VMware、虎牙直播、寒武纪、首都在线和美团。

## 硬件环境准备

| 物品         | 描述                                                         |
| ------------ | ------------------------------------------------------------ |
| Master服务器 | SuperEdge Master 服务器， 用于应用调度，可采用X86 or Arm 架构，本例中采用X86服务器 |
| Khadas VIM3  | 应用负载工作节点，内置 A311D SoC 的单板计算机，内置 5Tops NPU 加速器，各大商城有售 |
| USB 摄像头   | 连接Khadas VIM3，输入实时视频流                              |
| 液晶显示器   | 连接Khadas VIM3，控制台操作，实时输出示例运行结果            |
| HDMI连接线   | 由于Khadas VIM3 的 TYPE C 接口与 HDMI 接口过于紧凑，需要寻找小一点接口的 HMD |





# TensorFlow怎么对接到Tengine

Tengine是一个推理引擎，

可以适应TensorFlow的model来进行推理。

那跟直接使用TensorFlow在板端进行推理，有哪些不同？Tengine的价值体现在哪里？

提供了多种model的对接，比TensorFlow通用性更好一点？

提供了对NPU的支持。

# 移植到C305X

ldd查看可执行程序的依赖：

```
linux-vdso.so.1 =>  (0x00007fffb1f19000)
        libtengine-lite.so => ./build/install/lib/libtengine-lite.so (0x00007fa6ead2e000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007fa6eaa25000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fa6ea65b000)
        libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007fa6ea457000)
        libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007fa6ea23a000)
        libOpenVX.so.1 => not found
        libgomp.so.1 => /usr/lib/x86_64-linux-gnu/libgomp.so.1 (0x00007fa6ea018000)
        libstdc++.so.6 => /usr/lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007fa6e9c96000)
        libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007fa6e9a80000)
        /lib64/ld-linux-x86-64.so.2 (0x00007fa6eb4bc000)
```

我当前板端是有openvx的库的。所以适合采用这种方式。

```
第三种是不进行集成编译，指定 CMake 选项 -DTENGINE_ENABLE_TIM_VX_INTEGRATION=OFF，TIM-VX 编译为单独的 libtim-vx.so，编译完成后，libtegine-lite.so 依赖 libtim-vx.so，libtim-vx.so 依赖其他的用户态驱动 libCLC.so 等一系列 so。
```

```
gcc-linaro-7.3.1-2018.05-x86_64_aarch64-linux-gnu.tar.xz
```

需要先把这个编译过程理清楚。

关键是链接是怎么做的。

把cmake文件看了一遍。

tim-vx编译得到的是什么？

看看tim-vx下面的内容。

```
├── Android.mk
├── BUILD
├── cmake 下面有一个A311D.cmake的文件。
├── CMakeLists.txt
├── docs
├── include：60多个头文件。
├── LICENSE
├── prebuilt-sdk：下面主要是x86_64_linux这个目录，libGAL.so这些库文件和头文件。
├── README.md
├── samples：一些测试程序。
├── src：有1000多个文件。
├── toolchains：有gcc-linaro-7.3.1-2018.05-x86_64_aarch64-linux-gnu。
├── VERSION：当前版本1.1.32
└── WORKSPACE
```

prebuilt-sdk下面的库

```
├── lib
│   ├── libArchModelSw.so
│   ├── libCLC.so
│   ├── libEmulator.so
│   ├── libGAL.so
│   ├── libNNArchPerf.so
│   ├── libOpenVXC.so
│   ├── libOpenVX.so -> libOpenVX.so.1.3.0
│   ├── libOpenVX.so.1 -> libOpenVX.so.1.3.0
│   ├── libOpenVX.so.1.3.0
│   ├── libOpenVXU.so
│   ├── libvdtproxy.so
│   └── libVSC.so
```



而我们当前的buildroot里有什么？

```
└── lib64
    ├── libArchModelSw.so
    ├── libGAL.so
    ├── libNNArchPerf.so
    ├── libOpenCL.so
    ├── libOpenVX.so
    ├── libOpenVXU.so
    ├── libovxlib.so
    └── libVSC_Lite.so
```

略有不同。应该可以运行吧。

从这里下载这个压缩包，10M大的。里面应该就是这些so文件和头文件。

https://github.com/VeriSilicon/TIM-VX/releases/download/v1.1.28/aarch64_A311D_D312513_A294074_R311680_T312233_O312045.tgz
我应该不需要这些，但是我要看看目录结构是怎么样的。

就是这样的：

```
.
├── include
│   ├── CL
│   │   └── cl_viv_vx_ext.h
│   └── VX
│       ├── viv_nn_compatibility.h
│       ├── vx_api.h
│       ├── vx_compatibility.h
│       ├── vx_ext_program.h
│       ├── vx_ext_target.h
│       ├── vx.h
│       ├── vx_helper.h
│       ├── vx_import.h
│       ├── vx_kernels.h
│       ├── vx_khr_cnn.h
│       ├── vx_khr_compatible.h
│       ├── vx_khr_dot.h
│       ├── vx_khr_icd.h
│       ├── vx_khr_import_kernel.h
│       ├── vx_khr_interp.h
│       ├── vx_khr_ix.h
│       ├── vx_khr_nn.h
│       ├── vx_khr_nn_internal.h
│       ├── vx_khr_node_memory.h
│       ├── vx_khr_opencl.h
│       ├── vx_khr_tiling.h
│       ├── vx_khr_variants.h
│       ├── vx_khr_xml.h
│       ├── vx_lib_debug.h
│       ├── vx_lib_extras.h
│       ├── vx_lib_xyz.h
│       ├── vx_nodes.h
│       ├── vx_types.h
│       ├── vxu.h
│       ├── vx_vendors.h
│       └── vx_viv_sys.h
└── lib
    └── x86_64
        ├── libArchModelSw.so
        ├── libCLC.so
        ├── libEmulator.so
        ├── libGAL.so
        ├── libNNArchPerf.so
        ├── libOpenVXC.so
        ├── libOpenVX.so -> libOpenVX.so.1.3.0
        ├── libOpenVX.so.1 -> libOpenVX.so.1.3.0
        ├── libOpenVX.so.1.3.0
        ├── libOpenVXU.so
        ├── libvdtproxy.so
        └── libVSC.so
```

npu当前是怎么被编译的？

通过npu.mk里调用aml_buildroot.sh来编译的。

include对应到buildroot那边的hardware/aml-4.9/npu/nanoq/sdk/inc目录。

lib目录对应到hardware/aml-4.9/npu/nanoq/sharelib/lib64

我就手动把这些内容拷贝过来。

看吧到tengine-lite的3party/tim-vx/include和lib/aarch64目录下。

然后我这样来编译：

```
$ cd <tengine-lite-root-dir>
$ mkdir build && cd build
$ cmake -DTENGINE_ENABLE_TIM_VX=ON -DCMAKE_SYSTEM_NAME=Linux -DCMAKE_SYSTEM_PROCESSOR=aarch64 -DCMAKE_C_COMPILER=/mnt/nfsroot/hanliang.xiong/work/npu-test/output/c2_af400_a64_release/host/bin/aarch64-linux-gnu-gcc -DCMAKE_CXX_COMPILER=/mnt/nfsroot/hanliang.xiong/work/npu-test/output/c2_af400_a64_release/host/bin/aarch64-linux-gnu-g++ ..
$ make -j`nproc` && make install
```

执行cmake报错。

```
CMake Error at source/device/tim-vx/CMakeLists.txt:79 (MESSAGE):
  Tengine: TIM-VX source was not found.  Please read
  doc/npu_tim-vx_user_manual.md for more info.
```

是要执行这个。

```
cp -rf ../TIM-VX/include  ./source/device/tim-vx/
cp -rf ../TIM-VX/src      ./source/device/tim-vx/
```

编译最后链接报错。

```
cannot find -lCLC
cannot find -lVSC
```

这个我当前确实没有放进去。

那就从下载的A311D的压缩包里取出来放进去。

现在编译出来了。

把内容推送到板端。

运行还报了libgomp库找不到的错误。我搜索了一下buildroot，找到了这个文件，推送到板端。就可以运行了。

但是运行landmark，出了段错误。

```
/data/tengine # ./tm_landmark -m ./landmark.tmfile -i mobileface02.jpg
tengine-lite library version: 1.5-dev
Repeat [1] min 83.251 ms, max 83.251 ms, avg 83.251 ms
Segmentation fault
```

是出错在这里

```
Thread 2 "tm_landmark" received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0x7ff5fc4160 (LWP 30215)]
0x0000007ff634df54 in start_thread () from /lib/libpthread.so.0
(gdb) bt
#0  0x0000007ff634df54 in start_thread () from /lib/libpthread.so.0
#1  0x0000007ff610c3dc in ?? () from /lib/libc.so.6
```

但是图片其实已经出来了。效果是对的。

我还是把libgomp的禁止掉，重新编译一个看看。

cmake的时候，加上：

```
-DTENGINE_OPENMP=OFF
```

再运行。还是报错。但是错误不一样了。

```
start_thread: Assertion `freesize < pd->stackblock_size' failed.
```

运行timvx版本的

```
 ./tm_landmark_timvx  -m ./landmark.tmfile -i mobileface02.jpg
```

报错又不一样。

```
/data/tengine # ./tm_landmark_timvx  -m ./landmark.tmfile -i mobileface02.jpg
tengine-lite library version: 1.5-dev
Tengine: Size of tensor != size of buffer(248832 vs 62208).
Set input tensor buffer failed
```

timvx搭配uint8的model运行，错误又不一样。

```
/data/tengine # ./tm_landmark_timvx  -m ./landmark_uint8.tmfile -i mobileface02.
jpg
tengine-lite library version: 1.5-dev
Repeat [1] min 3.120 ms, max 3.120 ms, avg 3.120 ms
tm_landmark_timvx: pthread_create.c:554: start_thread: Assertion `freesize < pd->stackblock_size' failed.
Aborted
```

那么我把所有的动态库都替换为从github上下在的A311D的看看。

这样情况就更糟糕了。直接导致系统都重启了。

是导致内核出错了。

我先把后面放入的so文件都删除掉。运行命令，查看gal的中断，并没有一个中断产生。

说明工作并不正常。

难度是ko文件版本不匹配导致的？

我替换ko文件看看。insmod失败。

```
/data/tengine # insmod ./lib/galcore.ko
insmod: can't insert './lib/galcore.ko': invalid module format
```

串口打印

```
[  558.249448@0] galcore: no symbol version for module_layout
[  558.249612@0] galcore: module PLT section(s) missing
[  558.285823@0] galcore: module PLT section(s) missing
```

应该是ko跟内核不匹配导致的。

那么就是不能正常移植到C305X上了。

timvx版本的，是uint8的数据，应该要配合uint8的模型来使用的。



# 在MCU上的使用

https://mp.weixin.qq.com/s/w1aUR6nnR8XBOsHtC30-2w



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