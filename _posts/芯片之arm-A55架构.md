---
title: 芯片之arm-A55架构
date: 2021-12-02 11:10:33
tags:
	- 芯片

---

--

想要理解 Cortex-A55 的真正潜力，

先来简要回顾一下其上一代产品：ARM Cortex-A53。

采用这款 CPU 的设备已超过 15亿台，

该 CPU 依然是当今业界出货量最高的 64 位 Cortex-A 系列 CPU。

Cortex-A53 于 2012 年发布，

其独一无二的设计，集性能、低功耗以及尺寸扩展性于一身，具备一系列多用途特性，

因而可应用于诸多市场，

其中包括高端智能手机、网络基础设施、汽车信息娱乐、高级驾驶员辅助系统 (ADAS)、数字电视、入门级移动设备和消费级设备乃至人造卫星。

然而自 2012 年以来，我们周围的世界发生了许多变化。

我们现在看到的新兴趋势表明，

保持互联、万物智能的数字世界具有非常大的发展潜力。

从完全自主的自动驾驶汽车到各类设备上的智能应用程序，

人工智能 (AI) 和机器学习 (ML) 将真正融入到我们的日常生活中，这一点已成定局。

物联网 (IoT) 应用的盛行意味着“物”的爆炸性增长，

越来越多的“物”在持续生成数据、消费数据以及与数据进行交互。

增强现实、虚拟现实以及混合现实 (AR、VR 以及 MR) 注定会彻底改变我们人类之间以及人机之间的互动方式，将现实世界与数字世界融于一体。

在过去两年里，ARM 的工程师致力于研究 Cortex-A53 的后继产品，以满足这类新兴技术的需求，我们的目标是打造出一款性能、效能以及扩展性均大幅提升的 CPU，而且这款 CPU 还需要具备诸多先进的特性，从而满足从端到云的各种未来应用需求，幸运的是我们做到了。

Cortex-A55 采用最新的 ARMv8.2 架构，并在其前代产品的基础上打造而成。它在性能方面突破了极限，同时依旧保持了与 Cortex-A53 相同的功耗水平。我们尽全力改进 Cortex-A53，并赋予其以下特性：

➤ 在相同的频率与工艺条件下，内存性能最高可达 Cortex-A53 的两倍

➤ 在相同的频率与工艺条件下，效能比 Cortex-A53 高 15%

➤ 扩展性比 Cortex-A53 高十倍以上



除了性能与效率以外，Cortex-A55 的物理芯片尺寸以及计算性能也具有极高的扩展性。为此，它包含了多个 RTL 配置选项，从而使可配置容量达到了 Cortex-A53 的十倍。事实上，它拥有 3,000 多种独特的配置，因而成为了史上最具扩展性的 Cortex-A CPU。



参考资料

1、揭秘 Cortex-A55，为何它是对未来数字世界举足轻重的处理器？

https://blog.csdn.net/super_marie/article/details/73382436