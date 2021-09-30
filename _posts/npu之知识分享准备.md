---
title: npu之知识分享准备
date: 2021-09-27 15:57:33
tags:
	- npu

---

--

NN相关知识分享

最终是用ppt的方式来呈现，多图表，少公式，少文字。

```
引言
	先用图文给大家一些直观的认识，
什么是NN？
	概念
		为什么叫这个名字？
	各个概念之间的关系
		NN
		CNN
		DNN
		RNN
		ImageNet
		人工智能
		机器学习
		深度学习
		TensorFlow
		
	构成
		CNN
		DNN
	框架
	分类
	
NN的发展历史
	
NN的现状
	各个公司的框架
	经典网络
	经典问题
	研究方向
	华人学者
NN的应用场景
	NN图像类应用
	NN音频类应用
边缘计算
	简单的应用
```



人工智能的底层模型是"神经网络"（neural network）。



参考资料

维基百科介绍，这个权威，作为概念的依据。
https://zh.wikipedia.org/wiki/%E4%BA%BA%E5%B7%A5%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C

阮一峰的文章，

http://www.ruanyifeng.com/blog/2017/07/neural-network.html

有意思的应用。

https://www.zhihu.com/question/263415714

传统机器学习和深度学习对比

https://ai.baidu.com/forum/topic/show/864067

深度学习的发展历程（思维导图、时间轴）

https://blog.csdn.net/weixin_41171061/article/details/106039242

2018图灵奖：深度学习三巨头Hinton、Bengio、LeCun，30年坚持有回报

https://wenhui.whb.cn/third/yidian/201903/28/252400.html



三巨头的主要贡献



ImageNet的发展历史

https://www.jiqizhixin.com/graph/technologies/f3400606-ef61-441c-8bc3-dd5663313fb9

https://zhuanlan.zhihu.com/p/28142670

https://zh.wikipedia.org/wiki/ImageNet

历届冠军

https://www.kaggle.com/getting-started/149448



ppt绘制时间轴



深度学习华人学者信息

https://www.163.com/dy/article/G34ONHDM05118O92.html

李沐

https://www.leiphone.com/category/academic/c4iSpQH5S8A7J9UP.html

李沐和陈天奇都是上海交大ACM班的。李沐是学长。

https://www.sohu.com/a/367456281_129720



https://www.huxiu.com/article/412021.html

DNN、RNN、CNN.…..一文带你读懂这些绕晕人的名词

https://zhuanlan.zhihu.com/p/51241366



一些动画说明卷积

http://www.labview.help/topic/104329

讲解一下LeNet

动画贴上去。

https://blog.csdn.net/itchosen/article/details/104894754



https://bbs.cvmart.net/articles/4131

mnist数据集细节

https://www.graviti.cn/v3/article/xiang-jie-mnistshu-ju-ji

LeNet-5网络结构及训练参数计算

https://blog.csdn.net/dcrmg/article/details/79210596

激活函数怎么理解？

人工神经元计算输入的“加权和”，加上偏置，接着决定是否需要“激活”（好吧，其实是激活函数决定是否激活，但是现在让我们先这样理解吧）。

上式中，Y的值可能是负无穷大到正无穷大之间的任意值。神经元并不知道值的界限。所以我们如何决定神经元是否需要激活呢？

为此，我们决定增加“激活函数”。

```
经典卷积神经网络的结构一般满足如下表达式：

输出层 -> （卷积层+ -> 池化层？）+  -> 全连接层+
上述公式中，“+”表示一个或者多个，“？”表示一个或者零个，如“卷积层+”表示一个或者多个卷积层，“池化层？”表示一个或者零个池化层。“->”表示 forward 方向。
```

卷积核尺寸



https://www.cnblogs.com/wuliytTaotao/p/9544625.html

我一直不太明白，lenet的第二个卷积层16个，怎么跟前面的输入对接起来的？

关于LeNet-5卷积神经网络 S2层与C3层连接的参数计算的思考？？？

https://blog.csdn.net/saw009/article/details/80590245

该层第一个难点：6个输入图如何通过卷积得到16个特征图？

如图2所示，C3的前六个特征图(0,1,2,3,4,5)由S2的相邻三个特征图作为输入，接下来的6个特征图(6,7,8,9,10,11)由S2的相邻四个特征图作为输入，12,13,14号特征图由S2间断的四个特征图作为输入，15号特征图由S2全部(6个)特征图作为输入。

我可以理解为几个拼起来用。



ppt放入代码美化

这个网站不错。可以生成很好看到的图片。

https://codeimg.io/



常见的深度学习模型

https://www.leiphone.com/category/academic/P17m2mt9pwdUgpwP.html

深度学习网络模型和深度学习网络结构什么关系

https://zhuanlan.zhihu.com/p/80831152

CNN/DNN/RNN这个就是网络结构。

网络结构的抽象层次高于网络模型。

11种主要神经网络结构图解

https://zhuanlan.zhihu.com/p/152057236



标准网络、循环网络、卷积网络和自动编码器。

深度学习模型大合集：GitHub趋势榜第一，两天斩获2000星

https://www.jiqizhixin.com/articles/2019-06-08-4

CNN经典结构（Lenet，AlexNet，VGG，GoogleNet，ResNet, Resnext, Densenet, Senet, BAM,mobilenet）及其pytorch实现

https://www.jianshu.com/p/975d377a2745



移动端推理框架

https://blog.csdn.net/qq_41955989/article/details/105818458

https://aijishu.com/a/1060000000118864



深度学习一般要调哪些参数？

https://zhuanlan.zhihu.com/p/56745640



机器学习的六大主要技术领域：深度学习、强化学习、迁移学习、元学习、联邦学习和自动化机器学习。



当然，提到架构，很多人会想到迁移学习：把ImageNet上训练的ResNet拿来，换个我需要的数据集再训练训练更新一下权重，不就好了嘛！
这种方法的确也可行，但是要想得到最好的效果，还是根据实际情况设计自己的网络架构比较靠谱。

关于automl

AutoML和神经架构搜索（NAS），是深度学习领域的新一代王者。

这些方法能**快糙猛**地搞定机器学习任务，简单有效，高度符合当代科技公司核心价值观。



但是，用450个GPU来训练，找到一个优秀的架构也需要训练3到4天。也就是说，对于除了Google之外的普通贫民用户们，这种方法还是门槛太高、效率太低。

用「动图」和「举例子」讲讲 RNN

https://zhuanlan.zhihu.com/p/36455374

- CNN能「看懂」图形
- RNN能「记住」顺序

RNN如此有效就在于它拥有记忆能力，尤其是LSTM（RNN的一个应用广泛的变种）更是在长期记忆方面有不俗的表现。



RNN之所以有记忆力，是因为在每个t完成后，其产生的结果会在下一个t开始时，与X一起输送给RNN运算，相当于输入中包含了之前所有t的「精华」

现在将RNN的运算部分包装起来，并把相应变量修改为惯例字母。**其实普通RNN内部并非为多层网络，仅仅是一个tanh层。**

很多初学者在接触time_step时，很容易与全神经网络下的batch混淆。

碎纸机这个说明非常到位。

为什么要batch？把LeNet的keras实现各个参数都说明一下。

LeNet的TensorFlow和pytorch实现。

什么叫全连接神经网络？



用keras实现RNN 看看。



分类和回归的区别在于输出变量的类型。

定量输出称为回归，或者说是连续变量预测；
定性输出称为分类，或者说是离散变量预测。

举个例子：
预测明天的气温是多少度，这是一个回归任务；
预测明天是阴、晴还是雨，就是一个分类任务。



激活函数跟dropout关系？



GPU、NPU等性能对比

https://www.daimajiaoliu.com/daima/6cb3cd2fb0f6c01



gpt3的

https://www.pingwest.com/a/214772

https://cloud.tencent.com/developer/article/1672427

包括用GPT-3生成网页、图表、代码、文本以及推理。其中令人吃惊的是，GPT-3能生成Keras编写的卷积神经网络的代码，还能应对程序员面试、回复邮件、写积分表达式、回答物理问题。特别是，网友还对它进行了一场图灵测试，而GPT-3表现得还不错。但是，GPT-3真的通过图灵测试了吗？



深度学习的常用算子

tanh、sigmoid、conv2d这些都是算子。



把automl和autoKeras了解一下。

https://cloud.tencent.com/developer/article/1441557?from=14588

什么是图像分类的Top-5错误率？

imagenet图像通常有1000个可能的类别，对每幅图像你可以猜5次结果(即同时预测5个类别标签)，当其中有任何一次预测对了，结果都算对，**当5次全都错了的时候，才算预测错误**，这时候的分类错误率就叫top5错误率



重新看了一下《深度学习500问》



https://blog.csdn.net/m0_37867246/article/details/79766371

# v2

当前考虑到分享的范围会扩大，需要进行一些完善。

1、首先比较明显的，就是中间的分割ppt，需要换一个风格。当前的太丑了。

2、对典型应用需要再增加一些，例如推荐系统。

3、音频应用展开说一下。把梅尔谱图贴一下，解释一下。以唤醒词为例展开说。

4、明显的错误改一下。



