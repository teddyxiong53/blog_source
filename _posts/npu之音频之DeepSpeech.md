---
title: npu之音频之DeepSpeech
date: 2021-09-08 19:03:33
tags:
	- npu

---

--

DeepSpeech2由百度硅谷AI实验室在2015年发布，

是一个采用PaddlePaddle深度学习框架实现的端到端自动语音识别系统，

它能通过简单学习算法较准确的识别英语和中文。

百度在DeepSpeech2之前发布过DeepSpeech，可通过pip直接安装，但它用于主要用于识别英文。

DeepSpeech系列在2017年推出Deep Speech 3，但目前开源了DeepSpeech2，

官方推荐直接下载docker镜像安装，下载的文件已帮您安装好各种依赖，但该镜像是GPU环境，需要安装nvidia-docker工具，

安装好环境后别急着运行，官方提供了训练好的模型文件，包括声学模型和语言模型，可直接下载使用，两者缺一不可，后者在前者的基础上生成最终识别的文本。

我的硬件配置如下：显卡MX250，内存16G，而虚拟机8G.

经优化后最终在虚拟机中实现6S识别一句话；而GPU环境下的Linux系统2S识别，在公司服务器上的GPU环境下可1S识别。



参考资料

1、基于DeepSpeech2实现中文语音识别，实施全流程讲解，拿来即用

https://baijiahao.baidu.com/s?id=1675202226359497084&wfr=spider&for=pc