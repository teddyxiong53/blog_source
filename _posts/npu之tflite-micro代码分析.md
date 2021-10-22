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

参考资料

1、TensorFlow lite 深度解析 笔记

https://zhuanlan.zhihu.com/p/156861036