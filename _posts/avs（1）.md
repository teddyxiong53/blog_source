---
title: avs（1）
date: 2018-05-09 21:03:10
tags:
	- avs

---



avs是Alexa Voice Service。



# 核心依赖

1、c++11版本以上。

2、gcc 4.8.5或者clang 3.3

3、cmake 3.1 。

其他。

# 媒体播放器依赖

1、gstreamer1.10.4以上版本。



# sample app的依赖

1、PortAudio

2、gstreamer。



# 代码分析

Alexa语音服务允许开发者通过麦克风和扬声器为连接的产品提供语音功能.

一旦集成,你的产品将有权访问Alexa内置功能(如音乐播放、定时器和闹钟、快递追踪、电影列表、日历管理等)

以及使用Alexa技能工具包开发的第三方技能。

AVSDevice SDK 提供基于C ++（11或更高版本）的库，

利用 AVS API 为 Alexa 启用的产品创建设备软件。

它是模块化和抽象的，提供用于处理离散功能（如语音捕获，音频处理和通信）的组件，

**每个组件都会显示可以使用和定制的API，用于集成。**

它还包括一个示例应用程序，演示与AVS的互动

![img](../images/random_name/20180521155249650)

上图说明了构成用于 C++ 的 AVS Device SDK 的组件之间的数据流

Audio Signal Processor：算法处理模块。所应用的算法被设计用于产生干净的音频数据，包括回声消除，波束形成，语音活动检测等。如果存在多麦克风阵列，则 ASP 构建并输出阵列的单个音频流。

SharedData Stream：共享数据流主要有两个作用，1.在发送到 AVS 之前，在ASP、唤醒语引擎ACL之间传递音频数据。2，通过 Alexa 通信库将由 AVS 发送的数据内容，传递给特定能力的代理。

Audio Input Process：用于处理通过 ACL 发送到 AVS 的音频输入。

Alexa Communications Library：提供消息发送和接收功能并建立和维护与AVS的长期持续连接。

Alexa Directive Sequencer Library：AVS指令集，接收从AVS Server接收到的指令，并送给指定的能力集代理处理。

 Mediaplayer：语音播放。

# 使用到的设计模式

avs代码里使用到的设计模式还是不少。

如果不能梳理出这些设计模式。就不能很好地理解代码的内部逻辑。

搜索“avs-sdk design pattern”

avs引入了一个名字为Manufactory的组件来简化客户的集成操作。

有了这个组件，客户就不需要深入理解core代码，就可以很顺利地添加、删除、定制一个avs组件。

1.21版本的sdk，提供了一个preview的例子，来demo这个的用法。

这个机制在2021年基本稳定。

下面的内容，就描述Manufactory是如何工作的。

avs sdk的演化

2017年8月的1.0版本。支持5个capability agents，代码量150K行。

2020年6月的1.20版本，支持14个capability agents。代码量480K行。

所以这个时候，就有必要进行优化sdk的集成工作了。



sdk本身是可定制的。

你完全可以添加、删除、定制组件。

当前sdk使用了依赖注入把组件注入到sdk core里。



在1.20版本，DefaultClient的create函数，接收的参数超过了58个。

这个对于集成的挑战就非常大了。

## 通过组件化来提高模块化水平

现在sdk由这4种组件组成：

* 核心组件。例如DirectiveSequencer、FocusManager。是avs的核心，必须使用。
* 可选组件。例如SmartHomeEndpoints、DisplayCard。
* 外部组件。例如电话、MRM，默认不包含，需要另外获取代码进行集成。
* 其他feature。播放器、唤醒词、授权方法等等。

## 通过Manufactory来定制你的device

有了Manufactory，你可以不关注组件的细节。

你只需要request一个组件，然后使用。

Manufactory负责create和init对象，处理依赖关系，管理对象的生命周期。

一个组件包含了多个factory。这些factory用来创建各种object。

Manufactory对外提供一个`get<>()`方法。

App可以通过`get<>()`方法来request一个对象。

Manufactory会先从object cache里检查是否有现成的。

如果没有，就调用factory产生一个。



如果你要增加一个新的受到Manufactory管理的class。

这样做：

1、在你的class里提供一个factory方法。

2、定义一个组件。

3、把factory添加到组件。

4、把组件传递给Manufactory。

5、从Manufactory申请你的对象。



Manufactory通过c++模板来实现类型检查和依赖关系解析。



## ComponentAccumulator的方法

```
addPrimaryFactory
addComponent
addUnloadableFactory
	可以卸载的对象。
addRetainedFactory
	这个创建的对象会一直alive。
```

# 关于namespace

我之前一直觉得这个namespace层数太多了。

现在仔细看，发现还是有规律的。

Interface的定义，都是在AVSCommon\SDKInterfaces目录下。

这个下面只有include。所以只有抽象。

几乎所有的类都以Interface结尾。

而在AVSCommon\SDKInterfaces下的子目录里的。

```
例如AVSCommon\SDKInterfaces\include\AVSCommon\SDKInterfaces\Endpoints
下面的文件名字，都是以Endpoint开头的。
所以using namespace的时候，也可以知道哪个类在哪个namespace下。
信息有一定冗余，但是极大地提高了识别性。
```

应用编程时，都是面向Interface的。




# 参考资料

1、Linux平台:Alexa语音服务快速入门指南

https://blog.csdn.net/z2066411585/article/details/78573368

2、wiki

https://github.com/alexa/avs-device-sdk/wiki

3、

https://blog.csdn.net/teksky163/article/details/80393304

4、Managing AVS Device SDK components with Manufactory

https://developer.amazon.com/en-US/blogs/alexa/device-makers/2020/12/managing-avs-device-sdk-components-with-manufactory