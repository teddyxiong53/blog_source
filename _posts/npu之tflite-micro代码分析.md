---
title: npu之tflite-micro代码分析
date: 2021-10-20 16:40:33
tags:
	- npu

---

--

不管业务逻辑是怎么写的，这个简单实用的C++用法也是值得学习的。

把代码文件分布，画了一个思维导图在这里：

https://naotu.baidu.com/file/c28951134d080676d6bef364ce640ab7



schema_generated.h内容分析

```
先是一些这些的结构体声明
struct Tensor;
struct TensorT;

struct Conv2DOptions;
struct Conv2DOptionsT;

enum BuiltinOperator

一些这样的模板。
template<> struct BuiltinOptionsTraits<tflite::AddOptions> {
  static const BuiltinOptions enum_value = BuiltinOptions_AddOptions;
};

支持的激活函数
enum ActivationFunctionType

```

subgraph是什么？





TensorFlow lite的高效，体现在对模型进行了精简，并且基于移动平台对神经网络的计算过程组了基于指令集和硬件的加速。



# 模型的输入输出数据的确定

就以官方的例子来分析。

## HelloWorld

输入是什么？kXrange是2*pi。大概6.28 。position是0到1之间的一个小数。

```
float x = position * kXrange;
```

所以，输入x是一个浮点数，范围是0到2*pi。

输出y也是一个浮点数，范围是-1到1。

输入怎么给到模型？

因为模型是8bit的定点模型。

所以不能直接把浮点数x给到模型。

需要先量化一下。就是把浮点转成8bit范围内的整数。

```
int8_t x_quantized = x / input->params.scale + input->params.zero_point;
```

input的params是怎么来的呢？

对应的结构体是：

```
typedef struct TfLiteQuantizationParams {
  float scale;
  int32_t zero_point;
} TfLiteQuantizationParams;
```

计算公式是这样：

```
real_value = scale * (quantized_value - zero_point)
```

scale和zero_point是不是模型里就确定了的？我不用管，直接拿来用就可以了？

应该就是模型量化的时候就自动确定了的。

反正记住量化公式这么写就对了。

```
int8_t x_quantized = x / input->params.scale + input->params.zero_point;
```

然后这样把数据给到输入。

```
input->data.int8[0] = x_quantized;
```

input和output都是Tensor指针

```
TfLiteTensor* input = nullptr;
TfLiteTensor* output = nullptr;
```

这样来拿到指针

```
input = interpreter->input(0);
output = interpreter->output(0);
```

Input(0)和output(0)的0，都是index参数。

可以是其他值吗？

有点确认。先保留疑问。

调用模型进行预测

```
TfLiteStatus invoke_status = interpreter->Invoke();
```

返回成功或者失败。

从output里拿到输出

```
int8_t y_quantized = output->data.int8[0];
```

拿到的是量化后的，所以需要用公式转一下。

```
float y = (y_quantized - output->params.zero_point) * output->params.scale;
```

主要input的params和output的params是不同的。

这个完全可以理解，就是因为二者的范围都是不同的。



kTensorArenaSize 这个值是怎么确定的？

magic_wand的是60K。

而HelloWorld的是2K。

可能是逐步缩减测试出来的吧。复杂的用的就多，简单的用的就少。

是经验值吧。

到论坛上提问看看。



## magic_wand

这个是手势识别的。

这个目前只看到拿到input指针的。

```
model_input = interpreter->input(0);
```

看到这里，有必要把Tensor的结构体的成员梳理一下了。

主要的内容，如下图所示。

![image-20211029145932210](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20211029145932210.png)

这里获取到input，还进行了一下分析

```
if ((model_input->dims->size != 4) || (model_input->dims->data[0] != 1) ||
      (model_input->dims->data[1] != 128) ||
      (model_input->dims->data[2] != kChannelNumber) ||
      (model_input->type != kTfLiteFloat32)) {
```

维度要是4，且是`1*128*3`的。

这个在setup的时候，还有一个

```
TfLiteStatus setup_status = SetupAccelerometer(error_reporter);
```

这个设置加速器是做什么？

实际函数是空函数。直接返回0了。

这个是浮点的方式的了。input数据是这样填充的。input是model_input->data.f

```
for (int i = 0; i < length; ++i) input[i] = 0;
```

然后直接调用：

```
interpreter->Invoke();
```

输出是拿的这个：`interpreter->output(0)->data.f`

## micro_speech

这个拿到的input

```
model_input = interpreter->input(0);
  if ((model_input->dims->size != 2) || (model_input->dims->data[0] != 1) ||
      (model_input->dims->data[1] !=
       (kFeatureSliceCount * kFeatureSliceSize)) ||
      (model_input->type != kTfLiteInt8)) {
```

要是2维的。而且是int8类型的。

模型的数据指针：

```
model_input_buffer = model_input->data.int8;
```

在loop里，先把音频转成feature数据，在把feature数据传递给input的buffer。

```
  for (int i = 0; i < kFeatureElementCount; i++) {
    model_input_buffer[i] = feature_buffer[i];
  }
```

然后调用：

```
interpreter->Invoke();
```

拿到输出指针

```
TfLiteTensor* output = interpreter->output(0);
```

这样拿到输出的数据

```
previous_results_.push_back({current_time_ms, latest_results->data.int8});
```

这样处理得分

```
for (int i = 0; i < kCategoryCount; ++i) {
      if (offset == 0) {
        average_scores[i] = scores[i] + 128;
      } else {
        average_scores[i] += scores[i] + 128;
      }
    }
```

看命令是哪个

```
*found_command = current_top_label;
```

还是要重点分析一下声音的采集和特征提取怎么做的。

以arduino的为分析对象。

看audio_provider.cc的内容

```
#define DEFAULT_PDM_BUFFER_SIZE 512 //这个是arduino的sdk里定义的。
然后input的buffer_size是512*16，uint16_t类型
相当于可以放16个数据包。
output的buffer_size是512 uint16

```

录音数据是用这个函数读取进来的。

```
PDM.read(g_audio_capture_buffer + capture_index, DEFAULT_PDM_BUFFER_SIZE);
```



```
LatestAudioTimestamp  这个时间戳，是从0开始的毫秒。
```

PopulateFeatureData

```
输入参数：
	上次的时间戳
	当前的时间戳
输出参数：
	有多少片数据
处理逻辑：
	一个stride是20ms。
	1、把上次时间戳和当前时间戳，除以20，得到step值。
	2、然后得到slice_needed = 当前step - 上次step
	3、如果是第一次运行
		初始化特征
			这里就涉及到microfrontend目录下的一些东西，再后面描述。
```



microfrontend的东西

```
struct FrontendConfig {
  struct WindowConfig window;
  struct FilterbankConfig filterbank;
  struct NoiseReductionConfig noise_reduction;
  struct PcanGainControlConfig pcan_gain_control;
  struct LogScaleConfig log_scale;
};
```



看懂这个特征提取的代码，可能对后面我的工作有帮助。

因为也是需要做这个的。

### microfrontend

这个从字面是怎么理解？

应该就是前端处理。例如音频数据的特征提取，就是一种前端处理。

这里都是一些C函数，虽然写在cpp文件里。但是没有用namespace和class包装。

有个readme进行说明。

原始音频输入预计为 16 位 PCM 功能，具有可配置的采样率。 

更具体地说，音频信号经过预加重过滤器（可选）；

 然后被切成（可能重叠）帧和窗口函数应用于每一帧； 

之后，我们做一个傅立叶对每一帧进行变换（或更具体地说是短时傅立叶变换）并计算功率谱；

 然后计算滤波器组。

默认情况下，库配置了一组默认值来执行不同的处理任务。



在上面的例子中需要注意的是，前端消耗了尽可能多的从音频数据中生成单个特征向量所需的样本（根据到前端配置）。 

如果没有足够的样本可用于生成一个特征向量，返回的大小将为 0，值指针将为`空`。

frontend_main.cc 及其中提供了如何使用前端的示例frontend_main。

 此示例需要包含“int16”的文件的路径PCM 功能的采样率为 16KHz，

执行时将打印输出根据前端默认配置的系数。



### 把microfrontend库扒出来

这个可以拉出来单独用。不要跟tflite-micro深度绑定了。

依赖了kiss_fft这个第三方库。

我给系统安装一下就好了。后面集成到buildroot里，也是先编译kissfft。没有必要打包进来。

现在是可以编译运行，但是测试结果不过。

这整个库，对外提供的接口是啥？

主要实现了什么功能？



封装了kissfft的fft计算接口现在是这样用的。

```
struct FftState state;
FftPopulateState(&state, sizeof(kFakeWindow) / sizeof(kFakeWindow[0])
FftInit(&state);//这个现在是空函数了。
FftCompute(&state, kFakeWindow, kScaleShift);
```

封装也很浅，因为这个就已经很直观了。没什么太多可以搞的东西。



## person_detect

前面没有什么特别的。

这样来处理输出。

```
  TfLiteTensor* output = interpreter->output(0);

  // Process the inference results.
  int8_t person_score = output->data.uint8[kPersonIndex];
  int8_t no_person_score = output->data.uint8[kNotAPersonIndex];
  RespondToDetection(error_reporter, person_score, no_person_score);
```



参考资料

1、TensorFlow lite 深度解析 笔记

https://zhuanlan.zhihu.com/p/156861036