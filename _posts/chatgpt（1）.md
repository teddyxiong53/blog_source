---
title: chatgpt（1）
date: 2023-05-15 10:29:11
tags:
	- AI
---

--

chatgpt非常值得研究掌握，提高自己的工作效率。

# 资源网站

## AI工具箱

https://www.12330.com.cn/

这个网站收集了不少的知识，可以读一下。



# minigpt4

https://minigpt-4.github.io/

https://github.com/Vision-CAIR/MiniGPT-4

首先要看能不能在自己的电脑或者服务器上跑起一个demo。这样来帮助理解gpt。





最近的 GPT-4 展示了非凡的多模式能力，

例如直接从手写文本生成网站和识别图像中的幽默元素。

在以前的视觉语言模型中很少观察到这些特征。

我们认为 GPT-4 先进的多模态生成能力的主要原因在于使用了更先进的大型语言模型 (LLM)。

为了研究这种现象，我们提出了 MiniGPT-4，

它仅使用一个投影层将冻结的视觉编码器与冻结的 LLM Vicuna 对齐。

我们的研究结果表明，

MiniGPT-4 拥有许多类似于 GPT-4 所展示的功能，

例如详细的图像描述生成和从手写草稿创建网站。

此外，我们还观察了 MiniGPT-4 中的其他新兴功能，

包括根据给定图像写故事和诗歌，

为图像中显示的问题提供解决方案，

教用户如何根据食物照片做饭等。

在我们的实验中，

我们发现仅对原始图像文本对进行预训练可能会产生不自然的语言输出，

这些输出缺乏连贯性，包括重复和支离破碎的句子。

为了解决这个问题，我们在第二阶段策划了一个高质量、对齐良好的数据集，

以使用对话模板微调我们的模型。

事实证明，此步骤对于增强模型的生成可靠性和整体可用性至关重要。

值得注意的是，我们的模型计算效率很高，因为我们只使用大约 500 万个对齐的图像文本对训练投影层。



MiniGPT-4 由一个带有预训练 ViT 和 Q-Former 的视觉编码器、一个线性投影层和一个高级 Vicuna 大型语言模型组成。 

MiniGPT-4 只需要训练线性层将视觉特征与 Vicuna 对齐。

## 在windows上运行minigpt4



参考资料

1、

https://xlch.wolai.com/pBtGyPh6hyGx118o4deTk



## **BLIP-2 简介**

BLIP-2是一种通用且高效的视觉-语言预训练方法，

它可以从现成的冻结预训练图像编码器和冻结大型语言模型中引导视觉-语言预训练。

BLIP-2通过一个轻量级的Querying Transformer来弥合模态差距，

并在两个阶段进行预训练。

第一个阶段从冻结图像编码器引导视觉-语言表示学习。

第二个阶段从冻结语言模型中引导视觉-语言生成学习。

尽管比现有方法具有显著较少的可训练参数，但BLIP-2在各种视觉-语言任务上实现了最先进的性能。

在零样本 VQAv2 上，BLIP-2 相较于 80 亿参数的 Flamingo 模型，使用的可训练参数数量少了 54 倍，性能却提升了 8.7 %。



参考资料

1、

https://juejin.cn/post/7230642391031824421

## MiniGPT-4 模型训练原理

MiniGPT-4 的模型架构遵循 BLIP-2，因此，训练 MiniGPT-4 分两个阶段。

第一个传统预训练阶段使用 4 张 A100 卡在 10 小时内使用大约 500 万个对齐的图像-文本对进行训练。 

在第一阶段之后，Vicuna 虽然能够理解图像。 

但是Vicuna的生成能力受到了很大的影响。

为了解决这个问题并提高可用性，MiniGPT-4 提出了一种通过模型本身和 ChatGPT 一起创建高质量图像文本对的新方法。 

基于此，MiniGPT-4 随后创建了一个小规模（总共 3500 对）但高质量的数据集。

第二个微调阶段在对话模板中对该数据集进行训练，以显著提高其生成的可靠性和整体的可用性。 令人惊讶的是，这个阶段的计算效率很高，使用单个 A100 只需大约 7 分钟即可完成。



参考资料

1、

https://juejin.cn/post/7230642391031824421

# openassitant

代码：

https://github.com/LAION-AI/Open-Assistant

在线demo：（访问不了了）

https://open-assistant.io/chat

运行模型需要什么硬件？

目前最小的（Pythia）模型是 12B 参数，在消费类硬件上运行具有挑战性，但可以在单个专业 GPU 上运行。将来可能会有更小的模型，我们希望在整数量化等方法上取得进展，这有助于在更小的硬件上运行模型。





https://www.12330.com.cn/openassistant/68.html

# autogpt



参考资料

1、

https://www.12330.com.cn/agentgpt/56.html

# 用LLM做推荐系统



参考资料

1、

https://juejin.cn/post/7233209358981103673

# 用gpt来做code review



参考资料

1、

https://juejin.cn/post/7232700464403759164



# openai文档

https://github.com/openai/openai-quickstart-node



# MidJourney

这个是通过discord来进行交互的。

使用discord来登陆即可。没有什么障碍。

所有的行为都是公开的。

新人只能在newbie的话题下面进行交互。



# vscode使用codegpt插件

直接在vscode插件里搜索codegpt。搜索安装。

然后设置api key为自己的值。

需要配置vscode使用代理才能保证网络畅通。

插件的官网在这里：

https://codegpt.co/

插件是不开源的。

## 可以配置的apikey

有openai、cohere、AI21、Anthropic。

其余的不用管。基本不可用。

## 使用方法总结

这里演示了

https://www.codegpt.co/docs/tutorial-features/chat_code_gpt

1、选中一段代码，然后在chat那里写：用JavaScript来写这个代码。

# chatgpt的训练数据集是从哪里来的

https://metaso.cn/search/8451829596966232064

chatgpt的数据集之谜

https://zhuanlan.zhihu.com/p/606432878

# aishort用法



https://www.aishort.top/docs/guides/getting-started





虽然使用非英文提示词可能会得到不错的结果，但是当你再次输入相同的非英文提示时，结果可能会大相径庭。因为 ChatGPT 对非英文的理解每次都不同，所以建议大家在输入生产力型提示词时使用英文提示词，以保证输出效果。此外，英文提示词带来的回复也很可能是英文的。你可以在提示词结尾添加 `respond in Chinese`，将回复指定为中文。如果你的母语是其他语言，请将 "Chinese" 更改为你的母语。



# ChatGPT在编程中的应用

ChatGPT是对话式的，其回复的格式默认是使用markdown语法。

ChatGPT的基础数据更多为英文，

所以我们的问题，GPT会先转为英文进行分析生成英文回答，然后再翻译为中文。

编程方面的英文资料更多，GPT在编程方面表现出来的能力是远超过我们用中文在网络上进行搜索的。

ChatGPT-3.0支持4096个Token(BPE分词算法的最小单位)，

大概对应64000个英文单词，或2000个中文汉字。

也就是说ChatGPT-3.0每次对话的输入和输出，上下文总共都不通过超过4096个Token。

ChatGPT-4.0的上下文长度为8192个Token。

查询Token数据，访问https://gpttools.com/estimator。

因此，一个复杂的问题，我们需要分解为多个小问题来询问GPT。



https://blog.csdn.net/feihe0755/article/details/129698918