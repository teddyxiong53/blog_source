---
title: npu学习记录
date: 2021-08-24 14:11:33
tags:
	- npu

---

--

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