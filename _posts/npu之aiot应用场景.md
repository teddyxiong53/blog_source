---
title: npu之aiot应用场景
date: 2021-08-31 16:27:33
tags:
	- npu

---

--

乐鑫的MultiNet。

https://github.com/espressif/esp-sr/blob/master/speech_command_recognition/README_cn.md

MultiNet 是为了在 ESP32 上实现多命令词识别, 基于 [CRNN](https://arxiv.org/pdf/1703.05390.pdf) 网络和 [CTC](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.75.6306&rep=rep1&type=pdf) 设计的轻量化模型，目前支持 100 个以内的自定义命令词识别。

MultiNet 输入为音频经过 **MFCC** 处理后的特征值，输出为汉语/英语的“音素”分类。通过对输出音素进行组合，则可以对应到相应的汉字或单词。



瑞芯微RK3399 Pro是一款采用双Cortex-A72+四Cortex-A53大小核CPU结构，

主频高达1.8GHz的高性能处理器，

可支持4K 60fps VP9和4K 10bits H265/H264 视频解码，

外围接口丰富。

这款边缘AI处理器内置嵌入式神经网络处理器（NPU），算力可达3.0TOPs，

支持PCI-e/USB3.0/RGMIIMP，

可对多路摄像头及网络摄像头进行视频结构化识别和分析。

RK3399Pro融合了Rockchip在机器视觉、语音处理、深度学习等领域打造的NPU，

让典型深度神经网络Inception V3、ResNet34、VGG16等模型在其上的运行效果表现惊人，

性能大幅提升。

RK3399Pro适用于智能驾驶、图像识别、安防监控、无人机、语音识别等AI应用领域。



参考资料

1、EMQ X + CNN 在 AIoT 中的融合应用

https://www.emqx.com/zh/blog/emqx-and-1d-cnn-in-aiot

2、

http://www.woshipm.com/ai/2771252.html

3、

https://iot.ofweek.com/2020-09/ART-132216-8460-30457288_5.html

4、

https://www.eet-china.com/news/2021060711853.html

5、

https://zhidx.com/p/135212.html