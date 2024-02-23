---
title: AI之stable diffusion本地安装使用
date: 2024-02-23 12:17:17
tags:
	- AI

---

--

# Stable Diffusion介绍

Stable Diffusion是2022年发布的深度学习文本到图像生成模型。

它主要用于根据文本的描述产生详细图像，

尽管它也可以应用于其他任务，如内补绘制、外补绘制，以及在提示词指导下产生图生图的转变。[3]

它是一种潜在扩散模型，由慕尼黑大学的CompVis研究团体开发的各种生成性人工神经网络之一。[4]

它是由初创公司StabilityAI、CompVis与Runway合作开发，并得到EleutherAI和LAION的支持。

截至2022年10月，StabilityAI筹集了1.01亿美元的资金。[8]

Stable Diffusion的源代码和模型权重已分别公开发布在GitHub和Hugging Face，

可以在大多数配备有适度GPU的电脑硬件上运行。

而以前的专有文生图模型（如DALL-E和Midjourney）只能通过云计算服务访问。



Stable Diffusion模型支持通过使用提示词来产生新的图像，

描述要包含或省略的元素，[6]以及重新绘制现有的图像，

其中包含提示词中描述的新元素（该过程通常被称为“指导性图像合成”（guided image synthesis）[11]）通过使用模型的扩散去噪机制（diffusion-denoising mechanism）。

[6] 此外，该模型还允许通过提示词在现有的图中进内联补绘制和外补绘制来部分更改，当与支持这种功能的用户界面使用时，其中存在许多不同的开源软件。[12]

Stable Diffusion建议在10GB以上的显存（GDDR或HBM）下运行， 

但是显存较少的用户可以选择以float16的精度加载权重，而不是默认的float32，以降低显存使用率。



参考资料

1、

https://zh.wikipedia.org/wiki/Stable_Diffusion

# 在线免费试用SD

https://zhuanlan.zhihu.com/p/631005852