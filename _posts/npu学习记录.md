---
title: npu学习记录
date: 2021-08-24 14:11:33
tags:
	- npu

---

--

[TOC]

为了更好地梳理自己的思路，决定把学习过程记录下来。

# 8月24日之前

1、看了TensorFlow的入门知识，在google colab上把HelloWorld跟着做了一遍。

2、对keras基本概念过了一下。

3、下载了tflite-micro的代码，把HelloWorld的代码看了一下，了解了基本流程。

4、对于训练和预测的基本流程有了解了。

5、了解了TinyML的概念，这个是我们要应用的场景。

当前对概念的理解还不深入。

# 8月24日

1、看下面这个系列文章

https://blog.csdn.net/abc13526222160/article/details/101938410

2、看到第二篇，觉得需要先看一下keras的。

3、然后看到知乎上对CS231n课程的笔记。看了前面2篇的，暂时不要深入下去。

https://zhuanlan.zhihu.com/p/20900216

这个笔记属于《智能单元》这个专栏的。顺便把这个专栏的文章看一下。

4、觉得这个网站的文章不错

http://www.uml.org.cn/ai/201907173.asp

5、这个代码，是通过用usb把手机连接到电脑，在电脑上执行python脚本，通过AI来玩微信跳一跳游戏的。代码不多，就120行代码左右。是使用torch来做的。

通过截图分析再执行的步骤来玩的。

https://github.com/floodsung/wechat_jump_end_to_end

这个是讲解原理的知乎文章，还有配套的几个训练的仓库。

https://zhuanlan.zhihu.com/p/32819519

6、B站上有CS231n的视频

https://search.bilibili.com/all?keyword=CS231n&from_source=video_tag

7、还是回到第一步的系列文章。

把30篇左右的文章过了一遍。公式类的都没有看，因为看不懂。

后面可以继续回过头来看这个。

8、再看看tengine这个做了什么。能不能在x86上跑起来看看效果。

可以在x86上模拟使用。先集中精力看看这个。

9、看百度的飞桨平台，这里倒是罗列了不少的应用场景，可以学习一下。

https://baike.baidu.com/item/%E9%A3%9E%E6%A1%A8/23472642?fromtitle=PaddlePaddle&fromid=20110894&fr=aladdin

是一个类似谷歌TensorFlow的东西。

# 8月25日

1、看一下yolo的概念。

2、复习一下高数常用符号

https://wenku.baidu.com/view/c3adfd4e49649b6648d747c3.html

3、了解一下loss函数。

4、重新看keras的官方文档。

5、面向初学者的最小神经网络。这篇很有启发性。这个作者orDream的博客翻看一下。

https://blog.csdn.net/orDream/article/details/106343076

这个收集了常用的数据集。很全面，非常好。

https://blog.csdn.net/orDream/article/details/91606597

6、了解lenet。这个切入点非常好，把相关的知识点进行发散，找不到不少的资料。

https://www.jianshu.com/p/cd73bc979ba9

7、下面这篇文章里有不少的高明见解，值得多看看。

如何理解卷积神经网络（CNN）中的卷积和池化？

https://www.zhihu.com/question/49376084

8、这篇文章列举了所有的神经网络结构，非常好。并给出了keras的实现

https://www.cnblogs.com/skyfsm/p/8451834.html

9、这里有个吴恩达的课程的笔记。

https://github.com/SSQ/Coursera-Ng-Convolutional-Neural-Networks

github上的lenet-5主题，有不少有价值的东西。

https://github.com/topics/lenet-5

了解到kaggle这个数据科学竞赛平台，注册一下。

10、发现这个网站，里面资料也比较系统，把网站浏览一遍。

https://tensornews.cn/

11、TensorFlow中文资源网站

http://www.tensorflow123.com/

https://panchuang.net/

12、这些例子讲了TF的api的用法。

https://github.com/aymericdamien/TensorFlow-Examples

13、还是回到中文官网把例子直接跑ipynb文件，不自己手写了。

https://tensorflow.google.cn/

把所有的例子都执行了一遍。

14、还是回到keras的官网教程继续看。

15、GX8010 国芯的产品，看看这个开发介绍，有用到NPU。用到了TF，可以看看。

http://ai.nationalchip.com/docs/gx8010/

关键就是一个工具，把TF的模型转换一下格式，让NPU可以识别使用。

那么amlogic应该也是类似的思路，对应的转换工具是哪个？

有，下面就是工具的说明文档，用法还比较复杂。

https://doc.amlogic.com/file/detail?type=1&id=16726

RK的NPU模型转换

https://wiki.t-firefly.com/ROC-RK3568-PC/usage_npu.html

了解了一下caffe。说这个代码设计比较清晰，适合阅读和修改。

16、以“TensorFlow NPU”为关键字进行百度，浏览文章，看到这篇。

两套系统接口调用_《TensorFlow 内核剖析》笔记——系统架构

比较复杂，后面再看。

https://blog.csdn.net/weixin_33158363/article/details/113365924

机器学习性能提升480倍！Arm推最新Cortex-M处理器，搭首款microNPU

https://zhidx.com/p/192645.html

# 8月26日

1、今天打算看一下caffe的相关知识。在京东读书上搜索caffe。找到一本书《深度学习：21天实战caffe》。看到里面提到这个论坛，http://caffecn.cn/，先浏览一下。

从这个论坛也可以看出，caffe已经被放弃，很久没有人发帖了。不过作为学习原理的材料，还是可以的。

快速把书浏览了一遍，代码截图比较多。

京东读书上就这一本caffe的书是vip免费的。caffe的了解到此为止。

2、继续随意搜索流量。发现这个工具，可以解析model里包含的layer信息。

https://github.com/lutzroeder/netron

3、看看tflite-micro跟arm-nn的对接。

https://blog.csdn.net/a845414332/article/details/102718813

4、搜索树莓派GPU关键字。找到这篇文章。但是有点太难了。先不细看了。

https://petewarden.com/2014/08/07/how-to-optimize-raspberry-pi-code-using-its-gpu/

5、回过头看arm-nn。这个在amlogic的NPU方案里，怎么被使用的？

https://confluence.amlogic.com/display/SW/armnn

这里有提到。npu可以作为arm-nn的backend之一。

armnn类似一个中间件，前端是各种开源framework(tf,tflite,caffe)的parser，后端是各种硬件加速模块。这么说amlogic-nn也是跟arm-nn类似的东西，如果没有特殊的NPU，中间件就没有必要存在，TensorFlow直接就跟CPU或者GPU打交道。

6、搜索一下cnn语音识别。

TensorFlow唤醒词

https://blog.csdn.net/u010514105/article/details/99227361

这篇文章提供了唤醒词的模型算法。了解一下就可以了。

7、把tflite集成到buildroot里，在板端运行一下看看。

搜索树莓派TensorFlowLite

# 8月27日

1、在ubuntu下编译stm32f4的tflite-micro。分析编译过程。

tflite-micro的Makefile写得比较复杂，值得学习一下，可以适应非常多的环境，也可以生成各种ide的工程。

2、看tflite-micro的代码，搜索里面的关键结构体。找到这篇文章，这个系列分析不错。

TensorFlow技术内幕（五）：核心概念的实现分析

https://blog.csdn.net/gaofeipaopaotang/article/details/80598840

这个也不错。

tensorflow 19： tflite 概念理解

https://blog.csdn.net/yuanlulu/article/details/84063503

案例分享| 有道云笔记是如何使用TensorFlow Lite的？

https://blog.csdn.net/weixin_36841920/article/details/80376141

【移动端DL框架】当前主流的移动端深度学习框架一览

这篇文章的后面，有一个速成系列，写得不错。可以直观地看出不同的框架的使用上的特点。

https://zhuanlan.zhihu.com/p/67117914

tensorflow案例：一步一个脚印

这个系列文章，也是作者的学习笔记

https://blog.csdn.net/yuanlulu/category_9272622.html

这个是龙曲良的开源电子书，从ppt看起来还不错。

https://github.com/dragen1860/Deep-Learning-with-TensorFlow-book

3、把TensorFlow的api，在官网都浏览一遍，这样可以快速建立全局性的认识。

https://www.tensorflow.org/api_docs/python/tf/audio

在audio部分的例子，了解到yamnet这个

https://discuss.tf.wiki/t/topic/1337

4、鉴于TF的API比较多，而且版本变动比较大。我还是先从keras的api入手。

初学者的8个项目

https://elitedatascience.com/machine-learning-projects-for-beginners

Keras极简入门教程，这篇文章非常好，讲得非常到位，每一行代码的参数都解释了。

https://www.jianshu.com/p/132746857e3a

各层之间叠加，就像叠乐高。

5、还是把easy12306的代码再看看。这个是keras的小的实用的真实应用，可以了解keras可以帮我们做一些什么。

卷积神经网络VGG16详解，这篇文章讲到很多基础概念。

https://baijiahao.baidu.com/s?id=1667221544796169037&wfr=spider&for=pc

keras中文文档不错，讲解比较详细。

https://keras-cn.readthedocs.io/en/latest/getting_started/functional_API/

# 8月30日

1、打算了解一下tflite-micro的内置算子。

找到了这篇：

【手撕 - 深度学习】TF Lite 魔改：添加自定义 op

https://blog.csdn.net/qq_28739605/article/details/104212509



https://www.cnblogs.com/vitoyeah/p/10273299.html

https://discuss.tf.wiki/t/topic/1407

Tflite在端侧CPU/GPU上运行全过程（一）

https://zhuanlan.zhihu.com/p/183135939

深入理解TensorFlow中的tf.metrics算子

https://zhuanlan.zhihu.com/p/42438077

如何理解TensorFlow计算图？

这篇文章很好，作者还围绕着对话系统有2个github仓库，一个是研究记录，一个是代码，值得一读。

https://zhuanlan.zhihu.com/p/344846077

在知乎上搜索TensorFlow文章，浏览一下。

感觉谷歌确实在tf的接口设计上有各种反复横跳。导致了较大的混乱。

然后TensorFlow里面的子项目也是分分合合。

从我开发的深度学习框架看深度学习这几年：TensorFlow, PaddlePaddle（飞桨）, 无量

这个讲了框架的开发历史。

https://zhuanlan.zhihu.com/p/363271864



https://zhuanlan.zhihu.com/p/103049619

我有个大的疑问，训练模型，调参都是调哪些参数？具体是在做什么？

**这篇文章不错，引用的连接值得一看。**

https://blog.csdn.net/gdh756462786/article/details/79214099

《从入门到精通：卷积神经网络初学者指南》这篇文章非常好，帮我解答了很多的疑问。讲得非常浅显易懂。

Micheal Nielsen 的 「神经网络与深度学习（ Neural Networks and Deep Learning）」一书。我强烈推荐这本书。这本书可免费在线浏览：http://neuralnetworksanddeeplearning.com/）

觉得有必要把机器学习和深度学习了解一下。

搜索知乎上看看。



https://zhuanlan.zhihu.com/p/27018536



机器之心
深度学习大讲堂
李宏毅的教授，台湾大学讲机器学习



https://github.com/exacity/deeplearningbook-chinese

又搜索到几个新的概念。

完全解析RNN, Seq2Seq, Attention注意力机制

https://zhuanlan.zhihu.com/p/51383402

主流的深度学习模型有哪些？

https://zhuanlan.zhihu.com/p/29769502

这里列举了一下keras相关的资源，有模仿AlphaGo的。

https://github.com/fchollet/keras-resources



https://zhuanlan.zhihu.com/p/392435330

人工智能实战入门

https://baijiahao.baidu.com/s?id=1708508846118264313

# 8月31日

1、在csdn里搜索“深度学习”。找到这个网站。不错。

https://easyai.tech/ai-definition/

**2、吴恩达老师深度学习课程完整笔记**

**这个非常好。很多概念都涉及到了**

https://blog.csdn.net/wuzhongqiang/article/details/89702268

数学符号，这里可以参考查阅。说实话，很多都忘了。

https://baike.baidu.com/item/%E6%95%B0%E5%AD%A6%E7%AC%A6%E5%8F%B7/685756?fr=aladdin

Keras学习笔记(一)： Application 各model参数及应用

https://blog.csdn.net/XM_no_homework/article/details/89813367

还是看keras英文文档。把文档过了一遍。

https://keras.io/

谷歌搜索“keras aiot”。

找到这个。

https://www.emqx.com/zh/blog/emqx-and-1d-cnn-in-aiot

搜索“cnn树莓派”

这里有不少有趣的项目。

https://oldpan.me/ai-funny-news

《用树莓派4b构建深度学习应用》这个系列不错。

https://segmentfault.com/u/bluishfish

《Python深度学习》这个是keras的作者写的一本书，是很经典的一本书。

python深度学习——案例讲解

https://blog.csdn.net/weixin_40856057/article/details/90271194

想办法用keras搭建一个问答系统。

https://jishuin.proginn.com/p/763bfbd39e3f

**《美团机器学习实践》**

这本书讲述了机器学习的一些实践。

也不是层数越多越好。层数多了，可能出现过拟合，反而准确度会下降。



# 9月1日

1、今天把概念梳理一下，用自问自答的方式。想办法把概念解释清楚。

发现这个网站不错。ev表示Explained Visually。用视觉化的方式来进行解释。

https://setosa.io/ev/

深入学习卷积神经网络中卷积层和池化层的意义

这篇比较非常好。

https://www.cnblogs.com/wj-1314/p/9593364.html

**这个作者的博客很有体系。而且还有配套的B站视频。很好。**

https://blog.csdn.net/weixin_44791964/category_9408229.html

把上面这个博客都浏览了一遍。



https://github.com/PacktPublishing/Deep-Learning-with-Keras

可以搜索“用keras实现”

Deep-Learning-with-Keras 这本书很不错。

这个仓库，都是一些CNN 应用，不错。

https://github.com/TannerGilbert/Tutorials

# 9月2日

1、把kaggle的引导教程跟着走了一遍，对kaggle的流程有了了解。

2、看到使用了sklearn的东西，这个就涉及到很多的统计学知识，让我有点畏惧。涉及的数学知识点有点多。

3、有个疑问，这些网络层数为什么要这么安排？依据是什么？

我可以随意增减吗？

深度学习炼丹术 —— 与神经网络的初次邂逅：熟悉基本结构、设计和实现

https://www.zybuluo.com/tianxingjian/note/1286468

是属于这个作者的文章

https://blog.csdn.net/python__boy/category_10558794.html

李航——《统计学习方法》

《深度学习入门：基于Python的理论与实现》这本书很好。

# 9月3日

1、发现packt的github仓库非常丰富。而且关于深度学习的就不少。

https://github.com/orgs/PacktPublishing/repositories?q=deep&type=&language=&sort=

可以浏览一遍。

这个里面的实际项目，都是用的resnet来做。

https://github.com/PacktPublishing/Deep-Learning-with-Real-World-Projects

了解到mlflow这个管理平台。

2、我觉得需要了解各种场景的网络模型的用途。

**深度学习500问。从readme也可以看到，需要下载到本地来阅读。需要把typora的公式相关的设置一下。这个非常不错。整个结构非常好。很全面，各个方面的都涉及到了。值得多看看。**

https://github.com/jiajunhua/scutan90-DeepLearning-500-questions



https://github.com/PacktPublishing/Advanced-Deep-Learning-with-Keras

看看怎么对cnn模型进行微调。



看乐鑫实现了一个自己的离线语音引擎。可以支持100种左右的命令。我觉得这个非常实用。

全志有个R329，

R329的两大主要特点就是高算力与低功耗。其中高算力的部分，也更多涉及到了DSP与NPU。

NPU：周易 AIPU，800MHz， 0.256T；

发现极术社区这个网站。

https://aijishu.com/

cnn在音频分类上的应用

**基于CNN和LightGBM的环境声音分类，这篇论文很不错啊。把很多概念都串起来了。**

https://www.hanspub.org/journal/PaperInformation.aspx?paperID=32564

继续在hanspub.org上搜索“cnn声音”相关的论文。

https://www.hanspub.org/journal/Articles.aspx?searchCode=cnn%e5%a3%b0%e9%9f%b3&searchField=All&page=1

# 9月6日

1、在github上搜索“keras crack”。

找到这个：

https://github.com/senliuy/12306_crack

这个仓库，是对深度学习相关知识进行图表化，非常好。

**https://github.com/senliuy/AlphaTree-graphic-deep-neural-network**

AI千集，这个不错。

https://aiqianji.com/

这里搜集了不少的ai应用仓库。

https://aiqianji.com/explore/repos

AI 100天计划

https://github.com/weslynn/100-Days-Of-AI-Code

本计划分八个板块。以基础为主。想要对深度学习有个整个了解的，可以按顺序全刷　

－A　深度学习基础 －B　轻量级网络和大型网络 －C　物体检测 －D　物体分割 －E　人脸，文字的检测与识别 －F　肢体识别 －G　GAN基础 －H　GAN应用

类似的100天的学习项目，国外的先有的。

最近听说国外网红程序员Avik Jain的[机器学习100天](https://github.com/Avik-Jain/100-Days-Of-ML-Code)项目,神奇之余又激起了我想学习下的欲望。

https://github.com/Avik-Jain/100-Days-Of-ML-Code

居然还配套了中文版。

https://github.com/Avik-Jain/100-Days-of-ML-Code-Chinese-Version

学习过程是这样的：

1、数据预处理。

2、简单线性回归

3、多元线性回归。

4-6、逻辑回归。

7、K近邻法。

8、逻辑回归背后的数学。

9、支持向量机。

10、支持向量机和K近邻法。

11、K近邻法。

12-14、支持向量机。

15、朴素贝叶斯分类器和黑盒机器学习。

16、通过内核机器实现支持向量机。



这个是基于keras的一个库，对音频进行预处理的。

https://github.com/keunwoochoi/kapre

还是把这个的代码看一遍。

https://github.com/PacktPublishing/Advanced-Deep-Learning-with-Keras

对应的pdf文件也找到了。

这个的数据，尽量都是用mnist来做所有的实验，另外还有cifar10的。

但是讨论的题目大多数是跟GAN相关的。

当前我还用不上这个。先放过吧。

我当前还是找比较实用的代码看看。

这个是基于web的DL应用。可以看看。

https://github.com/PacktPublishing/Hands-On-Python-Deep-Learning-for-Web

基于flask、express的都有。

autoKeras。了解一下。

https://github.com/PacktPublishing/Automated-Machine-Learning-with-AutoKeras



https://github.com/PacktPublishing/Hands-On-Machine-Learning-using-JavaScript

把pytorch看一下。

https://github.com/PacktPublishing/PyTorch-Computer-Vision-Cookbook

了解到fastai。

https://github.com/PacktPublishing/Deep-Learning-with-fastai-Cookbook

这个作者在打kaggle比赛，可以看看他的这些博客。

https://www.jianshu.com/u/bbff6dea2496

深度学习调试技巧汇总

https://www.jianshu.com/p/e9e6d8db9f6f

# 9月7日

现在把重点放到板端。

编译C305X的镜像进行测试。



# 9月8日

现在把音频的分类理清楚。

这里有不少相关的知识。

https://www.zhihu.com/column/c_1299144188903120896



https://blog.csdn.net/wherewegogo/article/details/110369729

datafountain，国内的大数据竞赛网站。注册一下。

https://www.datafountain.cn/competitions/486

了解陆天奇，他开发的xgboost。这个在kaggle里使用了。

华盛顿大学计算机系博士生，此前毕业于上海交通大学ACM班。XGBoost、cxxnet等著名机器学习工具的作者，MXNet的主要贡献者之一。

了解到Baseline的概念

https://www.zhihu.com/question/313705075

把librosa研究一下，这个是分析音频用的一个库。

在C305X的板端把人脸识别的例子运行起来了。



# 9月9日

今天考虑一下音频识别的基础知识。

这个讲了一下sklearn的一些实用知识。

https://blog.csdn.net/u014248127/category_7189276.html

这个仓库不错。

https://github.com/ageron/handson-ml

把这篇博客及关联文章看了，大概明白了音频数据是怎么处理的了。

https://blog.csdn.net/wherewegogo/article/details/110369729

搜索一下fastai音频分类。

看见声音

https://zhuanlan.zhihu.com/p/113387375

这个fastai帖子收集了不少的音频分析资源。

https://forums.fast.ai/t/deep-learning-with-audio-thread/38123



https://medium.com/@ageitgey/machine-learning-is-fun-part-6-how-to-do-speech-recognition-with-deep-learning-28293c162f7a

# 9月10日

先把芯片npu的文档看看。

想办法自己找个模型转一下然后使用看看效果。

看看能不能把tengine编译到板端运行。

把tengine的所有例子在pc上跑了一下。

# 9月13日

今天先是尝试在板端运行tengine。

虽然可以跑起来，但是有段错误。也查不出哪里导致的问题。

因为代码多且复杂。而且有很多不开源的。

然后试了一下tengine的。

跟timvx一起的版本，也不能正常工作。

# 9月14日

现在领导给了方向，就围绕着NN在智能音箱的各个环节的应用为研究方向。

总共5个环节：唤醒、VAD、ASR、NLP、TTS。

最极致的用法就是完全在本地实现智能音箱的功能。

研究重点还是边缘计算。

首先从唤醒入手。

tflite-micro的micro_speech是个可以研究的对象。

我一直有的疑问就是数据取长时间的刚好可以足够识别，有能保证速度和准确性？

搜索到这个博客，很专业，专注音频开发的。

https://www.cnblogs.com/talkaudiodev/

我有一个疑问，唤醒词跟ASR的边界是什么？

ASR不是简单的分类任务。

我觉得可以看一下esp的命令词。

https://github.com/espressif/esp-skainet/blob/master/README_cn.md

目前支持唤醒词识别和命令词识别。

自定义唤醒词的流程。

https://github.com/espressif/esp-sr/blob/master/wake_word_engine/%E4%B9%90%E9%91%AB%E8%AF%AD%E9%9F%B3%E5%94%A4%E9%86%92%E8%AF%8D%E5%AE%9A%E5%88%B6%E6%B5%81%E7%A8%8B.md

我要想办法实现一个类似乐鑫wakenet的东西。

这篇文章对智能音箱的流程讲得比较好。

http://www.woshipm.com/ai/4144034.html

这个产品经理的6篇文章质量都不错。

http://www.woshipm.com/u/844241

这篇文章全面系统。值得一读。

https://wqw547243068.github.io/2020/09/17/voice-detection/

# 9月15日

我还是把注意力集中在TensorFlow上。

搜索“TensorFlow vad”。



这个kaggle代码，里面是一些对音频的处理。

https://www.kaggle.com/davids1992/speech-representation-and-data-exploration?scriptVersionId=1924001

这本在线书籍，很全面，讲音频技术的。

https://shichaog1.gitbooks.io/hand-book-of-speech-enhancement-and-recognition/content/chapter7.html

yamnet系列文章

https://blog.csdn.net/search_129_hr/category_11201015.html

把tflite编译了，运行末benchmark_model和label_image。把板端运行的梳理了一下。

搜索“tflite rpi speech command”

这里有个例子，把“stop”当成唤醒词的。在树莓派上运行的。

https://github.com/ShawnHymel/tflite-speech-recognition

用keras训练得到h5模型，转成tflite模型。

就是在音频回调函数里，每500ms调用一次。

```
word_threshold = 0.5
rec_duration = 0.5
```

就用mfcc的来做的。

在arduino上识别yesno。

https://create.arduino.cc/projecthub/superboys/wake-word-detection-43843a

我估计乐鑫的命令词也是根据谷歌的speech command来的。

就是自己用语料训练了模型而已。

micro_speech和speech_command的网络结构分别是怎样的？

micro_speech就是在speech_command里挑了2个单词而已。就这样。

How to train new TensorFlow Lite micro speech models

https://learn.adafruit.com/how-to-train-new-tensorflow-lite-micro-speech-models?view=all

https://github.com/ZhitongYan/Micro-Speech

直接到tfhub.dev上找模型。

想到deep speech，看看这个的用途，找找模型。看看怎么在板端用起来。

百度的 DeepSpeech 就是一个典型的端到端的语音识别框架：

这篇文章提到了不少的模型，值得了解一下。

https://antkillerfarm.github.io/speech/2019/03/01/Deep_ASR_2.html

看一下百度的语音技术相关的文档。

https://ai.baidu.com/ai-doc/SPEECH/tk7h8ya0f

语音识别初探

https://benzblog.site/2019-06-25-%E8%AF%AD%E9%9F%B3%E8%AF%86%E5%88%AB%E5%88%9D%E6%8E%A2/

11516 语音唤醒技术综述

https://zhuanlan.zhihu.com/p/90596982

ASRer

语音相关技术

https://www.zhihu.com/column/c_1241766528963534848

作为中国最大的搜索引擎公司，百度还收集了大量汉语（尤其是普通话）的音频数据，这些都为百度语音识别系统Deep Speech 2技术成果提供了基本的数据优势与支持。

个性化菜谱APP的实现（六） 语音识别功能实现

https://blog.csdn.net/liqiangstartcsdn/article/details/105111620

deepspeech可能是比较适合做理想语音识别吧。

《语音识别基本法》，这本书不错。

http://cslt.riit.tsinghua.edu.cn/mediawiki/images/2/25/Speech_book.pdf



目前一般会从Librispeech数据集开始，960 hours；

Timit数据集相当于CV领域的mnist，有些小的想法可以在这上面先进行验证，看是否work；

imagenet换算成语音大概是4096 hours；

google和facebook在文献中公布的使用语音数据量是1.3w hours，但实际上使用的应该是这个数字的10倍-20倍



https://zhuanlan.zhihu.com/p/131589687

ASRT这个项目。

本项目使用Keras、TensorFlow基于深度卷积神经网络和长短时记忆神经网络、注意力机制以及CTC实现。

当前，最好的模型在测试集上基本能达到80%的汉语拼音正确率

不过由于目前国际和国内的部分团队能做到98%，所以正确率仍有待于进一步提高

史上最全面的AI推理框架对比--OpenVINO、TensorRT、Mediapipe

https://zhuanlan.zhihu.com/p/344442534

迈向语音识别领域的 ImageNet 时刻

https://www.infoq.cn/article/4u58WcFCs0RdpoXev1E2



https://www.infoq.cn/article/lEe6GCRjF1CNToVITvNw

# 9月16日

搜索“边缘计算NLP”

NVIDIA的社区培训。可以看到各种应用场景。

https://www.nvidia.cn/developer/online-training/community-training/

看到openseq2seq这个东西。

基于seq2seq的中文聊天机器人（一）

https://blog.csdn.net/daniellibin/article/details/103290169

这个博客很不错，基于jekyll。评论系统基于github的issue。可以参考这个自己再搭建一次博客系统。

https://antkillerfarm.github.io/



先用开源数据做预训练使模型收敛，再用垂直领域的业务数据做fine-tune

https://taorui-plus.github.io/Chinese-ASR-gitbook/deepspeech-enhance/experience.html

看看全志R329的NPU做了哪些应用。

周易NPU的model zoo

https://github.com/Zhouyi-AIPU/Model_zoo

刚好极术社区今晚8点有个周易NPU的直播，报名听一下。

既然收集人工智能模型的一般叫model zoo。那么就搜索一下。

https://github.com/openvinotoolkit/open_model_zoo

极术社区确实挺不错的。这种轻博客网站，技术难度应该不大，难的是持续集聚人气和保证文章的质量。

腾讯的ncnn。是一个推理框架。

# 9月17日

今天就集中搜索model zoo。

这个组织是干啥的？好像不是什么正式组织。

https://github.com/TensorSpeech

提供了TensorFlowTTS和TensorFlowASR这2个仓库。

人气还可以。最近也还在更新。

是一个越南人在主导的项目。

发现nemo里有不少的模型。都梳理出来看看。

这里查看模型。模型格式是pytorch的。

https://ngc.nvidia.com/catalog/models/nvidia:nemospeechmodels

这就很全面了。

NeMo Speech Models include speech recognition, command recognition, speaker identification, speaker verification and voice activity detection. These models are used for Automatic Speech Recognition (ASR) and sub-tasks.

玩PyTorch？你不得不看的PyTorch资源大列表

https://blog.csdn.net/DBC_121/article/details/104578647



https://modelzoo.co/

WaveNet和Tacotron比较

https://becominghuman.ai/into-a-better-speech-synthesis-technology-29411b64f2a2?gi=3dc90159b870



https://heartbeat.fritz.ai/a-2019-guide-to-speech-synthesis-with-deep-learning-630afcafb9dd

wavernn

https://zhuanlan.zhihu.com/p/105788551

这个是语音合成的专栏。

https://www.zhihu.com/column/speech-synthesis

预训练模型+finetune的模式是否应用到ASR-语音识别领域，如果应用到了，目前ASR有哪些效果很棒的预训练模型呢？

https://www.zhihu.com/question/470641780/answer/1993620048



近几年ASR任务也逐渐采用端到端范式，模型架构从早期基于RNN到目前基于Transformer的编码器-解码器架构，性能相比之前有了很大提升。

目前的预训练方法普遍采用预训练特征提取器或编码器的方式，通过海量的无标注音频进行学习，取得了非常明显的效果。

# 9月18日

今天把tts的模型demo跑一下。

谷歌“NPU唤醒词”。找到一些有意思的内容。

从gx8010的npu的部分，看到提供了一个这样的pb文件
kws_i320_norm_cnn32_lstm96x2_with_ckpt.pb
这个从名字看，就是唤醒词，lstm模型。
集成了两颗用于语音识别的神经网络处理器（NPU），可运行TensorFlow模型，
实现激活词识别、语音识别、语音合成等深度神经网络算法；
这个是在国芯的板子上跑mnist的例子。
https://github.com/NationalChip/gxDNN
经深圳湾确认，Xiaomi Sound 采用的是全志 R329 芯片，这是去年 3 月发布的一款 AI 语音专用芯片，它搭载了 Arm 中国全新的 AI 处理器——周易 AIPU。
基于这款芯片强大的 AI 算力，Xiaomi Sound 就可以实现每秒 330 次的动态计算，针对不同的音乐曲风，做到实时计算调音，让每种类型的音乐在聆听时都更具特色。
最多可以实现 8 台音箱的互连，让音乐在房间的每一个角落自然地流动。
此次 Xiaomi Sound 还推出了家庭传声的功能，即广播功能，可以实现多台音箱之间的对讲，同时也支持音箱与手机、电视等设备的对讲功能。

典型的应用场景：当你放着音乐，在房间里码字时，从 Xiaomi Sound 传来妈妈喊你吃饭的提醒声，而这个声音，可能就来自客厅里的另一台 Xiaomi Sound 或是妈妈的手机。
我们在上一篇文章已经展示了苹果如何基于 UWB 超宽频技术，实现 iPhone 与 HomePod mini 的音乐接力。

如今，小米也将这一技术应用在了 Xiaomi Sound 上。当手机靠近音箱时，可以将手机上播放的音乐无缝传递至音箱，在音箱上开启播放。而手机再次靠近音箱时，还可以将音乐回传至手机。

AI芯片选型
http://aiiaorg.cn/uploadfile/2020/0730/20200730030838762.pdf

1.Toybrick 算力棒，算力卡；
2.致远电子 M1808 工业 AI 板；
3.点创 ADAS/DSM 设备；
4.动作识别智能摄像头

周易人工智能平台软件框架Tengine。Tengine是目前Arm平台上最快最好用的AI部署框架。同时周易大赛推荐使用EAIDK作为比赛硬件平台。

国产离线语音识别芯片对比
https://zhuanlan.zhihu.com/p/166078186

台湾 新塘\凌阳
围绕着台湾赛维的算法，几年前以新塘为首的台湾MCU厂家，大力推广离线语音识别，新塘ISD9160更是号称出货10kkpcs，国内外各大家电均有大力尝试推广，然而受限於技术，识别效果无法令消费者满意，导致退货率居高不下，厂商损失惨重，离线语音识别技术成为诸多老板和高管的雷区。
在家电以外，台湾系的语音识别，以低廉的价格和支持多国语言等特性，几乎垄断语音玩具行业。玩具消费者，对于识别率的要求比较宽容。

在线语音识别巨头：科大讯飞、思必驰、云知声
三家在线语音识别巨头，纷纷从云端落地到线下，利用成熟的识别算法技术优势，进一步下沉到端侧的离线语音识别芯片，打通线上和线下。三家各自市场侧重点都不同，讯飞侧重教育行业、思必驰侧重车载行业、云之声侧重家电行业，当然这个划分也非绝对，各自肯定有交叉竞争关系。
另外，讯飞和思必驰各自收购了芯片设计公司，补足硬件不足。

芯片语音处理核心，多为专用的NPU。同等资源下，NPU算力和能耗比远高于通用DSP。而且该类芯片多具有强大的前端信号处理能力，能真正做到降噪\远场识别等功能。加上持续优化的声学算法模型和语料定制，识别率通常在95%以上，且误识别率更低。

挑剔点四：离线与在线之争。这是目前离线语音面临最大的挑战。

离线比在线的优势点：更安全的隐私保护（离线不会将用户语音上传网络）；开发成本低，无需搭建联网和APP；反应速度及时，在线响应速度取决于用户的网络状态；中小品牌掌控度高，可自行决定命令词，以及实现差异化功能。

在线比离线的优势点：命令词更灵活多样；大厂带货属性强（例如天猫生态）；直接成本低（在线往往通过加蓝牙或WiFi模块实现，成本比语音模块便宜）。

在智能计算/人工智能领域，芯片占整体技术栈价值的40-50%，而在其他领域只占10%以下，这是芯片领域近几十年最大的机会 。
岚正科技推出的离线语音模组，拥有在无网络环境下的开放空间通过本地离线语音功能，实现语音识别、语音文字输出以及语音控制家电产品的能力。

根据市场反馈，用户在使用语音OS产品时，相对不满意的是语音识别准确率即聪明程度，试想一下，不应答的语音模块将会让智能产品的便捷形同虚设。
海凌科HLK-V01语音模块采用CPU+DSP+NPU 三核架构，
内置基于人工智能语音识别算法的NPU硬件加速核，
通过神经网络对音频信号进行训练学习，提高语音信号的识别能力。
DSP优化降噪算法，对接收的语音指令进行降噪和均衡处理，在测试距离6米以内，噪音40dB以下，HLK-V01语音模块语音识别准确率达到100%，在9米的测试范围内，强噪音干扰下也有良好的表现。

中国人工智能产业研究报告（2020）
https://pdf.dfcfw.com/pdf/H3_AP202101071448331621_1.pdf?1610032445000.pdf


离线语音从场景到设备再到芯片，听 5 位行业大佬解读端上 AI 的共性和趋势
https://aijishu.com/a/1060000000108731

Snips 是一个来自法国巴黎的语音助手初创公司，成立于 2013 年。通过 Snips 的离线语音平台，打造可以直接在设备端运行、无需将信息传输到云端的语音助手。这一主打离线操作语音平台也正是 Sonos 收购 Snips 的最重要原因。

思必驰创始人、首席科学家俞凯则认为，近期有关边缘计算的收购案很多，实际上是端上 AI。端上 AI 和边缘计算是两个概念，虽然都不需要经过云端，但边缘计算是在局域网和类局域网的边缘终端上进行的，而苹果和 Sonos 这些消费电子厂商在做的是端上 AI。
各家企业提出的「云+端」是普适的发展线路，云端比较集中，端上比较分散，无论是设备、技术、还是所提供的服务种类。针对端上的普适性语音助手的技术目前还不明确，大公司从布局的角度上，会选择收购小公司，来尽可能覆盖不同的设备场景。
这里还看到一个趋势——数字助理的行业化，是自然而然发生的。就像人类的社会分工，随着物质文明的进步，有专门的人钻研专门的知识。而随着数字助理的发展，也会有针对不同行业和领域的专门分工，有的公司做通用的数字助理，有的则选择垂直领域深钻。

端上语音交互：从云端到芯片，小型化，与业务逻辑深度整合，ASR、TTS、NLP 将成为标配

端上 AI 并不是简单在将云端的技术拿来在端上跑，虽然技术种类并没有区别，但难度更大，比如，端上可以识别语音的范围和种类受限。其次，端上语音 AI 的更新和定制，是要难于云端的，端上的深度学习更难。

梁家恩还指出，当前，离线挑战在于低资源、低功耗情况下保持高性能、低成本，减少环境复杂和模型压缩带来的精度损失。语音成为 IoT 设备的交互标配是大势所趋，边缘计算能力也成为必要条件。

Rokid 副总裁周军认为，随着模型小型化技术的进展，端侧可以用非常小的运算资源运行非常优秀的推理模型。比如在一个 DSP 上跑语音信号处理与多达 50 个离线命令词，噪声下可以达到 90% 以上识别率。

目前，端侧的语音识别（ASR）、语音合成（TTS）、甚至自然语言理解（NLP）占用的内存和运算资源还比较高，这也是创业公司的机会，通过创新的算法、模型设计以及新的芯片架构来解决。

端侧的 AI 训练也将是一个趋势，通过自学习进一步提高智能。此外，除了离线语音，未来也会与离线视觉/图像/环境理解结合，创造出更有意思的产品。

全志科技副总裁陈风则认为，语音识别（ASR）技术在大多数家居场景已经达到了实用程度，短期内再有大幅度提升不太现实，而「人工智障」的问题还有很大的改善空间，因此接下来的提升重点在于语义理解（NLP）。

NLP 的提升需要更高的深度学习算力，这就需要更强算力、更高能耗比的芯片支持。这意味着客户对芯片的深度学习算力、以及能耗比要求，都有了指数级的提升。对于芯片而言，集成音频 DSP 和音频 NPU 的需求已经出现，发展趋势非常明确。

本地 NLP 需要本地 ASR、本地 TTS 以及传统信号处理的配合，才能实现一个完整的端侧语音识别功能，对应芯片的需求就是需要音频 DSP 和音频 NPU 的标配支持。

现在 NPU 市场百花齐放，导致算法公司和客户存在大量的适配和优化工作，NPU 市场现阶段呈现碎片化状态形式。

TensorFlow也有模型库。但是没有音频相关的。

https://github.com/tensorflow/models/tree/master/official

下面这篇文章很不错。

基于端到端深度学习方法的语音唤醒(Keyword Spotting)模型和论文

https://blog.csdn.net/YZhang0108/article/details/105771069

发现heywhale和鲸这个网站，挺不错的。上面有很不错的笔记。

语音识别长篇研究（一）

这个系列似乎不错。

https://zhuanlan.zhihu.com/p/105454729

https://www.zhihu.com/column/c_188282848



https://www.beningo.com/wp-content/uploads/2018/06/MachineLearning_IoT.pdf

# 9月22日

今天还是继续梳理NPU在音频上的应用。

从使用的角度来看是否有可行性。

首先看BERT能不能做一个问答系统。

TensorFlow就有一个官方的BERT例子，运行一下看看。

运行不了，还需要谷歌云计算的资源。看一下代码。

https://colab.research.google.com/github/tensorflow/tpu/blob/master/tools/colab/bert_finetuning_with_cloud_tpus.ipynb#scrollTo=IhdjgZWAZ60C

代码也看不出什么来。

找找手机demo有没有。

这个是用bert对imdb的数据进行情感分析的。

https://www.tensorflow.org/text/tutorials/classify_text_with_bert

这个输入是一些句子，输出其实是二分类的，就是正面或者负面评价。

给的也是概率。

搜索“bert demo”

https://www.jianshu.com/p/3d0bb34c488a

使用预训练语言模型BERT做中文NER尝试，fine - tune BERT模型

自然语言处理（NLP）主要自然语言理解（NLU）和自然语言生成（NLG）。

为了让NLU任务发挥最大的作用，来自纽约大学、华盛顿大学等机构创建了一个多任务的自然语言理解基准和分析平台，也就是GLUE（General Language Understanding Evaluation）。

GLUE包含九项NLU任务，语言均为英语。

GLUE九项任务涉及到自然语言推断、文本蕴含、情感分析、语义相似等多个任务。

**像BERT、XLNet、RoBERTa、ERINE、T5等知名模型都会在此基准上进行测试。**

目前，大家要把预测结果上传到官方的网站上，官方会给出测试的结果。



MRPC(The Microsoft Research Paraphrase Corpus，微软研究院释义语料库)，相似性和释义任务，

是从在线新闻源中自动抽取句子对语料库，

并人工注释句子对中的句子是否在语义上等效。

类别并不平衡，其中68%的正样本，所以遵循常规的做法，报告准确率（accuracy）和F1值。



bert的实际应用场景

最经典的场景，有多分类和二分类，

二分类的典型场景就是垃圾邮件。

多分类的典型场景是情感分类。

传统的方法有tfidf提取特征后用LR做分类，或降维后用GBDT做分类，再后来就是word2vec或fasttext提取embedding后接各种NN网络做分类。

Bert出现后，整个pipeline更简单了，前面挂一个BertMainLayer提取特征，后面拼接不同的网络，训练2到3轮搞定。

这里用Jasper来动态生成youtube的视频的字幕。是把视频转成音频文件先。

https://colab.research.google.com/github/tugstugi/dl-colab-notebooks/blob/master/notebooks/NVidiaJasper.ipynb#scrollTo=3KUlO4oiA8CM



现在看VED的，声音事件检测。我们不是要VAD的，而是要VED的，也可以叫Sound Event Detection。简称SED。

http://dcase.community/challenge2019/task-sound-event-localization-and-detection

在github上搜索“sound event detection”。

从这里又可以看到一下kws的方案。

https://paperswithcode.com/sota/keyword-spotting-on-google-speech-commands

这个网站还是可以搜索到很多想要的东西。

https://paperswithcode.com/

这个是唤醒词相关的。

https://paperswithcode.com/task/keyword-spotting

关于fine tune的认识

https://www.cnblogs.com/andre-ma/p/8676186.html

| 名字                              | 说明                                                         |
| --------------------------------- | ------------------------------------------------------------ |
| QuartzNet15x5Base-En              | 在6个数据集上进行了训练： 1、LibriSpeech 2、Mozilla Common Voice  3、WSJ  4、Fisher 5、SwitchBoard  6、NSC Singapore English 用apex/amp优化器level O1训练了600轮。 在LibriSpeech的dev-clean数据集上，WER是3%左右。在dev-other（带噪音的语料）上WER在10%左右。 |
| QuartzNet15x5Base-Zh              | 在ai-shell2 这个数据集进行了训练。 这个数据集的介绍： http://www.aishelltech.com/aishell_2 经过专业语音校对人员转写标注，并通过严格质量检验，此数据库文本正确率在96%以上。（支持学术研究，未经允许禁止商用。） |
| QuartzNet5x5LS-En                 | 只在LibriSpeech数据集上进行了训练。 相比于QuartzNet15x5Base-En，WER略高一点。 |
| QuartzNet15x5NR-En                | NR表示噪音。这个模型适合在有噪音的场合使用。                 |
| Jasper10x5Dr-En                   | 在6个数据集上进行了训练。比QuartzNet15x5Base-En略好一点。    |
| ContextNet-192-WPE-1024-8x-Stride | ContextNet 模型。只在LibriSpeech数据集上训练了。             |
| MatchboxNet-3x1x64-v1             | MatchboxNet 模型。在Google Speech Commands dataset（v1版本，30种命令）上进行训练。 97%的准确率。 |
| MatchboxNet-3x2x64-v1             | 同上，准确率略高。                                           |
| MatchboxNet-3x1x64-v2             | 在Google Speech Commands dataset（v2版本，35种命令）上训练。 |
| MatchboxNet-3x1x64-v2-subset-task | 在Google Speech Commands dataset（v2版本子集，10+2种命令）上训练。 |
| MatchboxNet-VAD-3x2               | MatchboxNet 模型。在Google Speech Commands dataset（v2版本，35种命令）上训练。 |
| SpeakerNet_recognition            | 使用交叉熵损失函数。端到端的语音识别。 使用voxceleb1/2 数据集进行训练。在clean数据上，2.65%的WER。 |

# 9月23日

先初步提交了一个报告。

继续在这里看看代码和模型。

https://paperswithcode.com/area/speech

这个有点意思，代码复杂度都不高。

https://github.com/graykode/nlp-tutorial

Learning Sound Event Classifiers from Web Audio with Noisy Labels

https://arxiv.org/abs/1901.01189

这个仓库包含了基本的步骤：特征提取、训练、推理和评估。

在载入FSDnoisy18k这个数据集之后，计算对数梅尔谱图，一个CNN的baseline被训练和评估。

代码还可以测试4个noise-robust损失函数。

https://github.com/edufonseca/icassp19

这个可以跑demo。而且可以在树莓派上跑。

https://github.com/FIGLAB/ubicoustics



这个博士主要就是在研究声音的分类的。他的网站值得看看。来自于芬兰的坦佩雷大学。

他一直在参与DCASE的比赛。是为比赛提供baseline。

dcase_util就是他写的。他是Audio Research Group的成员。

https://homepages.tuni.fi/toni.heittola/research-sound-event-detection

https://github.com/toni-heittola?tab=repositories

这本在线书籍，就是将声音分类的。可以看看。

https://cassebook.github.io/

dcase_util

https://github.com/DCASE-REPO/dcase_util

这个是对应的文档

https://dcase-repo.github.io/dcase_util/

这个例子

https://github.com/TUT-ARG/CASSE_book_ch2_examples

sed_eval 

这个是声音事件检测评估系统。

https://github.com/TUT-ARG/sed_eval

这本书pdf非常好，很权威。

https://homepages.tuni.fi/toni.heittola/pubs/ICASSP2019_DCASE_tutorial.pdf

应用场景

场景相关的情况。

例如助听器，需要感知当前在哪个声音环境中。

自动驾驶、机器人这些需要感知当前所在环境的。

声音监测。

婴儿啼哭、窗户被打破、狗叫、鸟叫、管道故障检测、机器运行状况。

环境噪声检测。

视频的自动生成字幕。



# 9月24日

提供数据集服务的网站：

zenodo.org, ieee-dataport.org, archive.org

为了让你的研究可以让其他人可以进行复现，需要做这些事情：

1、使用一个开发的数据集或者公布你的数据集。数据集用一篇论文介绍，提供Baseline系统。

2、公布你的代码。

3、使用标准格式公布你的结果。

DCASE的目标

1、提供一个开发数据集。

2、鼓励可复现的研究。

3、吸引新的研究者。

4、创建参考标准。

当前的产出

1、开发了SOTA方法。

2、一下新的开放数据集。

3、研究者社区的快速成长。

这里提供了模型。h5格式的。

https://github.com/toni-heittola/icassp2019-tutorial/

自己动手写CNN Inference框架之 (一) 开篇

这个系列不错。但是并没有形成最终可用的代码。

https://zhuanlan.zhihu.com/p/72568569

在树莓派上运行各种NN例子。

https://qengineering.eu/deep-learning-examples-on-raspberry-32-64-os.html

模型转换工具。

https://blog.csdn.net/WZZ18191171661/article/details/99700992

为了将使用N卡的GPU训练出来的模型成功的部署在这些低功耗的设备上面，我们通常需要对这些模型进行模型压缩和模型加速操作，**比较有名的几个工具包括TensorRT、PocketFlow、TVM等**。

简而言之，模型转换工具的作用是：**将使用不同训练框架训练出来的模型相互联系起来，用户可以进行快速的转换，节省了大量的人力和物力花销**。

上图展示了tflite的整个流程。**首先需要选择一个合适的模型；然后使用Lite converter将模型转换为FlatBuffer格式；接着将.tflite文件部署到嵌入式设备中；最后进行模型量化操作。**



https://github.com/margaretmz/awesome-tensorflow-lite



https://github.com/lmoroney/odmlbook

# 9月26日

把前面的学习记录回顾一下。

把tflite-micro再看一下。

firefly的buildroot里有集成了TensorFlow的。看看。

```
$(TOPDIR)/../external/tensorflow
```

编译是用这个tensorflow/contrib/lite/Makefile文件。

就在笔记本上训练一个唤醒词模型。即使速度再慢。把流程走一遍。

https://learn.adafruit.com/users/adafruit2

搜索sound event detection deep learning

谷歌学术里有一些论文。看了一篇，不继续看论文了。

这样搜索到的第一页的数据，都是paperwithcode、dcase的。说明这个确实是主要的研究材料。

很多都是pdf文件链接。说明多是论文。

这个仓库里是一些零散的Python脚本。没有串起来。

https://github.com/sharathadavanne/seld-net

If you are only interested in the SELDnet model then just check the keras_model.py script.

这个进行了训练和保存。

https://github.com/sharathadavanne/seld-net/blob/master/seld.py

使用了哪些数据集，可以适用于哪些场景？

可以实现定位和事件检测。定位是指分析出事件开始和结束的时间点。

声音事件检测，在实际应用中怎么做？也是录制10s的数据，然后提交给模型去分析？或者可以短一点，1秒可以。这个都不是关键，可以根据实际情况调整。

这句话怎么理解？是说上面列举了7个数据集，但是你只需要下载其中一个的意思？

In order to test the SELDnet code you don't have to download the entire dataset. You can simply download one of the zip files and train the SELDnet for the respective overlap (ov) and split (split).



polyphonic SED 

这个是对于多个声音重叠的研究。

这个人也是聚焦研究这一块的。有好些仓库。

https://github.com/sharathadavanne

这样做的动机是人类听觉系统的双耳听觉，

它可以无缝地检测多个重叠的声音事件。

为了研究这一点，我们首先确定人类听觉系统采用耳间强度差 (IID)、耳间时间延迟 (ITD) 和感知特征来检测这种重叠的声音事件。

在此基础上，我们提出了表示与 IID、ITD 和双耳音频感知类似的信息的声学特征。

受双耳音频重叠声音事件检测改进的启发，我们很好奇使用两个以上的音频通道是否会进一步改进？

与仅使用单通道相比，多通道音频可以更好地识别重叠的声音事件



这些数据集包含来自相同场景的录音，

TAU Spatial Sound Events 2019 - Ambisonic 

提供四通道一阶环绕声 (FOA) 录音，

而 TAU Spatial Sound Events 2019 - 麦克风阵列

提供来自四面体阵列配置的四通道定向麦克风录音.

两种格式都从同一个麦克风阵列中提取，关于每种格式的空间特征的附加信息可以在下面找到。参与者可以根据他们喜欢的音频格式选择两个数据集之一，或两个数据集。这两个数据集都包含一个开发和评估集。

开发集包含 400 个以 48000 Hz 采样的一分钟长的录音，

分为四个交叉验证分割，

每个分割为 100 个录音。

评估集由 100 个一分钟的录音组成。

这些录音是使用从五个室内位置收集的空间房间脉冲响应 (IR) 合成的，具有 504 种独特的方位角-仰角-距离组合。

此外，为了合成录音，收集的 IR 与来自 DCASE 2016 任务 2 的孤立声音事件数据集进行了卷积。

最后，为了创建逼真的声音场景录音，在 IR 录音位置收集的**自然环境噪声**被添加到合成录音中，例如声音事件的平均 SNR 为 30 dB。

这篇文章罗列了一些论文，

https://pythonrepo.com/repo/soham97-awesome-sound_event_detection-python-audio

这篇论文说了一下基本知识关于SED。

https://arxiv.org/pdf/2107.05463.pdf

在现实生活中的录音中，各种**声音事件**可能在事件内部和事件之间**具有时间结构**。

例如，“脚步声”事件可能会重复，中间有暂停（事件内结构）。

另一方面，“汽车喇叭”很可能跟随或先于“汽车经过”声音事件（事件间结构）。

这种时间结构被用于其他机器学习任务，

例如机器翻译、图像字幕和语音识别。

在这些任务中，开发的方法还学习了目标类的时间关联模型。

**这些关联通常被称为语言模型。**

**SED 方法可以从语言模型中受益。**这个存储库中的方法正是关于这个。一种利用 SED 语言模型的方法。



华为AI服务业务。

https://developer.huawei.com/consumer/cn/doc/development/hiai-Guides/service-introduction-0000001050040017

华为的框架是mindspore。

端侧训练和推理

https://blog.csdn.net/free1993/article/details/111081271

还真有端侧训练啊。具体看看怎么做的。

# 9月27日

看了一下端侧训练的文章。都没有讲出什么东西来。

这个的必要性还是不大。

不看这个方向的。没有意义。

有必要keras再学习一下。自己掌握实现一些简单的网络。

通过https://keras-cn.readthedocs.io/ 把概念梳理了一下。暂时不继续深入了。

刚好要做一个分享，那的确需要梳理一下。

把那些之前没有理清楚的点，要搞清楚。

# 9月29日

写了一个ppt来分享知识。还是促使自己思考之前没有留意的内容。很有好处。

# 9月30日

继续思考。

深度学习 语音任务的难点和瓶颈

https://blog.csdn.net/lc013/article/details/100985711

**实现强人工智能要做什么？从现在看，其实就是上面说的几点：**

1. 记忆：能够学习海量信息（互联网、物联网）中的知识，并加以有效的存储
2. 总结：能够总结归纳海量信息中的知识，得出一般性规律
3. 生成：能够通过知识或规律举一反三，生成更多的类似的知识、规律
4. 推导：能够通过知识或规律得到更深入的、符合目标的知识或规律

**这四点就是核心难点，比较抽象，也没那么容易，每一点估计都要N年来解决**

**它们都可以用上深度学习，但肯定都不是简单设计个graph就可以搞定的**

目前绝大多数深度学习模型，不管神经网络的构建如何复杂，其实都是在做同样一件事：

**用大量训练数据去拟合一个目标函数 y=f(x)。**

语音，

数据难获取并且经常有坑（版权问题，录音质量问题，数据集大小问题），

输入输出的对应关系有时候就难定义（情绪识别，语音识别里的对齐，某些情况下对波形的分帧），

中间过程不直观（这个波形/频谱怎么对应到这个字的？or为什么这两句话说话人向量差了这么多？），

开源资源相对少的多（一个kaldi承载了多少做识别的人的青春…），

前置知识要求更多（没上过数字信号处理、信号与系统等基础EE课程是不可能做语音的，但很多时候CV和NLP只要上过基础机器学习就能上手了），

社区相对更小，等等……不一而足。这些问题都给语音设了更高的入门门槛，可能也是语音整体人数要远小于CV和NLP的一个原因。

很多人做语音识别的时候都会被kaldi、HTK之类的必备工具先洗礼一次，

而且过程一般都还挺痛苦。

但也不是一定就要走这条路，不做识别不就行了嘛。

我的个人兴趣全在前端处理（分离/降噪，去混响，阵列处理等）

而对后端几乎没有兴趣，所以我没有仔细啃过kaldi，在可见的未来里应该也不打算啃……

我一直忽悠对语音感兴趣的人从前端入手，

因为前端处理相对后端而言坑少并且工作量也低一些，

对于小实验室的人来说更容易独立出活，周期相对更短，自学难度也比识别等要低不少。

在建立了语音处理研究的概念和大框架以后如果对后端有了兴趣，继续学习的难度也比从零开始要容易的多了。

https://www.zhihu.com/question/277152459



瓶颈背后的原因，就是一个叫做“组合爆炸”的概念：
就说视觉领域，真实世界的图像，从组合学观点来看太大量了。任何一个数据集，不管多大，都很难表达出现实的复杂程度。

因为深度学习本身缺乏理论，深度学习理论是一块难啃的骨头，深度学习框架越来越傻瓜化，各种模型网上都有开源实现，现在业内很多人都是把深度学习当乐高用。
面对一个任务，把当前最好的几个模型的开源实现 git clone 下来，看看这些模型的积木搭建说明书（也就是论文），思考一下哪块积木可以改一改，积木的顺序是否能调换一样，加几个积木能不能让效果更好，减几个积木能不能让效率更高等等。

思考了之后，实验跑起来，实验效果不错，文章发起来，实验效果不如预期，重新折腾一遍。
这整个过程非常的工程师化思维，基本就是凭感觉 trial and error，深度思考缺位。很少有人去从理论的角度思考模型出了什么问题，针对这个问题，模型应该做哪些改进。

深度学习本应该是一门科学，需要用科学的思维去面对她，这样才能得到更好的结果。



https://www.agora.io/cn/community/blog/123-category/21377

把音频技术梳理一下。

【原创】10大音频处理任务，助你开启深度学习之路（附案例链接）

https://zhuanlan.zhihu.com/p/69116079

