---
title: npu之tflite
date: 2021-09-15 13:29:33
tags:
	- npu

---

--

# ubuntu下编译

在ubuntu下编译使用tflite。

```
git clone https://github.com/tensorflow/tensorflow.git 
```

然后执行：

```
cd tensorflow
mkdir build
cd build
cmake ../tensorflow/lite/ # 这一步会进行依赖的编译，所以很慢。我在服务器上都编译了好久。
```

然后在build目录下，再次执行cmake。

```
cmake --build . -j
```

上面这个，编译得到的是静态库文件libtensorflow-lite.a。里面包含了177个o文件。

如果要编译benchmark

```
cmake --build . -j -t benchmark_model
```

如果编译一个例子

```
cmake --build . -j -t label_image
```





创建一个使用了tflite的cmake项目工程

以minimal为例，需要这样来写CMakeLists.txt。

```
cmake_minimum_required(VERSION 3.16)
project(minimal C CXX)

set(TENSORFLOW_SOURCE_DIR "" CACHE PATH
  "Directory that contains the TensorFlow project" )
if(NOT TENSORFLOW_SOURCE_DIR)
  get_filename_component(TENSORFLOW_SOURCE_DIR
    "${CMAKE_CURRENT_LIST_DIR}/../../../../" ABSOLUTE)
endif()

add_subdirectory(
  "${TENSORFLOW_SOURCE_DIR}/tensorflow/lite"
  "${CMAKE_CURRENT_BINARY_DIR}/tensorflow-lite" EXCLUDE_FROM_ALL)

add_executable(minimal minimal.cc)
target_link_libraries(minimal tensorflow-lite)
```



要编译得到C API的库

```
cmake ../tensorflow_src/tensorflow/lite/c
cmake --build . -j
```



# benchmark_model

这个作用是什么？怎么用？

是用来测试模型的性能的。

模型的性能用什么数据来描述？



```
benchmark_model \
  --graph=your_model.tflite \
  --num_threads=4
```

我就用我下载的speech_command的模型来测试一下。

```
./tools/benchmark/benchmark_model --graph=/home/hanliang.xiong/work/test/tensorflow-test/conv_actions_tflite/conv_actions_frozen.tflite
```

从打印看，就是测量预测时间，消耗的内存。

benchmark_model相当于静态的可执行程序，大小在5M左右。

# label_image测试

在lite/examples下，就这么几个例子。

```
android  experimental_new_converter  ios  label_image  minimal  python
```

看起来label_image的算是一个比较好运行的例子。

编译：

```
cmake --build . -j`nproc` -t label_image
```

下载依赖的模型文件。

```
# Get model
curl https://storage.googleapis.com/download.tensorflow.org/models/mobilenet_v1_2018_02_22/mobilenet_v1_1.0_224.tgz | tar xzv -C /tmp

# Get labels
curl https://storage.googleapis.com/download.tensorflow.org/models/mobilenet_v1_1.0_224_frozen.tgz  | tar xzv -C /tmp  mobilenet_v1_1.0_224/labels.txt

mv /tmp/mobilenet_v1_1.0_224/labels.txt /tmp/
```

模型文件有90M，为什么这么大？

因为下面有多个后缀的模型文件。

labels.txt里，是1000种label。

```
0:background
1:tench, Tinca tinca
2:goldfish, Carassius auratus
3:great white shark, white shark, man-eater, man-eating shark, Carcharodon carcharias
4:tiger shark, Galeocerdo cuvieri
5:hammerhead, hammerhead shark
6:electric ray, crampfish, numbfish, torpedo
7:stingray
8:cock
9:hen
```

运行

```
./examples/label_image/label_image \
  --tflite_model /home/hanliang.xiong/work/test/tensorflow-test/mobilenet_v1_1.0_224.tflite \
  --labels /home/hanliang.xiong/work/test/tensorflow-test/labels.txt \
  --image ../tensorflow/lite/examples/label_image/testdata/grace_hopper.bmp
```

输出如下：

```
INFO: Loaded model /home/hanliang.xiong/work/test/tensorflow-test/mobilenet_v1_1.0_224.tflite
INFO: resolved reporter
INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
INFO: invoked
INFO: average time: 53.252 ms
INFO: 0.860174: 653 653:military uniform
INFO: 0.0481019: 907 907:Windsor tie
INFO: 0.00786707: 466 466:bulletproof vest
INFO: 0.00644937: 514 514:cornet, horn, trumpet, trump
INFO: 0.00608026: 543 543:drumstick
```

这个是从图片里分析出来的东西。

我另外换一张图片看看。我用了一张有几个人的图片。结果就出错了。

```
INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
ERROR: /home/hanliang.xiong/work/test/tensorflow-test/tensorflow/tensorflow/lite/core/subgraph.cc BytesRequired number of elements overflowed.

Segmentation fault
```

我再换了一张只有2个人的图片，还是一样的错误。

是因为图片的尺寸问题？

我看看最开始那张图片的尺寸。是512x600的。

我把这个图片拷贝一个，把尺寸改大一点看看。

果然就出错了。

不是，是我把格式也改了导致的。

我把格式改回bmp的。也不会挂掉。

代码里是这样处理图片的。

```
  int image_width = 224;
  int image_height = 224;
  int image_channels = 3;
  std::vector<uint8_t> in = read_bmp(settings->input_bmp_name, &image_width,
                                     &image_height, &image_channels, settings);
```

我之前给的图片都是jpg的。所以出错。

改成bmp的就正常了。

# minimal

这个是最小例子。

编译：

```
cmake --build . -j -t minimal
```

这样编译居然不行。

必须另外弄一个build目录来完整编译一遍。算了，先不编译了。



# examples分析

看https://github.com/tensorflow/examples/tree/master/lite/examples 这个目录下。

## digit_classifier

就是mnist的例子。

安卓app的例子是手写一个数字然后识别出来。

## gesture_classification

就是用摄像头来识别姿势。

## 声音分类

## 语音命令

就是yes、no、up那些单词的。

从这里下载模型。

https://storage.googleapis.com/download.tensorflow.org/models/tflite/conv_actions_tflite.zip

下载的模型，有一个tflite文件，一个txt文件，txt文件里就是yes、no这些单词。

```
_silence_
_unknown_
yes
no
up
down
left
right
on
off
stop
go
```





参考资料

1、

https://www.tensorflow.org/lite/guide/build_cmake