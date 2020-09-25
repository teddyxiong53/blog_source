---
title: 音频之pdm接口
date: 2020-09-24 10:36:30
tags:
	- 音频

---

1

pdm是跟pcm类似的东西。

PDM = Pulse Density Modulation是一种用**数字信号表示模拟信号的调制方法。**

PDM则使用远高于PCM采样率的时钟采样调制模拟分量，只有1位输出，要么为0，要么为1。因此通过PDM方式表示的数字音频也被称为Oversampled 1-bit Audio。

相比PDM一连串的0和1，PCM的量化结果更为直观简单。

以PDM方式作为模数转换的接收端，需要用到抽取滤波器（Decimation Filter），

将密密麻麻的0和1代表的密度分量转换为幅值分量，**而PCM方式得到的已经是幅值分量了。**



PDM方式的逻辑相对复杂，但只需要两根线，时钟和数据。



# PCM/PDM区别

主要区别是：

PCM：

1.使用等间隔采样方法：将每次采样的模拟分量幅度表示为N位的数字分量（N = 量化深度）

2.每次采样的结果都是N bit字长的数据

3.逻辑更加简单

4.需要用到**数据时钟，采样时钟和数据信号三根信号线**



PDM：

1.使用远高于PCM采样率的时钟采样调制模拟分量

2.PDM采样的音频数据 也常被叫做：Oversampled 1-bit Audio

3.只有1位输出：要么为0，要么为1

4.逻辑相对复杂

5.只需要两根信号线，即时钟和数据

参考资料

1、PDM接口介绍

https://blog.csdn.net/weixin_42509369/article/details/83549211

2、音频传输的PCM和PDM有什么区别

https://www.icxbk.com/ask/detail/37151.html