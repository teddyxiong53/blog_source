---
title: npu之speechbrain
date: 2021-10-21 15:46:33
tags:
	- npu

---

--

Spearmbrain是基于Pytorch的开源和一体化语音工具包。

目标是创建一个灵活和用户友好的工具包，

可用于轻松开发最先进的语音技术，

包括语音识别，扬声器识别，语音增强，多麦克风信号处理系统和很多其他的。

目前处于Beta版本

# 关键特性

提供了各种有用的工具，来加速语音相关技术的开发，包括：

1、集成到HuggingFace数据集里的预训练模型。没有集成进去的部分，就放到了google drive上。

2、brain class。一个完全可定制的工具，用来管理对数据的训练和评估。帮你处理烦人的细节，同时保持灵活性。

3、基于yml的超参数调整。通过蒸馏基本算法组件，大大简化了代码。

4、可以使用多GPU来训练和预测。

5、使用混合精度来加速训练。

6、透明且完全可定制的数据输入输出pipeline。SpeechBrain跟pytorch载入数据集的风格类似。

# 语音识别

支持最先进的方法，支持端到端的语音识别。

1、支持调优过的wave2vec2.0模型。

2、在多个benchmark上，跟其他的同类toolkit相比，有更好的表现。

3、定制语言模型很简单，包括RNNLM和TransformerLM。

4、混合CTC/Attention端到端的ASR。

5、Transducer端到端ASR，使用一个定制的numba损失函数，用来加速训练。任何其他的encoder和decoder都可以插入到这个Transducer，包括VGG+RNN+DNN和conformer。

6、预训练的ASR模型，用来转录一个音频文件或者特征给下游的模块。

# 特征提取和参数化

# 说话者识别

# 语音翻译

# 语音增强和分离

# 多mic处理

# 性能

在不同的数据集上的测试表现。

# 文档和教程

SpeechBrain是用来加速语音技术的开发的。

提供了3种不同层级的文档

1、底层的。

2、函数级别的。

3、教程级别的。

# 安装

```
pip install speechbrain
```

https://speechbrain.github.io/tutorial_basics.html



文件夹说明

speechbrain：主要代码

recipes：训练脚本。

samples：一个简单的数据集。

test：单元测试和集成测试。

# 可以用SpeechBrain做什么

声音分类

声音增强

语音识别



参考资料

1、

https://github.com/speechbrain/speechbrain