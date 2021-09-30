---
title: npu之sed声音事件检测
date: 2021-09-22 14:49:33
tags:
	- npu

---

--



# 基本信息

机器将声音信号转化为有意义的信息的过程被称为 computational auditory scene analysis（CASS）。

CASS有很多相关的任务，比如声音场景识别，声音事件识别与声音分离。

这三个任务难度从易到难。

声音场景识别：通过声音判别场景，在办公室，饭店或者火车上

声音事件识别（SED）：通过单独的声音事件的音频，检测并判断到事件

声音分离：从混合的声音信号（含有多个声音事件）的音频中分理出单个的声音事件

这三个任务是互相关联的

SED有两个方面：分类和定位，即我们需要识别事件的种类以及决定事件的开始和结束时间。

声音事件可以根据多种方面划分：

1.他们的来源不同和他们的来源是否在移动：人，动物，机器，自然等等

2.他们的声音特征不同：分为音调的（在频谱中有特定的峰，比如警报）和像噪音的（在频谱有持续时间长并且频率广的带（band），如加油声）

3.他们的时序表现不同：分为短暂声音事件（通常短于一秒钟，如枪声），长时间声音事件（在这之中，又分为静态的，如引擎声，和动态的频率特征变化的，如音乐），间歇声音事件（在一个短的时间间隔中重复发生）



SED应用的价值：

给电视的内容自动生成字幕来便利听觉障碍的人群

可以用作监视目的，如在医院中检测是否有人跌落楼梯等

给网络上的视频加标签（metadata）来方便搜索



SED难点：

1.时序特征（The temporal features）和频率特征（The spectral features）具有多样的变化性，因此事件之间会在时间上重叠。也因此。SED系统分为单调的（在一个时间点只识别一个事件）和复调的（在一个时间点识别多个事件）

2.数据的缺少，数据集时间短，基本只有弱标注的数据



1.传统的非深度学习的工作

2.深度学习的工作

a.利用CNN来识别频谱，表现胜过了传统的工作。

b.CNN只能关注部分的信息，决定很受限，于是提出用RNN来处理。即使有些事件很快就会结束，但是RNN可以提供他们背景的信息。

c.结合CNN和RNN。CNN可以更好的学习指定部分的数据，RNN可以同时利用短时间和长时间的信息



所谓「声音事件」，指的是像猫叫狗叫、风声雨声这样的声音，

当然人的说话声以及音乐声也算。

声音事件检测，就是给出一段录音后，确定其中包含哪些声音事件（tagging），

以及每个事件的起止时间（localization）。

声音事件检测有很多用途，比如可以辅助识别用户上传的视频的内容，便于检索；

也可以作为语音识别的预处理，过滤掉非语音的内容。

既然要检测事件的起止时间，那么**理想的训练数据**，就应该也标注了每个事件的起止时间。

**然而进行这样的「强标注」是一件特别麻烦的事情，**

也正是因为如此，声音事件检测领域长期没有足够的训练数据，一直发展不起来。

为了突破这一限制，人们开始研究怎么用「**弱标注**」的训练数据来做声音事件检测。

2017 年 3 月，Google 公布了一个叫做 [Audio Set](https://link.zhihu.com/?target=https%3A//research.google.com/audioset/) 的数据集，含有 8 个月的弱标注数据，

一下子把 SED 这个领域带火了起来。



我的博士课题，就研究了两种「弱标注」数据。

第一种标注是最弱的：

它只告诉你一段训练数据中有哪些事件，但没有任何关于事件起止时间的信息。

比如，它只告诉你一段录音中有狗叫和说话声，但你并不知道谁先谁后，还是二者重叠。

这种标注我称为「**有无标注**」（presence/absence labeling），它也是 Audio Set 提供的标注形式。

第二种标注稍微强一点，

它告诉你各个事件发生的顺序（因为事件可能重叠，事实上知道的是事件边界——即起止点——的顺序），但不知道边界的具体时间。

这种标注我称为「**顺序标注**」（sequential labeling）。



用「有无标注」来做声音事件检测，

一般作为一个**多实例学习**（multiple instance learning，MIL）的二分类（binary classification）问题来处理。

「多实例学习」是指，每个训练样本的正负是未知的，样本被划分成多个「包」（bag），我只知道每个「包」的正负。

如果包是负的，则其中的样本都是负的；

但如果包是正的，则只说明其中至少有一个样本是正的。

在声音事件检测中，对于每一种事件，我们可以把一整条录音看成一个包，其中的每一帧看成一个样本，这就转化成一个 MIL 问题了。

MIL 问题的一种通用解法是：

用一个模型预测出每个样本为正的概率，然后用一个**聚合函数**（pooling function）把它们转换成每个包为正的概率，使之与包的标注差别尽可能小。





https://github.com/yinkalario/General-Purpose-Sound-Recognition-Demo

这里有个图形界面的声音事件检测demo。

是用pyaudio录音来进行预测的。

# ubicoustics

```
git clone https://github.com/FIGLAB/ubicoustics.git
pip install numpy==1.14.1 tensorflow==1.5.0 keras==2.1.6 wget
```

执行：

```
python example_fileprediction_simple.py
```

就会自动下载800M左右的模型。模型放在这里。

https://www.dropbox.com/s/cq1d7uqg0l28211/example_model.hdf5

但是跑不起来。是utf8解码有问题。

readme要求的就是3.6，我安装但也是3.6的。

但是keras里对str使用了decode('utf8')。

网上搜索了一下，这里找到答案。

https://blog.csdn.net/lidichengfo0412/article/details/109516612

只需要把h5py降级到2.10.0，就可以正常运行了。

pyaudio的callback回调周期是多长时间？

回调函数的参数是这样，只要有数据，就会去调用。

```
 callback(<input_data>, <frame_count>, <time_info>, <status_flag>)
```

注意要选择default这个声卡，其余都会报错。

# Sound_event_detection

https://github.com/Kikyo-16/Sound_event_detection

这个是dcase 2018和2019的代码。

Specialized Decision Surface and Disentangled Feature for Weakly-Supervised Polyphonic Sound Event Detection

Specialized Decision Surface：缩写为SDS。怎么理解？可以翻译为专业决策面。

Disentangled Feature：解开特征。不知道怎么理解。

需要在data目录下新建wav和feature这2个目录。

从DCASE网站下载音频文件并放到wav目录下。

要使用还比较麻烦。



# BirdVoxDetect

这个看readme，是说用来做航班电话的检测和分类的。

https://github.com/BirdVox/birdvoxdetect

是一个预训练的系统。

直接pip就可以安装使用。



# dnd-sed

https://github.com/dr-costas/dnd-sed

这个需要自己下载数据集进行训练。

不知道要训练多久。

数据集的下载网页找不到了。



# DcaseNet

https://github.com/Jungjee/DcaseNet

训练需要使用NVIDIA的GPU。

下载DCASE task1a、task2、task3的数据。

修改train.sh里的参数然后执行。

后面可以看看。



# denet

https://github.com/MiviaLab/DENet

这里提到几个数据集和几个网络。可以了解一下。

只给出了layers代码，没有给出训练和推理代码。

## MIVIA音频事件数据集

https://mivia.unisa.it/datasets/audio-analysis/mivia-audio-events/

MIVIA 音频事件数据集由总共 6000 个用于监控应用的事件组成，即玻璃破碎、枪声和尖叫声。 

6000 个事件分为训练集（由 4200 个事件组成）和测试集（由 1800 个事件组成）。

以 32000 Hz 采样并以每个 PCM 样本 16 位量化。音频剪辑作为 WAV 文件分发。训练集的持续时间约为 20 小时，而测试集的持续时间约为 9 小时。

## MIVIA road audio events data set

https://mivia.unisa.it/datasets/audio-analysis/mivia-road-audio-events-data-set/

以 32000 Hz 采样并以每个 PCM 样本 16 位量化。音频剪辑作为 WAV 文件分发。

含多个时长约 1 分钟的音频文件，其中一系列危险事件叠加在典型的道路背景声音中。每个音频文件都有不同的背景声音，因此可以模拟几种不同的真实情况。

感兴趣的事件分为两类（车祸和轮胎打滑）



参考资料

1、CMU Sound Event Detection Thesis总结

https://zhuanlan.zhihu.com/p/69560501

2、

https://www.zhihu.com/question/309785896/answer/583985814

3、

https://zhuanlan.zhihu.com/p/373295853

4、

https://zhuanlan.zhihu.com/p/343528946