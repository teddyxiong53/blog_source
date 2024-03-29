---
title: npu之seq2seq
date: 2021-09-16 11:15:33
tags:
	- npu

---

--



我们尝试交叉编译过程，移植深度学习推理框架（如NCNN，TNN等），

使用zhouyi AIPU跑深度学习模型，使用双核DSP做回声消除等等，

最终的目的是跑一个语音模型实现关键词唤醒，

跑yolo实现目标检测功能，咱先实现功能，性能、精度调优留到第三步。

边缘嵌入式端模型工程部署是伴随着AI的发展而蓬勃兴起的，

17年左右开始发展，在19年到达顶峰，目前已趋于平缓；

而原来学校阶段基本教的都是嵌入式的基础知识，毕竟那时候AI还没火起来呢，

现在相当于在原来的嵌入式基础上加入了AI的相关属性，

因此 一部分的嵌入式工程师学习深度学习的知识，

或者新晋的深度学习算法工程师学习嵌入式知识，

**从而就衍生了边缘端部署优化工程师的岗位，**

属于传统HPC领域中的一个小分支。



安谋科技自研IP“周易”NPU自正式商用以来，受到业内广泛关注。

2021年7月，“周易”NPU 团队在极术社区发布了[周易NPU Compass SDK公测版](https://aijishu.com/a/1060000000215443)，

同时还开放了涵盖分类，检测，分割，语音识别等AI基础模型的[模型库Model-Zoo](https://aijishu.com/a/1060000000223632)，

以便工程师能使用“周易”NPU快速开发AI应用。



比如在[智能家居](http://smarthome.ailab.cn/)场景，R329可以检测各种声音做出智能反应；

比如听到婴儿的哭声时智能开灯并提醒宝妈；

比如主人设定外出期间在室内检测到开关门声、脚步声自动发出报警声和信息提醒等等。



R329提供了一种全新的[语音识别](http://voice.ailab.cn/)硬件加速[神经网络](http://anns.ailab.cn/)，

支持int8、int16混合精度流式处理，

从而可以在更快地处理请求，[语音识别](http://voice.ailab.cn/)体验更快，

平均响应时间从2秒左右减少到200毫秒以内，这是一个不容小觑的提升。

R329同时具有同类优秀的能源效率，能源消耗减少了25倍，语音处理速度提高了30倍。



从通用处理器选择A53就能看出R329的定位，不过在IP选择上更能凸显高算力的应该还在于DSP与AI专核。

前文就已经提到通用处理器部分跑的是操作系统、应用、网络连接等；

DSP负责信号处理算法、音效；

**还有AI专核，即NPU专门用于本地ASR（自动语音识别）、NLP（自然语言识别）和TTS（Textto Speech）——都是在本地执行的，也就是我们常说的边缘计算。**



在更具体的应用上，全志表示：“ASR、NLP、TTS等技术对专用AI处理器提出了迫切需求；

传统算法也逐渐被AI算法替代，国内外均有发布，**用深度学习做端到端的算法**，

相对于传统降噪、回声消除和关键词识别算法，效果更优，具有更高的识别率。”



所以全志也告诉我们，在R329用上DSP+NPU+2MBSRAM时，让大模型双麦降噪算法跑在DSP上，

大模型深度学习唤醒词跑在NPU上，能够实现低功耗特性。

这应该是权衡算力与功耗之后，一种相对合理的搭配方式。



这一期能解决的问题是：

你能用R329上的AIPU跑个resnet50啥的，你能用R329的CPU跑起来NCNN，跑个resnet50，mobilenet啥的，并对比性能数据。



**这一期大概要解决的问题如下：**

1. ”我要怎么样才能在R329上跑模型的呀？不要多了，能跑你们官方的demo就行，我主要想对整体的开发流程有个主观印象。”
2. ”我想跟NCNN跑的数据做对比，我该如何在R329上移植NCNN并跑benchmark的呀？要怎么准备环境、怎么跑的呀？“
3. “我要跑自定义模型该如何操作的呀？”
4. ”我的模型贼复杂，有前后处理balabala的，我想一部分在CPU上做一部分在AIPU上做（这有个装逼的名字叫"切图"），这要怎么搞得呀？“



要能跑起来AIPU首先驱动层得支持，其次runtime库也得支持，接着我们才可以在应用层调用AIPU；

这里得好消息是驱动默认就支持了，坏消息是runtime库一时半会还不会完全开源，因此我们需要先解决runtime库得问题。

上期我们说过了，由于AIPU的知识产权是属于ARM china的，

所以全志暂时是不会开放出来给我们使用的（对应的就是在开发的源码中把这一部分库代码给删除了），



我们知道resnet50的理论计算量大概是4Gops，而我们AIPU的理论算力是128MAC*0.8Gpbs=102.4GOPS

因此理论峰值算力下的FPS为：FPS=102.4/4=25FPS

而真实的算力约为10FPS，算力仅利用完一半不到，也就是可以大致推断出访存部分是瓶颈，嗯，访存带宽的问题没有做好呀



做优化的都知道，访存其实这个也好分析，

resnet中存在大量的3X3跟1X1卷积层，

这些卷积层在硬件底层都是由脉动阵列进行计算的，

而3x3的卷积属于计算密集型，实际上MAC利用率能达到百分之八九十，



参考资料

1、探游·R329·AI部署实战（一）

https://zhuanlan.zhihu.com/p/357074919

2、极术公开课|使用“周易”NPU开发AI模型及应用实战

https://bbs.csdn.net/topics/600692838

3、

http://www.ailab.cn/voice/20201030106286.html

4、极术社区上R329相关资料。很全面。

https://aijishu.com/a/1060000000221780

5、探游·R329·AI部署实战（二）移植搭建AI环境

https://aijishu.com/a/1060000000198659